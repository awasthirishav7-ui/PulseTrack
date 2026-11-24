
import pandas as pd
import numpy as np

from heart_rate_engine import (
    calculate_max_heart_rate,
    calculate_zone_boundaries,
    classify_heart_rate
)


def load_heart_rate_data(file):
    """
    Load and clean heart rate data.
    Supports Timestamp + Heart_Rate and Pulse datasets.
    """

    df = pd.read_csv(file)

    # Clean column headings
    df.columns = df.columns.str.strip()

    # Match column names without case sensitivity
    column_map = {col.lower(): col for col in df.columns}

    # Accept Heart_Rate or Pulse
    if "heart_rate" in column_map:
        actual_hr_column = column_map["heart_rate"]

    elif "pulse" in column_map:
        actual_hr_column = column_map["pulse"]

    else:
        raise ValueError(
            "Missing required column: Heart_Rate or Pulse"
        )

    # Standardize heart rate column
    if actual_hr_column != "Heart_Rate":
        df.rename(
            columns={actual_hr_column: "Heart_Rate"},
            inplace=True
        )

    # Check for Timestamp
    column_map = {col.lower(): col for col in df.columns}

    if "timestamp" in column_map:

        actual_timestamp_column = column_map["timestamp"]

        if actual_timestamp_column != "Timestamp":
            df.rename(
                columns={actual_timestamp_column: "Timestamp"},
                inplace=True
            )

        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

    else:

        # Generate placeholder timestamps when unavailable.
        # These do not represent actual workout times.
        df["Timestamp"] = pd.date_range(
            start="2026-01-01 08:00:00",
            periods=len(df),
            freq="min"
        )

    # Convert heart rate to numeric
    df["Heart_Rate"] = pd.to_numeric(
        df["Heart_Rate"],
        errors="coerce"
    )

    # Remove invalid records
    df.dropna(
        subset=["Timestamp", "Heart_Rate"],
        inplace=True
    )

    # Keep realistic heart rate readings
    df = df[
        df["Heart_Rate"].between(30, 220)
    ]

    # Sort by timestamp
    df.sort_values(
        "Timestamp",
        inplace=True
    )

    # Remove duplicate timestamps
    df.drop_duplicates(
        subset=["Timestamp"],
        inplace=True
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    if df.empty:
        raise ValueError(
            "No valid heart rate data found."
        )

    return df


def analyze_heart_rate(df, age):
    """
    Calculate heart rate statistics and zones.
    """

    heart_rates = df["Heart_Rate"].to_numpy()

    max_hr = calculate_max_heart_rate(age)

    zone_limits = calculate_zone_boundaries(max_hr)

    # Calculate basic statistics
    average_hr = np.mean(heart_rates)
    minimum_hr = np.min(heart_rates)
    maximum_hr = np.max(heart_rates)
    standard_deviation = np.std(heart_rates)

    # Assign heart rate zones
    df = df.copy()

    df["Zone"] = df["Heart_Rate"].apply(
        lambda hr: classify_heart_rate(
            hr, zone_limits
        )
    )

    # Calculate time between readings
    time_difference = (
        df["Timestamp"].diff().dt.total_seconds()
    )

    interval = time_difference.median()

    if pd.isna(interval) or interval <= 0:
        interval = 60

    df["Duration_Seconds"] = (
        time_difference.fillna(interval)
    )

    # Avoid counting very large gaps
    df["Duration_Seconds"] = (
        df["Duration_Seconds"].clip(
            lower=0,
            upper=interval * 2
        )
    )

    # Calculate time spent in each zone
    zone_time = df.groupby("Zone")[
        "Duration_Seconds"
    ].sum()

    all_zones = [
        "Zone 1",
        "Zone 2",
        "Zone 3",
        "Zone 4",
        "Zone 5"
    ]

    zone_time = zone_time.reindex(
        all_zones,
        fill_value=0
    )

    total_seconds = zone_time.sum()

    if total_seconds > 0:
        zone_percentage = (
            zone_time / total_seconds * 100
        )
    else:
        zone_percentage = zone_time * 0

    # Prepare final statistics
    statistics = {
        "Average HR": round(average_hr, 2),

        "Minimum HR": int(minimum_hr),

        "Maximum HR": int(maximum_hr),

        "Estimated Max HR": max_hr,

        "Standard Deviation": round(
            standard_deviation, 2
        ),

        "Total Duration (Minutes)": round(
            total_seconds / 60, 2
        ),

        "Zone Time": zone_time,

        "Zone Percentage": zone_percentage,

        "Zone Limits": zone_limits
    }

    return df, statistics
