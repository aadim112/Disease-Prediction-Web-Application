"""
Heart Disease Prediction — Flask Web Application
Serves the frontend and provides a /predict API endpoint.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load model artifacts
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), "feature_columns.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(COLUMNS_PATH)

# Constants
CATEGORICAL_FEATURES = ["cp", "slope", "ca", "restecg", "thal"]
CONTINUOUS_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Convert string values to appropriate numeric types
        processed = {}
        for key, value in data.items():
            try:
                if "." in str(value):
                    processed[key] = float(value)
                else:
                    processed[key] = int(value)
            except (ValueError, TypeError):
                processed[key] = value

        # Create DataFrame from input
        input_df = pd.DataFrame([processed])

        # One-hot encode categorical features
        input_df = pd.get_dummies(input_df, columns=CATEGORICAL_FEATURES)

        # Ensure all expected columns are present (fill missing one-hot columns with 0)
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns to match training order
        input_df = input_df[feature_columns]

        # Scale continuous features
        input_df[CONTINUOUS_FEATURES] = scaler.transform(input_df[CONTINUOUS_FEATURES])

        # Convert to float32
        input_values = input_df.values.astype(np.float32)

        # Predict
        prediction = model.predict(input_values)[0]
        probability = model.predict_proba(input_values)[0]

        result = {
            "prediction": int(prediction),
            "probability": round(float(probability[1]) * 100, 1),
            "confidence": round(float(max(probability)) * 100, 1),
            "risk_level": "High Risk" if prediction == 1 else "Low Risk"
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
