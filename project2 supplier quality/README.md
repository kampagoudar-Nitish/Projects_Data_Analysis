# Supplier Quality Audit – Structured Review & Gap Analysis

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 02 – Supplier Quality Audit: Structured Review & Inconsistency Detection  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas), SQL, Excel  
**Context:** Based on analytical work patterns from automotive supplier coordination at BOSCH BGSW

---

## Overview

This project applies structured data review techniques to a synthetic supplier quality dataset. The scenario: an operations team receives a quarterly supplier audit export and needs to verify whether the figures are internally consistent before they are used in a management review.

The work focuses on what is often skipped in favour of building visuals: verifying that the data is actually reliable. That means checking whether categories are applied consistently, whether performance figures are supported by the detail behind them, and whether anomalies have been silently aggregated away.

---

## What the project covers

1. **Structural inspection** — understanding the dataset before analysing it
2. **Category standardisation** — supplier tier classifications, defect codes, and region labels
3. **Figure cross-checking** — verifying that summary-level figures are supported by row-level data
4. **Anomaly detection** — identifying suppliers with implausible defect rates, missing audit cycles, or contradictory status flags
5. **Gap analysis** — surfacing which suppliers have incomplete records before any benchmarking is done
6. **Structured output** — a clean working file and a written review note

---

## Files

| File | Description |
|---|---|
| `raw_supplier_data.csv` | Synthetic raw data: 150 suppliers, 8 quarters of quality metrics |
| `audit_review.py` | Python: full cleaning, cross-check, and anomaly detection pipeline |
| `gap_analysis.sql` | SQL: queries to identify missing audit periods and inconsistent flags |
| `supplier_review_note.md` | Written review: findings, unresolved issues, reviewer actions required |
| `output/cleaned_suppliers.csv` | Cleaned dataset with anomaly flags |
| `output/gap_report.csv` | Suppliers with missing data by quarter |

---

## Key patterns detected (synthetic data)

- Supplier tier classification inconsistent across 23% of records (e.g., "Tier 1", "T1", "tier-1", same supplier, different labels)
- 6 suppliers had defect rates reported as 0 for every quarter, plausible only if verified; flagged for confirmation
- Summary-level on-time delivery figure (94.3%) did not reconcile with the row-level average (91.7%), difference of 2.6 percentage points documented
- 11 suppliers missing at least one quarter of audit data, excluded from trend analysis pending explanation

---

## Design note

The analysis does not attempt to explain the anomalies. It surfaces them with enough structure for a reviewer to make informed decisions. The script is commented throughout so that every decision point is visible and challengeable.
