# ============================================================
# HYDROSCAN - DEVELOPMENT RUNNER
# ============================================================
# Alternative way to run the app:
#     python run.py
# ============================================================

from app import create_app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
