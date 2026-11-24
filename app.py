
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_processor import load_heart_rate_data, analyze_heart_rate


# PDF report import
try:
    from report_generator import generate_workout_report
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PulseTrack | Fitness Analytics",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DATA = BASE_DIR / "heart_rate_data.csv"


# =========================================================
# 2. PROFESSIONAL DASHBOARD STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #172554);
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #263247;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

h1, h2, h3, h4 {
    color: #f8fafc !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e293b, #172033);
    border: 1px solid #334155;
    padding: 16px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-weight: bold;
}

div[data-testid="stFileUploader"] {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 10px;
}

.stDownloadButton button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    width: 100%;
}

.stDownloadButton button:hover {
    border: 1px solid #38bdf8;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <h1 style="color:#38bdf8;">❤️ PulseTrack</h1>
    <p style="color:#94a3b8;">Smart Heart Rate Analytics</p>
    """, unsafe_allow_html=True)

    st.divider()

    st.header("⚙️ Dashboard Settings")

    age = st.number_input(
        "Enter your age",
        min_value=1,
        max_value=120,
        value=20,
        step=1
    )

    st.caption(
        "Your age is used to estimate maximum heart rate."
    )

    st.divider()

    st.subheader("📁 Upload Workout Data")

    uploaded_file = st.file_uploader(
        "Upload your Heart Rate CSV file",
        type=["csv"],
        help="Your CSV must contain Timestamp and Heart_Rate columns."
    )

    st.divider()

    st.markdown("""
    **Required CSV columns:**

    - Timestamp
    - Heart_Rate

    **Optional column:**

    - Activity
    """)

    st.caption("PulseTrack Analytics System")


# =========================================================
# 4. MAIN HEADER
# =========================================================

st.markdown("""
<div style="padding:5px 0 20px 0;">

<h1 style="
    font-size:40px;
    font-weight:800;
    margin-bottom:0;
">
❤️ PulseTrack Analytics
</h1>

<p style="
    font-size:19px;
    color:#94a3b8;
">
Smart Heart Rate Monitoring & Workout Intelligence
</p>

<p style="
    color:#64748b;
">
Analyze workout intensity, heart rate patterns,
and fitness activity statistics.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 5. STATUS BANNER
# =========================================================

st.success("PulseTrack System Active | Fitness Data Analysis Ready")


# =========================================================
# 6. LOAD AND ANALYZE DATA
# =========================================================

try:

    if uploaded_file is not None:

        df = load_heart_rate_data(uploaded_file)

        data_source = uploaded_file.name

    else:

        if not SAMPLE_DATA.exists():

            st.error("Sample heart rate file was not found.")

            st.info(
                "Place heart_rate_data.csv in the same folder as app.py."
            )

            st.stop()

        df = load_heart_rate_data(SAMPLE_DATA)

        data_source = "Built-in Sample Workout"


    if df.empty:

        st.error("No valid heart rate records were found.")

        st.stop()


    analyzed_df, stats = analyze_heart_rate(df, age)

    
    

except Exception as e:

    st.error("Unable to process your heart rate data.")

    st.exception(e)

    st.info(
        "Check your CSV file. It must contain valid "
        "Timestamp and Heart_Rate columns."
    )

    st.stop()


# =========================================================
# 7. DATA INFORMATION
# =========================================================

st.caption(f"📂 Data Source: {data_source}")

st.caption(
    f"👤 Age: {age} years | "
    f"📊 Records Analyzed: {len(analyzed_df)}"
)


# =========================================================
# 8. WORKOUT OVERVIEW
# =========================================================

st.markdown("## 📊 Workout Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "❤️ Average Heart Rate",
        f"{stats['Average HR']:.1f} BPM"
    )

with col2:

    st.metric(
        "🔥 Maximum Heart Rate",
        f"{stats['Maximum HR']} BPM"
    )

with col3:

    st.metric(
        "💙 Minimum Heart Rate",
        f"{stats['Minimum HR']} BPM"
    )

with col4:

    st.metric(
        "⏱ Workout Duration",
        f"{stats['Total Duration (Minutes)']:.1f} min"
    )


# =========================================================
# 9. ADDITIONAL STATISTICS
# =========================================================

st.markdown("### 📌 Additional Statistics")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Estimated Maximum Heart Rate",
        f"{stats['Estimated Max HR']} BPM"
    )

with col2:

    st.metric(
        "Heart Rate Standard Deviation",
        f"{stats['Standard Deviation']:.2f}"
    )


