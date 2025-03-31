from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sasmodels.core import load_model
from sasmodels.direct_model import call_kernel
import sys
sys.path.append('hierarchical_SAS_analysis-main 2')
import numpy as np
import startup

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://sasgui.cse.uconn.edu:5173","sasgui.cse.uconn.edu:5173", "http://sasgui.cse.uconn.edu", "sasgui.cse.uconn.edu", "http://localhost:5173"]}})
# TODO: database connection
DATABASE = {}

# FIle Handling
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    if file:
        file.save(os.path.join("./", file.filename))
        return jsonify({'message': 'File successfully uploaded'}), 200
    return startup.main2() # returns predicted dimensions 
    
@app.route("/shape", methods=['POST','GET'])
def chd():
    if request.method == 'POST':
            json  = request.get_json()
            shape = json.get('shape')
            return startup.main(shape) #returns dimensions for morphology
    return {'name': 5}


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


# DB # TODO: update
@app.route('/save_to_database', methods=['POST'])
def save_to_database():
    """Saves prediction or curve data to the database."""
    data = request.json
    
    # TODO: Implement database save logic
    DATABASE["latest"] = data  # test database save
    
    return jsonify({"message": "Data saved successfully"})


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

