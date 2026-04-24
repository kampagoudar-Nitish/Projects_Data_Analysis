# Sales Report Consistency Check – Verifying a Management Summary

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 03 – Sales Report Consistency Check  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas), SQL, Excel  

---

## Overview

This project addresses a common and underappreciated problem in data work: a management summary is produced, circulated, and cited, but no one has checked whether it is actually supported by the underlying data.

The scenario: a regional sales report is prepared for a quarterly business review. The summary shows regional breakdowns, product category performance and year-over-year comparisons. The task is to verify that these figures are internally consistent, that categories are applied correctly, and that the YoY comparisons are using a consistent basis.

---

## What the project covers

1. **Summary vs detail reconciliation** — does the summary add up to the detail?
2. **Category consistency** — are product categories applied consistently across regions and periods?
3. **YoY comparison basis** — are prior-year figures drawn from the same dataset, or is there a version mismatch?
4. **Regional attribution** — are transactions correctly attributed to the right region?
5. **Rounding and aggregation checks** — do subtotals and totals hold mathematically?
6. **Anomaly report** — structured output of every discrepancy found

---

## Files

| File | Description |
|---|---|
| `raw_sales_data.csv` | Synthetic raw transaction data (500 rows, 2 years) |
| `summary_report.csv` | The management summary being verified |
| `consistency_check.py` | Python: full verification pipeline |
| `consistency_check.sql` | SQL: alternative verification queries |
| `discrepancy_report.md` | Written report: every discrepancy found, with context |

---

## Key findings (synthetic scenario)

- Regional total for "North" in the summary (€2,340,000) did not match row-level sum (€2,287,400) — difference of €52,600
- YoY growth figure of +12.4% for Product Category B was based on a prior-year figure from a different dataset version; correct figure using consistent basis = +8.1%
- Two product subcategories were attributed to different parent categories in different periods — affecting category-level totals
- Three rounding errors in summary subtotals (differences of €50–€200 individually, but compound to €480 at total level)

---

## Why this matters

A summary cited in a business review that has not been verified against its source data is not reliable, regardless of how polished it looks. This project documents how to systematically verify a management report before it is used for decisions.
