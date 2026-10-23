# HydroScan AI

<div align="center">

![HydroScan Banner](https://img.shields.io/badge/IoT-Water%20Quality%20Monitoring-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit%20Learn-F7931E)

</div>

HydroScan AI is a smart water quality monitoring system that combines ESP32 sensor data, machine learning, and a Flask-based web dashboard to predict water safety and visualize quality trends over time.

The project helps monitor key water parameters, detect quality issues, and provide actionable recommendations for safe usage. It is designed for environmental monitoring, smart city applications, and IoT-based water management.

## Live Output

Open the application here:

https://hydroscan-ai.onrender.com

This deployment provides the live dashboard and prediction interface for the project.

## Overview

Access to clean water is essential for health, agriculture, and daily life. Traditional water testing is often slow and manual. HydroScan AI brings automation to this process by using sensor inputs and intelligent prediction to monitor and evaluate water quality efficiently.

### Main capabilities

- Real-time water quality prediction
- ESP32 sensor data integration
- Historical trend tracking
- Statistical analysis
- Report generation
- Recommendation system for safe usage
- Interactive dashboard UI

## Features

- Predict water quality using a trained ML model
- Monitor live and historical readings
- Analyze trends and water quality patterns
- Generate downloadable reports
- Display recommendations based on water condition
- Use Flask for a lightweight web application
- Support ESP32 and IoT-based monitoring workflows

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
hydroScanAI/
├── app.py
├── config.py
├── main.py
├── run.py
├── train.py
├── requirements.txt
├── README.md
├── .gitignore
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
└── TODO.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SPOORTHI-05428/hydroScanAI.git
cd hydroScanAI
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

On Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the app with:

```bash
python app.py
```

or:

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Retrain the Model

To train the model again using the dataset:

```bash
python train.py
```

## Use Cases

- Smart city water monitoring
- Residential water safety checking
- Industrial water quality analysis
- Agricultural irrigation management
- Environmental research and reporting

## Why This Project Matters

This project helps bridge the gap between IoT sensing and intelligent environmental decision-making. By turning water quality data into actionable insights, HydroScan AI supports safer communities and smarter resource management.

## Future Improvements

- Real-time cloud data streaming
- Database integration for persistent storage
- Mobile app support
- Advanced alert notifications
- Enhanced data visualizations
- Deployment for live production environments

## Author

SPOORTHI

## Project Status

Active development project for smart water quality monitoring and AI-driven analysis.

## License

This project is intended for educational and personal use.
