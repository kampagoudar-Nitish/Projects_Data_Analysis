# Student Admission Prediction – Model Audit & Input Data Review

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 07 – Admission Prediction Model: Input Validation & Output Audit  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas, numpy, scikit-learn), SQL  
**Background:** Extends work from ML internship at Knowledge Solution India Limited (Sep–Nov 2020), where a student admission prediction model was developed for a structured dataset

---

## Overview

Most model audits focus on performance metrics. This one focuses on something more fundamental: whether the data going into the model is reliable, and whether the model's outputs can be trusted given the quality of that input.

The scenario: a university admissions support team uses a predictive model to help prioritise applications. A new analyst is asked to review both the input dataset and the model's behaviour before it is used in the upcoming admissions cycle.

This is not a model-building project. The model already exists. The task is to audit it — checking the inputs, the feature distributions, the prediction outputs, and whether the model behaves consistently across comparable applicant profiles.

---

## What the project covers

1. **Input data validation** — checking for missing values, out-of-range scores, and encoding inconsistencies in categorical features
2. **Feature distribution review** — identifying whether the training data distribution is representative of the current applicant pool
3. **Prediction consistency check** — testing whether the model produces consistent outputs for applicant profiles that should be near-identical
4. **Threshold sensitivity analysis** — examining how the accept/reject boundary behaves near the decision threshold
5. **Demographic balance audit** — checking whether acceptance rates vary materially across subgroups in a way that warrants review
6. **Output documentation** — a structured note summarising what the audit found and what should be reviewed before deployment

---

## Files

| File | Description |
|---|---|
| `applicant_data.csv` | Synthetic applicant dataset: 500 records, 12 features |
| `model_audit.py` | Python: full audit pipeline |
| `audit_note.md` | Written audit note: findings and recommended actions |
| `output/input_flags.csv` | Row-level input data issues |
| `output/prediction_consistency.csv` | Near-identical profiles with divergent predictions |
| `output/threshold_sensitivity.csv` | Prediction probabilities near the decision boundary |

---

## Key findings (synthetic scenario)

- 8.4% of records had at least one input feature with a value outside the expected range (e.g., GPA > 4.0 on a 4.0 scale)
- 14 pairs of near-identical applicant profiles received opposite predictions (accept/reject) — consistent with boundary instability near the threshold
- The decision threshold of 0.5 produced an acceptance rate of 34%; at 0.48 it rises to 39% — a 5-percentage-point swing from a 2-point threshold change
- One categorical feature (department) was encoded differently in 12% of records compared to training data encoding — affecting predictions for those records silently

---

## Connection to original internship work

The original admission prediction model built during the ML internship at Knowledge Solution India Limited was focused on developing and evaluating the model itself. This project asks the follow-on question: given a model like that one, what would a responsible pre-deployment audit look like? It represents the analytical discipline that should accompany model use — not just model building.
