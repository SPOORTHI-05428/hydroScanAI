# ============================================================
# HYDROSCAN ANALYSIS SERVICE
# ============================================================
# Contains the logic for:
#   1. Water Quality Score (0-100)
#   2. AI Explanation (why safe/unsafe)
#   3. Purification Recommendations
#   4. Water Usage Recommendations
#   5. Statistics (averages, totals)
#   6. Alerts
#
# All thresholds are defined in config.py.
# ============================================================

import config


# ------------------------------------------------------------
# NUMBER FORMATTING
# ------------------------------------------------------------

def _round(value, ndigits=2):
    try:
        return round(float(value), ndigits)
    except Exception:
        return value


# ------------------------------------------------------------
# 1. WATER QUALITY SCORE
# ------------------------------------------------------------

def compute_score(ph, turbidity, tds, temperature):
    """
    Compute a water quality score from 0 to 100.

    Each parameter is scored 0-100 based on how far it is
    from the safe range, then weighted average is taken.

    Returns: (score, category, color, details)
    where details is a list of per-parameter scores.
    """

    ranges = config.SAFE_RANGES
    weights = config.SCORE_WEIGHTS

    readings = {
        "pH": ph,
        "Turbidity_NTU": turbidity,
        "TDS_mg_L": tds,
        "Temperature_C": temperature
    }

    details = []
    weighted_sum = 0.0
    total_weight = 0.0

    for param, weight in weights.items():

        value = float(readings[param])
        safe = ranges[param]

        # Score = 100 if within safe range
        #         0 if far outside, linear falloff beyond range
        if value < safe["min"]:
            # below min
            span = max(safe["min"] - 0.0, 1e-6)
            ratio = min(abs(value - safe["min"]) / span, 1.0)
            param_score = max(0, 100 - ratio * 100)
        elif value > safe["max"]:
            span = max(safe["max"] * 0.5 + 1e-6, 1e-6)
            ratio = min(abs(value - safe["max"]) / span, 1.0)
            param_score = max(0, 100 - ratio * 100)
        else:
            param_score = 100.0

        weighted_sum += param_score * weight
        total_weight += weight

        details.append({
            "parameter": safe["label"],
            "value": _round(value),
            "min": safe["min"],
            "max": safe["max"],
            "score": _round(param_score),
            "status": "ok" if param_score >= 70 else (
                "warning" if param_score >= 40 else "poor"
            )
        })

    if total_weight == 0:
        total_weight = 1

    overall_score = weighted_sum / total_weight

    # Assign category & color
    if overall_score >= 90:
        category = "Excellent"
        color = "green"
    elif overall_score >= 70:
        category = "Good"
        color = "yellow"
    elif overall_score >= 50:
        category = "Moderate"
        color = "orange"
    else:
        category = "Poor"
        color = "red"

    return {
        "score": _round(overall_score),
        "category": category,
        "color": color,
        "details": details
    }


# ------------------------------------------------------------
# 2. AI EXPLANATION
# ------------------------------------------------------------

def generate_explanation(ph, turbidity, tds, temperature):
    """
    Generate a human-readable explanation of WHY the water is
    safe/unsafe, automatically based on sensor values.
    """

    ranges = config.SAFE_RANGES

    issues = []
    ok_points = []

    # pH
    if ph < ranges["pH"]["min"]:
        issues.append("pH is below the safe range (acidic).")
    elif ph > ranges["pH"]["max"]:
        issues.append("pH is above the safe range (alkaline).")
    else:
        ok_points.append("pH is within the safe range.")

    # Turbidity
    if turbidity > ranges["Turbidity_NTU"]["max"]:
        issues.append("Turbidity is high (cloudy water).")
    else:
        ok_points.append("Turbidity is acceptable.")

    # TDS
    if tds > ranges["TDS_mg_L"]["max"]:
        issues.append("TDS is high (excess dissolved solids).")
    else:
        ok_points.append("TDS is acceptable.")

    # Temperature
    if temperature < ranges["Temperature_C"]["min"]:
        issues.append("Temperature is below the normal range.")
    elif temperature > ranges["Temperature_C"]["max"]:
        issues.append("Temperature is above the normal range.")
    else:
        ok_points.append("Temperature is normal.")

    if issues:
        verdict = "Unsafe"
        summary = "Water is Unsafe because:"
        points = issues
    else:
        verdict = "Safe"
        summary = "Water is Safe because:"
        points = ok_points

    return {
        "verdict": verdict,
        "summary": summary,
        "points": points,
        "issues": issues,
        "ok_points": ok_points
    }


# ------------------------------------------------------------
# 3. PURIFICATION RECOMMENDATIONS
# ------------------------------------------------------------

def get_purification(ph, turbidity, tds, temperature):
    """
    Suggest purification methods based on detected problems.
    Returns a list of recommendation dicts.
    """

    ranges = config.SAFE_RANGES

    recommendations = []

    if tds > ranges["TDS_mg_L"]["max"]:
        recommendations.append({
            "icon": "💧",
            "title": "Reverse Osmosis (RO)",
            "detail": "High TDS detected. RO removes dissolved solids."
        })

    if turbidity > ranges["Turbidity_NTU"]["max"]:
        recommendations.append({
            "icon": "🪨",
            "title": "Sediment Filter",
            "detail": "High turbidity. Sediment filter removes suspended particles."
        })

    if ph < ranges["pH"]["min"]:
        recommendations.append({
            "icon": "⚗️",
            "title": "Neutralization",
            "detail": "Low pH. Use alkaline neutralizer to balance acidity."
        })
    elif ph > ranges["pH"]["max"]:
        recommendations.append({
            "icon": "⚗️",
            "title": "Acid Neutralizer / pH Correction",
            "detail": "High pH. Use pH correction treatment."
        })

    # If unsafe overall, suggest boiling
    if issues_count(
        ph, turbidity, tds, temperature
    ) > 0:
        recommendations.append({
            "icon": "♨️",
            "title": "Boiling",
            "detail": "Boil water before use to kill pathogens."
        })

    if not recommendations:
        recommendations.append({
            "icon": "✅",
            "title": "No Purification Needed",
            "detail": "All parameters are within safe limits."
        })

    return recommendations


