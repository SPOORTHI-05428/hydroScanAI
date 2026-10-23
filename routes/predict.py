# ============================================================
# PREDICT ROUTES
# ============================================================
# Endpoints that combine live sensor data + ML prediction +
# analysis (score, explanation, purification, usage, alerts).
# ============================================================

from flask import Blueprint, jsonify

from services import ml_service, thingspeak, analysis

predict_bp = Blueprint("predict", __name__)


# ------------------------------------------------------------
# GET FULL ANALYSIS (used by dashboard on button click)
# ------------------------------------------------------------

@predict_bp.route("/predict")
def predict():
    """
    Fetch latest ThingSpeak data, run ML model, and return
    a complete analysis payload for the dashboard.
    """

    # 1. Check model loaded
    if not ml_service.is_loaded():
        return jsonify({
            "success": False,
            "error": "ML model is not loaded"
        })

    # 2. Get latest sensor data
    sensor_data, error = thingspeak.get_latest()

    if error:
        return jsonify({
            "success": False,
            "error": error
        })

    ph = sensor_data["pH"]
    turbidity = sensor_data["Turbidity_NTU"]
    tds = sensor_data["TDS_mg_L"]
    temperature = sensor_data["Temperature_C"]

    # 3. Run ML prediction
    ml_result = ml_service.predict(ph, turbidity, tds, temperature)

    if not ml_result["success"]:
        return jsonify({
            "success": False,
            "error": ml_result["error"]
        })

    # 4. Compute water quality score
    score_data = analysis.compute_score(ph, turbidity, tds, temperature)

    # 5. Generate AI explanation
    explanation = analysis.generate_explanation(ph, turbidity, tds, temperature)

    # 6. Purification recommendations
    purification = analysis.get_purification(ph, turbidity, tds, temperature)

    # 7. Usage recommendations
    usage = analysis.get_usage(ph, turbidity, tds, temperature)

    # 8. Alerts
    alerts = analysis.get_alerts(ph, turbidity, tds, temperature)

    # 9. Build response
    result = {
        "success": True,
        "prediction": ml_result["prediction"],
        "prediction_code": ml_result["prediction_code"],
        "confidence": ml_result["confidence"],
        "probabilities": ml_result["probabilities"],
        "sensor": {
            "pH": round(ph, 2),
            "Turbidity_NTU": round(turbidity, 2),
            "TDS_mg_L": round(tds, 2),
            "Temperature_C": round(temperature, 2),
            "timestamp": sensor_data["timestamp"]
        },
        "score": score_data,
        "explanation": explanation,
        "purification": purification,
        "usage": usage,
        "alerts": alerts
    }

    return jsonify(result)
