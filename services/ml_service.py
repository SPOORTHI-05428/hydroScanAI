# ============================================================
# HYDROSCAN ML SERVICE
# ============================================================
# Handles loading of the trained Random Forest model and
# performing predictions.
#
# The trained model (.pkl files) are KEPT UNCHANGED.
# This module only loads and uses them.
# ============================================================

import joblib
import numpy as np

import config


# ------------------------------------------------------------
# GLOBALS (loaded once at startup)
# ------------------------------------------------------------

model = None
scaler = None
label_encoder = None
feature_names = config.FEATURE_NAMES


# ------------------------------------------------------------
# LOAD MODEL
# ------------------------------------------------------------

def load_model():
    """Load the ML model, scaler and label encoder from disk."""

    global model, scaler, label_encoder, feature_names

    try:

        model = joblib.load(config.MODEL_FILE)
        scaler = joblib.load(config.SCALER_FILE)
        label_encoder = joblib.load(config.ENCODER_FILE)

        # Try to load feature names if present
        try:
            feature_names = joblib.load(config.FEATURES_FILE)
        except Exception:
            feature_names = config.FEATURE_NAMES

        return True, "ML model loaded successfully"

    except Exception as e:

        model = None
        scaler = None
        label_encoder = None

        return False, f"Model loading failed: {e}"


# ------------------------------------------------------------
# MODEL STATUS
# ------------------------------------------------------------

def is_loaded():
    return model is not None


def get_model_info():
    """Return model type and loaded feature names."""

    return {
        "model_type": type(model).__name__ if model else None,
        "labels": list(label_encoder.classes_) if label_encoder else [],
        "feature_names": feature_names,
        "loaded": is_loaded()
    }


# ------------------------------------------------------------
# PREDICT
# ------------------------------------------------------------
# Input is a dict with PH, Turbidity, TDS, Temperature.
# Returns prediction dict.

def predict(ph, turbidity, tds, temperature):
    """
    Predict water quality from sensor readings.

    Returns a dict:
    {
      "success": bool,
      "prediction": str,
      "prediction_code": int,
      "confidence": float or None,
      "probabilities": dict or None,
      "error": str (if failed)
    }
    """

    if not is_loaded():
        return {
            "success": False,
            "error": "ML model is not loaded"
        }

    try:

        # Build input array in the SAME ORDER as training
        input_data = np.array([
            [
                float(ph),
                float(turbidity),
                float(tds),
                float(temperature)
            ]
        ])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)
        prediction_code = int(prediction[0])

        # Decode label
        predicted_label = label_encoder.inverse_transform(
            prediction
        )[0]

        # Confidence
        confidence = None
        probabilities = None

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(input_scaled)[0]
            confidence = float(np.max(probs) * 100)
            probabilities = {
                str(label_encoder.inverse_transform(
                    np.array([i])
                )[0]): round(float(p) * 100, 2)
                for i, p in enumerate(probs)
            }

        return {
            "success": True,
            "prediction": str(predicted_label),
            "prediction_code": prediction_code,
            "confidence": confidence,
            "probabilities": probabilities
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ------------------------------------------------------------
# MODEL PERFORMANCE (accuracy, feature importance, confusion)
# ------------------------------------------------------------
# The Random Forest model exposes feature_importances_.
# For accuracy/confusion we retrain quickly on the dataset,
# or derive from the loaded model. Here we compute feature
# importance from the loaded model and store accuracy info.

def get_feature_importance():
    """Return feature importance from the loaded model."""

    if not is_loaded():
        return []

    if not hasattr(model, "feature_importances_"):
        return []

    importances = model.feature_importances_

    return [
        {
            "feature": feature_names[i]
                if i < len(feature_names)
                else f"Feature {i}",
            "importance": round(float(imp) * 100, 2)
        }
        for i, imp in enumerate(importances)
    ]
