
# ==========================================
# PULSETRACK - DATA PROCESSOR
# ==========================================

import pandas as pd
import numpy as np

from heart_rate_engine import (
    calculate_max_heart_rate,
    calculate_zone_boundaries,
    classify_heart_rate
)


def load_heart_rate_data(file):
    """
    Load heart rate data from CSV.
    """

    df = pd.read_csv(file)

    required_columns = ["Timestamp", "Heart_Rate"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    df["Heart_Rate"] = pd.to_numeric(
        df["Heart_Rate"], errors="coerce"
    )

    # Remove missing values
    df = df.dropna(subset=["Timestamp", "Heart_Rate"])

    # Remove unrealistic heart rate readings
    df = df[
        df["Heart_Rate"].between(30, 220)
    ]

    # Sort readings by time
    df = df.sort_values("Timestamp")

    # Remove duplicate timestamps
    df = df.drop_duplicates(subset=["Timestamp"])

    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid heart rate data found.")

    return df


def analyze_heart_rate(df, age):
    """
    Calculate heart rate statistics and zones.
    """

    heart_rates = df["Heart_Rate"].to_numpy()

    max_hr = calculate_max_heart_rate(age)

    zone_limits = calculate_zone_boundaries(max_hr)

    # NumPy calculations
    average_hr = np.mean(heart_rates)
    minimum_hr = np.min(heart_rates)
    maximum_hr = np.max(heart_rates)
    standard_deviation = np.std(heart_rates)

    # Assign zones
    df = df.copy()

    df["Zone"] = df["Heart_Rate"].apply(
        lambda hr: classify_heart_rate(hr, zone_limits)
    )

    # Calculate time intervals between readings
    time_difference = df["Timestamp"].diff().dt.total_seconds()

    # Use median interval for the first and last readings
    interval = time_difference.median()

    if pd.isna(interval) or interval <= 0:
        interval = 60

    df["Duration_Seconds"] = time_difference.fillna(interval)

    # Avoid counting huge gaps as continuous exercise
    df["Duration_Seconds"] = df["Duration_Seconds"].clip(
        lower=0, upper=interval * 2
    )

    # Time spent in each zone
    zone_time = df.groupby("Zone")["Duration_Seconds"].sum()

    # Ensure all zones appear in results
    all_zones = [
        "Zone 1",
        "Zone 2",
        "Zone 3",
        "Zone 4",
        "Zone 5"
    ]

    zone_time = zone_time.reindex(
        all_zones, fill_value=0
    )

    total_seconds = zone_time.sum()

    if total_seconds > 0:
        zone_percentage = (
            zone_time / total_seconds * 100
        )
    else:
        zone_percentage = zone_time * 0

    statistics = {
        "Average HR": round(average_hr, 2),
        "Minimum HR": int(minimum_hr),
        "Maximum HR": int(maximum_hr),
        "Estimated Max HR": max_hr,
        "Standard Deviation": round(standard_deviation, 2),
        "Total Duration (Minutes)": round(
            total_seconds / 60, 2
        ),
        "Zone Time": zone_time,
        "Zone Percentage": zone_percentage,
        "Zone Limits": zone_limits
    }

    return df, statistics
