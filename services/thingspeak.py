# ============================================================
# HYDROSCAN THINGSPEAK SERVICE
# ============================================================
# Handles fetching live and historical sensor data from
# ThingSpeak. Uses the SAME channel and API keys as the
# original project. No hardware changes.
# ============================================================

import requests

import config


# ------------------------------------------------------------
# INTERNAL: build request params
# ------------------------------------------------------------

def _build_params(extra=None):
    params = {}
    if config.THINGSPEAK_READ_API_KEY:
        params["api_key"] = config.THINGSPEAK_READ_API_KEY
    if extra:
        params.update(extra)
    return params


# ------------------------------------------------------------
# GET LATEST SENSOR DATA
# ------------------------------------------------------------

def get_latest():
    """
    Fetch the latest sensor reading from ThingSpeak.

    Returns (sensor_data, error)
    sensor_data dict:
    {
      "pH": float, "Turbidity_NTU": float,
      "TDS_mg_L": float, "Temperature_C": float,
      "timestamp": str
    }
    """

    try:

        url = (
            f"https://api.thingspeak.com/channels/"
            f"{config.THINGSPEAK_CHANNEL_ID}/feeds/last.json"
        )

        response = requests.get(
            url,
            params=_build_params(),
            timeout=10
        )

        if response.status_code != 200:
            return None, (
                f"ThingSpeak returned HTTP {response.status_code}"
            )

        data = response.json()

        if not isinstance(data, dict):
            return None, "Unexpected ThingSpeak response"

        ph = data.get(config.FIELD_PH)
        turbidity = data.get(config.FIELD_TURBIDITY)
        tds = data.get(config.FIELD_TDS)
        temperature = data.get(config.FIELD_TEMPERATURE)

        if (
            ph is None or
            turbidity is None or
            tds is None or
            temperature is None
        ):
            return None, "Some ThingSpeak fields are empty"

        sensor_data = {
            "pH": float(ph),
            "Turbidity_NTU": float(turbidity),
            "TDS_mg_L": float(tds),
            "Temperature_C": float(temperature),
            "timestamp": data.get("created_at", "")
        }

        return sensor_data, None

    except Exception as e:

        return None, str(e)


# ------------------------------------------------------------
# GET HISTORY (for charts / statistics)
# ------------------------------------------------------------

def get_history(results=None):
    """
    Fetch historical sensor data from ThingSpeak.

    Returns (list_of_dicts, error).
    Each dict:
    {
      "timestamp": str,
      "ph": float, "turbidity": float,
      "tds": float, "temperature": float
    }
    """

    if results is None:
        results = config.THINGSPEAK_HISTORY_RESULTS

    try:

        url = (
            f"https://api.thingspeak.com/channels/"
            f"{config.THINGSPEAK_CHANNEL_ID}/feeds.json"
        )

        response = requests.get(
            url,
            params=_build_params({"results": results}),
            timeout=10
        )

        if response.status_code != 200:
            return None, (
                f"ThingSpeak returned HTTP {response.status_code}"
            )

        data = response.json()

        feeds = data.get("feeds", [])

        history = []

        for feed in feeds:

            ph = feed.get(config.FIELD_PH)
            turbidity = feed.get(config.FIELD_TURBIDITY)
            tds = feed.get(config.FIELD_TDS)
            temperature = feed.get(config.FIELD_TEMPERATURE)

            if (
                ph is None or
                turbidity is None or
                tds is None or
                temperature is None
            ):
                continue

            history.append({
                "timestamp": feed.get("created_at", ""),
                "ph": float(ph),
                "turbidity": float(turbidity),
                "tds": float(tds),
                "temperature": float(temperature)
            })

        return history, None

    except Exception as e:

        return None, str(e)
