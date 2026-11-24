
# =========================================================
# PULSETRACK - UTILITY FUNCTIONS
# =========================================================

from datetime import datetime


def format_duration(minutes):
    """Convert minutes into hours and minutes."""

    minutes = int(minutes)

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours > 0:
        return f"{hours} hr {remaining_minutes} min"

    return f"{remaining_minutes} min"


def format_heart_rate(value):
    """Format heart rate with BPM."""

    return f"{round(value)} BPM"


def format_percentage(value):
    """Format a number as a percentage."""

    return f"{value:.1f}%"


def validate_age(age):
    """Check whether age is valid."""

    return 1 <= age <= 120


def get_current_date():
    """Return the current date."""

    return datetime.now().strftime("%d %B %Y")


def get_status(heart_rate):
    """Return a simple heart rate status."""

    if heart_rate < 60:
        return "Low"

    elif heart_rate <= 100:
        return "Normal"

    else:
        return "Elevated"
