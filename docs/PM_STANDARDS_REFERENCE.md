# PM recommendations & standards reference

This file is the **normative companion** to the high-level themes shown in the app (`/governance`) and in [`src/health/traceability.py`](../src/health/traceability.py). It explains **what is actually required or described** in each cited instrument, and how the demo maps **conceptually**—without claiming certification, legal compliance, or that any particular KPI threshold appears in a standard.

**Disclaimer:** This is not legal, engineering, or compliance advice. Standards are **copyright** and **edition-specific**; always use the official text purchased from the publisher or accessed under licence. Statutory text below from public law sources is cited for accuracy as of the retrieval date noted.

---

## 1. How to read the mapping

| Term in the app | Meaning |
|-----------------|--------|
| **Trace ID** (`PM-REC-…`) | A label for a **demo** recommendation triggered from mock KPI/anomaly logic. |
| **Cross-reference** | A **topic-level** link (e.g. “lockout before service”) to a standard that **genuinely** addresses that topic—not a claim that the standard mandates that exact sensor check. |

---

## 2. Canadian Electrical Code, Part I (CSA **C22.1**)

**Verified publication identity:** The CSA product is commonly cited as **CSA C22.1**, *Canadian Electrical Code, Part I*; CSA Group and resellers describe it as a **safety standard for electrical installations** (edition names vary, e.g. 2021, 2024). See [CSA Group store – C22.1](https://www.csagroup.org/store/product/CSA%20C22.1:21/) and related product listings.

**What the Code actually is:** A **national installation standard** for electrical wiring and equipment in the scopes covered by each edition’s rules. It is **not** a predictive-maintenance algorithm standard; the app references it when recommendations involve **electrical installation integrity**, **equipment for utilization of electrical power**, or work that must respect installation rules.

**Demo use:** When a recommendation mentions verification of interlocks, motors, or electrical work, the cross-reference reminds users that **field changes** must follow the **applicable Code edition** and local adoption.

---

## 3. CSA **Z460** — Control of hazardous energy (lockout and related methods)

**Verified scope (summary):** CSA **Z460** addresses **control of hazardous energy** (with **lockout** as a primary method) for activities such as **maintenance, inspection, troubleshooting, servicing**, etc., on machines and equipment where hazardous energy exists. Editions have been updated over time (e.g. historical **Z460-13**; newer editions such as **CSA Z460:20** appear in catalogues—confirm the edition in force for your jurisdiction).

**Authoritative product description:** See [Standards Council of Canada / CSA notices](https://www.scc-ccn.ca/standards/notices-of-intent/csa-group/control-hazardous-energy-lockout-and-other-methods) and [CSA Group product pages](https://www.csagroup.org/) for the official title and scope wording.

**Demo use:** Cross-references to Z460 apply when the recommended action is **servicing equipment** where **stored or supplied energy** must be controlled before return to service (e.g. after demand-failure or corrective maintenance).

---

## 4. CSA **Z462** — Workplace electrical safety

**Verified scope (summary):** **CSA Z462** sets requirements for **workplace electrical safety** in Canada, including **risk assessment**, **safe work practices**, **PPE**, and provisions relevant to **work on or near electrical equipment** (including maintenance and inspection contexts). It is complementary to installation rules in C22.1.

**Demo use:** Referenced when recommendations involve **electrical inspection or repair** (e.g. motors, enclosures), where **Z462**-aligned practices for **energized vs. de-energized work**, boundaries, and PPE would apply in real programs.

---

## 5. Canada Labour Code, Part II (occupational health and safety)

**Source:** [Canada Labour Code, section 125](https://laws-lois.justice.gc.ca/eng/acts/L-2/section-125.html), *Specific duties of employer* (federal workplaces). Text is **reproduced from the official consolidation**; always confirm the current version.

The following **verbatim** excerpts are **true statutory wording** relevant to this demo’s themes (investigation, equipment safety, hazard prevention):

**(c) Investigation of occurrences**

> (c) except as provided for in the regulations, **investigate, record and report**, in accordance with the regulations, all accidents, occurrences of harassment and violence, occupational illnesses and **other hazardous occurrences** known to the employer;

**(m) Electrical and other equipment**

> (m) ensure that the use, operation and maintenance of the following are in accordance with prescribed standards:
> …
> (iii) all **equipment for the generation, distribution or use of electricity**,

**(t) Machinery and tools**

> (t) ensure that the **machinery, equipment and tools** used by the employees in the course of their employment meet prescribed health, safety and ergonomic standards and are **safe under all conditions of their intended use**;

**(z.03) Hazard prevention program**

> (z.03) develop, implement and monitor, in consultation with the policy committee or, if there is no policy committee, with the work place committee or the health and safety representative, a prescribed **program for the prevention of hazards** in the work place appropriate to its size and the nature of the hazards in it that also provides for the education of employees in health and safety matters;

**Demo use:** Cross-references to Part II support recommendations about **recording and investigating** abnormal operating indications, **safe equipment**, and **hazard prevention**—aligned with the **topics** of paragraphs (c), (m)(iii), (t), and (z.03), not with any specific dashboard threshold.

---

## 6. ISO **9001** — Quality management systems

**Normative document:** **ISO 9001:2015**, *Quality management systems — Requirements* (copyright ISO). Clause numbering below follows the **fifth edition (2015)** structure.

**Verified clause titles** (standardized English titles widely published in ISO handbooks and accredited summaries):

| Clause | Title (ISO 9001:2015) |
|--------|------------------------|
| **8.5.1** | Control of production and service provision |
| **8.7** | Control of nonconforming outputs |
| **9.1** | Monitoring, measurement, analysis and evaluation |

**What these clauses address (high level, non-exhaustive):**

- **8.5.1** — Controlling production/service under controlled conditions; the standard lists types of controls (e.g. documented information, monitoring, infrastructure—see the normative text).
- **8.7** — Addressing outputs that do not conform to requirements.
- **9.1** — Determining what to monitor and measure, methods, when, and analysis of results.

**Demo use:** The app cites ISO 9001 when recommendations emphasize **documented operational control**, **monitoring/measuring** health signals, or **handling abnormal indications**—**analogous** to themes in 8.5.1, 8.7, and 9.1. It does **not** implement an ISO 9001 QMS and does **not** assert conformity.

---

## 7. Trace ID → standard topics (reference table)

| Trace ID | Trigger (demo logic) | Standards cited | Factual basis for the link |
|----------|----------------------|-----------------|----------------------------|
| **PM-REC-AVL-01** | Availability below 98% | ISO 9001; Canada Labour Code Part II | **9.1** (monitoring/measurement); **125(1)(t)** and **(z.03)** (safe equipment, hazard prevention)—see §5–6. |
| **PM-REC-DMF-01** | Demand failures above zero | Z460; C22.1; Part II | **Z460** hazardous energy control during service; **C22.1** installation/equipment rules where electrical; **125(1)(c)** investigation of hazardous occurrences. |
| **PM-REC-WO-01** | Open work orders above zero | ISO 9001; Z460 | **8.5.1** / **8.7** themes (controlled conditions, nonconforming outputs); **Z460** when WOs imply service with energy control. |
| **PM-REC-ANO-01** | Outlier rate ≥ 0.5% in 24h | Z462; C22.1; ISO 9001 | **Z462** electrical work practices; **C22.1** where installation/equipment affected; **9.1** monitoring. |
| **PM-REC-ANO-02** | Sporadic outliers | ISO 9001; Part II | **8.5.1** / **9.1** measurement integrity; **125(1)(c)** if occurrences are investigated as hazardous. |
| **PM-REC-BASE-00** | No trigger | ISO 9001; Z460 | Baseline **PM** and **energy-control** culture—**8.5.1** and **Z460** as general good practice references. |

---

## 8. Revision

| Date | Change |
|------|--------|
| 2026-03-27 | Initial companion document with sourced Labour Code quotes and ISO clause titles; CSA scopes summarized from public catalogue descriptions. |

When standards are updated, **re-validate** titles, editions, and clause references against your purchased copies.
