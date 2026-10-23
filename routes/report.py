# ============================================================
# REPORT ROUTES
# ============================================================
# Generate and download a PDF report of the latest analysis.
# ============================================================

from flask import Blueprint, jsonify, send_file, Response
import io

from services import (
    ml_service, thingspeak, analysis, report as report_service
)

report_bp = Blueprint("report", __name__)


@report_bp.route("/api/report")
def generate_report():
    """
    Generate a PDF report of the latest sensor reading and
    analysis, and return it as a downloadable PDF.
    """

    # 1. Get latest sensor data
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

    # 2. ML prediction
    ml_result = ml_service.predict(ph, turbidity, tds, temperature)

    # 3. Score
    score_data = analysis.compute_score(ph, turbidity, tds, temperature)

    # 4. Explanation
    explanation = analysis.generate_explanation(ph, turbidity, tds, temperature)

    # 5. Purification
    purification = analysis.get_purification(ph, turbidity, tds, temperature)

    # 6. Usage
    usage = analysis.get_usage(ph, turbidity, tds, temperature)

    # 7. Build report data
    report_data = {
        "sensor_values": {
            "pH": ph,
            "Turbidity_NTU": turbidity,
            "TDS_mg_L": tds,
            "Temperature_C": temperature
        },
        "prediction": ml_result.get("prediction", "N/A"),
        "confidence": ml_result.get("confidence"),
        "score": score_data["score"],
        "score_category": score_data["category"],
        "explanation": explanation,
        "purification": purification,
        "usage": usage,
        "timestamp": sensor_data["timestamp"]
    }

    # 8. Generate PDF bytes
    try:
        pdf_bytes = report_service.generate_report(report_data)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"PDF generation failed: {e}"
        })

    # 9. Return PDF as download
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; filename=hydroscan_report.pdf"
        }
    )
