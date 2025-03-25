import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔥 Add this line
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)  # 🔥 Allow all origins (Fixes CORS issues)

# Ensure model and scaler files exist
model_path = "ml_model.pkl"
scaler_path = "scaler.pkl"

if os.path.exists(model_path) and os.path.exists(scaler_path):
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
    with open(scaler_path, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
else:
    raise FileNotFoundError("Model or Scaler file is missing!")

@app.route("/")
def home():
    return "ICU Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        features = data.get("features")
        if not features or not isinstance(features, list):
            return jsonify({"error": "Invalid input format. Expected JSON with 'features' list."}), 400

        # Convert to NumPy array and reshape
        features_array = np.array(features).reshape(1, -1)

        # Standardize using the scaler
        scaled_features = scaler.transform(features_array)

        # Get probability prediction
        probability = model.predict_proba(scaled_features)[:, 1][0]  

        return jsonify({"probability": float(probability)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
