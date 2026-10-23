from flask import Flask, render_template, jsonify
import requests
import joblib
import numpy as np
import traceback
import os

app = Flask(__name__)

# ============================================================
# THINGSPEAK SETTINGS
# ============================================================

CHANNEL_ID = "3438348"

# Leave blank if your channel is public
READ_API_KEY = "GBVIDCOP4MMZNNYR"

# ============================================================
# FEATURE ORDER
# ============================================================

FEATURE_NAMES = [
    "pH",
    "TDS_mg_L",
    "Turbidity_NTU",
    "Temperature_C"
]

# ============================================================
# MODEL FILES
# ============================================================

MODEL_FILE = "hydroscan_water_quality_model.pkl"
SCALER_FILE = "hydroscan_scaler.pkl"
ENCODER_FILE = "hydroscan_label_encoder.pkl"

# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    label_encoder = joblib.load(ENCODER_FILE)

    print("========================================")
    print("HYDROSCAN ML MODEL LOADED SUCCESSFULLY")
    print("========================================")

    print("Model Type :", type(model))
    print("Scaler Type :", type(scaler))
    print("Label Encoder Type :", type(label_encoder))

except Exception as e:

    print("========================================")
    print("MODEL LOADING FAILED")
    print("========================================")
    traceback.print_exc()

    model = None
    scaler = None
    label_encoder = None

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")

# ============================================================
# GET LATEST THINGSPEAK DATA
# ============================================================

def get_thingspeak_data():

    try:

        url = (
            f"https://api.thingspeak.com/channels/"
            f"{CHANNEL_ID}/feeds/last.json"
        )

        params = {}

        if READ_API_KEY:
            params["api_key"] = READ_API_KEY

        print("\n========================================")
        print("REQUESTING DATA FROM THINGSPEAK")
        print("========================================")
        print("URL :", url)
        print("PARAMS :", params)

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        print("HTTP STATUS :", response.status_code)
        print("RAW RESPONSE :")
        print(response.text)

        if response.status_code != 200:

            return None, (
                f"ThingSpeak returned HTTP "
                f"{response.status_code}"
            )

        data = response.json()

        print("\nJSON TYPE :", type(data))
        print("JSON DATA :", data)

        if not isinstance(data, dict):

            return None, (
                f"Unexpected ThingSpeak response "
                f"type : {type(data)}"
            )

        # --------------------------------------------
        # READ VALUES
        # --------------------------------------------

        ph = data.get("field1")
        turbidity = data.get("field2")
        tds = data.get("field3")
        temperature = data.get("field4")

        print("\nSensor Values")
        print("----------------------------")
        print("pH :", ph)
        print("Turbidity :", turbidity)
        print("TDS :", tds)
        print("Temperature :", temperature)

        if (
            ph is None or
            turbidity is None or
            tds is None or
            temperature is None
        ):

            return None, (
                "Some ThingSpeak fields are empty."
            )

        sensor_data = {

            "pH": float(ph),

            "Turbidity_NTU": float(turbidity),

            "TDS_mg_L": float(tds),

            "Temperature_C": float(temperature),

            "timestamp": data.get(
                "created_at",
                ""
            )

        }

        print("\nSensor Dictionary")
        print(sensor_data)

        return sensor_data, None

    except Exception as e:

        traceback.print_exc()

        return None, str(e)
    # ============================================================
# PREDICT WATER QUALITY
# ============================================================

@app.route("/predict", methods=["GET"])
def predict():

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if model is None:

        return jsonify({

            "success": False,

            "error": "ML Model is not loaded."

        })

    # --------------------------------------------------------
    # GET SENSOR DATA
    # --------------------------------------------------------

    sensor_data, error = get_thingspeak_data()

    if error:

        return jsonify({

            "success": False,

            "error": error

        })

    try:

        # ----------------------------------------------------
        # EXTRACT SENSOR VALUES
        # ----------------------------------------------------

        ph = sensor_data["pH"]

        turbidity = sensor_data["Turbidity_NTU"]

        tds = sensor_data["TDS_mg_L"]

        temperature = sensor_data["Temperature_C"]

        print("\n========================================")
        print("NEW WATER QUALITY PREDICTION")
        print("========================================")

        print("pH :", ph)
        print("Turbidity :", turbidity)
        print("TDS :", tds)
        print("Temperature :", temperature)

        # ----------------------------------------------------
        # CREATE INPUT ARRAY
        # ----------------------------------------------------

        input_data = np.array([
            [
                ph,
                turbidity,
                tds,
                temperature
            ]
        ])

        print("\nInput Array")
        print(input_data)

        # ----------------------------------------------------
        # SCALE INPUT
        # ----------------------------------------------------

        print("\nScaling Input...")

        input_scaled = scaler.transform(input_data)

        print("Scaled Input")
        print(input_scaled)

        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        print("\nRunning Prediction...")

        prediction = model.predict(input_scaled)

        print("Prediction Output :", prediction)
        print("Prediction Type :", type(prediction))

        # ----------------------------------------------------
        # LABEL DECODING
        # ----------------------------------------------------

        print("\nDecoding Label...")

        predicted_label = label_encoder.inverse_transform(
            prediction
        )[0]

        print("Predicted Label :", predicted_label)

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        confidence = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                input_scaled
            )[0]

            print("\nPrediction Probabilities")
            print(probabilities)

            confidence = float(
                np.max(probabilities) * 100
            )

            print("Confidence :", confidence)

        # ----------------------------------------------------
        # PREPARE RESPONSE
        # ----------------------------------------------------

        result = {

            "success": True,

            "prediction": str(predicted_label),

            "confidence":
                round(confidence, 2)
                if confidence is not None
                else None,

            "pH":
                round(ph, 2),

            "Turbidity_NTU":
                round(turbidity, 2),

            "TDS_mg_L":
                round(tds, 2),

            "Temperature_C":
                round(temperature, 2),

            "timestamp":
                sensor_data["timestamp"]

        }

        print("\nPrediction Completed Successfully")

        print(result)

        return jsonify(result)

    except Exception as e:

        print("\n========================================")
        print("PREDICTION ERROR")
        print("========================================")

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        })
    # ============================================================
# RUN FLASK SERVER
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("HydroScan Water Quality Monitoring")
    print("Flask Server Starting...")
    print("========================================")

    print("Server URL (Local):")
    print("http://127.0.0.1:5000")

    print("\nServer URL (Network):")
    print("http://0.0.0.0:5000")

    print("\nWaiting for client requests...")
    print("========================================\n")

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True

    )