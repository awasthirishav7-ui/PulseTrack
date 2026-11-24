
# ==========================================
# PULSETRACK - APPLICATION CONFIGURATION
# ==========================================

APP_NAME = "PulseTrack"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Smart Heart Rate Monitoring and Fitness Analytics"

# Application Theme
PRIMARY_COLOR = "#38BDF8"
BACKGROUND_COLOR = "#0B1120"
CARD_COLOR = "#1E293B"

# Heart Rate Settings
MIN_HEART_RATE = 30
MAX_HEART_RATE = 220

# Heart Rate Zone Names
HEART_RATE_ZONES = [
    "Zone 1",
    "Zone 2",
    "Zone 3",
    "Zone 4",
    "Zone 5"
]

# Zone Descriptions
ZONE_DESCRIPTIONS = {
    "Zone 1": "Very Light - Warm-up",
    "Zone 2": "Light - Comfortable activity",
    "Zone 3": "Moderate - Aerobic activity",
    "Zone 4": "Hard - High intensity",
    "Zone 5": "Maximum - Very high intensity"
}

# File Settings
DEFAULT_DATA_FILE = "heart_rate_data.csv"
SUPPORTED_FILE_FORMATS = ["csv"]

# Dashboard Settings
DASHBOARD_TITLE = "PulseTrack Analytics"
CHART_HEIGHT = 400

# Report Settings
REPORT_NAME = "PulseTrack Workout Report"
