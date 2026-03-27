"""
Traceable predictive-maintenance recommendations mapped to Canadian and ISO themes.

Illustrative only: not legal advice or a compliance attestation. Supports audit-style
trace IDs from live KPI and anomaly state.
"""
from __future__ import annotations

from typing import Any


FRAMEWORKS: list[dict[str, str]] = [
    {
        "code": "CSA C22.1",
        "name": "Canadian Electrical Code, Part I",
        "theme": "Electrical installation and equipment integrity for instrument, control, and power circuits supporting monitored plant loads.",
    },
    {
        "code": "CSA Z460",
        "name": "Control of hazardous energy (lockout)",
        "theme": "Procedures and verification before equipment is returned to service after maintenance or abnormal conditions.",
    },
    {
        "code": "CSA Z462",
        "name": "Workplace electrical safety",
        "theme": "Risk assessment, safe work practices, and PPE when electrical equipment is accessed for inspection or repair.",
    },
    {
        "code": "Canada Labour Code, Part II",
        "name": "Occupational health and safety (federal)",
        "theme": "Employer duties: hazard identification, investigation of dangerous occurrences, and preventive measures.",
    },
    {
        "code": "ISO 9001",
        "name": "Quality management systems (themes)",
        "theme": "Documented operational controls, monitoring and measurement, nonconformity and corrective action (e.g. Clauses 8.5, 8.7, 9.1).",
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
                "standard_refs": _refs("ISO 9001", "Canada Labour Code, Part II"),
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
                "standard_refs": _refs("ISO 9001", "CSA Z460"),
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
                "standard_refs": _refs("CSA Z462", "CSA C22.1", "ISO 9001"),
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
                "standard_refs": _refs("ISO 9001", "Canada Labour Code, Part II"),
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
                "standard_refs": _refs("ISO 9001", "CSA Z460"),
            }
        )

    return recs
