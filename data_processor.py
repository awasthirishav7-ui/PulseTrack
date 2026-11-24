
import pandas as pd
import numpy as np


def load_heart_rate_data(uploaded_file):

    """
    Load and clean heart rate data.

    Supports:
    1. Timestamp + Heart_Rate CSV files
    2. Duration + Pulse + Maxpulse + Calories CSV files
    """

    try:

        # Read uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Make column matching case-insensitive
        column_map = {
            col.lower(): col for col in df.columns
        }

        # Support Pulse as an alternative to Heart_Rate
        if "heart_rate" not in column_map:

            if "pulse" in column_map:
                df.rename(
                    columns={column_map["pulse"]: "Heart_Rate"},
                    inplace=True
                )
            else:
                raise ValueError(
                    "Missing required column: Heart_Rate or Pulse"
                )

        else:
            df.rename(
                columns={column_map["heart_rate"]: "Heart_Rate"},
                inplace=True
            )

        # Check whether Timestamp exists
        column_map = {
            col.lower(): col for col in df.columns
        }

        timestamp_generated = False

        if "timestamp" not in column_map:

            # Generate sample timestamps for datasets
            # that contain no actual timestamp.
            df["Timestamp"] = pd.date_range(
                start="2026-01-01 08:00:00",
                periods=len(df),
                freq="min"
            )

            timestamp_generated = True

        else:

            df.rename(
                columns={column_map["timestamp"]: "Timestamp"},
                inplace=True
            )

        # Convert heart rate into numeric values
        df["Heart_Rate"] = pd.to_numeric(
            df["Heart_Rate"],
            errors="coerce"
        )

        # Convert timestamp into datetime format
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"],
            errors="coerce"
        )

        # Remove rows with missing required values
        df.dropna(
            subset=["Timestamp", "Heart_Rate"],
            inplace=True
        )

        # Keep valid heart rate values
        df = df[
            (df["Heart_Rate"] >= 30) &
            (df["Heart_Rate"] <= 220)
        ]

        # Remove duplicate timestamps
        df.drop_duplicates(
            subset=["Timestamp"],
            keep="first",
            inplace=True
        )

        # Sort data by timestamp
        df.sort_values(
            by="Timestamp",
            inplace=True
        )

        # Reset row numbering
        df.reset_index(
            drop=True,
            inplace=True
        )

        # Stop if no valid data remains
        if df.empty:
            raise ValueError(
                "No valid heart rate data found in this CSV file."
            )

        # Keep track of generated timestamps
        df.attrs["timestamp_generated"] = timestamp_generated

        # Return cleaned dataset
        return df

    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded CSV file is empty.")

    except pd.errors.ParserError:
        raise ValueError("Unable to read this CSV file. Check its format.")

    except Exception as e:
        raise ValueError(str(e))


def calculate_heart_rate_statistics(df):

    """
    Calculate basic heart rate statistics.
    """

    return {
        "Average Heart Rate": round(
            df["Heart_Rate"].mean(), 2
        ),

        "Maximum Heart Rate": int(
            df["Heart_Rate"].max()
        ),

        "Minimum Heart Rate": int(
            df["Heart_Rate"].min()
        ),

        "Standard Deviation": round(
            df["Heart_Rate"].std(), 2
        )
    }


def get_heart_rate_summary(df):

    """
    Return a simple heart rate summary.
    """

    return {
        "Total Readings": len(df),

        "Average Heart Rate": round(
            df["Heart_Rate"].mean(), 2
        ),

        "Maximum Heart Rate": int(
            df["Heart_Rate"].max()
        ),

        "Minimum Heart Rate": int(
            df["Heart_Rate"].min()
        )
    }
