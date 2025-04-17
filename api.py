from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sasmodels.core import load_model
from sasmodels.direct_model import call_kernel
import sys
sys.path.append('hierarchical_SAS_analysis-main 2')
import numpy as np
import startup
import dbFunctions

import structlog
import logging
from pathlib import Path
from contextvars import ContextVar
import socket
import threading
import platform
from datetime import datetime
import time
import uuid
import traceback
import json
import logging.handlers
from functools import wraps

logging_dir = Path("./logs")
logging_dir.mkdir(exist_ok=True)

request_id_var = ContextVar("request_id", default=None)
request_start_time_var = ContextVar("request_start_time", default=None)

import hashlib
from collections import defaultdict
import threading

SAMPLING_CONFIG = {
    "simulate_graph": {
        "rate": 0.01, # 1% of requests
        "summary_interval": 1200 # 20 minutes
    }
}

endpoint_metrics = defaultdict(lambda: {
    "calls": 0,
    "errors": 0,
    "total_duration": 0,
    "min_duration_ms": float('inf'),
    "max_duration_ms": float('-inf'),
    "last_summary_time": time.time(),
    "by_morphology": defaultdict(lambda: {
        "calls": 0,
        "errors": 0,
        "total_duration": 0
    })
})

metrics_lock = threading.Lock() # can remove endpoint metrics if performace heavily impacted

def should_sample(request_id, endpoint): # threading + stateless
    """Determine if this request should be sampled for logging"""
    if endpoint not in SAMPLING_CONFIG:
        return True
    
    hash_val = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
    return (hash_val % 100) < (SAMPLING_CONFIG[endpoint]["rate"] * 100)

def update_metrics(endpoint, duration_ms, error=False, metadata=None):
    with metrics_lock:
        metrics = endpoint_metrics[endpoint]
        metrics["calls"] += 1
        metrics["total_duration"] += duration_ms
        metrics["min_duration_ms"] = min(metrics["min_duration_ms"], duration_ms)
        metrics["max_duration_ms"] = max(metrics["max_duration_ms"], duration_ms)

        if error:
            metrics["errors"] += 1

        if metadata and "morphology" in metadata:
            morphology = metadata["morphology"]
            morph_matrics = metrics["by_morphology"][morphology]
            morph_matrics["calls"] += 1
            morph_matrics["total_duration"] += duration_ms
            if error:
                morph_matrics["errors"] += 1
        
        current_time = time.time()
        if (current_time - metrics["last_summary_time"]) > SAMPLING_CONFIG.get(endpoint, {}).get("summary_interval", 60):
            log_metrics_summary(endpoint)
            metrics["last_summary_time"] = current_time

def log_metrics_summary(endpoint):
    """Log a summary of metrics for the endpoint"""
    with metrics_lock:
        metrics = endpoint_metrics[endpoint]

        if metrics["calls"] == 0:
            return
        
        avg_duration = metrics["total_duration"] / metrics["calls"]
        error_rate = metrics["errors"] / metrics["calls"] if metrics["calls"] > 0 else 0

        logger.info(
            f"{endpoint}_summary",
            calls=metrics["calls"],
            errors=metrics["errors"],
            error_rate_percent=round(error_rate, 2),
            avg_duration_ms=round(avg_duration, 2),
            min_duration_ms=round(metrics["min_duration_ms"],2),
            max_duration_ms=round(metrics["max_duration_ms"],2),
        )

        if metrics["by_morphology"]:
            top_morphology = sorted(
                metrics["by_morphology"].items(),
                key=lambda x: x[1]["calls"],
                reverse=True
            )[:3]

            for morphology, morph_metrics in top_morphology:
                morph_avg_duration = morph_metrics["total_duration"] / morph_metrics["calls"] if morph_metrics["calls"] > 0 else 0
                morph_error_rate = (morph_metrics["errors"] / morph_metrics["calls"]) * 100 if morph_metrics["calls"] > 0 else 0

                logger.info(
                    f"{endpoint}_morphology_summary",
                    morphology=morphology,
                    calls=morph_metrics["calls"],
                    percentage=round((morph_metrics["calls"] / metrics["calls"]) * 100, 2),
                    avg_duration_ms=round(morph_avg_duration, 2),
                    error_rate_percent=round(morph_error_rate, 2),
                )

        metrics["calls"] = 0
        metrics["errors"] = 0
        metrics["total_duration"] = 0
        metrics["min_duration_ms"] = float('inf')
        metrics["max_duration_ms"] = float('-inf')
        metrics["by_morphology"] = defaultdict(lambda: {"calls": 0, "errors": 0, "total_duration_ms": 0})


