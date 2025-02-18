from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# TODO: database connection
DATABASE = {}

# FIle Handling
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file upload."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    filepath = os.path.join("uploads", file.filename)
    
    # TODO: Save file to gibven path
    file.save(filepath)
    
    return jsonify({"message": "File uploaded successfully", "filepath": filepath})


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

if __name__ == '__main__':
    app.run(debug=True)