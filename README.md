# System Health Monitor (Nuclear/Power Systems)

A concise, practical example of **system health monitoring** and **reliability analytics** for a balance‑of‑plant system (e.g., Service Water, Condenser Cooling). It demonstrates:
- KPI trending (availability, demand failures, maintenance deferrals)
- **Anomaly detection** on sensor time‑series (Isolation Forest)
- Simple **Weibull** fit for failure-time data to estimate hazard and remaining useful life (RUL)
- A minimal **Flask** dashboard that renders charts from CSV inputs

> Uses only mock/public data and generic logic—safe for GitHub portfolios.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_mock_data.py
python app.py
# open http://127.0.0.1:5000
```

## Data
- `data/mock_sensors.csv`: minute-level readings (flow, dp, temp, vibration)
- `data/events.csv`: outages, work orders, and failures with start/stop times

## Screens
- **/ (home)**: KPIs, last 24h trend, open WOs
- **/anomalies**: outlier timeline and counts
- **/reliability**: Weibull fit summary

## Disclaimer
Illustrative use only; integrate with plant PI/Maximo/OSIsoft via appropriate security/governance when adapting for real sites.



---

## 👀 At a glance (Simple)
We “listen” to a plant system (flow, pressure, temperature, vibration) and:
- Show health **KPIs** (availability, demand failures, open work orders).
- **Spot anomalies** automatically.
- Estimate reliability with a **Weibull** fit for failure intervals.

## 🧠 How the code achieves it (Technical)
- `src/health/kpi.py` computes KPIs from raw time series and events.
- `src/health/anomaly.py` runs an Isolation Forest across multiple sensors to flag outliers.
- `app.py` serves charts (Flask). A small Weibull fit estimates shape/scale from inter-failure times.

## 🏷️ Badges
![Flask App](https://img.shields.io/badge/Flask-Server-ff69b4)
![ML: IsolationForest](https://img.shields.io/badge/ML-IsolationForest-blueviolet)
![Reliability: Weibull](https://img.shields.io/badge/Reliability-Weibull-green)

## 📸 Screenshots
<img src="outputs_last24.png" width="720" alt="Last-24h trend"/>
<br>
<img src="outputs_anomalies.png" width="720" alt="Anomaly view"/>

## 📄 Report
The full write-up (including appendix and references) is in [`report/report.tex`](report/report.tex).
