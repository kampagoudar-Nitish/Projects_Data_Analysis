"""
Sales Report Consistency Check
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Verifies whether a management sales summary is supported by its
underlying transaction data. Does not produce charts. Produces
a structured discrepancy report.
"""

import pandas as pd
import numpy as np
import os

RAW_FILE     = "raw_sales_data.csv"
SUMMARY_FILE = "summary_report.csv"
OUTPUT_DIR   = "output"
DISC_FILE    = os.path.join(OUTPUT_DIR, "discrepancies.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load both files ───────────────────────────────────────────────────────────
raw     = pd.read_csv(RAW_FILE, parse_dates=["transaction_date"])
summary = pd.read_csv(SUMMARY_FILE)

raw.columns     = [c.strip().lower().replace(" ", "_") for c in raw.columns]
summary.columns = [c.strip().lower().replace(" ", "_") for c in summary.columns]

discrepancies = []

def flag(issue_type, field, summary_val, computed_val, note):
    diff = round(computed_val - summary_val, 2) if isinstance(summary_val, (int, float)) else "N/A"
    discrepancies.append({
        "issue_type"    : issue_type,
        "field"         : field,
        "summary_value" : summary_val,
        "computed_value": computed_val,
        "difference"    : diff,
        "note"          : note
    })
    print(f"  FLAGGED [{issue_type}]: {field} | Summary={summary_val} | Computed={computed_val}")

# ─── Check 1: Regional totals ──────────────────────────────────────────────────
print("CHECK 1: Regional revenue totals")
regional_computed = (
    raw.groupby("region")["revenue"]
    .sum()
    .reset_index()
    .rename(columns={"revenue": "computed_revenue"})
)

# Load expected regional figures from summary
# Assumes summary has columns: region, total_revenue
if "region" in summary.columns and "total_revenue" in summary.columns:
    merged = summary.merge(regional_computed, on="region", how="left")
    for _, row in merged.iterrows():
        diff = abs(row["computed_revenue"] - row["total_revenue"])
        if diff > 100:  # tolerance: €100
            flag(
                "regional_total_mismatch",
                f"revenue | region={row['region']}",
                row["total_revenue"],
                round(row["computed_revenue"], 2),
                f"Summary and row-level totals differ by {round(diff, 2)}. "
                f"Investigate before citing."
            )
        else:
            print(f"  OK: {row['region']} — within tolerance (diff={round(diff,2)})")

# ─── Check 2: Category consistency across periods ──────────────────────────────
print("\nCHECK 2: Product category consistency across years")
if "product_category" in raw.columns and "year" in raw.columns:
    cat_by_year = (
        raw.groupby(["product_category", "year"])["revenue"]
        .sum()
        .unstack(fill_value=0)
    )
    # Check for categories that appear in one year but not another
    years = raw["year"].unique()
    if len(years) >= 2:
        yr1, yr2 = sorted(years)[:2]
        cats_yr1 = set(raw[raw["year"] == yr1]["product_category"].unique())
        cats_yr2 = set(raw[raw["year"] == yr2]["product_category"].unique())
        only_yr1 = cats_yr1 - cats_yr2
        only_yr2 = cats_yr2 - cats_yr1
        if only_yr1:
            flag("category_disappears", "product_category", f"Present in {yr1}", f"Absent in {yr2}",
                 f"Categories {only_yr1} appear in {yr1} but not {yr2}. Check if renamed or discontinued.")
        if only_yr2:
            flag("category_appears", "product_category", f"Absent in {yr1}", f"Present in {yr2}",
                 f"Categories {only_yr2} appear in {yr2} but not {yr1}. Check if new or renamed.")

# ─── Check 3: Grand total reconciliation ──────────────────────────────────────
print("\nCHECK 3: Grand total reconciliation")
row_level_total = raw["revenue"].sum()
if "total_revenue" in summary.columns:
    summary_total = summary["total_revenue"].sum()
    diff = abs(row_level_total - summary_total)
    if diff > 500:
        flag("grand_total_mismatch", "total_revenue",
             round(summary_total, 2), round(row_level_total, 2),
             f"Grand total differs by {round(diff, 2)}. Source of discrepancy unclear.")
    else:
        print(f"  OK: Grand total within tolerance (diff={round(diff,2)})")

# ─── Check 4: Rounding consistency ────────────────────────────────────────────
print("\nCHECK 4: Checking for rounding accumulation")
# If summary rounds each row before summing, the total may drift
if "total_revenue" in summary.columns:
    sum_of_rounded = summary["total_revenue"].apply(lambda x: round(x, 0)).sum()
    actual_sum     = summary["total_revenue"].sum()
    rounding_drift = abs(sum_of_rounded - actual_sum)
    if rounding_drift > 10:
        flag("rounding_drift", "total_revenue",
             round(actual_sum, 2), round(sum_of_rounded, 2),
             f"Rounding before summing creates a drift of {round(rounding_drift,2)}.")
    else:
        print(f"  OK: Rounding drift within tolerance ({round(rounding_drift,2)})")

# ─── Write discrepancy report ──────────────────────────────────────────────────
disc_df = pd.DataFrame(discrepancies)
disc_df.to_csv(DISC_FILE, index=False)
print(f"\n{len(disc_df)} discrepancies written to {DISC_FILE}")
print("\nNote: All discrepancies require reviewer judgement before any treatment is applied.")
