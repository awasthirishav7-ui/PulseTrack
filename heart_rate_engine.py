
# ==========================================
# PULSETRACK - HEART RATE ENGINE
# ==========================================

def calculate_max_heart_rate(age):
    """
    Estimate maximum heart rate using age.
    Formula: 220 - age
    """
    return 220 - age


def calculate_zone_boundaries(max_hr):
    """
    Calculate heart rate zone boundaries
    using percentages of estimated max HR.
    """

    zones = {
        "Zone 1": (0.50, 0.60),
        "Zone 2": (0.60, 0.70),
        "Zone 3": (0.70, 0.80),
        "Zone 4": (0.80, 0.90),
        "Zone 5": (0.90, 1.00)
    }

    zone_limits = {}

    for zone, percentages in zones.items():
        lower_percent, upper_percent = percentages

        lower_hr = round(max_hr * lower_percent)
        upper_hr = round(max_hr * upper_percent)

        zone_limits[zone] = (lower_hr, upper_hr)

    return zone_limits


def classify_heart_rate(hr, zone_limits):
    """
    Identify the zone for a heart rate reading.
    """

    for zone, limits in zone_limits.items():
        lower_hr, upper_hr = limits

        if lower_hr <= hr < upper_hr:
            return zone

    # Include the upper boundary of Zone 5
    if hr == zone_limits["Zone 5"][1]:
        return "Zone 5"

    return "Below Zone 1 or Above Zone 5"


def get_zone_description(zone):
    """
    Return a simple description of each zone.
    """

    descriptions = {
        "Zone 1": "Very Light - Warm-up",
        "Zone 2": "Light - Comfortable activity",
        "Zone 3": "Moderate - Aerobic activity",
        "Zone 4": "Hard - High intensity",
        "Zone 5": "Maximum - Very high intensity"
    }

    return descriptions.get(zone, "Outside defined zones")

