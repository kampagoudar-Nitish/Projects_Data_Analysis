# OEM Software Delivery – KPI Consistency Review & Tracking

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 05 – OEM Software Delivery KPI Review  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas, numpy), SQL, Excel  
**Background:** Draws on patterns from 2+ years of software delivery at BOSCH BGSW across seven OEM programmes

---

## Overview

This project applies structured data review to a synthetic software delivery KPI dataset modelled on the kind of reporting produced in a multi-OEM automotive software environment. The scenario: a programme manager receives a quarterly delivery dashboard and asks for a second pair of eyes before the figures go to the customer review meeting.

The work is not about building a new dashboard. It is about verifying whether the one that already exists is reliable.

---

## What the project covers

1. **KPI definition audit** — checking whether the same metric is calculated consistently across OEM programmes
2. **Defect density cross-check** — verifying that defect counts and line-of-code denominators are drawn from the same snapshot
3. **Timeline integrity** — checking whether milestone dates in the summary are consistent with the underlying delivery log
4. **Inter-programme comparison validity** — identifying where a "like-for-like" comparison between OEMs is not actually like-for-like
5. **Missing data audit** — surfacing which programmes have incomplete reporting periods
6. **Structured review note** — a written output that a programme manager could act on

---

## Files

| File | Description |
|---|---|
| `raw_delivery_log.csv` | Synthetic delivery log: 6 OEM programmes × 8 quarters |
| `kpi_summary.csv` | The summary dashboard being reviewed |
| `kpi_review.py` | Python: full consistency review pipeline |
| `kpi_queries.sql` | SQL: milestone and aggregate verification |
| `review_note.md` | Written note: findings, unresolved issues, recommended actions |
| `output/anomaly_flags.csv` | Row-level anomaly log |

---

## Key findings (synthetic scenario)

- Defect density figures for two OEM programmes used different LOC snapshot dates, making the comparison between them invalid
- One programme's "on-time delivery" rate was calculated against planned milestones, another against revised milestones, the basis of comparison was not stated in the summary
- Q3 figures for one programme were missing from the raw log but appeared (as estimated values) in the summary, not disclosed
- Summary total for delivered features (284) did not reconcile with row-level count (271), discrepancy of 13 features undocumented

---

## Why this matters

In multi-customer delivery environments, KPI summaries are often produced under time pressure and circulated before they are properly verified. This project demonstrates the checks that should happen before figures are presented to customers or used for resource planning decisions.