def add_app_context(logger, function, event_dict):
    """Add application context to structred log events"""
    event_dict["app_name"] = ""
    event_dict["enviroment"] = os.environ.get("FLASK_ENV", "development")
    event_dict["host"] = socket.gethostname()
    event_dict["process_id"] = os.getpid()
    event_dict["thread_id"] = threading.get_ident()
    event_dict["python_version"] = platform.python_version()

    request_id = request_id_var.get()
    if request_id:
        event_dict["request_id"] = request_id
    
    if "timestamp" not in event_dict:
        event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"

    return event_dict

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        add_app_context,
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True
)

def config_logging():
    """Configure logging for the application"""
    json_formatter = logging.Formatter('%(message)s')

    info_file_handler = logging.handlers.RotatingFileHandler(
        "logs/info.log", maxBytes=10**6, backupCount=5
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(json_formatter)

    error_file_handler = logging.handlers.RotatingFileHandler(
        "logs/error.log", maxBytes=10**6, backupCount=5
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(json_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(json_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(info_file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(console_handler)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    return root_logger

root_logger = config_logging()
logger = structlog.get_logger()

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)
        request_start_time_var.set(time.time())

        orig_start_response = start_response

        def custom_start_response(status, headers, exc_info=None):
            headers.append(("X-Request-ID", request_id))
            return orig_start_response(status, headers, exc_info)
        
        try:
            with structlog.contextvars.bound_contextvars(
                request_id=request_id,
                http_method=environ.get("REQUEST_METHOD"),
                path=environ.get("PATH_INFO"),
                remote_addr=environ.get("REMOTE_ADDR"),
                user_agent=environ.get("HTTP_USER_AGENT", "")
            ):
                logger.info("Request started", query_string=environ.get("QUERY_STRING", ""))

            response = self.app(environ, custom_start_response)

            duration = time.time() - request_start_time_var.get()

            with structlog.contextvars.bound_contextvars(
                request_id=request_id,
                duration_ms=round(duration * 1000, 2)
            ):
                logger.info("Request completed")
            
            return response
        except Exception as e:
            duration = time.time() - request_start_time_var.get()
            with structlog.contextvars.bound_contextvars(
                request_id=request_id,
                duration_ms=round(duration * 1000, 2),
                error=str(e),
                traceback=traceback.format_exc()
            ):
                logger.error("Request failed")
            raise

def log_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        endpoint = request.endpoint
        method = request.method
        length = request.content_length or 0

        request_id = request_id_var.get()
        if not request_id:
            request_id = str(uuid.uuid4())
            request_id_var.set(request_id)

        if not request_start_time_var.get():
            request_start_time_var.set(time.time())
        
        try:
            params = {}
            if request.args:
                params['query'] = request.args.to_dict()
            
            if request.is_json and request.get_json():
                params['json'] = request.get_json()
            elif request.form:
                params['form'] = request.form.to_dict()

            params_str = json.dumps(params)
            if len(params_str) > 1000:
                params_str = params_str[:1000] + "..."
        except Exception as e:
            params_str = f"Error parsing params: {str(e)}"

        logger.info(
            "endpoint_called",
            endpoint=endpoint,
            method=method,
            path=request.path,
            context_length=length,
            params=params_str,
            remote_addr=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        
        try:
            start_time = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start_time

            status_code = result.status_code if hasattr(result, 'status_code') else 200

            try:
                if isinstance(result, tuple):
                    response_data = result[0]
                    status_code = result[1] if len(result) > 1 else 200
                else:
                    response_data = result
                
                if hasattr(response_data, 'get_json'):
                    response_data = response_data.get_json()
                elif not isinstance(response_data, (str, dict, list)):
                    response_data = str(response_data)
                
                response_json_str = json.dumps(response_data)
                if len(response_json_str) > 1000:
                    response_str = response_json_str[:1000] + "..."
            except Exception as e:
                response_str = "[Response data could not be parsed]"
            
            logger.info(
                "endpoint_succeeded",
                endpoint=endpoint,
                method=method,
                duration_ms=round(duration * 1000, 2),
                status_code=status_code,
                response_size=len(response_str) if isinstance(response_str, str) else 0,
            )

            return result
        except Exception as e:
            duration = time.time() - request_start_time_var.get()
            
            logger.error(
                "endpoint_failed",
                endpoint=endpoint,
                duration_ms=round(duration * 1000, 2),
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc()
            )

            raise

    return decorated

app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)
cors = CORS(app, resources={r"/*": {"origins": ["http://sasgui.cse.uconn.edu:5173","sasgui.cse.uconn.edu:5173", "http://sasgui.cse.uconn.edu", "sasgui.cse.uconn.edu", "http://localhost:5173"]}})

@app.errorhandler(404)
def page_not_found(e):
    logger.warning("page_not_found", path=request.path, method=request.method)
    return jsonify({"error": "Resource Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error("internal_server_error", error=str(e), traceback=traceback.format_exc())
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("unhandled_exception", error=str(e), error_type=type(e).__name__, traceback=traceback.format_exc())
    return jsonify({"error": "An unexpected error occurred"}), 500

def log_performace(logger, operation, start_time, **kwargs):
    duration = time.time() - start_time
    logger.info(
        f"{operation}_performance",
        duration_ms=round(duration * 1000, 2),
        **kwargs
    )


# FIle Handling
UPLOAD_FOLDER = os.path.abspath("hierarchical_SAS_analysis-main 2/data") # Directly use the existing folder path

@app.route('/upload', methods=['POST'])
#@log_request
def upload_file():
    operation_start = time.time()
    logger.info("file_upload_started")

    if 'file' not in request.files:
        logger.warning("file_upload_failed", reason="No file part in the request")
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['file']
   
    if file.filename == '':
        logger.warning("file_upload_failed", reason="No file selected for uploading")
        return jsonify({'message': 'No file selected for uploading'}), 400
    
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Fixed filename
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        file_extension = os.path.splitext(file.filename)[1]
        logger.info(
            "file_uploaded",
            filename=file.filename,
            file_size_bytes=file_size,
            file_extension=file_extension,
            context_type=file.content_type
        )
        log_performace(
            logger,
            "file_upload",
            operation_start,
            file_size_bytes=file_size,
            filename=file.filename
        )
        result = startup.main2(file_path)
        os.remove(file_path)
        return jsonify(result)
    except Exception as e:
        logger.error(
        "file_upload_failed",
        filename=file.filename if file else "unknown",
        error=str(e),
        traceback=traceback.format_exc()
        )
        return jsonify({'message': 'File upload failed'}), 500

# @app.route("/shape", methods=['POST','GET'])
# def chd():
#     if request.method == 'POST':
#             json  = request.get_json()
#             shape = json.get('shape')
#             return startup.main(shape) #returns dimensions for morphology
#     return {'name': 5}

# @app.route('/get_all_files', methods=['GET'])
# def get_all_files():
#     """Returns the names of all files in the upload folder."""
#     try:
#         # List all files in the upload folder
#         file_names = os.listdir(UPLOAD_FOLDER)
        
#         # Filter out directories, keep only files
#         file_names = [f for f in file_names if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        
#         return jsonify({"message": "Files retrieved successfully", "files": file_names}), 200
#     except Exception as e:
#         return jsonify({"message": "Error retrieving files", "error": str(e)}), 500
    
# @app.route('/delete_file', methods=['DELETE'])
# def delete_file():
#     """Deletes a specified file from the upload folder."""
#     try:
#         # Get the filename from the request data
#         data = request.get_json()
#         file_name = data.get('file_name')
        
#         if not file_name:
#             return jsonify({"message": "No file name provided"}), 400

#         # Construct the full file path
#         file_path = os.path.join(UPLOAD_FOLDER, file_name)

#         # Check if file exists
#         if not os.path.exists(file_path):
#             return jsonify({"message": "File not found"}), 404
        
#         # Remove the file
#         os.remove(file_path)
        
#         return jsonify({"message": f"File {file_name} deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"message": "Error deleting file", "error": str(e)}), 500


# # Param Updates, dont think we use this
# @app.route('/update_params', methods=['POST'])
# def update_params():
#     """Updates parameters for the prediction model."""
#     params = request.json
    
#     # TODO: Validate and update parameters in the system
#     return jsonify({"message": "Parameters updated", "params": params})


# # ML?
# @app.route('/predict', methods=['POST'])
# def predict():
#     """Calls the ML classifier to predict shape."""
#     input_data = request.json  # Expecting input parameters
    
#     # TODO: Call the trained ML model for prediction
#     prediction = {"shape": "predicted_shape", "confidence": 0.95}  # test response
    
#     return jsonify({"message": "Prediction successful", "prediction": prediction})


@app.route('/save_to_database', methods=['POST'])
#saving still works with @log_request uncommented but it throws an error
#@log_request 
def save_to_database():
    """Saves prediction or curve data to the database."""
    operation_start = time.time()
    try:
        data = request.json
        
        logger.info("database_save_request", data_size=len(json.dumps(data)))

        if "name" in data:
            dbFunctions.add_to_scans(file_name = data.get("name"), file_data = data.get("data"), userId = data.get("userId"))
            logger.info("database_save_success")
            log_performace(
                logger,
                "database_save",
                operation_start
            )            
            return jsonify({"message": "Data saved successfully"})
        else:
            result = dbFunctions.add_to_users(username = data.get("username"), password = data.get("password"), email = data.get("email"), securityAnswer = data.get("securityAnswer"), securityQuestion = data.get("securityQuestion"))
            if result["success"]:
                logger.info("database_save_success")
                log_performace(
                    logger,
                    "database_save",
                    operation_start
                )            
                return jsonify({"message": "Data saved successfully"})
            else:
                return jsonify(result)
    except Exception as e:
        logger.error(
            "database_save_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Failed to save data", "error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400
        
        db_result = dbFunctions.get_id_by_username(username)
        if not db_result:
            return jsonify({"message": "Unknown username or password"}), 401
        else:
            userId = db_result.get("userId")
        
        user_credentials = dbFunctions.get_user_info(userId)
        
        if user_credentials and user_credentials['password'] == password and user_credentials['username'] == username:
            return jsonify({"message": "Login successful", "userId": user_credentials['userId']}), 200
        else:
            return jsonify({"message": "Unknown username or password"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "An error occurred during login", "error": str(e)}), 500
    
@app.route('/get_security_question', methods=['POST'])
def get_security_question():
    try:
        data = request.json
        email = data.get('email')
        db_result = dbFunctions.get_id_by_username(email)
        if not db_result:
            return jsonify({"message": "Unknown email"}), 401
        else:
            userId = db_result.get("userId")
        user_credentials = dbFunctions.get_user_info(userId)
        return jsonify({"message": "email found", "security_question": user_credentials["security_question"], "userId": user_credentials["userId"]}), 200
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "An error occurred during login", "error": str(e)}), 500

@app.route('/reset_password_with_security_question', methods=['POST'])
def reset_password_with_security_question():
    """Resets the password for a user based on security question answer."""
    try:
        data = request.json
        userId = data.get('userId')
        security_answer = data.get('security_answer')
        new_password = data.get('password')

        if not security_answer or not new_password:
            return jsonify({"message": "Missing required fields"}), 400

        user_credentials = dbFunctions.get_user_info(userId)
        if user_credentials and user_credentials['security_answer'] == security_answer:
            # Update the password in the database
            dbFunctions.change_password_by_userId(userId, new_password)
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Incorrect security answer"}), 401

    except Exception as e:
        print(f"Error during password reset: {e}")
        return jsonify({"message": "An error occurred during password reset", "error": str(e)}), 500
    

# @app.route('/get_database_data', methods=['GET'])
# def get_database_data():
#     """Retrieves data from the database."""
    
#     # TODO: Implement database retrieval logic
#     stored_data = DATABASE.get("latest", {})
    
#     return jsonify({"message": "Data retrieved", "data": stored_data})

@app.route('/get_user_scans', methods=['GET'])
def get_user_scans_route():
    """Retrieve all scan names for a specific user by userId."""
    try:
        userId = request.args.get('userId')  # Get userId from query parameter
        
        if not userId:
            return jsonify({"message": "userId parameter is required"}), 400
        
        # Assuming dbFunctions.get_user_scans(userId) returns a list of scans
        scans = dbFunctions.get_user_scans(userId)
        
        if not scans:
            return jsonify({"message": "No scans found for the given userId"}), 404
        
        # Extract just the scan names (assuming 'name' is the field in the scan data)
        scan_names = [scan[1] for scan in scans]
        
        return jsonify({"message": "Scans retrieved successfully", "scans": scan_names}), 200
    except Exception as e:
        print(f"Error retrieving user scans: {e}")
        return jsonify({"message": "Error retrieving user scans", "error": str(e)}), 500

@app.route('/get_scan_data', methods=['GET'])
def get_scan_data_route():
    """Retrieve scan data for a specific scan name and userId."""
    try:
        userId = request.args.get('userId')  # Get userId from query parameter
        scan_name = request.args.get('name')  # Get scan name from query parameter
        
        if not userId or not scan_name:
            return jsonify({"message": "Both userId and name parameters are required"}), 400
        
        # Call the dbFunctions.get_scan_data_by_name_and_user_id function to fetch scan data
        scan_data = dbFunctions.get_scan_data_by_name_and_user_id(userId, scan_name) 
        
        if not scan_data:
            return jsonify({"message": "No data found for the given scan name and userId"}), 404
        
        return jsonify({"message": "Scan data retrieved successfully", "data": scan_data}), 200
    except Exception as e:
        print(f"Error retrieving scan data: {e}")
        return jsonify({"message": "Error retrieving scan data", "error": str(e)}), 500
# -----
#SASVIEW
def process_request(json, model_name, param_mapping):
    """Helper function to process requests and generate scattering data."""
    q = np.loadtxt('q_200.txt', delimiter=',', dtype=float)
    pars = param_mapping.copy()
    
    for key, json_key in param_mapping.items():
        if json_key in json:
            pars[key] = json.get(json_key)
    
    model = load_model(model_name)
    kernel = model.make_kernel([q])
    Iq = call_kernel(kernel, pars) + 0.001
    
    return {'xval': np.array(q).tolist(), 'yval': np.array(Iq).tolist()}
"""@app.route("/simulate_graph", methods=["POST"])
def sim_graph():
    if request.method == 'POST':
        json_data = request.get_json()
        return(json_data)"""

def graphASphere(data):
    """'radius_pd_type':'schulz',
            'radius_pd_n' : '40',
            'radius_pd_nsigma': '3',"""
    param_mapping = {
            'background': 'sphereBackground',
            'radius_pd': 'spherePolydispersity',
            'radius' : 'sphereRadius',
            'scale': 'sphereScale',
            'sld': 'sphereScatteringLengthDensity',
            'sld_solvent': 'sphereScatteringLengthSolvent',
            'radius_pd_type':'schulz',
            'radius_pd_n' : 40,
            'radius_pd_nsigma': 3

    }
    return process_request(data, 'sphere', param_mapping)
def graphACoreShellSphere(data):
    param_mapping = {
            'background': 'coreShellSphereBackground',
            'radius_pd': 'coreShellSpherePolydispersity',
            'radius': 'coreShellSphereRadius',
            'scale': 'coreShellSphereScale',
            'sld_core': 'coreShellSphereScatteringLengthCore',
            'sld_shell': 'coreShellSphereScatteringLengthShell',
            'sld_solvent': 'coreShellSphereScatteringLengthSolvent',
            'thickness': 'coreShellSphereThickness',
            'radius_pd_type':'schulz',
            'radius_pd_n' : 40,
            'radius_pd_nsigma': 3
    }
    return process_request(data, 'core_shell_sphere', param_mapping)

def graphACylinder(data):
    param_mapping = {
            'background': 'cylinderBackground',
            'length': 'cylinderLength',
            'radius_pd': 'cylinderPolydispersity',
            'radius': 'cylinderRadius',
            'scale': 'cylinderScale',
            'sld': 'cylinderScatteringLengthDensity',
            'sld_solvent': 'cylinderScatteringLengthSolvent',
            'radius_pd_type': 'schulz',
            'radius_pd_n': 40,
            'radius_pd_nsigma': 3
    }
    return process_request(data, 'cylinder', param_mapping)
def graphACoreShellCylinder(data):
    param_mapping = {
            'background': 'coreShellCylinderBackground',
            'length': 'coreShellCylinderLength',
            'radius_pd': 'coreShellCylinderPolydispersity',
            'radius': 'coreShellCylinderRadius',
            'scale': 'coreShellCylinderScale',
            'sld_core': 'coreShellCylinderScatteringLengthCore',
            'sld_shell': 'coreShellCylinderScatteringLengthShell',
            'sld_solvent': 'coreShellCylinderScatteringLengthSolvent',
            'thickness': 'coreShellCylinderThickness',
            'radius_pd_type': 'schulz',
            'radius_pd_n': 40,
            'radius_pd_nsigma': 3
    }
    return process_request(data, 'core_shell_cylinder', param_mapping)
def graphADisk(data):
    param_mapping = {
            'background': 'diskBackground',
            'length': 'diskLength',
            'radius_pd': 'diskPolydispersity',
            'radius': 'diskRadius',
            'scale': 'diskScale',
            'sld': 'diskScatteringLengthDensity',
            'sld_solvent': 'diskScatteringLengthSolvent',
            'radius_pd_type': 'schulz',
            'radius_pd_n': 40,
            'radius_pd_nsigma': 3
    }
    return process_request(data, 'cylinder', param_mapping)

def graphACoreShellDisk(data):
    param_mapping = {
            'background': 'coreShellDiskBackground',
            'length': 'coreShellDiskLength',
            'radius_pd': 'coreShellDiskPolydispersity',
            'radius': 'coreShellDiskRadius',
            'scale': 'coreShellDiskScale',
            'sld_core': 'coreShellDiskScatteringLengthCore',
            'sld_shell': 'coreShellDiskScatteringLengthShell',
            'sld_solvent': 'coreShellDiskScatteringLengthSolvent',
            'thickness': 'coreShellDiskThickness',
            'radius_pd_type': 'schulz',
            'radius_pd_n': 40,
            'radius_pd_nsigma': 3
    }
    return process_request(data, 'core_shell_cylinder', param_mapping)

MORPHOLOGY_FUNCTIONS = {
    "Sphere": graphASphere,
    "CoreShellSphere": graphACoreShellSphere,
    "Cylinder": graphACylinder,
    "CoreShellCylinder": graphACoreShellCylinder,
    "Disk": graphADisk,
    "CoreShellDisk": graphACoreShellDisk
}

@app.route('/simulate_graph', methods=['POST'])
def simulate_graph():
    operation_start = time.time()
    request_id = request_id_var.get() or str(uuid.uuid4())
    error_occured = False
    morphology = None
    
    data = request.get_json()
    try:
        if not data or "morphology" not in data:
            logger.warning("simulate_graph_validation_failed", reason="Morphology not specified")
            return jsonify({"error": "Morphology not specified"}), 400
        morphology = data["morphology"]
    
        if morphology not in MORPHOLOGY_FUNCTIONS:
            logger.warning(
                "simulate_graph_validation_failed",
                reason="Invalid morphology",
                requested_morphology=morphology,
                available_morphologies=list(MORPHOLOGY_FUNCTIONS.keys())
            )
            return jsonify({"error": "Invalid morphology"}), 400
        should_log = should_sample(request_id, "simulate_graph") # 1% condition is met, log the request
        if should_log:
            logger.info(
                "simulate_graph_requested",
                request_id=request_id,
                morphology=morphology,
                parameters=data
            )
        # Call the function
        try:
            response = MORPHOLOGY_FUNCTIONS[morphology](data)
            if should_log:
                logger.info(
                    "simulate_graph_calculation_completed",
                    request_id=request_id,
                    morphology=morphology,
                    duration_ms=round((time.time() - operation_start) * 1000, 2)
                )
        except Exception as e:
            error_occured = True

            logger.error(
                "simulate_graph_calculation_failed",
                request_id=request_id,
                morphology=morphology,
                error=str(e),
                traceback=traceback.format_exc()
            )
            return jsonify({"error": f"Calculation error: {str(e)}"}), 500
        
        total_duration_ms = round((time.time() - operation_start) * 1000, 2)

        update_metrics(
            "simulate_graph",
            total_duration_ms,
            error=error_occured,
            metadata={
                "morphology": morphology,
            }
        )

        if should_log: # log performance
            log_performace(
                logger,
                "simulate_graph",
                operation_start,
                request_id=request_id,
                morphology=morphology,
                duration_ms=total_duration_ms,
            )

        return jsonify(response)
    except Exception as e:
        error_occured = True

        logger.error(
            "simulate_graph_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )

        duration_ms = round((time.time() - operation_start) * 1000, 2)
        update_metrics( # update metrics with an error
            "simulate_graph",
            duration_ms,
            error=True,
            metadata={
                "morphology": morphology,
            }
        )
        return jsonify({"error": "Graph simulation failed"}), 500


@app.before_first_request
def log_app_start():
    """Log flask startup info"""
    logger.info(
        "application_start",
        version="senior_design_2025",
        flask_env=os.environ.get("FLASK_ENV", "development"),
        debug_mode=True,
        python_version=platform.python_version(),
        platform=platform.platform(),
        host=socket.gethostname()
    )

def log_health():
    """Program health logging"""
    mem_usage = 0
    try:
        import psutil # yes this works and how it should be imported in this case
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss
    except ImportError:
        pass

    logger.info(
        "health_check",
        memory_usage_mb=round(mem_usage / (1024 * 1024), 2) if mem_usage else None,
        uptime_seconds=int(time.time() - app.config.get("START_TIME", time.time()))
    )

@app.route('/health_check', methods=['GET'])
def health_check():
    log_health()
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.config["START_TIME"] = time.time()
    app.run(debug=True)

