# Metrics & terminology

Definitions for KPIs, sensors, and Weibull plots used in the dashboard and [`README.md`](../README.md).

## Key Performance Indicators

**Availability** — Share of time the system is “capable” (flow above an operability threshold).

$$\text{Availability} = \frac{\text{Minutes Meeting Threshold}}{\text{Total Minutes}} \times 100\%$$

*Example:* If the last 7 days contain 10,080 minutes and 9,780 minutes met the threshold:

$$\text{Availability} \approx \frac{9{,}780}{10{,}080} = 97.0\%$$

**Demand Failures** — Count of episodes where the system was demanded but flow was below a safe threshold (“rising edges” of low-flow in the series).

---

## Sensor parameters

| Sensor | Unit | Description |
|--------|------|-------------|
| `flow_kg_s` | kg/s | Flow rate (proxy for capacity) |
| `dp_kPa` | kPa | Differential pressure (hydraulic resistance) |
| `temp_C` | °C | Temperature (thermal condition) |
| `vib_mm_s` | mm/s | Vibration velocity (mechanical health) |

---

## Weibull reliability

Times between failures are often modeled with a **Weibull** distribution; a straight line on a Weibull probability plot suggests a reasonable fit.

**Shape** $\beta$ (beta):

- $\beta < 1$ → Early/infant mortality (decreasing hazard)
- $\beta \approx 1$ → Random failures (constant hazard)
- $\beta > 1$ → Wear-out (increasing hazard)

**Scale** $\eta$ (eta) — characteristic life where roughly 63.2% of the population has failed:

$$P(T \leq \eta) \approx 0.632$$
