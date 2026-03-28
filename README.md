# System Health Monitor (Nuclear/Power Systems)

## 🏷️ ![Flask App](https://img.shields.io/badge/Flask-Server-ff69b4) ![ML: IsolationForest](https://img.shields.io/badge/ML-IsolationForest-blueviolet) ![Reliability: Weibull](https://img.shields.io/badge/Reliability-Weibull-green)

- Built an equipment health monitoring application that highlights trends for **preventive maintenance** and **reliability** decisions on nuclear and power-plant style signals (flow, pressure, temperature, vibration).
- Explored **predictive maintenance** with **traceable recommendations** tied to Canadian Electrical Code (C22.1), CSA Z460/Z462, Canada Labour Code safety themes, and ISO 9001–oriented quality assurance—documented in [docs/PM_STANDARDS_REFERENCE.md](docs/PM_STANDARDS_REFERENCE.md) and shown in-app under **`/governance`**.
- Explored predictive-maintenance **scenarios informed by operating expenditure (OPEX)**—turning analysis output into recommendations for **asset strategy** and **inspection focus** ([`src/health/opex_strategy.py`](src/health/opex_strategy.py), same `/governance` view and `/api/recommendations` payload).
- Implemented **Python** analytics and **anomaly detection** (Isolation Forest) so emerging equipment issues surface before they affect operations.

**Extra detail (optional reads):** [Standards & verified citations](docs/PM_STANDARDS_REFERENCE.md) · [KPI definitions, sensors, Weibull formulas](docs/METRICS_AND_TERMINOLOGY.md)

A concise, practical example of **system health monitoring** and **reliability analytics** for a balance-of-plant system (for example Service Water, Condenser Cooling). It demonstrates:

- KPI trending (availability, demand failures, maintenance deferrals)
- **Anomaly detection** on sensor time series (Isolation Forest)
- A simple **Weibull** fit on failure-time data to estimate hazard and remaining useful life (RUL)
- **Traceable preventive maintenance recommendations** from live state, with standards cross-references (`/governance`, [`src/health/traceability.py`](src/health/traceability.py))
- **OPEX-informed scenarios** (planned spend vs. unplanned-outage risk) for asset strategy and inspection emphasis ([`src/health/opex_strategy.py`](src/health/opex_strategy.py))
- A minimal **Flask** dashboard that renders charts from CSV inputs

> Uses only mock/public data and generic logic.

## 👀 At a glance

We treat the plant like a single system we “listen” to (flow, pressure, temperature, vibration). The app then:

- Shows health **KPIs**: availability, demand failures, and open work orders.
- **Flags anomalies** automatically on the sensor streams.
- Estimates **reliability** with a **Weibull** fit on failure intervals.
- On **`/governance`**, turns that analysis into **OPEX-aware** suggestions (where to focus inspections and how to think about asset strategy under operating-spend vs. outage-risk trade-offs), alongside standards-traceable preventive maintenance items.

## Screenshots (running app)

**Home — KPIs and last 24h trend**  
Overview cards and a multi-series time chart (flow, differential pressure, temperature, vibration) for the most recent day.

<img width="1605" height="620" alt="Home dashboard: KPI cards and last 24h sensor trend" src="https://github.com/user-attachments/assets/1434d019-2707-47bf-9d48-8f78023f3418" />

**Anomalies — flow and outliers**  
Flow signal for the last 24 hours with outlier samples marked so you can see where the model disagrees with normal multivariate behaviour.

<img width="1394" height="250" alt="Anomalies view: flow with outlier markers" src="https://github.com/user-attachments/assets/6385bc0a-45a0-4be4-90f2-02e2795cef21" />

**Reliability — Weibull plot**  
Empirical failure spacing vs. fitted Weibull line in transformed coordinates (shape/scale summarized on the chart).

<img width="1663" height="339" alt="Reliability view: Weibull probability plot with fit" src="https://github.com/user-attachments/assets/eca28272-925d-4edd-8110-4a3414849047" />

## What you’ll see

| Screen | Description |
|--------|-------------|
| **Home** | KPI cards (availability, demand failures, open work orders) and a **last 24 hours** trend chart for all four sensors. |
| **Anomalies** | Flow over the last 24 hours with outlier points highlighted from the isolation-forest model. |
| **Reliability** | Weibull probability–style plot with a line fit (uses mock spacing if failure data are sparse). |
| **Preventive maintenance & standards** (`/governance`) | Standards reference table, **OPEX-informed** asset strategy and inspection-focus scenarios from KPIs/anomalies/Weibull (see below), plus **traceable** preventive-maintenance items; JSON at `/api/recommendations` (`opex_strategy` + `recommendations`). |

## 🧠 How the code achieves it

- [`src/health/kpi.py`](src/health/kpi.py) computes KPIs from raw time series and events.
- [`src/health/anomaly.py`](src/health/anomaly.py) runs an Isolation Forest across multiple sensors to flag outliers.
- [`src/health/traceability.py`](src/health/traceability.py) maps live KPI and anomaly context to trace IDs with suggested actions; standards mapping is explained in [docs/PM_STANDARDS_REFERENCE.md](docs/PM_STANDARDS_REFERENCE.md).
- [`src/health/opex_strategy.py`](src/health/opex_strategy.py) turns the same analysis into **OPEX-framed** scenarios (asset strategy, inspection focus) using KPIs, anomaly density, and Weibull shape when available.
- [`app.py`](app.py) serves the Flask UI, Chart.js endpoints, static plots, and the Weibull fit for the reliability view.

---

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
