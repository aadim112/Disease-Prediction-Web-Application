"""
Train the Heart Disease Prediction model and save artifacts.
Run this script once to generate model.pkl, scaler.pkl, and feature_columns.pkl
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

def train_and_save():
    # Load dataset
    df = pd.read_csv("HeartDisease.csv")
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Separate features and target (FIX: properly exclude target from features)
    y = df["target"].values
    X = df.drop("target", axis=1)

    # One-hot encode categorical features
    categorical_features = ["cp", "slope", "ca", "restecg", "thal"]
    X = pd.get_dummies(X, columns=categorical_features)

    # Scale continuous features
    continuous_features = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    scaler = StandardScaler()
    X[continuous_features] = scaler.fit_transform(X[continuous_features])

    # Save feature column order (important for prediction)
    feature_columns = X.columns.tolist()
    print(f"Total features after preprocessing: {len(feature_columns)}")
    print(f"Features: {feature_columns}")

    # Convert to float32 for consistency
    X_values = X.values.astype(np.float32)
    y_values = y.astype(np.float32)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_values, y_values, test_size=0.2, random_state=42
    )

    # Train RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    train_acc = rf.score(X_train, y_train) * 100
    test_acc = rf.score(X_test, y_test) * 100
    print(f"\nTraining Accuracy: {train_acc:.2f}%")
    print(f"Testing Accuracy:  {test_acc:.2f}%")

    # Save artifacts
    joblib.dump(rf, "model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(feature_columns, "feature_columns.pkl")

    print("\nModel artifacts saved:")
    print(f"  - model.pkl ({os.path.getsize('model.pkl') / 1024:.1f} KB)")
    print(f"  - scaler.pkl ({os.path.getsize('scaler.pkl') / 1024:.1f} KB)")
    print(f"  - feature_columns.pkl ({os.path.getsize('feature_columns.pkl') / 1024:.1f} KB)")

    # Quick validation
    sample = X_test[0].reshape(1, -1)
    pred = rf.predict(sample)[0]
    proba = rf.predict_proba(sample)[0]
    print(f"\nValidation — Sample prediction: {int(pred)}, Probabilities: {proba}")


if __name__ == "__main__":
    train_and_save()
