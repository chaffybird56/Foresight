# System Health Monitor (Nuclear/Power Systems)
## 🏷️ ![Flask App](https://img.shields.io/badge/Flask-Server-ff69b4) ![ML: IsolationForest](https://img.shields.io/badge/ML-IsolationForest-blueviolet) ![Reliability: Weibull](https://img.shields.io/badge/Reliability-Weibull-green)

A concise, practical example of **system health monitoring** and **reliability analytics** for a balance‑of‑plant system (e.g., Service Water, Condenser Cooling). It demonstrates:
- KPI trending (availability, demand failures, maintenance deferrals)
- **Anomaly detection** on sensor time‑series (Isolation Forest)
- Simple **Weibull** fit for failure-time data to estimate hazard and remaining useful life (RUL)
- A minimal **Flask** dashboard that renders charts from CSV inputs

> Uses only mock/public data and generic logic

## What you'll see
- **Home**: KPI cards (Availability, Demand Failures, Open WOs) + Last-24h chart  
- **Anomalies**: Outlier scatter on flow (last 24h)  
- **Reliability**: Weibull probability plot with fit (mock fallback if data sparse)

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
## 📊 Metrics & Terminology

### Key Performance Indicators

**Availability** — Percentage of time the system is "capable" (flow above an operability threshold).

$$\text{Availability} = \frac{\text{Minutes Meeting Threshold}}{\text{Total Minutes}} \times 100\%$$

*Example:* If the last 7 days contain 10,080 minutes and 9,780 minutes met the threshold:

$$\text{Availability} \approx \frac{9{,}780}{10{,}080} = 97.0\%$$

**Demand Failures** — Count of times the system was demanded but flow was below a safe threshold. We detect "rising edges" of low-flow episodes in the data.

---

### Sensor Parameters & Units

| Sensor | Unit | Description |
|--------|------|-------------|
| `flow_kg_s` | kg/s | Flow rate (proxy for capacity) |
| `dp_kPa` | kPa | Differential pressure (hydraulic resistance) |
| `temp_C` | °C | Temperature (thermal condition) |
| `vib_mm_s` | mm/s | Vibration velocity (mechanical health) |

---

### Weibull Reliability Analysis

Reliability engineers often model the distribution of times between failures with a **Weibull distribution**. A straight line on a Weibull probability plot implies a good fit.

**Shape Parameter** $\beta$ **(beta):**
- $\beta < 1$ → Early/infant mortality (decreasing hazard rate)
- $\beta \approx 1$ → Random failures (constant hazard rate)
- $\beta > 1$ → Wear-out (increasing hazard rate)

**Scale Parameter** $\eta$ **(eta):**  
Characteristic life parameter where approximately 63.2% of the population has failed:

$$P(T \leq \eta) \approx 0.632$$

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




