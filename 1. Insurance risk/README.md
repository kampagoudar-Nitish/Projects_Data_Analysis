# Insurance Risk Dataset – Data Cleaning & Analytical Review

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 01 – Insurance Risk Data Cleaning & Review  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas, numpy), Excel, SQL  

---

## Overview

This project demonstrates structured data cleaning, consistency checking, and analytical review applied to a synthetic insurance risk dataset. The work reflects the kind of careful, detail-oriented analysis required in advisory and decision-support contexts, where the goal is not to produce a dashboard, but to ensure that the figures, categories and assumptions underlying a dataset are actually reliable before anyone draws conclusions from them.

The dataset simulates a typical scenario: raw policy and claims data exported from an operational system, handed to an analyst with the instruction to "make it usable."

---

## What the project covers

1. **Raw data inspection** — identifying structural problems before any analysis begins
2. **Column-level audit** — checking data types, missing values, formatting inconsistencies
3. **Category consistency check** — flagging where the same concept appears under different labels (e.g., "Motor" vs "motor" vs "Motor Vehicle")
4. **Numeric validation** — identifying implausible values (negative claim amounts, impossible dates, premium-to-sum-insured ratios that don't hold)
5. **Source cross-check** — comparing aggregate figures in summary tab against row-level detail
6. **Cleaned output** — producing a working file with documented changes and a short analytical note

---

## Files

| File | Description |
|---|---|
| `raw_insurance_data.csv` | Synthetic raw dataset (200 rows, intentional errors embedded) |
| `data_cleaning.py` | Python script: full cleaning pipeline with inline comments |
| `anomaly_log.csv` | Output: rows flagged as anomalous with reason codes |
| `cleaned_output.csv` | Final cleaned dataset |
| `analytical_note.md` | Short written note: what was found, what was corrected, what remains uncertain |
| `consistency_check.sql` | SQL queries used to verify category and aggregate consistency |

---

## Key findings (synthetic data)

- 14% of rows had at least one data quality issue
- 3 distinct inconsistent labels for the same product category, consolidated to 1
- 7 records with claim amounts exceeding policy sum insured (flagged, not removed — flagging is the analyst's job; decision is the client's)
- Summary tab totals did not reconcile with row-level data (difference: 4.2%) — documented in analytical note
- 11 records with missing premium data — imputation approach documented and justified

---

## Design philosophy

This project is not about building a model or producing visualisations. It is about doing the upstream work carefully — the work that determines whether any downstream analysis is worth trusting. The cleaning logic is documented so that someone else can follow, verify, or challenge every decision made.

---

## How to run

```bash
pip install pandas numpy openpyxl
python data_cleaning.py
```

Output files will be written to `/output/`.
