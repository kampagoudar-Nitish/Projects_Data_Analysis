# Projects – Data Analysis & Structured Review

**GitHub:** [kampagoudar-Nitish/Projects_Data_Analysis](https://github.com/kampagoudar-Nitish/Projects_Data_Analysis)  
**Author:** Nitish Kampagoudar  
**Contact:** nitishkampagoudar1@gmail.com | [LinkedIn](https://www.linkedin.com/in/nitish-kampagoudar-66a440b5/)

---

## About this repository

This repository contains structured data analysis projects focused on data review, anomaly detection, consistency checking, multi-source reconciliation, and pre-deployment model auditing. The work draws on patterns from professional experience at BOSCH Global Software Technologies (2023–2025), an ML internship at Knowledge Solution India Limited (2020), and MBA coursework in International Trade at Hochschule Anhalt (2025–present).

The projects are not built around dashboards or visualisation. They are built around the upstream work that determines whether any analysis is worth trusting: verifying figures, cleaning fragmented data, flagging inconsistencies, and documenting every decision so that a reviewer can follow, verify or challenge the work.

---

## Projects

| # | Project | Domain | Core techniques | Status |
|---|---|---|---|---|
| 01 | [Insurance Risk Dataset – Data Cleaning & Review](./project1_insurance_risk/) | Insurance / Financial | Python cleaning pipeline, SQL checks, anomaly flagging, analytical note | Complete |
| 02 | [Supplier Quality Audit – Review & Gap Analysis](./project2_supplier_quality/) | Automotive / Operations | Category normalisation, figure reconciliation, gap detection | Complete |
| 03 | [Sales Report Consistency Check](./project3_sales_consistency/) | Sales / Finance | Summary vs detail verification, YoY basis check | Complete |
| 04 | [Contract Data Reconciliation – Multi-source Review](./project4_contract_anomaly/) | Legal / Operations | Three-source merge, conflict detection, orphan identification | Complete |
| 05 | [OEM Software Delivery – KPI Consistency Review](./project5_oem_kpi_tracker/) | Automotive / Software | KPI reconciliation, milestone basis audit, cross-programme comparison validity | Complete |
| 06 | [International Trade Dataset – Structural Review](./project6_trade_data_review/) | International Trade / Economics | Mirror statistics analysis, HS code validation, period mixing detection | Complete |
| 07 | [Admission Model – Input Validation & Output Audit](./project7_admission_model_audit/) | Education / ML | Input range checks, encoding mismatch, threshold sensitivity, prediction consistency | Complete |

---

## Background behind each project

| Project | Professional / Academic connection |
|---|---|
| 01 – Insurance Risk | ML internship, Knowledge Solution India Limited (2020) — insurance risk prediction |
| 02 – Supplier Quality | BOSCH BGSW (2023–2025) — supplier and OEM quality tracking |
| 03 – Sales Consistency | Cross-functional reporting and summary verification at BOSCH |
| 04 – Contract Reconciliation | Multi-source documentation management across OEM programmes at BOSCH |
| 05 – OEM KPI Review | Direct experience tracking software delivery KPIs across 7 OEM programmes at BOSCH |
| 06 – Trade Data | MBA in International Trade, Hochschule Anhalt — International Economic Theory (1.7), Economic Statistics (1.3) |
| 07 – Admission Model Audit | Extends ML internship admission prediction work with pre-deployment audit methodology |

---

## Tools used

Python (pandas, numpy, scikit-learn) · SQL · Excel · Markdown

---

## Design principles

1. Surface anomalies; do not silently resolve them.
2. Check figures before using them.
3. Document every decision, every flag includes a reason and a note.
4. Presentation is secondary to substance.
5. Flag boundary cases explicitly; pass judgement calls to the reviewer.
