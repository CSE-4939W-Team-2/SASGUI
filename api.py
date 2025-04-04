from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sasmodels.core import load_model
from sasmodels.direct_model import call_kernel
import sys
sys.path.append('hierarchical_SAS_analysis-main 2')
import numpy as np

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

import startup

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

# TODO: database connection
DATABASE = {}

# FIle Handling
import os

UPLOAD_FOLDER = os.path.abspath("hierarchical_SAS_analysis-main 2/data") # Directly use the existing folder path

@app.route('/upload', methods=['POST'])
@log_request
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
        file.save(os.path.join("./", file.filename))

        file_size = os.path.getsize(file.filename)
        file_extension = os.path.splitext(file.filename)[1]

        logger.info(
            "file_uploaded",
            filename=file.filename,
            file_size_bytes=file_size,
            file_extension=file_extension,
            context_type=file.context_type
        )

        log_performace(
            logger,
            "file_upload",
            operation_start,
            file_size_bytes=file_size,
            filename=file.filename
        )

        return jsonify({'message': 'File successfully uploaded'}), 200
    except Exception as e:
        logger.error(
            "file_upload_failed",
            filename=file.filename if file else "unknown",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({'message': 'File upload failed'}), 500

@app.route("/chd", methods=['POST','GET'])
@log_request
def chd():
    if request.method == 'POST':
            operation_start = time.time()

            try:
                json  = request.get_json()
                shape = json.get('shape')
                logger.info("chd_shape_received", shape=shape)

                # result = startup.main(shape)

                logger.info("chd_processing_success", shape=shape)

                log_performace(
                    logger,
                    "chd_processing",
                    operation_start,
                    shape=shape
                )

                return None #result
            except Exception as e:
                logger.error(
                    "chd_processing_failed",
                    error=str(e),
                    error_type=type(e).__name__,
                    traceback=traceback.format_exc()
                )
                return jsonify({'message': 'CHD processing failed'}), 500
            
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Fixed filename
        file.save(file_path)
        #return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200
        result = startup.main2(file_path)
        print("Function output:", result)  # Check if function returns a valid dictionary
        os.remove(file_path)
        return jsonify(result)
    return jsonify({'message': 'Fatal error in ML model'}), 400
    

@app.route("/shape", methods=['POST','GET'])
def chd():
    if request.method == 'POST':
            json  = request.get_json()
            shape = json.get('shape')
            return startup.main(shape) #returns dimensions for morphology
    return {'name': 5}


# Param Updates, dont think we use this -- Not added to logging
@app.route('/update_params', methods=['POST'])
def update_params():
    """Updates parameters for the prediction model."""
    params = request.json
    
    # TODO: Validate and update parameters in the system
    return jsonify({"message": "Parameters updated", "params": params})


# ML?
@app.route('/predict', methods=['POST'])
@log_request
def predict():
    """Calls the ML classifier to predict shape."""
    operation_start = time.time()

    try:
        input_data = request.json  # Expecting input parameters

        logger.info("prediction_request", input_data=input_data)
        
        # TODO: Call the trained ML model for prediction
        prediction = {"shape": "predicted_shape", "confidence": 0.95}  # test response

        logger.info("prediction_success", prediction=prediction, confidence=prediction.get("confidence"))

        log_performace(
            logger,
            "prediction",
            operation_start,
        )
        
        return jsonify({"message": "Prediction successful", "prediction": prediction})
    except Exception as e:
        logger.error(
            "prediction_failed",
            error = str(e),
            input_data = input_data if 'input_data' in locals() else None,
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Prediction failed"}), 500


# Curve SImulations
@app.route('/simulate_curve', methods=['POST'])
@log_request
def simulate_curve():
    """Simulates a curve based on input parameters."""
    operation_start = time.time()

    try:
        params = request.json

        logger.info("curve_simulation_request", params=params)
        
        # TODO: Implement curve simulation logic
        simulated_curve = {"curve_data": [0, 1, 2, 3]}  # test response

        logger.info("curve_simulation_success", curve_points=len(simulated_curve.get("curve_data", [])))

        log_performace(
            logger,
            "curve_simulation",
            operation_start
        )

        
        return jsonify({"message": "Curve simulated", "curve": simulated_curve})
    except Exception as e:
        logger.error(
            "curve_simulation_failed",
            error=str(e),
            params=params if 'params' in locals() else None,
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Curve simulation failed"}), 500


@app.route('/get_3d_model', methods=['GET'])
@log_request
def get_3d_model():
    """Fetches a 3D model."""
    operation_start = time.time()
    
    try:
        logger.info("3d_model_request")

        # TODO: Fetch or generate a 3D model
        model_data = {"model": "3D_model_placeholder"}  # test response

        logger.info("3d_model_generated")

        log_performace(
            logger,
            "3d_model_generation",
            operation_start
        )

        return jsonify({"message": "3D Model generated", "model": model_data})
    except Exception as e:
        logger.error(
            "3d_model_generation_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "3D Model generation failed"}), 500


# DB # TODO: update
@app.route('/save_to_database', methods=['POST'])
@log_request
def save_to_database():
    """Saves prediction or curve data to the database."""
    operation_start = time.time()

    try:
        data = request.json

        logger.info("database_save_request", data_size=len(json.dumps(data)))
        
        # TODO: Implement database save logic
        DATABASE["latest"] = data  # test database save

        logger.info("database_save_success")

        log_performace(
            logger,
            "database_save",
            operation_start
        )
        
        return jsonify({"message": "Data saved successfully"})
    except Exception as e:
        logger.error(
            "database_save_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Database save failed"}), 500


@app.route('/get_database_data', methods=['GET'])
@log_request
def get_database_data():
    """Retrieves data from the database."""
    operation_start = time.time()
    
    try:
        logger.info("database_retrieval_request")

        # TODO: Implement database retrieval logic
        stored_data = DATABASE.get("latest", {})

        logger.info("database_retrieval_success", data_found=bool(stored_data),data_size=len(json.dumps(stored_data)) if stored_data else 0)

        log_performace(
            logger,
            "database_retrieval",
            operation_start
        )
        
        return jsonify({"message": "Data retrieved", "data": stored_data})
    except Exception as e:
        logger.error(
            "database_retrieval_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Database retrieval failed"}), 500


# Output and Visualization
@app.route('/generate_graph', methods=['POST'])
@log_request
def generate_graph():
    """Generates a graph based on input data."""
    operation_start = time.time()

    try:
        input_data = request.json
        
        logger.info("graph_generation_request", input_data=input_data)

        # TODO: Implement graph generation logic
        graph_data = {"graph": "graph_placeholder"}  # test response

        logger.info("graph_generation_success")

        log_performace(
            logger,
            "graph_generation",
            operation_start
        )
        
        return jsonify({"message": "Graph generated", "graph": graph_data})
    except Exception as e:
        logger.error(
            "graph_generation_failed",
            error=str(e),
            input_data=input_data if 'input_data' in locals() else None,
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "Graph generation failed"}), 500


@app.route('/output_3d_model', methods=['GET'])
@log_request
def output_3d_model():
    """Outputs the 3D model for display."""
    operation_start = time.time()
    
    try:
        logger.info("3d_model_display_request")

        # TODO: Retrieve and serve 3D model data
        output_model = {"3D_model": "display_3D_model_placeholder"}  # test response

        logger.info("3d_model_display_success")
        
        log_performace(
            logger,
            "3d_model_display",
            operation_start
        )
        
        return jsonify({"message": "3D Model displayed", "model": output_model})
    except Exception as e:
        logger.error(
            "3d_model_display_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"message": "3D Model display failed"}), 500

# -----
#SASVIEW
def process_request(json, model_name, param_mapping):
    """Helper function to process requests and generate scattering data."""
    operation_start = time.time()
    request_id = request_id_var.get() or str(uuid.uuid4())

    try:
        logger.info(
            "scattering_calculation_requested",
            request_id=request_id,
            model_name=model_name,
            param_count=len(param_mapping)
        )

        q = np.loadtxt('q_200.txt', delimiter=',', dtype=float)

        logger.info("q_values_loaded", q_points=len(q))

        pars = param_mapping.copy()
        
        for key, json_key in param_mapping.items():
            if json_key in json:
                pars[key] = json.get(json_key)
            
        logger.info("parameters_mapped", parameters=pars)
        
        model = load_model(model_name)

        logger.info("model_loaded", model_name=model_name)

        kernel = model.make_kernel([q])

        logger.info("kernel_made")

        Iq = call_kernel(kernel, pars) + 0.001

        logger.info("scattering_calculation_completed", q_points=len(q), Iq_points=len(Iq))
        
        response = {'xval': np.array(q).tolist(), 'yval': np.array(Iq).tolist()}
        
        log_performace(
            logger,
            "scattering_calculation",
            operation_start,
            q_points=len(q),
            Iq_points=len(Iq)
        )

        return response
    
    except Exception as e:
        logger.error(
            "scattering_calculation_failed",
            error=str(e),
            request_id=request_id,
            traceback=traceback.format_exc()
        )
        raise

"""@app.route("/simulate_graph", methods=["POST"])
def sim_graph():
    if request.method == 'POST':
        json_data = request.get_json()
        return(json_data)"""

def graphASphere(data):
    """'radius_pd_type':'schulz',
            'radius_pd_n' : '40',
            'radius_pd_nsigma': '3',"""
    logger.info("sphere_calculation_requested", data=data)
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
@log_request
def simulate_graph():
    operation_start = time.time()
    try:
        data = request.get_json()

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

        logger.info(
            "simulate_graph_request",
            morphology=morphology,
            parameters=data
        )

        # Call the function
        response = MORPHOLOGY_FUNCTIONS[morphology](data)

        logger.info("simulate_graph_success", morphology=morphology)

        log_performace(
            logger,
            "simulate_graph",
            operation_start,
            morphology=morphology
        )

        return jsonify(response)
    except Exception as e:
        logger.error(
            "simulate_graph_failed",
            error=str(e),
            traceback=traceback.format_exc()
        )
        return jsonify({"error": "Graph simulation failed"}), 500
    
# @app.route("/graphcsd", methods=['POST','GET'])
# def chartcsd():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'length': 'h',
#             'radius': 'radius',
#             'background': 0.001,
#             'scale': 1,
#             'length_pd': 0.5,
#             'length_pd_type': 'schulz',
#             'length_pd_n': 40,
#             'length_pd_nsigma': 3
#         }
#         return process_request(json_data, 'cylinder', param_mapping)
#     return {'name': 5}

# @app.route("/csd", methods=['POST','GET'])
# def csd():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'length': 'h',
#             'radius': 'radius',
#             'thickness': 'thickness',
#             'sld_core': 'sldcore',
#             'sld_shell': 'sldshell',
#             'sld_solvent': 'sldsolvent',
#             'background': 'background',
#             'scale': 'scale',
#             'length_pd': 'pd'
#         }
#         return process_request(json_data, 'core_shell_cylinder', param_mapping)
#     return {'name': 5}

# @app.route("/graph", methods=['POST','GET'])
# def chart():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'length': 'h',
#             'radius': 'radius',
#             'scale': 'scale',
#             'sld': 'sld',
#             'sld_solvent': 'sldsolvent',
#             'background': 'background',
#             'length_pd': 'pd'
#         }
#         return process_request(json_data, 'cylinder', param_mapping)
#     return {'name': 5}

# @app.route("/sph", methods=['POST','GET'])
# def spheregraph():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'radius': 'sphereRadius',
#             'scale': 'sphereScale',
#             'sld': 'sphereScatteringLengthDensity',
#             'background': 'sphereBackground',
#             'radius_pd': 'spherePolydispersity',
#             'sld_solvent': 'sphereScatteringLengthSolvent'
#         }
#         return process_request(json_data, 'sphere', param_mapping)
#     return {'name': 5}

# @app.route("/css", methods=['POST','GET'])
# def cssgraph():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'radius': 'radius',
#             'thickness': 'thickness',
#             'scale': 'scale',
#             'background': 'background',
#             'sld_core': 'sldcore',
#             'sld_shell': 'sldshell',
#             'sld_solvent': 'sldsolvent',
#             'radius_pd': 'pd'
#         }
#         return process_request(json_data, 'core_shell_sphere', param_mapping)
#     return {'name': 5}

# @app.route("/csc", methods=['POST','GET'])
# def cscgraph():
#     if request.method == 'POST':
#         json_data = request.get_json()
#         param_mapping = {
#             'radius': 'radius',
#             'thickness': 'thickness',
#             'length': 'h'
#         }
#         return process_request(json_data, 'core_shell_cylinder', param_mapping)
#     return {'name': 5}


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


"""def graphASphere(data):
    param_mapping = {
            'radius': 'sphereRadius',
            'scale': 'sphereScale',
            'sld': 'sphereScatteringLengthDensity',
            'background': 'sphereBackground',
            'radius_pd': 'spherePolydispersity',
            'sld_solvent': 'sphereScatteringLengthSolvent'
    }
    return process_request(data, 'sphere', param_mapping)"""

