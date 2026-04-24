"""
Insurance Risk Dataset – Data Cleaning Pipeline
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Purpose:
    Clean and validate a synthetic raw insurance dataset before it enters
    any analytical workflow. The goal is to ensure that figures, categories
    and date fields are internally consistent and that anomalies are logged
    rather than silently dropped.

Design note:
    This script is intentionally verbose in its comments. In an advisory
    context, every cleaning decision needs to be traceable and defensible.
    An analyst who cannot explain why they made a change has not done the
    work properly.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ─── Configuration ────────────────────────────────────────────────────────────

INPUT_FILE  = "raw_insurance_data.csv"
OUTPUT_DIR  = "output"
LOG_FILE    = os.path.join(OUTPUT_DIR, "anomaly_log.csv")
CLEAN_FILE  = os.path.join(OUTPUT_DIR, "cleaned_output.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Step 1: Load & initial inspection ────────────────────────────────────────

print("=" * 60)
print("STEP 1: Loading raw data and initial inspection")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumns:\n{list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing value counts:\n{df.isnull().sum()}")

# ─── Step 2: Standardise column names ─────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 2: Standardising column names")
print("=" * 60)

# Strip whitespace and enforce lowercase with underscores
original_cols = df.columns.tolist()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

renamed = {o: n for o, n in zip(original_cols, df.columns) if o != n}
if renamed:
    print(f"Renamed columns: {renamed}")
else:
    print("No column renaming required.")

# ─── Step 3: Category consistency audit ───────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 3: Category consistency – product_type field")
print("=" * 60)

# Log what exists before cleaning
raw_categories = df["product_type"].value_counts(dropna=False)
print(f"\nRaw product_type values:\n{raw_categories}")

# Normalise: strip whitespace, title-case, consolidate known variants
category_map = {
    "motor"          : "Motor Vehicle",
    "motor vehicle"  : "Motor Vehicle",
    "Motor"          : "Motor Vehicle",
    "property"       : "Property",
    "Property ins."  : "Property",
    "life"           : "Life",
    "Life ins"       : "Life",
    "health"         : "Health",
    "Health Insurance": "Health",
}

df["product_type_raw"] = df["product_type"].copy()  # preserve original
df["product_type"] = (
    df["product_type"]
    .str.strip()
    .map(lambda x: category_map.get(x, x))
)

cleaned_categories = df["product_type"].value_counts(dropna=False)
print(f"\nCleaned product_type values:\n{cleaned_categories}")

# ─── Step 4: Numeric field validation ─────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 4: Numeric validation – claim_amount, premium, sum_insured")
print("=" * 60)

anomaly_rows = []

# 4a. Negative claim amounts
neg_claims = df[df["claim_amount"] < 0]
if not neg_claims.empty:
    print(f"\nFlagged: {len(neg_claims)} rows with negative claim_amount")
    for idx, row in neg_claims.iterrows():
        anomaly_rows.append({
            "row_index"   : idx,
            "policy_id"   : row.get("policy_id", "N/A"),
            "issue_type"  : "negative_claim_amount",
            "field"       : "claim_amount",
            "value"       : row["claim_amount"],
            "action"      : "flagged – not modified",
            "note"        : "Negative claim amount is not plausible; "
                            "requires source verification before any treatment."
        })

# 4b. Claim exceeds sum insured
excess_claims = df[df["claim_amount"] > df["sum_insured"]]
if not excess_claims.empty:
    print(f"Flagged: {len(excess_claims)} rows where claim_amount > sum_insured")
    for idx, row in excess_claims.iterrows():
        anomaly_rows.append({
            "row_index"   : idx,
            "policy_id"   : row.get("policy_id", "N/A"),
            "issue_type"  : "claim_exceeds_sum_insured",
            "field"       : "claim_amount / sum_insured",
            "value"       : f"{row['claim_amount']} / {row['sum_insured']}",
            "action"      : "flagged – not modified",
            "note"        : "Claim amount exceeds policy sum insured. "
                            "May indicate data entry error or reinsurance recovery. "
                            "Decision on treatment rests with reviewer."
        })

# 4c. Missing premium — document and tag, do not impute silently
missing_premium = df[df["premium"].isnull()]
if not missing_premium.empty:
    print(f"Flagged: {len(missing_premium)} rows with missing premium")
    df.loc[df["premium"].isnull(), "premium_status"] = "missing – unimputed"
    df.loc[df["premium"].notnull(), "premium_status"] = "present"
    for idx, row in missing_premium.iterrows():
        anomaly_rows.append({
            "row_index"   : idx,
            "policy_id"   : row.get("policy_id", "N/A"),
            "issue_type"  : "missing_premium",
            "field"       : "premium",
            "value"       : np.nan,
            "action"      : "flagged – tagged with premium_status column",
            "note"        : "Missing premium. Imputation not applied without "
                            "justification. Rows included in cleaned file with tag."
        })

# ─── Step 5: Date field validation ────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 5: Date field validation – policy_start, policy_end, claim_date")
print("=" * 60)

for date_col in ["policy_start", "policy_end", "claim_date"]:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        unparseable = df[df[date_col].isnull()][date_col].count()
        print(f"  {date_col}: {unparseable} unparseable values → set to NaT")

# Flag where claim_date is before policy_start
if "claim_date" in df.columns and "policy_start" in df.columns:
    impossible_dates = df[df["claim_date"] < df["policy_start"]]
    if not impossible_dates.empty:
        print(f"Flagged: {len(impossible_dates)} rows where claim_date < policy_start")
        for idx, row in impossible_dates.iterrows():
            anomaly_rows.append({
                "row_index"   : idx,
                "policy_id"   : row.get("policy_id", "N/A"),
                "issue_type"  : "impossible_date_sequence",
                "field"       : "claim_date / policy_start",
                "value"       : f"{row['claim_date']} / {row['policy_start']}",
                "action"      : "flagged – not modified",
                "note"        : "Claim date precedes policy start. "
                                "Possible backdating or data entry error."
            })

# ─── Step 6: Write anomaly log ─────────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 6: Writing anomaly log")
print("=" * 60)

anomaly_df = pd.DataFrame(anomaly_rows)
anomaly_df.to_csv(LOG_FILE, index=False)
print(f"Anomaly log: {len(anomaly_df)} rows written to {LOG_FILE}")

# ─── Step 7: Write cleaned output ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 7: Writing cleaned output")
print("=" * 60)

df.to_csv(CLEAN_FILE, index=False)
print(f"Cleaned file: {df.shape[0]} rows written to {CLEAN_FILE}")

# ─── Summary ──────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
total_issues = len(anomaly_df)
pct_affected = round(total_issues / len(df) * 100, 1) if len(df) > 0 else 0
print(f"Total rows in raw file   : {len(df)}")
print(f"Total anomalies flagged  : {total_issues} ({pct_affected}% of rows)")
print(f"Anomaly log              : {LOG_FILE}")
print(f"Cleaned output           : {CLEAN_FILE}")
print("\nNote: All anomalous rows are retained in the cleaned file.")
print("Flagging decisions are documented. Treatment decisions are not made")
print("unilaterally — they are passed to the reviewer for judgement.")
