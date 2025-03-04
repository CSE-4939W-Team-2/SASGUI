from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sasmodels.core import load_model
from sasmodels.direct_model import call_kernel
import sys
sys.path.append('hierarchical_SAS_analysis-main 2')
import numpy as np


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins":"http://localhost:5173"}})
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

@app.route("/chd", methods=['POST','GET'])
def chd():
    if request.method == 'POST':
            json  = request.get_json()
            shape = json.get('shape')
            return startup.main(shape)
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

@app.route("/graphcsd", methods=['POST','GET'])
def chartcsd():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'length': 'h',
            'radius': 'radius',
            'background': 0.001,
            'scale': 1,
            'length_pd': 0.5,
            'length_pd_type': 'schulz',
            'length_pd_n': 40,
            'length_pd_nsigma': 3
        }
        return process_request(json_data, 'cylinder', param_mapping)
    return {'name': 5}

@app.route("/csd", methods=['POST','GET'])
def csd():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'length': 'h',
            'radius': 'radius',
            'thickness': 'thickness',
            'sld_core': 'sldcore',
            'sld_shell': 'sldshell',
            'sld_solvent': 'sldsolvent',
            'background': 'background',
            'scale': 'scale',
            'length_pd': 'pd'
        }
        return process_request(json_data, 'core_shell_cylinder', param_mapping)
    return {'name': 5}

@app.route("/graph", methods=['POST','GET'])
def chart():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'length': 'h',
            'radius': 'radius',
            'scale': 'scale',
            'sld': 'sld',
            'sld_solvent': 'sldsolvent',
            'background': 'background',
            'length_pd': 'pd'
        }
        return process_request(json_data, 'cylinder', param_mapping)
    return {'name': 5}

@app.route("/sph", methods=['POST','GET'])
def spheregraph():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'radius': 'radius',
            'scale': 'scale',
            'sld': 'sld',
            'background': 'background',
            'radius_pd': 'pd',
            'sld_solvent': 'solvent'
        }
        return process_request(json_data, 'sphere', param_mapping)
    return {'name': 5}

@app.route("/css", methods=['POST','GET'])
def cssgraph():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'radius': 'radius',
            'thickness': 'thickness',
            'scale': 'scale',
            'background': 'background',
            'sld_core': 'sldcore',
            'sld_shell': 'sldshell',
            'sld_solvent': 'sldsolvent',
            'radius_pd': 'pd'
        }
        return process_request(json_data, 'core_shell_sphere', param_mapping)
    return {'name': 5}

@app.route("/csc", methods=['POST','GET'])
def cscgraph():
    if request.method == 'POST':
        json_data = request.get_json()
        param_mapping = {
            'radius': 'radius',
            'thickness': 'thickness',
            'length': 'h'
        }
        return process_request(json_data, 'core_shell_cylinder', param_mapping)
    return {'name': 5}
if __name__ == '__main__':
    app.run(debug=True)