# =========================================================
# 10. HEART RATE LINE CHART
# =========================================================

st.divider()

st.markdown("## 📈 Heart Rate Monitoring")

st.caption(
    "Observe how your heart rate changes throughout the workout."
)

fig, ax = plt.subplots(figsize=(12, 4.5))

ax.plot(
    analyzed_df["Timestamp"],
    analyzed_df["Heart_Rate"],
    linewidth=2.5,
    marker="o",
    markersize=3,
    label="Heart Rate"
)

ax.fill_between(
    analyzed_df["Timestamp"],
    analyzed_df["Heart_Rate"],
    alpha=0.12
)

ax.set_title("Heart Rate During Workout")
ax.set_xlabel("Time")
ax.set_ylabel("Heart Rate (BPM)")
ax.grid(True, linestyle="--", alpha=0.25)

fig.autofmt_xdate()
plt.tight_layout()

st.pyplot(fig, use_container_width=True)

plt.close(fig)


# =========================================================
# 11. HEART RATE ZONE ANALYSIS
# =========================================================

st.divider()

st.markdown("## 🎯 Heart Rate Zone Analysis")

st.caption(
    "Understand workout intensity using estimated heart rate zones."
)

zone_time = stats["Zone Time"]
zone_percentage = stats["Zone Percentage"]

zone_colors = {
    "Zone 1": "#3b82f6",
    "Zone 2": "#22c55e",
    "Zone 3": "#eab308",
    "Zone 4": "#f97316",
    "Zone 5": "#ef4444"
}

zone_descriptions = {
    "Zone 1": "Very Light",
    "Zone 2": "Light",
    "Zone 3": "Moderate",
    "Zone 4": "Hard",
    "Zone 5": "Maximum"
}

zone_emojis = {
    "Zone 1": "🔵",
    "Zone 2": "🟢",
    "Zone 3": "🟡",
    "Zone 4": "🟠",
    "Zone 5": "🔴"
}

zone_columns = st.columns(5)

for i, zone in enumerate(zone_colors.keys()):

    seconds = float(zone_time.get(zone, 0))
    percentage = float(zone_percentage.get(zone, 0))
    minutes = seconds / 60

    with zone_columns[i]:

        with st.container(border=True):

            st.markdown(f"### {zone_emojis[zone]} {zone}")

            st.caption(zone_descriptions[zone])

            st.metric("Time", f"{minutes:.1f} min")

            st.progress(
                min(max(percentage / 100, 0.0), 1.0)
            )

            st.caption(f"{percentage:.1f}% of workout")


# =========================================================
# 12. ZONE DISTRIBUTION BAR CHART
# =========================================================

st.markdown("### 📊 Time Spent in Heart Rate Zones")

zone_names = list(zone_colors.keys())

zone_minutes = [
    float(zone_time.get(zone, 0)) / 60
    for zone in zone_names
]

fig2, ax2 = plt.subplots(figsize=(10, 4.5))

ax2.bar(
    zone_names,
    zone_minutes,
    color=[zone_colors[zone] for zone in zone_names]
)

ax2.set_title("Workout Zone Distribution")
ax2.set_xlabel("Heart Rate Zones")
ax2.set_ylabel("Time (Minutes)")
ax2.grid(axis="y", linestyle="--", alpha=0.2)

plt.tight_layout()

st.pyplot(fig2, use_container_width=True)

plt.close(fig2)


# =========================================================
# 13. HEART RATE DISTRIBUTION HISTOGRAM
# =========================================================

st.markdown("### 📉 Heart Rate Distribution")

fig3, ax3 = plt.subplots(figsize=(10, 4.5))

sns.histplot(
    data=analyzed_df,
    x="Heart_Rate",
    bins=10,
    kde=True,
    ax=ax3
)

ax3.set_title("Heart Rate Frequency")
ax3.set_xlabel("Heart Rate (BPM)")
ax3.set_ylabel("Frequency")
ax3.grid(axis="y", linestyle="--", alpha=0.2)

plt.tight_layout()

st.pyplot(fig3, use_container_width=True)

plt.close(fig3)


# =========================================================
# 14. HEART RATE ZONE DETAILS TABLE
# =========================================================

st.divider()

st.markdown("## 📋 Heart Rate Zone Details")

zone_limits = stats["Zone Limits"]

zone_table = []

