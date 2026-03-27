# System Health Monitor (Nuclear/Power Systems)

## 🏷️ ![Flask App](https://img.shields.io/badge/Flask-Server-ff69b4) ![ML: IsolationForest](https://img.shields.io/badge/ML-IsolationForest-blueviolet) ![Reliability: Weibull](https://img.shields.io/badge/Reliability-Weibull-green)

- **Health monitoring** for balance-of-plant style signals (preventive maintenance & reliability)—KPIs, isolation-forest anomalies, Weibull-style reliability, and a Flask UI over CSV data.
- **Traceable PM** recommendations and standards cross-references (C22.1, CSA Z460/Z462, Canada Labour Code Part II, ISO 9001:2015)—see [docs/PM_STANDARDS_REFERENCE.md](docs/PM_STANDARDS_REFERENCE.md) and in-app **`/governance`**.

**More detail:** [Standards & citations](docs/PM_STANDARDS_REFERENCE.md) · [KPIs, sensors & Weibull math](docs/METRICS_AND_TERMINOLOGY.md)

> Mock/public data only; generic logic for demos.

## What it does

| Area | Implementation |
|------|------------------|
| KPIs | `src/health/kpi.py` |
| Anomalies | `src/health/anomaly.py` (Isolation Forest) |
| PM trace IDs | `src/health/traceability.py` → `/governance`, `/api/recommendations` |
| Charts & Weibull | `app.py` |

## Routes

| Page | What you get |
|------|----------------|
| **Home** | KPI cards, last-24h trend |
| **Anomalies** | Flow + outliers (24h) |
| **Reliability** | Weibull probability plot (mock fallback if sparse) |
| **PM & standards** | Framework table + live recommendations |

<img width="1605" height="620" alt="SCR-20251001-puqu" src="https://github.com/user-attachments/assets/1434d019-2707-47bf-9d48-8f78023f3418" />

<img width="1394" height="250" alt="SCR-20251001-pusu" src="https://github.com/user-attachments/assets/6385bc0a-45a0-4be4-90f2-02e2795cef21" />

<img width="1663" height="339" alt="SCR-20251001-puvq" src="https://github.com/user-attachments/assets/eca28272-925d-4edd-8110-4a3414849047" />
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
