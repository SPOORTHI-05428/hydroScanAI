# ============================================================
# STATISTICS ROUTES
# ============================================================
# Returns averages, totals, trends, and ML model info.
# ============================================================

from flask import Blueprint, jsonify

from services import thingspeak, analysis, ml_service

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/api/statistics")
def statistics():
    """
    Return statistics from historical data plus ML model info.
    """

    from flask import request

    results = request.args.get("results", default=None, type=int)

    # Check model info
    model_info = ml_service.get_model_info()

    # Fetch history
    history_data, error = thingspeak.get_history(results)

    if error:
        return jsonify({
            "success": False,
            "error": error
        })

    # Compute statistics
    stats = analysis.compute_statistics(history_data)

    # Feature importance
    feature_importance = ml_service.get_feature_importance()

    return jsonify({
        "success": True,
        "statistics": stats,
        "model": model_info,
        "feature_importance": feature_importance
    })
