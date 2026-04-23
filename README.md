# Projects – Data Analysis & Structured Review

**GitHub:** [kampagoudar-Nitish/Projects_Data_Analysis](https://github.com/kampagoudar-Nitish/Projects_Data_Analysis)  
**Author:** Nitish Kampagoudar  
**Contact:** nitishkampagoudar1@gmail.com | [LinkedIn](https://www.linkedin.com/in/nitish-kampagoudar-66a440b5/)

---

## About this repository

This repository contains a series of data analysis projects focused on structured data review, anomaly detection, consistency checking, and the organisation of messy or fragmented information into usable working files.

The projects are not built around dashboards or visualisation outputs. They are built around the kind of careful, documented analytical work that matters in advisory and decision-support contexts, where the reliability of the underlying data is the primary concern, and where every cleaning decision needs to be traceable and defensible.

Each project includes:
- A README explaining the scenario, scope and findings
- Python scripts with inline documentation of every decision
- SQL queries for independent verification
- A written analytical note summarising what was found, what remains uncertain, and what a reviewer needs to do

---

## Projects

| # | Project | Core Skills | Status |
|---|---|---|---|
| 01 | [Insurance Risk Dataset – Data Cleaning & Review](./project1_insurance_risk/) | Python, pandas, SQL, anomaly flagging, analytical note | Complete |
| 02 | [Supplier Quality Audit – Review & Gap Analysis](./project2_supplier_quality/) | Python, pandas, SQL, figure reconciliation, gap detection | Complete |
| 03 | [Sales Report Consistency Check](./project3_sales_consistency/) | Python, pandas, SQL, summary vs detail verification | Complete |
| 04 | [Contract Data Reconciliation – Multi-source Review](./project4_contract_anomaly/) | Python, pandas, conflict detection, structured notes | Complete |

---

## Tools used

- **Python:** pandas, numpy (data cleaning, validation, flagging)
- **SQL:** consistency checks, aggregate verification, gap analysis
- **Excel:** cross-checking, structured working files
- **Markdown:** analytical notes, review documentation

---

## Design principles

These projects reflect a specific approach to data work:

1. **Surface anomalies; do not silently resolve them.** An analyst who removes a row without documenting why has made a decision that the reviewer cannot see or challenge.

2. **Check figures before using them.** A summary that has not been verified against its source data is not reliable, regardless of how it looks.

3. **Document every decision point.** Every cleaning choice in these scripts is commented. Someone else should be able to follow, verify or challenge every step.

4. **Presentation is secondary to substance.** These projects do not produce polished charts. They produce reliable working files and clear written notes.

---
