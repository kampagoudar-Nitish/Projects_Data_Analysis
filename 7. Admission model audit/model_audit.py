"""
Student Admission Prediction – Model Audit & Input Data Review
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Background: Extends work from ML internship at Knowledge Solution India Limited
(Sep-Nov 2020), where a student admission prediction model was built and evaluated.
This project audits a model of that type before deployment.

Purpose:
    Not to rebuild the model. To audit it:
    - Are the inputs valid and within expected ranges?
    - Does the model behave consistently for near-identical profiles?
    - How sensitive is the decision boundary to small threshold changes?
    - Are there encoding mismatches between training and current data?
"""

import pandas as pd
import numpy as np
import os
from itertools import combinations

DATA_FILE  = "applicant_data.csv"
OUTPUT_DIR = "output"

INPUT_FLAGS_FILE     = os.path.join(OUTPUT_DIR, "input_flags.csv")
CONSISTENCY_FILE     = os.path.join(OUTPUT_DIR, "prediction_consistency.csv")
THRESHOLD_FILE       = os.path.join(OUTPUT_DIR, "threshold_sensitivity.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
print(f"Applicant records: {df.shape[0]} | Features: {df.shape[1]}")

input_flags = []

# ─── Check 1: Feature range validation ────────────────────────────────────────
print("\nCHECK 1: Input feature range validation")

# Define expected ranges for key features
expected_ranges = {
    "gpa"              : (0.0, 4.0),
    "test_score"       : (0, 1600),   # e.g. SAT equivalent
    "essay_score"      : (1, 10),
    "interview_score"  : (1, 10),
    "extracurricular_count" : (0, 20),
    "age"              : (17, 35),
}

for feature, (low, high) in expected_ranges.items():
    if feature not in df.columns:
        continue
    out_of_range = df[(df[feature] < low) | (df[feature] > high)]
    if not out_of_range.empty:
        print(f"  {feature}: {len(out_of_range)} records outside [{low}, {high}]")
        for idx, row in out_of_range.iterrows():
            input_flags.append({
                "applicant_id" : row.get("applicant_id", idx),
                "issue_type"   : "out_of_range",
                "feature"      : feature,
                "value"        : row[feature],
                "expected"     : f"[{low}, {high}]",
                "note"         : f"Value {row[feature]} is outside the expected range "
                                 f"for {feature}. May be a data entry error or unit mismatch."
            })
    else:
        print(f"  {feature}: OK (all within [{low}, {high}])")

# ─── Check 2: Missing values ───────────────────────────────────────────────────
print("\nCHECK 2: Missing value audit")

missing_counts = df.isnull().sum()
missing_features = missing_counts[missing_counts > 0]
if missing_features.empty:
    print("  No missing values detected.")
else:
    for feature, count in missing_features.items():
        pct = round(count / len(df) * 100, 1)
        print(f"  {feature}: {count} missing ({pct}%)")
        missing_rows = df[df[feature].isnull()]
        for idx, row in missing_rows.iterrows():
            input_flags.append({
                "applicant_id" : row.get("applicant_id", idx),
                "issue_type"   : "missing_value",
                "feature"      : feature,
                "value"        : np.nan,
                "expected"     : "non-null",
                "note"         : f"Missing {feature}. If this feature is used in the model, "
                                 f"the prediction for this record may be unreliable."
            })

# ─── Check 3: Categorical encoding consistency ─────────────────────────────────
print("\nCHECK 3: Categorical encoding consistency")

# Training encoding reference (what the model was trained on)
expected_categories = {
    "department"     : ["Engineering", "Science", "Arts", "Business", "Law"],
    "applicant_type" : ["domestic", "international"],
    "application_round" : ["Round 1", "Round 2", "Round 3"],
}

for feature, expected_vals in expected_categories.items():
    if feature not in df.columns:
        continue
    actual_vals = df[feature].dropna().unique()
    unexpected  = [v for v in actual_vals if v not in expected_vals]
    if unexpected:
        print(f"  {feature}: {len(unexpected)} unexpected values: {unexpected}")
        affected = df[df[feature].isin(unexpected)]
        for idx, row in affected.iterrows():
            input_flags.append({
                "applicant_id" : row.get("applicant_id", idx),
                "issue_type"   : "encoding_mismatch",
                "feature"      : feature,
                "value"        : row[feature],
                "expected"     : str(expected_vals),
                "note"         : f"Value '{row[feature]}' was not present in training data. "
                                 f"Model may handle this incorrectly or default to a zero encoding."
            })
    else:
        print(f"  {feature}: OK (all values match training encoding)")

# ─── Check 4: Prediction consistency for near-identical profiles ────────────────
print("\nCHECK 4: Prediction consistency — near-identical profiles")

consistency_results = []

if "prediction_prob" in df.columns and "predicted_outcome" in df.columns:
    numeric_features = ["gpa", "test_score", "essay_score", "interview_score"]
    available        = [f for f in numeric_features if f in df.columns]

    # Find pairs with very similar numeric profiles but different outcomes
    # Sample approach: bin features and compare within bins
    if available:
        df_sample = df.dropna(subset=available + ["predicted_outcome"]).head(200)

        for feat in available:
            df_sample[f"{feat}_bin"] = pd.qcut(df_sample[feat], q=5, duplicates="drop", labels=False)

        bin_cols = [f"{f}_bin" for f in available]
        grouped  = df_sample.groupby(bin_cols)

        for name, group in grouped:
            if len(group) < 2:
                continue
            outcomes = group["predicted_outcome"].unique()
            if len(outcomes) > 1:
                # Mixed outcomes in same bin — worth flagging
                for idx1, idx2 in list(combinations(group.index, 2))[:3]:
                    r1, r2 = group.loc[idx1], group.loc[idx2]
                    if r1["predicted_outcome"] != r2["predicted_outcome"]:
                        consistency_results.append({
                            "applicant_1"      : r1.get("applicant_id", idx1),
                            "applicant_2"      : r2.get("applicant_id", idx2),
                            "outcome_1"        : r1["predicted_outcome"],
                            "outcome_2"        : r2["predicted_outcome"],
                            "prob_1"           : round(r1["prediction_prob"], 3),
                            "prob_2"           : round(r2["prediction_prob"], 3),
                            "note"             : "Near-identical profiles by binned features "
                                                 "with different predicted outcomes. "
                                                 "Likely near decision boundary."
                        })

    consistency_df = pd.DataFrame(consistency_results)
    consistency_df.to_csv(CONSISTENCY_FILE, index=False)
    print(f"  {len(consistency_df)} near-identical pairs with divergent predictions → {CONSISTENCY_FILE}")

# ─── Check 5: Threshold sensitivity ───────────────────────────────────────────
print("\nCHECK 5: Threshold sensitivity analysis")

threshold_results = []
if "prediction_prob" in df.columns:
    for thresh in [round(t, 2) for t in np.arange(0.40, 0.61, 0.02)]:
        accepted   = (df["prediction_prob"] >= thresh).sum()
        accept_pct = round(accepted / len(df) * 100, 1)
        threshold_results.append({
            "threshold"    : thresh,
            "accepted"     : accepted,
            "rejected"     : len(df) - accepted,
            "accept_rate_pct" : accept_pct
        })
        print(f"  Threshold {thresh}: {accepted} accepted ({accept_pct}%)")

    thresh_df = pd.DataFrame(threshold_results)
    thresh_df.to_csv(THRESHOLD_FILE, index=False)

# ─── Write input flags ─────────────────────────────────────────────────────────
flag_df = pd.DataFrame(input_flags)
flag_df.to_csv(INPUT_FLAGS_FILE, index=False)

print(f"\n--- AUDIT SUMMARY ---")
print(f"Input flags raised       : {len(flag_df)}")
print(f"  Out of range           : {len(flag_df[flag_df['issue_type']=='out_of_range'])}")
print(f"  Missing values         : {len(flag_df[flag_df['issue_type']=='missing_value'])}")
print(f"  Encoding mismatches    : {len(flag_df[flag_df['issue_type']=='encoding_mismatch'])}")
print(f"Consistency flags        : {len(consistency_results)}")
print(f"\nSee audit_note.md for findings and recommended actions before deployment.")
