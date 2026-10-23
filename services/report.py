# ============================================================
# HYDROSCAN PDF REPORT SERVICE
# ============================================================
# Generates a professional, downloadable PDF report with:
#   - Date & Time
#   - Sensor values (pH, Turbidity, TDS, Temperature)
#   - ML Prediction
#   - Water Quality Score
#   - Reason (AI explanation)
#   - Recommendations
#
# Uses ReportLab. Install with:
#     pip install reportlab
# ============================================================

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER


# ------------------------------------------------------------
# COLORS (match dashboard theme)
# ------------------------------------------------------------

PRIMARY = colors.HexColor("#0d6efd")
DARK = colors.HexColor("#0b1e3a")
GREEN = colors.HexColor("#198754")
YELLOW = colors.HexColor("#ffc107")
ORANGE = colors.HexColor("#fd7e14")
RED = colors.HexColor("#dc3545")
LIGHT = colors.HexColor("#e9f2ff")


# ------------------------------------------------------------
# GENERATE PDF
# ------------------------------------------------------------

def generate_report(data):
    """
    Generate a PDF report as bytes.

    data dict keys:
      sensor_values: dict {pH, Turbidity_NTU, TDS_mg_L, Temperature_C}
      prediction: str
      confidence: float or None
      score: float
      score_category: str
      explanation: dict {summary, points}
      purification: list [{title, detail}]
      usage: list [{name, allowed}]
      timestamp: str
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=DARK,
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = styles["Normal"]

    story = []

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    story.append(Paragraph("💧 HydroScan", title_style))
    story.append(Paragraph(
        "IoT Based Water Quality Monitoring Report", subtitle_style
    ))

    # Generated date
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(
        f"Generated: {generated}", subtitle_style
    ))

    # --------------------------------------------------------
    # Sensor Values Table
    # --------------------------------------------------------

    story.append(Paragraph("1. Sensor Readings", heading_style))

    sv = data["sensor_values"]

    sensor_rows = [
        ["Parameter", "Value", "Status"],
        ["pH", f"{sv['pH']}", ("OK" if 6.5 <= sv['pH'] <= 8.5 else "ALERT")],
        ["Turbidity (NTU)",
         f"{sv['Turbidity_NTU']}",
         ("OK" if sv['Turbidity_NTU'] <= 5 else "ALERT")],
        ["TDS (mg/L)",
         f"{sv['TDS_mg_L']}",
         ("OK" if sv['TDS_mg_L'] <= 500 else "ALERT")],
        ["Temperature (°C)",
         f"{sv['Temperature_C']}",
         ("OK" if 10 <= sv['Temperature_C'] <= 30 else "ALERT")]
    ]

    sensor_table = Table(sensor_rows, colWidths=[70*mm, 40*mm, 40*mm])
    sensor_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sensor_table)

    # --------------------------------------------------------
    # Prediction & Score
    # --------------------------------------------------------

    story.append(Paragraph("2. ML Prediction", heading_style))

    confidence = data.get("confidence")
    conf_str = (
        f"{round(confidence, 2)}%" if confidence is not None else "N/A"
    )

    pred_rows = [
        ["Field", "Value"],
        ["Prediction", data["prediction"]],
        ["ML Confidence", conf_str],
        ["Water Quality Score",
         f"{data['score']} / 100 ({data['score_category']})"]
    ]

    pred_table = Table(pred_rows, colWidths=[70*mm, 80*mm])
    pred_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(pred_table)

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    story.append(Paragraph("3. Reason (AI Explanation)", heading_style))

    explanation = data.get("explanation", {})
    story.append(Paragraph(
        f"<b>{explanation.get('summary', '')}</b>", body_style
    ))
    story.append(Spacer(1, 4))

    for point in explanation.get("points", []):
        story.append(Paragraph(f"• {point}", body_style))

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    story.append(Paragraph("4. Purification Recommendations", heading_style))

    for rec in data.get("purification", []):
        story.append(Paragraph(
            f"<b>• {rec.get('title', '')}</b>: "
            f"{rec.get('detail', '')}",
            body_style
        ))

    story.append(Paragraph("5. Water Usage", heading_style))

    usage_lines = []
    for u in data.get("usage", []):
        mark = "✓" if u["allowed"] else "✗"
        usage_lines.append(f"{mark} {u['name']}")

    story.append(Paragraph(
        "&nbsp;&nbsp;".join(usage_lines), body_style
    ))

    # --------------------------------------------------------
    # Footer note
    # --------------------------------------------------------

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "<i>Report generated automatically by the HydroScan "
        "Water Quality Monitoring System. The prediction is "
        "based on a Random Forest ML model using live sensor "
        "data from ThingSpeak.</i>",
        ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.grey
        )
    ))

    doc.build(story)

    buffer.seek(0)
    return buffer.read()
