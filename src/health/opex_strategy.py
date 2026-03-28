"""
OPEX-informed predictive-maintenance scenarios.

Maps analysis outputs (KPIs, anomalies, optional Weibull shape) to narrative
recommendations for asset strategy and inspection focus under an operating-
expenditure (OPEX) lens: balancing planned spend (inspections, minor PM)
against the risk cost of unplanned outages and deferrals.

Illustrative demo logic only—not an economic model or budget authority.
"""
from __future__ import annotations

from typing import Any

import pandas as pd
import numpy as np


def fit_weibull_shape_eta(df_events: pd.DataFrame) -> tuple[float | None, float | None]:
    """Same Weibull line fit as the reliability API; returns (beta, eta) or (None, None)."""
    df = df_events[df_events["type"] == "failure"].copy()
    if df.empty or len(df.sort_values("start")["start"].values) < 3:
        x = np.array([100, 140, 220, 300], dtype=float)
    else:
        t = df.sort_values("start")["start"].values
        x = np.diff(t).astype("timedelta64[m]").astype(float)
    x = np.asarray(x, dtype=float).ravel()
    if x.size < 2:
        return None, None
    x = np.sort(np.asarray(x))
    F = (np.arange(1, len(x) + 1) - 0.3) / (len(x) + 0.4)
    y = np.log(np.log(1 / (1 - F)))
    X = np.vstack([np.log(x), np.ones(len(x))]).T
    beta, a = np.linalg.lstsq(X, y, rcond=None)[0]
    eta = float(np.exp(-a / beta))
    return float(beta), eta


