# HydroScan - Smart Water Quality Monitoring System

HydroScan is an intelligent water quality monitoring and prediction system built using ESP32, Python, Flask, and Machine Learning. The project analyzes sensor-based water parameters, predicts water quality status, and presents insights through a web dashboard.

## Project Overview

This system is designed to monitor water quality in a smarter and faster way. It helps users identify whether water is safe for use by combining sensor data with machine learning-based predictions. It also includes historical trends, statistical summaries, and report generation for environmental monitoring.

## Features

- Real-time water quality monitoring
- ESP32-based sensor data support
- Machine learning prediction of water quality
- Historical and statistical analysis
- Report generation
- Recommendations for safe water usage
- Flask web dashboard
- Responsive user interface

## Tech Stack

- Python
- Flask
- JavaScript
- HTML/CSS
- Pandas
- NumPy
- scikit-learn
- Joblib
- ReportLab
- ESP32

## Project Structure

```text
Water ESP32/
├── app.py
├── config.py
├── main.py
├── run.py
├── requirements.txt
├── train.py
├── dataset/
│   └── HydroScan Water Quality.csv
├── routes/
│   ├── __init__.py
│   ├── history.py
│   ├── main.py
│   ├── predict.py
│   ├── report.py
│   └── statistics.py
├── services/
│   ├── __init__.py
│   ├── analysis.py
│   ├── ml_service.py
│   ├── report.py
│   └── thingspeak.py
├── static/
│   ├── css/
│   ├── js/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── history.html
│   ├── index.html
│   ├── live.html
│   ├── recommendations.html
│   ├── reports.html
│   └── statistics.html
├── hydroscan_features.pkl
├── hydroscan_label_encoder.pkl
├── hydroscan_scaler.pkl
├── hydroscan_water_quality_model.pkl
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SPOORTHI-05428/Water-ESP32.git
cd Water-ESP32
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

or

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Model Training

```bash
python train.py
```

## Author

SPOORTHI

## Project Status

Active development / academic IoT and ML project
