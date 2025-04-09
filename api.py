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

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://sasgui.cse.uconn.edu:5173","sasgui.cse.uconn.edu:5173", "http://sasgui.cse.uconn.edu", "sasgui.cse.uconn.edu", "http://localhost:5173"]}})
# TODO: database connection
DATABASE = {}

# FIle Handling
import os

UPLOAD_FOLDER = os.path.abspath("hierarchical_SAS_analysis-main 2/data") # Directly use the existing folder path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Fixed filename
        file.save(file_path)
        #return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200
        result = startup.main2(file_path)
        print("Function output:", result)  # Check if function returns a valid dictionary
        os.remove(file_path)
        return jsonify(result)
    return jsonify({'message': 'Fatal error in ML model'}), 400

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
        scan_names = [scan['name'] for scan in scans]
        
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
        
        # Assuming dbFunctions.get_scan_data_by_name_and_user_id(userId, scan_name) returns the scan data
        scan_data = dbFunctions.get_scan_data_by_name_and_user_id(userId, scan_name)
        
        if not scan_data:
            return jsonify({"message": "No data found for the given scan name and userId"}), 404
        
        return jsonify({"message": "Scan data retrieved successfully", "data": scan_data}), 200
    except Exception as e:
        print(f"Error retrieving scan data: {e}")
        return jsonify({"message": "Error retrieving scan data", "error": str(e)}), 500

@app.route("/shape", methods=['POST','GET'])
def chd():
    if request.method == 'POST':
            json  = request.get_json()
            shape = json.get('shape')
            return startup.main(shape) #returns dimensions for morphology
    return {'name': 5}

@app.route('/get_all_files', methods=['GET'])
def get_all_files():
    """Returns the names of all files in the upload folder."""
    try:
        # List all files in the upload folder
        file_names = os.listdir(UPLOAD_FOLDER)
        
        # Filter out directories, keep only files
        file_names = [f for f in file_names if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        
        return jsonify({"message": "Files retrieved successfully", "files": file_names}), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving files", "error": str(e)}), 500
    
@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    """Deletes a specified file from the upload folder."""
    try:
        # Get the filename from the request data
        data = request.get_json()
        file_name = data.get('file_name')
        
        if not file_name:
            return jsonify({"message": "No file name provided"}), 400

        # Construct the full file path
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"message": "File not found"}), 404
        
        # Remove the file
        os.remove(file_path)
        
        return jsonify({"message": f"File {file_name} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting file", "error": str(e)}), 500


# Param Updates, dont think we use this
@app.route('/update_params', methods=['POST'])
def update_params():
    """Updates parameters for the prediction model."""
    params = request.json
    
    # TODO: Validate and update parameters in the system
    return jsonify({"message": "Parameters updated", "params": params})


# ML?
@app.route('/predict', methods=['POST'])
def predict():
    """Calls the ML classifier to predict shape."""
    input_data = request.json  # Expecting input parameters
    
    # TODO: Call the trained ML model for prediction
    prediction = {"shape": "predicted_shape", "confidence": 0.95}  # test response
    
    return jsonify({"message": "Prediction successful", "prediction": prediction})


# Curve SImulations
@app.route('/simulate_curve', methods=['POST'])
def simulate_curve():
    """Simulates a curve based on input parameters."""
    params = request.json
    
    # TODO: Implement curve simulation logic
    simulated_curve = {"curve_data": [0, 1, 2, 3]}  # test response
    
    return jsonify({"message": "Curve simulated", "curve": simulated_curve})


@app.route('/get_3d_model', methods=['GET'])
def get_3d_model():
    """Fetches a 3D model."""
    
    # TODO: Fetch or generate a 3D model
    model_data = {"model": "3D_model_placeholder"}  # test response
    
    return jsonify({"message": "3D Model generated", "model": model_data})


@app.route('/save_to_database', methods=['POST'])
def save_to_database():
    """Saves prediction or curve data to the database."""
    try:
        data = request.json
        print(data)
        if "name" in data:
            dbFunctions.add_to_scans(file_name = data.get("name"), file_data = data.get("data"), userId = data.get("userId"))
            return jsonify({"message": "Data saved successfully"})
        else:
            dbFunctions.add_to_users(username = data.get("username"), password = data.get("password"), email = data.get("email"))
            return jsonify({"message": "Data saved successfully"})
    except Exception as e:
        print(f"Error saving to database: {e}")
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
    

@app.route('/get_database_data', methods=['GET'])
def get_database_data():
    """Retrieves data from the database."""
    
    # TODO: Implement database retrieval logic
    stored_data = DATABASE.get("latest", {})
    
    return jsonify({"message": "Data retrieved", "data": stored_data})


# Output and Visualization
@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    """Generates a graph based on input data."""
    input_data = request.json
    
    # TODO: Implement graph generation logic
    graph_data = {"graph": "graph_placeholder"}  # test response
    
    return jsonify({"message": "Graph generated", "graph": graph_data})


@app.route('/output_3d_model', methods=['GET'])
def output_3d_model():
    """Outputs the 3D model for display."""
    
    # TODO: Retrieve and serve 3D model data
    output_model = {"3D_model": "display_3D_model_placeholder"}  # test response
    
    return jsonify({"message": "3D Model displayed", "model": output_model})


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
    data = request.get_json()

    if not data or "morphology" not in data:
        return jsonify({"error": "Morphology not specified"}), 400

    morphology = data["morphology"]
    
    if morphology not in MORPHOLOGY_FUNCTIONS:
        return jsonify({"error": "Invalid morphology"}), 400

    # Call the function
    response = MORPHOLOGY_FUNCTIONS[morphology](data)

    return jsonify(response)
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




if __name__ == '__main__':
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

