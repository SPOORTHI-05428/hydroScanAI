# ============================================================
# HYDROSCAN - FLASK APPLICATION ENTRY POINT
# ============================================================
# Creates and configures the Flask application (app factory).
# Registers all blueprints and loads the ML model.
#
# Run with:
#     python app.py
# ============================================================

from flask import Flask

import config
from services import ml_service
from routes.main import main_bp
from routes.predict import predict_bp
from routes.history import history_bp
from routes.statistics import statistics_bp
from routes.report import report_bp


def create_app():
    """Application factory for the HydroScan Flask app."""

    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # --------------------------------------------------------
    # Register blueprints
    # --------------------------------------------------------

    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(report_bp)

    # --------------------------------------------------------
    # Load ML model at startup
    # --------------------------------------------------------

    ok, msg = ml_service.load_model()

    print("\n========================================")
    print("HYDROSCAN WATER QUALITY MONITORING")
    print("========================================")
    print("ML Model:", msg)
    if ok:
        print("Model Type:", ml_service.get_model_info()["model_type"])
        print("Labels:", ml_service.get_model_info()["labels"])
    print("========================================\n")

    return app


app = create_app()


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n========================================")
    print("HydroScan Flask Server Starting...")
    print("========================================")
    print(f"Local URL  : http://127.0.0.1:{config.FLASK_PORT}")
    print(f"Network URL: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print("========================================\n")

    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG,
        threaded=True
    )
