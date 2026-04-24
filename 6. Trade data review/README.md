# International Trade Data Review – Structural Analysis & Inconsistency Detection

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 06 – International Trade Dataset: Structural Review & Gap Analysis  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas, numpy), SQL, Excel  
**Background:** MBA in International Trade, Hochschule Anhalt (2025–present); module in International Economic Theory and Policy (grade 1.7) and Economic Statistics & Empirical Methods (grade 1.3)

---

## Overview

This project applies structured data review techniques to a synthetic international trade dataset, the kind of data that trade analysts, policy researchers, and consulting teams encounter when working with export/import records, tariff classifications, and trade flow reports.

The scenario: a research team is preparing a country-level trade analysis. They receive a dataset compiled from multiple sources across different reporting periods and ask for a preliminary data quality review before any analytical conclusions are drawn.

---

## What the project covers

1. **Source consistency check** — the dataset combines figures from two reporting bodies that use different classification systems; checking where they conflict
2. **HS code validation** — verifying that Harmonized System codes are formatted correctly and fall within expected ranges for the declared product categories
3. **Trade flow reconciliation** — checking whether reported export values from Country A to Country B match Country B's reported import values from Country A (they often don't; the question is by how much and why)
4. **Period alignment** — identifying where figures from different reporting periods have been combined without adjustment
5. **Outlier detection** — flagging trade values that are implausible relative to historical trends or partner country GDP
6. **Structured analytical note** — documenting what the data supports and what it does not

---

## Files

| File | Description |
|---|---|
| `raw_trade_data.csv` | Synthetic trade flow dataset: 40 country pairs × 5 years |
| `hs_reference.csv` | Reference table: valid HS code ranges by product category |
| `trade_review.py` | Python: full review pipeline |
| `trade_queries.sql` | SQL: bilateral reconciliation and period consistency checks |
| `analytical_note.md` | Written note: what the data supports, what it does not |
| `output/flagged_records.csv` | Row-level flags with reason codes |

---

## Key findings (synthetic scenario)

- Mirror statistics gap (export vs import discrepancy) averaged 6.2% across country pairs — within the range seen in real WTO/UN Comtrade data, but with 4 country pairs showing gaps above 18% requiring explanation
- 23 HS codes formatted incorrectly (5 digits instead of 6) — affecting product-category attribution
- 3 country pairs had figures from 2022 and 2023 combined without adjustment for currency or price level changes
- 2 trade values were implausible relative to exporting country GDP — flagged as possible data entry errors or re-export misattribution

---

## Design note

Mirror statistics gaps — where Country A's reported exports to Country B differ from Country B's reported imports from Country A are a known and well-documented issue in international trade statistics. This project does not treat them as errors; it quantifies them, contextualises them, and documents which are within normal range and which warrant further investigation.
