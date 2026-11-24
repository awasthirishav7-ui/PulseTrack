
import pandas as pd
import numpy as np


def analyze_workout(file):
    df = pd.read_csv(file)

    if "Heart_Rate" not in df.columns:
        raise ValueError("CSV must contain a Heart_Rate column.")

    df["Heart_Rate"] = pd.to_numeric(
        df["Heart_Rate"], errors="coerce"
    )

    df = df.dropna(subset=["Heart_Rate"])

    if df.empty:
        raise ValueError("No valid heart rate data found.")

    heart_rate = df["Heart_Rate"]

    avg_hr = round(heart_rate.mean(), 2)
    max_hr = int(heart_rate.max())
    min_hr = int(heart_rate.min())

    duration = 0

    if "Timestamp" in df.columns:
        timestamps = pd.to_datetime(
            df["Timestamp"], errors="coerce"
        ).dropna()

        if len(timestamps) >= 2:
            duration = round(
                (timestamps.max() - timestamps.min()).total_seconds() / 60,
                2
            )

    intensity = (
        "High" if avg_hr >= 150
        else "Moderate" if avg_hr >= 120
        else "Low"
    )

    return {
        "Average Heart Rate": avg_hr,
        "Maximum Heart Rate": max_hr,
        "Minimum Heart Rate": min_hr,
        "Duration (Minutes)": duration,
        "Workout Intensity": intensity,
    }

def compare_heart_rate_trends(file1, file2):

    import pandas as pd

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df1["Heart_Rate"] = pd.to_numeric(
        df1["Heart_Rate"], errors="coerce"
    )
    df2["Heart_Rate"] = pd.to_numeric(
        df2["Heart_Rate"], errors="coerce"
    )

    df1 = df1.dropna(subset=["Heart_Rate"])
    df2 = df2.dropna(subset=["Heart_Rate"])

    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    comparison = pd.DataFrame({
        "Workout 1": df1["Heart_Rate"],
        "Workout 2": df2["Heart_Rate"]
    })

    return comparison
