"""
Supplier Quality Audit – Review & Inconsistency Detection
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

This script processes a synthetic supplier quality audit dataset.
The goal is not to produce a summary chart. It is to verify whether
the data is internally consistent before it is used in any management
review or benchmarking exercise.

Every decision in this script is documented so it can be audited.
"""

import pandas as pd
import numpy as np
import os

INPUT_FILE = "raw_supplier_data.csv"
OUTPUT_DIR = "output"
CLEAN_FILE = os.path.join(OUTPUT_DIR, "cleaned_suppliers.csv")
GAP_FILE   = os.path.join(OUTPUT_DIR, "gap_report.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE)
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}\n")

# ─── Column standardisation ────────────────────────────────────────────────────
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# ─── Supplier tier normalisation ───────────────────────────────────────────────
# Multiple labels observed for the same tier in raw data.
tier_map = {
    "tier 1" : "Tier 1", "t1"     : "Tier 1", "tier-1" : "Tier 1",
    "tier 2" : "Tier 2", "t2"     : "Tier 2", "tier-2" : "Tier 2",
    "tier 3" : "Tier 3", "t3"     : "Tier 3", "tier-3" : "Tier 3",
}
df["supplier_tier_raw"] = df["supplier_tier"].copy()
df["supplier_tier"] = df["supplier_tier"].str.strip().str.lower().map(
    lambda x: tier_map.get(x, x)
)

unmapped = df[~df["supplier_tier"].isin(["Tier 1", "Tier 2", "Tier 3"])]
if not unmapped.empty:
    print(f"WARNING: {len(unmapped)} rows with unrecognised tier labels:")
    print(unmapped[["supplier_id", "supplier_tier"]].value_counts(), "\n")

# ─── Defect rate validation ────────────────────────────────────────────────────
# Flag: defect_rate_pct should be between 0 and 100.
invalid_defect = df[(df["defect_rate_pct"] < 0) | (df["defect_rate_pct"] > 100)]
print(f"Flagged: {len(invalid_defect)} rows with defect_rate_pct outside [0, 100]")

# Flag: suppliers reporting exactly 0 defects for every quarter.
# This is possible but statistically uncommon; flag for confirmation.
zero_defect_suppliers = (
    df.groupby("supplier_id")["defect_rate_pct"]
    .apply(lambda x: (x == 0).all())
)
all_zero = zero_defect_suppliers[zero_defect_suppliers].index.tolist()
print(f"Flagged: {len(all_zero)} suppliers with zero defects in ALL quarters → {all_zero}")
df["all_zero_defect_flag"] = df["supplier_id"].isin(all_zero)

# ─── Delivery figure reconciliation ───────────────────────────────────────────
# The summary report states aggregate on-time delivery = 94.3%.
# Check against row-level data.
reported_otd  = 94.3
computed_otd  = df["on_time_delivery_pct"].mean()
discrepancy   = abs(reported_otd - computed_otd)
print(f"\nOTD reconciliation:")
print(f"  Reported (summary): {reported_otd}%")
print(f"  Computed (row avg): {round(computed_otd, 2)}%")
print(f"  Discrepancy       : {round(discrepancy, 2)} pp")
if discrepancy > 1.0:
    print("  STATUS: DISCREPANCY > 1 pp — documented for reviewer.")

# ─── Gap analysis: missing quarters ───────────────────────────────────────────
# Each supplier should have a record for every quarter in the dataset.
all_quarters  = df["quarter"].unique()
all_suppliers = df["supplier_id"].unique()

gap_rows = []
for supplier in all_suppliers:
    present = df[df["supplier_id"] == supplier]["quarter"].tolist()
    missing = [q for q in all_quarters if q not in present]
    if missing:
        gap_rows.append({
            "supplier_id"      : supplier,
            "missing_quarters" : ", ".join(str(q) for q in sorted(missing)),
            "count_missing"    : len(missing)
        })

gap_df = pd.DataFrame(gap_rows)
gap_df.to_csv(GAP_FILE, index=False)
print(f"\nGap report: {len(gap_df)} suppliers with missing quarters → {GAP_FILE}")

# ─── Write cleaned output ──────────────────────────────────────────────────────
df.to_csv(CLEAN_FILE, index=False)
print(f"Cleaned file: {df.shape[0]} rows → {CLEAN_FILE}")

# ─── Summary ──────────────────────────────────────────────────────────────────
print("\n--- REVIEW SUMMARY ---")
print(f"Tier normalisation     : applied (variants consolidated, {len(unmapped)} unmapped)")
print(f"Invalid defect rates   : {len(invalid_defect)} flagged")
print(f"All-zero defect flag   : {len(all_zero)} suppliers")
print(f"OTD discrepancy        : {round(discrepancy, 2)} pp (>{1.0} pp = requires investigation)")
print(f"Suppliers with gaps    : {len(gap_df)}")
print("\nAll anomalies retained in cleaned file. Treatment decisions are for the reviewer.")