for zone in zone_names:

    limits = zone_limits.get(zone, (0, 0))

    zone_table.append({
        "Zone": zone,
        "Intensity": zone_descriptions[zone],
        "Lower BPM": limits[0],
        "Upper BPM": limits[1],
        "Time (Minutes)": round(
            float(zone_time.get(zone, 0)) / 60, 2
        ),
        "Workout Percentage": round(
            float(zone_percentage.get(zone, 0)), 2
        )
    })

zone_table_df = pd.DataFrame(zone_table)

st.dataframe(
    zone_table_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 15. WORKOUT DATA EXPLORER
# =========================================================

st.divider()

st.markdown("## 📁 Workout Data Explorer")

st.caption(
    "View the cleaned and analyzed heart rate records."
)

with st.expander("🔎 Open Processed Workout Records"):

    st.dataframe(
        analyzed_df,
        use_container_width=True,
        hide_index=True
    )





# =========================================================
# 17. EXPORT ANALYZED DATA
# =========================================================

st.divider()

st.markdown("## 📥 Export Your Analysis")

csv_data = analyzed_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Analyzed Heart Rate Data (CSV)",
    data=csv_data,
    file_name="PulseTrack_Heart_Rate_Analysis.csv",
    mime="text/csv",
    key="download_csv"
)


# =========================================================
# 18. PDF WORKOUT REPORT
# =========================================================

st.markdown("### 📄 Professional Workout Report")

if PDF_AVAILABLE:

    try:

        pdf_report = generate_workout_report(
            stats=stats,
            age=age,
            data_source=data_source
        )

        st.download_button(
            label="📥 Download Workout Report (PDF)",
            data=pdf_report,
            file_name="PulseTrack_Workout_Report.pdf",
            mime="application/pdf",
            key="download_pdf_report"
        )

    except Exception as e:

        st.error("PDF report generation failed.")

        st.exception(e)

else:

    st.warning(
        "PDF generator could not be imported. "
        "Check your report_generator.py file."
    )


# =========================================================
# 19. FOOTER
# =========================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">

<h3 style="color:#38bdf8;">
❤️ PulseTrack
</h3>

<p style="color:#94a3b8;">
Smart Heart Rate Monitoring & Fitness Analytics System
</p>

<p style="font-size:13px; color:#64748b;">
Developed using Python, Streamlit, Pandas, NumPy,
Matplotlib and Seaborn
</p>

<p style="font-size:11px; color:#64748b;">
Educational fitness analytics application.
Not intended for medical diagnosis.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# WORKOUT COMPARISON
# ==========================================

import workout_comparison

st.markdown("---")
st.markdown("## ⚖️ Workout Comparison")
st.markdown("Compare two workout sessions side by side.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏃 Workout 1")
    file1 = st.file_uploader(
        "Upload first workout CSV",
        type=["csv"],
        key="comparison_file1"
    )

with col2:
    st.markdown("### 🚴 Workout 2")
    file2 = st.file_uploader(
        "Upload second workout CSV",
        type=["csv"],
        key="comparison_file2"
    )

if file1 is not None and file2 is not None:

    if st.button("Compare Workouts", key="compare_workouts_button"):

        try:
            workout1 = workout_comparison.analyze_workout(file1)
            workout2 = workout_comparison.analyze_workout(file2)

            st.markdown("### 📊 Comparison Results")

            metrics = list(workout1.keys())

            for metric in metrics:

                c1, c2, c3 = st.columns([2, 2, 2])

                with c1:
                    st.metric("Workout 1", workout1[metric])

                with c2:
                    st.metric("Workout 2", workout2[metric])

                with c3:
                    if isinstance(workout1[metric], (int, float)) and isinstance(workout2[metric], (int, float)):
                        difference = round(workout2[metric] - workout1[metric], 2)
                        st.metric("Difference (W2 - W1)", difference)

            comparison_df = pd.DataFrame({
                "Metric": metrics,
                "Workout 1": [workout1[m] for m in metrics],
                "Workout 2": [workout2[m] for m in metrics]
            })

            st.markdown("### 📋 Summary Table")
            st.dataframe(comparison_df, use_container_width=True)

            numeric_metrics = [
                "Average Heart Rate",
                "Maximum Heart Rate",
                "Minimum Heart Rate",
                "Duration (Minutes)"
            ]

            chart_df = comparison_df[
                comparison_df["Metric"].isin(numeric_metrics)
            ].set_index("Metric")

            st.markdown("### 📈 Visual Comparison")
            st.bar_chart(chart_df)

        except Exception as e:
            st.error(f"Comparison error: {e}")
