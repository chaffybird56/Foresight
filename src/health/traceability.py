"""
Traceable predictive-maintenance recommendations mapped to Canadian and ISO themes.

Illustrative only: not legal advice or a compliance attestation. Supports audit-style
trace IDs from live KPI and anomaly state.

Verified clause titles, statutory quotes, and mapping rationale:
see repository file docs/PM_STANDARDS_REFERENCE.md
"""
from __future__ import annotations

from typing import Any


FRAMEWORKS: list[dict[str, str]] = [
    {
        "code": "CSA C22.1",
        "name": "Canadian Electrical Code, Part I — Safety Standard for Electrical Installations",
        "theme": "National installation rules for electrical equipment and conductors (edition-specific). Referenced when work may affect installations or utilization equipment—not a substitute for the Code text.",
    },
    {
        "code": "CSA Z460",
        "name": "Control of hazardous energy — Lockout and other methods",
        "theme": "Published scope covers lockout and other methods for maintenance, inspection, servicing, etc., where hazardous energy exists (confirm edition in force).",
    },
    {
        "code": "CSA Z462",
        "name": "Workplace electrical safety",
        "theme": "Workplace electrical safety requirements (e.g. risk assessment, safe work practices, PPE) for work on or near electrical equipment.",
    },
    {
        "code": "Canada Labour Code, Part II",
        "name": "Occupational health and safety (federal employers)",
        "theme": "Employer duties in s. 125 include investigation of hazardous occurrences (s. 125(1)(c)), safe machinery/equipment (s. 125(1)(t)), and electrical equipment (s. 125(1)(m)(iii))—see verbatim excerpts in docs/PM_STANDARDS_REFERENCE.md.",
    },
    {
        "code": "ISO 9001:2015",
        "name": "Quality management systems — Requirements",
        "theme": "Clause titles used in mapping: 8.5.1 Control of production and service provision; 8.7 Control of nonconforming outputs; 9.1 Monitoring, measurement, analysis and evaluation (confirm against your normative copy).",
    },
]


def _refs(*codes: str) -> list[dict[str, str]]:
    code_set = set(codes)
    return [
        {"code": f["code"], "name": f["name"], "theme": f["theme"]}
        for f in FRAMEWORKS
        if f["code"] in code_set
    ]


def build_traceable_recommendations(
    availability_pct: float,
    demand_failures: int,
    open_work_orders: int,
    outliers_last_24h: int,
    samples_last_24h: int,
) -> list[dict[str, Any]]:
    """
    Produce trace IDs with rationale and standard cross-references from current health signals.
    """
    recs: list[dict[str, Any]] = []
    outlier_rate = (
        outliers_last_24h / samples_last_24h if samples_last_24h > 0 else 0.0
    )

    if availability_pct < 98.0:
        recs.append(
            {
                "trace_id": "PM-REC-AVL-01",
                "title": "Availability below operability target",
                "rationale": f"Rolling availability is {availability_pct:.2f}%; investigate sustained or recurring flow shortfalls against design basis.",
                "actions": [
                    "Trend demand vs. capacity; schedule inspection of pumps, valves, and strainers.",
                    "Record findings in the work management system with cause codes for trending.",
                ],
                "standard_refs": _refs("ISO 9001:2015", "Canada Labour Code, Part II"),
            }
        )

    if demand_failures > 0:
        recs.append(
            {
                "trace_id": "PM-REC-DMF-01",
                "title": "Demand-failure episodes detected",
                "rationale": f"{demand_failures} low-flow demand episode(s) in the window; treat as precursors to forced outages if unmitigated.",
                "actions": [
                    "Verify setpoints and interlocks; confirm sensors against redundant or portable references where policy allows.",
                    "Plan corrective maintenance only under controlled energy isolation (see Z460).",
                ],
                "standard_refs": _refs("CSA Z460", "CSA C22.1", "Canada Labour Code, Part II"),
            }
        )

    if open_work_orders > 0:
        recs.append(
            {
                "trace_id": "PM-REC-WO-01",
                "title": "Open work orders on the system",
                "rationale": f"{open_work_orders} open WO(s) may defer defect elimination; align deferrals with risk acceptance.",
                "actions": [
                    "Prioritize WOs affecting safety-related or production-critical paths.",
                    "Ensure deferral rationale and approvals are documented for QA traceability.",
                ],
                "standard_refs": _refs("ISO 9001:2015", "CSA Z460"),
            }
        )

    if outliers_last_24h > 0 and outlier_rate >= 0.005:
        recs.append(
            {
                "trace_id": "PM-REC-ANO-01",
                "title": "Elevated multivariate anomaly rate (24h)",
                "rationale": f"{outliers_last_24h} outlier minute(s) in last 24h (~{100*outlier_rate:.2f}% of samples); multivariate deviation may precede functional failure.",
                "actions": [
                    "Correlate outliers with vibration, ΔP, and temperature; schedule targeted inspection.",
                    "If electrical enclosure or motor work is required, apply Z462 work practices.",
                ],
                "standard_refs": _refs("CSA Z462", "CSA C22.1", "ISO 9001:2015"),
            }
        )
    elif outliers_last_24h > 0:
        recs.append(
            {
                "trace_id": "PM-REC-ANO-02",
                "title": "Sporadic sensor outliers",
                "rationale": f"{outliers_last_24h} isolated outlier(s); monitor for clustering or drift before full work package.",
                "actions": [
                    "Review calibration records and signal quality flags.",
                    "Retain anomaly timestamps for post-event review (measurement traceability).",
                ],
                "standard_refs": _refs("ISO 9001:2015", "Canada Labour Code, Part II"),
            }
        )

    if not recs:
        recs.append(
            {
                "trace_id": "PM-REC-BASE-00",
                "title": "No automated triggers fired",
                "rationale": "Current KPIs and 24h anomaly density are within demo thresholds; continue scheduled PM and periodic reliability review.",
                "actions": [
                    "Maintain preventive maintenance intervals per plant program.",
                    "Periodically re-validate Isolation Forest contamination and thresholds against operating experience.",
                ],
                "standard_refs": _refs("ISO 9001:2015", "CSA Z460"),
            }
        )

    return recs
