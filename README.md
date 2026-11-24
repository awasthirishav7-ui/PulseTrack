
# ❤️ PulseTrack
### Smart Heart Rate Monitoring & Fitness Analytics System

PulseTrack is a Python-based fitness analytics application designed to analyze heart rate data and provide meaningful workout insights.

It helps users understand workout intensity, heart rate patterns, time spent in different heart rate zones, and overall workout statistics through an interactive dashboard.

---

## 🎯 Project Objectives

- Analyze heart rate data from CSV files.
- Calculate average, minimum, and maximum heart rate.
- Estimate maximum heart rate based on age.
- Classify heart rate into five exercise zones.
- Calculate time spent in each heart rate zone.
- Display interactive graphs and workout statistics.
- Generate downloadable workout reports.

---

## ✨ Features

- Interactive fitness dashboard
- CSV file upload
- Heart rate data cleaning
- Age-based heart rate zone calculation
- Five-zone workout analysis
- Heart rate monitoring graph
- Workout duration analysis
- Zone distribution charts
- Data export
- PDF workout report generation

---

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- ReportLab

---

## 📂 Project Structure

PulseTrack/
│
├── app.py
├── data_processor.py
├── heart_rate_engine.py
├── visualizations.py
├── config.py
├── utils.py
├── report_generator.py
├── heart_rate_data.csv
├── requirements.txt
├── README.md
│
└── assets/

---

## 📊 Heart Rate Zones

| Zone | Intensity | Purpose |
|------|-----------|---------|
| Zone 1 | Very Light | Warm-up |
| Zone 2 | Light | Comfortable exercise |
| Zone 3 | Moderate | Aerobic training |
| Zone 4 | Hard | High intensity |
| Zone 5 | Maximum | Very high intensity |

---

## 🚀 Installation

### Step 1: Install Python

Install Python on your computer if it is not already installed.

### Step 2: Install Required Libraries

Open the terminal inside the project folder and run:

pip install -r requirements.txt

### Step 3: Run PulseTrack

Run the following command:

python -m streamlit run app.py

### Step 4: Open the Dashboard

Streamlit will open PulseTrack in your web browser.

---

## 📁 Input Data Format

The application accepts CSV files containing heart rate readings.

Required columns:

- Timestamp
- Heart_Rate

Optional column:

- Activity

Example:

| Timestamp | Heart_Rate | Activity |
|-----------|------------|----------|
| 09:00:00 | 80 | Warm-up |
| 09:01:00 | 95 | Jogging |
| 09:02:00 | 120 | Running |

---

## 📈 Output

PulseTrack provides:

- Workout statistics
- Heart rate graphs
- Heart rate zone analysis
- Workout duration
- Zone distribution
- Processed dataset
- Downloadable reports

---

## ⚠️ Disclaimer

PulseTrack is an educational fitness analytics project.

It is not intended for medical diagnosis, treatment, or emergency monitoring.

---

## 👨‍💻 Project

Developed as a Python application project for learning data analysis, programming, visualization, and application development.
