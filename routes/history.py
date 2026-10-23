# ============================================================
# HISTORY ROUTES
# ============================================================
# Fetch historical ThingSpeak data for charts and trend analysis.
# ============================================================

from flask import Blueprint, jsonify

from services import thingspeak

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history")
def history():
    """
    Return historical sensor data from ThingSpeak for charts.
    Query param: ?results=50 (optional)
    """

    from flask import request

    results = request.args.get("results", default=None, type=int)

    history_data, error = thingspeak.get_history(results)

    if error:
        return jsonify({
            "success": False,
            "error": error
        })

    return jsonify({
        "success": True,
        "history": history_data
    })