def build_opex_informed_strategy(
    availability_pct: float,
    demand_failures: int,
    open_work_orders: int,
    outliers_last_24h: int,
    samples_last_24h: int,
    weibull_beta: float | None,
    weibull_eta_min: float | None,
) -> dict[str, Any]:
    """
    Produce OPEX-framed scenarios: where to lean inspection vs. corrective spend,
    informed by current health signals (not dollar amounts—qualitative trade-offs).
    """
    outlier_rate = (
        outliers_last_24h / samples_last_24h if samples_last_24h > 0 else 0.0
    )
    scenarios: list[dict[str, Any]] = []

    # Scenario A: demand failures drive unplanned-outage risk → prioritize corrective + targeted inspection
    if demand_failures > 0:
        scenarios.append(
            {
                "id": "OPEX-SC-DMF",
                "title": "Demand-failure pressure on operating budget",
                "opex_framing": (
                    f"{demand_failures} demand-failure episode(s) imply higher probability of forced derates or trips; "
                    "unplanned outage cost typically dominates incremental inspection OPEX. "
                    "Shift near-term spend toward confirming root causes (hydraulic path, controls) before optimizing routine rounds."
                ),
                "asset_strategy": [
                    "Treat hydraulic capacity and control logic as the asset class driving marginal risk.",
                    "Defer non-critical cosmetic or low-risk PM only after demand stability is restored or explicitly risk-accepted.",
                ],
                "inspection_focus": [
                    "Pumps, valves, and strainers on the flow path; verify actuator response and setpoint integrity.",
                    "Spot-check differential pressure trends against historical baselines for fouling or blockage signatures.",
                ],
            }
        )

    # Scenario B: availability headroom eroding
    if availability_pct < 98.5:
        scenarios.append(
            {
                "id": "OPEX-SC-AVL",
                "title": "Availability margin vs. run-maintain balance",
                "opex_framing": (
                    f"Availability at {availability_pct:.2f}% narrows margin to operability targets; "
                    "OPEX trade-off is between additional condition-monitoring / minor interventions now versus higher loss-of-production cost if the trend continues."
                ),
                "asset_strategy": [
                    "Prioritize restoring design margin (capacity, cooling, or control band) before broad inspection rotation increases.",
                    "Sequence work to avoid stacking outages on the same production window.",
                ],
                "inspection_focus": [
                    "Thermal and flow margin: heat exchangers, cooling circuits, and load-following behaviour.",
                    "Cross-check sensor agreement (flow vs. ΔP) to avoid chasing instrumentation noise.",
                ],
            }
        )

    # Scenario C: anomaly density → inspection OPEX allocation
    if outliers_last_24h > 0 and outlier_rate >= 0.003:
        scenarios.append(
            {
                "id": "OPEX-SC-ANO",
                "title": "Elevated multivariate anomaly rate",
                "opex_framing": (
                    f"~{100 * outlier_rate:.2f}% of last-24h samples flagged multivariate outliers; "
                    "warranted inspection OPEX is often lower than a full outage but higher than 'monitor only'—reallocate walkdowns toward rotating and electrical assets feeding these sensors."
                ),
                "asset_strategy": [
                    "Increase condition-monitoring frequency on the affected train until the cluster clears or is explained.",
                    "Hold major capital-style changes until failure mode is classified (mechanical vs. instrument vs. process upset).",
                ],
                "inspection_focus": [
                    "Rotating equipment and couplings (vibration context), motor and drive auxiliaries if electrical work is in scope.",
                    "Field verification of instrument loops feeding the isolation-forest feature set.",
                ],
            }
        )

    # Scenario D: Weibull wear-out hint (beta > 1)
    if weibull_beta is not None and weibull_beta > 1.05:
        eta_txt = (
            f"{weibull_eta_min:.0f} min"
            if weibull_eta_min is not None
            else "characteristic life from fit"
        )
        scenarios.append(
            {
                "id": "OPEX-SC-WBL",
                "title": "Wear-out regime in failure spacing (Weibull shape β > 1)",
                "opex_framing": (
                    f"Weibull shape β ≈ {weibull_beta:.2f} suggests increasing failure rate with age; "
                    "OPEX-efficient strategy often front-loads planned replacements or overhauls before the steeper hazard region rather than repeated minor repairs."
                ),
                "asset_strategy": [
                    f"Align major maintenance windows with characteristic life context ({eta_txt}) and spares lead time.",
                    "Favor time- or usage-based replacement for components in wear-out when cost of failure exceeds planned renewal.",
                ],
                "inspection_focus": [
                    "Borescope or NDE on critical rotating elements per program; trending same failure mode family.",
                    "Verify lubrication and alignment programs match rising hazard if β remains elevated.",
                ],
            }
        )

    # Scenario E: backlog
    if open_work_orders > 0:
        scenarios.append(
            {
                "id": "OPEX-SC-WO",
                "title": "Work-order backlog and OPEX absorption",
                "opex_framing": (
                    f"{open_work_orders} open work order(s) tie up labour and contractor capacity; "
                    "effective asset strategy sequences WOs by combined safety, production, and OPEX impact—not FIFO alone."
                ),
                "asset_strategy": [
                    "Rank backlog by consequence of failure and schedule slack, then by estimated labour efficiency.",
                    "Bundle inspections with pending WOs on the same system to reduce repeated isolations.",
                ],
                "inspection_focus": [
                    "Systems already tagged in open WOs: complete field verification before closing.",
                    "Quick visual rounds on adjacent equipment that shares utilities with deferred work.",
                ],
            }
        )

    if not scenarios:
        scenarios.append(
            {
                "id": "OPEX-SC-BASE",
                "title": "Stable window — sustain program and tune thresholds",
                "opex_framing": (
                    "No strong OPEX tilt from current demo triggers; maintain baseline preventive maintenance and "
                    "periodic reliability review. Revisit anomaly thresholds as operating season or duty cycle changes."
                ),
                "asset_strategy": [
                    "Keep scheduled PM and calibration cycles per plant program.",
                    "Reserve discretionary inspection OPEX for upcoming duty changes (seasonal load, outages).",
                ],
                "inspection_focus": [
                    "Continue routine rounds per existing route sheets.",
                    "Spot-check data quality and historian alignment for the four monitored signals.",
                ],
            }
        )

    summary = (
        "Operating expenditure (OPEX) framing: prioritize inspections and minor interventions where analysis shows "
        "the largest reduction in unplanned outage or availability risk per unit of spend; scenarios below translate "
        "current KPI, anomaly, and (when available) Weibull context into asset strategy and inspection emphasis."
    )

    return {"summary": summary, "scenarios": scenarios}
