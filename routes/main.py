# ============================================================
# MAIN ROUTES (all dashboard pages)
# ============================================================

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Overview / Dashboard page."""
    return render_template("dashboard.html", active="dashboard")


@main_bp.route("/live")
def live():
    """Live monitoring page."""
    return render_template("live.html", active="live")


@main_bp.route("/history")
def history_page():
    """Historical analysis page."""
    return render_template("history.html", active="history")


@main_bp.route("/recommendations")
def recommendations():
    """Recommendations page."""
    return render_template("recommendations.html", active="recommendations")


@main_bp.route("/statistics")
def statistics_page():
    """Statistics & ML insights page."""
    return render_template("statistics.html", active="statistics")


@main_bp.route("/reports")
def reports():
    """PDF reports page."""
    return render_template("reports.html", active="reports")
