# ============================================================
# HYDROSCAN CONFIGURATION
# ============================================================
# Central configuration for the HydroScan Water Quality
# Monitoring System.
#
# IMPORTANT:
# Keep your existing hardware / sensors / ML model unchanged.
# Only the FEATURE ORDER must match the model training order.
# ============================================================

import os

# ------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------
# THINGSPEAK SETTINGS
# ------------------------------------------------------------

# ThingSpeak channel ID (your existing channel)
THINGSPEAK_CHANNEL_ID = "3438348"

# Leave blank if your channel is public
THINGSPEAK_READ_API_KEY = "GBVIDCOP4MMZNNYR"

# Number of historical readings to fetch for charts/settings
THINGSPEAK_HISTORY_RESULTS = 50


# ------------------------------------------------------------
# THINGSPEAK FIELD MAPPING
# ------------------------------------------------------------
# Field 1 = pH
# Field 2 = Turbidity (NTU)
# Field 3 = TDS (mg/L)
# Field 4 = Temperature (C)

FIELD_PH = "field1"
FIELD_TURBIDITY = "field2"
FIELD_TDS = "field3"
FIELD_TEMPERATURE = "field4"


# ------------------------------------------------------------
# FEATURE ORDER (must match model training order)
# ------------------------------------------------------------
# Order used in train.py:
#     FEATURES = [pH, Turbidity_NTU, TDS_mg_L, Temperature_C]

FEATURE_NAMES = [
    "pH",
    "Turbidity_NTU",
    "TDS_mg_L",
    "Temperature_C"
]


# ------------------------------------------------------------
# MODEL FILES
# ------------------------------------------------------------

MODEL_FILE = os.path.join(BASE_DIR, "hydroscan_water_quality_model.pkl")
SCALER_FILE = os.path.join(BASE_DIR, "hydroscan_scaler.pkl")
ENCODER_FILE = os.path.join(BASE_DIR, "hydroscan_label_encoder.pkl")
FEATURES_FILE = os.path.join(BASE_DIR, "hydroscan_features.pkl")


# ------------------------------------------------------------
# SAFE RANGES (WHO / general guidelines)
# ------------------------------------------------------------
# Used for water quality score, explanations, recommendations,
# alerts and usage advice.

SAFE_RANGES = {
    "pH": {
        "min": 6.5,
        "max": 8.5,
        "label": "pH"
    },
    "Turbidity_NTU": {
        "min": 0,
        "max": 5,
        "label": "Turbidity"
    },
    "TDS_mg_L": {
        "min": 0,
        "max": 500,
        "label": "TDS"
    },
    "Temperature_C": {
        "min": 10,
        "max": 30,
        "label": "Temperature"
    }
}

# Weight of each parameter in the water quality score (sum = 100)
SCORE_WEIGHTS = {
    "pH": 30,
    "Turbidity_NTU": 25,
    "TDS_mg_L": 30,
    "Temperature_C": 15
}

# Alert thresholds (beyond which a red warning is shown)
ALERT_THRESHOLDS = {
    "pH": {"min": 6.0, "max": 8.8},
    "Turbidity_NTU": {"max": 5},
    "TDS_mg_L": {"max": 500},
    "Temperature_C": {"min": 10, "max": 30}
}


# ------------------------------------------------------------
# WATER USAGE CRITERIA
# ------------------------------------------------------------
# Each category has a max allowable value. If a sensor value
# exceeds the category limit, that usage is not allowed.

USAGE_LIMITS = {
    "Drinking": {"TDS_mg_L": 500, "Turbidity_NTU": 5, "pH_min": 6.5, "pH_max": 8.5},
    "Cooking": {"TDS_mg_L": 500, "Turbidity_NTU": 5},
    "Bathing": {"TDS_mg_L": 1200, "Turbidity_NTU": 10},
    "Washing": {"TDS_mg_L": 1500, "Turbidity_NTU": 20},
    "Irrigation": {"TDS_mg_L": 2000, "Turbidity_NTU": 50}
}


# ------------------------------------------------------------
# FLASK SETTINGS
# ------------------------------------------------------------

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("PORT", os.getenv("FLASK_PORT", "5000")))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in {"1", "true", "yes", "on"}

# Secret key for sessions (change in production)
SECRET_KEY = os.getenv("SECRET_KEY", "hydroscan-secret-key-change-me")
