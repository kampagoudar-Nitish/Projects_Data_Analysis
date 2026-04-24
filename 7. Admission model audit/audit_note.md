# Audit Note – Student Admission Prediction Model

**Prepared by:** Nitish Kampagoudar  
**Status:** Pre-deployment review — findings require action before model is used in current admissions cycle

---

## Purpose of this audit

This note documents the findings from a pre-deployment audit of the student admission prediction model. The audit covers input data quality, prediction consistency, and decision threshold sensitivity. It does not assess whether the model's underlying methodology is appropriate — that is a separate question. It addresses whether, given the model that exists, the current data and configuration make it safe to use as an admissions support tool.

---

## Input data findings

### Out-of-range values (8.4% of records affected)
The most common issue is GPA values above 4.0 on a 4.0 scale. There are also test score entries above the stated maximum. These are likely data entry errors — a GPA of 4.3 or a test score of 1,680 on a 1,600-point scale should not exist. The model will still produce predictions for these records, but those predictions are based on input values it was not trained on. These records should be corrected or excluded before the model is run.

### Missing values
Eleven records have no interview score. If interview score is a feature in the model, predictions for these records are unreliable. The model likely defaults to a zero or mean imputation, but this is not documented and may not be the intended behaviour. These records should be handled explicitly before use.

### Encoding mismatches
Twelve percent of records have a department value that was not present in the training data. Specifically, "Natural Sciences" appears in the current data but was not a category during training. The model's handling of this is not documented. These records should be re-mapped to the closest training category (likely "Science") or excluded, with the remapping decision documented.

---

## Prediction consistency findings

Fourteen pairs of near-identical applicant profiles (matched by binned GPA, test score, essay score, and interview score) received opposite predicted outcomes. This is expected near the decision boundary, applicants close to the threshold will sometimes fall on different sides due to minor differences in other features. However, the volume of boundary cases is high enough that it warrants a review of whether the current threshold is set appropriately.

---

## Threshold sensitivity findings

The model is currently configured with a decision threshold of 0.5. At this threshold, 34% of applicants are predicted as admit. At a threshold of 0.48, that rises to 39% — a five-percentage-point change from a two-point threshold adjustment. The team should be aware of this sensitivity and should document the basis for the chosen threshold (whether it is based on historical admit rates, capacity targets, or simply left at the default). A threshold that is not explicitly chosen is not a neutral decision.

---

## Recommended actions before deployment

1. Correct or exclude the 42 records with out-of-range input values
2. Decide how to handle missing interview scores — do not rely on silent default imputation
3. Remap or exclude the 12% of records with unrecognised department values; document the mapping
4. Review the decision threshold and document the basis for the chosen value
5. Flag boundary cases (prediction probability between 0.45 and 0.55) for human review rather than automatic decision

---

## What this audit does not cover

This audit does not assess whether the model's features are fair proxies for academic potential, whether the training data reflects the current applicant pool, or whether the model's overall accuracy is sufficient for the use case. These are important questions but they require a different kind of review, one that goes beyond data quality and into model design and validation methodology.
