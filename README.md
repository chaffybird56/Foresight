# System Health Monitor (Nuclear/Power Systems)

A concise, practical example of **system health monitoring** and **reliability analytics** for a balance‑of‑plant system (e.g., Service Water, Condenser Cooling). It demonstrates:
- KPI trending (availability, demand failures, maintenance deferrals)
- **Anomaly detection** on sensor time‑series (Isolation Forest)
- Simple **Weibull** fit for failure-time data to estimate hazard and remaining useful life (RUL)
- A minimal **Flask** dashboard that renders charts from CSV inputs

> Uses only mock/public data and generic logic

## 🏷️ Badges
![Flask App](https://img.shields.io/badge/Flask-Server-ff69b4)
![ML: IsolationForest](https://img.shields.io/badge/ML-IsolationForest-blueviolet)
![Reliability: Weibull](https://img.shields.io/badge/Reliability-Weibull-green)

## Quick Start (no Docker)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_mock_data.py
python app.py
# open http://127.0.0.1:8000
```

## Quick Start (Docker)

```bash
docker build -t shm:latest .
docker run --rm -p 8000:8000 shm:latest
# open http://localhost:8000
```

## What you'll see
- **Home**: KPI cards (Availability, Demand Failures, Open WOs) + Last-24h chart  
- **Anomalies**: Outlier scatter on flow (last 24h)  
- **Reliability**: Weibull probability plot with fit (mock fallback if data sparse)

<img width="1605" height="620" alt="SCR-20251001-puqu" src="https://github.com/user-attachments/assets/1434d019-2707-47bf-9d48-8f78023f3418" />

<img width="1394" height="250" alt="SCR-20251001-pusu" src="https://github.com/user-attachments/assets/6385bc0a-45a0-4be4-90f2-02e2795cef21" />

<img width="1663" height="339" alt="SCR-20251001-puvq" src="https://github.com/user-attachments/assets/eca28272-925d-4edd-8110-4a3414849047" />
---

Availability — percentage of time the system is “capable” (here: flow above an operability threshold). For example, if the last 7 days contain 10,080 minutes and 9,780 minutes met the threshold, availability ≈ 9,780/10,080 = 97.0%.

Demand failures — count of times the system was demanded but flow was below a safe threshold (we detect “rising edges” of low-flow episodes in the data).

Sensors & units

flow_kg_s: flow rate in kilograms per second (proxy for capacity).

dp_kPa: differential pressure in kilopascals (hydraulic resistance).

temp_C: temperature in °C (thermal condition).

vib_mm_s: vibration velocity in mm/s (mechanical health).

Weibull fit — reliability engineers often model the distribution of times between failures with a Weibull distribution; a straight line on a Weibull probability plot implies a good fit. The slope is β (beta):

β < 1 → early/infant mortality (decreasing hazard),

β ≈ 1 → random failures (constant hazard),

β > 1 → wear-out (increasing hazard).
The scale η (eta) is a characteristic life parameter (where ~63.2% of a population has failed).

## Notes
- Headless plotting enforced via `MPLBACKEND=Agg`.
- Mock data generator is rerunnable and safe.

## Disclaimer
Illustrative use only; integrate with plant PI/Maximo/OSIsoft via appropriate security/governance when adapting for real sites.

---

## 👀 At a glance (Simple)
We “listen” to a plant system (flow, pressure, temperature, vibration) and:
- Show health **KPIs** (availability, demand failures, open work orders).
- **Spot anomalies** automatically.
- Estimate reliability with a **Weibull** fit for failure intervals.

## 🧠 How the code achieves it 
- `src/health/kpi.py` computes KPIs from raw time series and events.
- `src/health/anomaly.py` runs an Isolation Forest across multiple sensors to flag outliers.
- `app.py` serves charts (Flask). A small Weibull fit estimates shape/scale from inter-failure times.




