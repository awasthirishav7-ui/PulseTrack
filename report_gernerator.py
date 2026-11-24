
# =========================================================
# PULSETRACK - PDF REPORT GENERATOR
# =========================================================

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_workout_report(stats, age, data_source="Workout Data"):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=15,
        spaceAfter=8
    )

    normal_style = styles["Normal"]

    content = []

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    content.append(Paragraph("PulseTrack", title_style))

    content.append(
        Paragraph(
            "Smart Heart Rate Monitoring & Fitness Analytics Report",
            normal_style
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            f"Report Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            normal_style
        )
    )

    content.append(
        Paragraph(f"Data Source: {data_source}", normal_style)
    )

    content.append(
        Paragraph(f"User Age: {age} years", normal_style)
    )

    content.append(Spacer(1, 20))

    # -----------------------------------------------------
    # WORKOUT OVERVIEW
    # -----------------------------------------------------

    content.append(
        Paragraph("Workout Overview", heading_style)
    )

    overview_data = [
        ["Metric", "Value"],
        ["Average Heart Rate", f"{stats['Average HR']:.1f} BPM"],
        ["Maximum Heart Rate", f"{stats['Maximum HR']} BPM"],
        ["Minimum Heart Rate", f"{stats['Minimum HR']} BPM"],
        ["Estimated Maximum HR", f"{stats['Estimated Max HR']} BPM"],
        ["Workout Duration", f"{stats['Total Duration (Minutes)']:.2f} minutes"],
        ["Heart Rate Variation", f"{stats['Standard Deviation']:.2f}"]
    ]

    overview_table = Table(
        overview_data,
        colWidths=[230, 230]
    )

    overview_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#EFF6FF")]),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ])
    )

    content.append(overview_table)

    # -----------------------------------------------------
    # HEART RATE ZONE ANALYSIS
    # -----------------------------------------------------

    content.append(
        Paragraph("Heart Rate Zone Analysis", heading_style)
    )

    zone_time = stats["Zone Time"]
    zone_percentage = stats["Zone Percentage"]
    zone_limits = stats["Zone Limits"]

    zone_data = [
        ["Zone", "Heart Rate Range", "Time (Min)", "Percentage"]
    ]

    for zone in ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]:

        lower_hr, upper_hr = zone_limits[zone]

        minutes = float(zone_time.get(zone, 0)) / 60

        percentage = float(zone_percentage.get(zone, 0))

        zone_data.append([
            zone,
            f"{lower_hr}-{upper_hr} BPM",
            f"{minutes:.2f}",
            f"{percentage:.1f}%"
        ])

    zone_table = Table(
        zone_data,
        colWidths=[80, 140, 110, 110]
    )

    zone_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F0FDFA")]),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ])
    )

    content.append(zone_table)

    # -----------------------------------------------------
    # ZONE DESCRIPTIONS
    # -----------------------------------------------------

    content.append(
        Paragraph("Zone Information", heading_style)
    )

    zone_descriptions = [
        "Zone 1 - Very Light: Warm-up and light activity.",
        "Zone 2 - Light: Comfortable, steady activity.",
        "Zone 3 - Moderate: Aerobic exercise.",
        "Zone 4 - Hard: High-intensity exercise.",
        "Zone 5 - Maximum: Very high-intensity activity."
    ]

    for description in zone_descriptions:
        content.append(Paragraph(description, normal_style))
        content.append(Spacer(1, 5))

    # -----------------------------------------------------
    # FOOTER / DISCLAIMER
    # -----------------------------------------------------

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("Report Summary", heading_style)
    )

    content.append(
        Paragraph(
            "This report presents workout heart rate statistics, "
            "estimated heart rate zones, and workout duration "
            "based on the uploaded data.",
            normal_style
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Disclaimer: PulseTrack is an educational fitness analytics "
            "application. The results are estimates and are not intended "
            "for medical diagnosis or treatment.",
            normal_style
        )
    )

    # -----------------------------------------------------
    # GENERATE PDF
    # -----------------------------------------------------

    document.build(content)

    buffer.seek(0)

    return buffer.getvalue()