def issues_count(ph, turbidity, tds, temperature):
    """Count number of parameters out of safe range."""
    ranges = config.SAFE_RANGES
    count = 0
    if not (ranges["pH"]["min"] <= ph <= ranges["pH"]["max"]):
        count += 1
    if not (ranges["Turbidity_NTU"]["min"] <= turbidity <= ranges["Turbidity_NTU"]["max"]):
        count += 1
    if not (ranges["TDS_mg_L"]["min"] <= tds <= ranges["TDS_mg_L"]["max"]):
        count += 1
    if not (ranges["Temperature_C"]["min"] <= temperature <= ranges["Temperature_C"]["max"]):
        count += 1
    return count


# ------------------------------------------------------------
# 4. WATER USAGE RECOMMENDATIONS
# ------------------------------------------------------------

def get_usage(ph, turbidity, tds, temperature):
    """
    Recommend where water can be used based on sensor values.
    Returns list of {name, allowed, icon}.
    """

    limits = config.USAGE_LIMITS

    usages = []

    for name, lim in limits.items():

        allowed = True
        reasons = []

        if tds > lim.get("TDS_mg_L", 1e9):
            allowed = False
            reasons.append("high TDS")
        if turbidity > lim.get("Turbidity_NTU", 1e9):
            allowed = False
            reasons.append("high turbidity")
        if "pH_min" in lim:
            if not (lim["pH_min"] <= ph <= lim["pH_max"]):
                allowed = False
                reasons.append("pH out of range")

        usages.append({
            "name": name,
            "allowed": allowed,
            "icon": {
                "Drinking": "🚰",
                "Cooking": "🍳",
                "Bathing": "🛁",
                "Washing": "🧺",
                "Irrigation": "🌱"
            }.get(name, "✅"),
            "reason": ", ".join(reasons) if reasons else "within limits"
        })

    return usages


# ------------------------------------------------------------
# 5. ALERTS
# ------------------------------------------------------------

def get_alerts(ph, turbidity, tds, temperature):
    """
    Check if any sensor value exceeds alert thresholds.
    Returns list of {parameter, message, level}.
    """

    thresholds = config.ALERT_THRESHOLDS
    alerts = []

    if ph < thresholds["pH"]["min"] or ph > thresholds["pH"]["max"]:
        alerts.append({
            "parameter": "pH",
            "value": _round(ph),
            "message": f"pH ({_round(ph)}) is outside safe range.",
            "level": "critical"
        })

    if turbidity > thresholds["Turbidity_NTU"]["max"]:
        alerts.append({
            "parameter": "Turbidity",
            "value": _round(turbidity),
            "message": f"Turbidity ({_round(turbidity)} NTU) is too high.",
            "level": "critical"
        })

    if tds > thresholds["TDS_mg_L"]["max"]:
        alerts.append({
            "parameter": "TDS",
            "value": _round(tds),
            "message": f"TDS ({_round(tds)} mg/L) is too high.",
            "level": "critical"
        })

    if temperature < thresholds["Temperature_C"]["min"] or \
       temperature > thresholds["Temperature_C"]["max"]:
        alerts.append({
            "parameter": "Temperature",
            "value": _round(temperature),
            "message": f"Temperature ({_round(temperature)}°C) is abnormal.",
            "level": "warning"
        })

    return alerts


# ------------------------------------------------------------
# 6. STATISTICS
# ------------------------------------------------------------

def compute_statistics(history, latest_prediction=None):
    """
    Compute statistics from historical data.
    history: list of dicts from thingspeak.get_history()
    Returns dict of averages, counts, and trend info.
    """

    if not history:
        return {
            "total_readings": 0,
            "safe_readings": 0,
            "unsafe_readings": 0,
            "avg_ph": 0, "avg_tds": 0,
            "avg_turbidity": 0, "avg_temperature": 0,
            "trends": {}
        }

    phs = [h["ph"] for h in history]
    tds = [h["tds"] for h in history]
    turbs = [h["turbidity"] for h in history]
    temps = [h["temperature"] for h in history]

    def avg(lst):
        return round(sum(lst) / len(lst), 2)

    # Determine trend (increasing/decreasing) per param
    def trend(lst):
        if len(lst) < 2:
            return "stable"
        first_half = sum(lst[:len(lst)//2]) / (len(lst)//2)
        second_half = sum(lst[len(lst)//2:]) / (len(lst) - len(lst)//2)
        if second_half > first_half * 1.02:
            return "increasing"
        elif second_half < first_half * 0.98:
            return "decreasing"
        return "stable"

    return {
        "total_readings": len(history),
        "safe_readings": 0,  # filled from predictions if available
        "unsafe_readings": 0,
        "avg_ph": avg(phs),
        "avg_tds": avg(tds),
        "avg_turbidity": avg(turbs),
        "avg_temperature": avg(temps),
        "trends": {
            "ph": trend(phs),
            "tds": trend(tds),
            "turbidity": trend(turbs),
            "temperature": trend(temps)
        }
    }
