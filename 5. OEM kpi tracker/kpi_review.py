"""
OEM Software Delivery – KPI Consistency Review
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Background: Based on analytical patterns from software delivery tracking
across seven OEM programmes at BOSCH Global Software Technologies (2023–2025).

Purpose:
    Verify whether a quarterly KPI summary dashboard is internally consistent
    and whether inter-programme comparisons are valid before figures are used
    in customer review meetings or resource planning decisions.

Design principle:
    Every flagged issue is documented with its source, the values involved,
    and the reason it requires reviewer judgement. Nothing is silently corrected.
"""

import pandas as pd
import numpy as np
import os

INPUT_LOG     = "raw_delivery_log.csv"
INPUT_SUMMARY = "kpi_summary.csv"
OUTPUT_DIR    = "output"
FLAG_FILE     = os.path.join(OUTPUT_DIR, "anomaly_flags.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load ──────────────────────────────────────────────────────────────────────
log = pd.read_csv(
    INPUT_LOG, 
    parse_dates=["planned_milestone_date", "revised_milestone_date", "actual_date", "loc_snapshot_date"]
)
summary = pd.read_csv(INPUT_SUMMARY)

for df in [log, summary]:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

print(f"Delivery log  : {log.shape[0]} rows across {log['oem_programme'].nunique()} programmes")
print(f"KPI summary   : {summary.shape[0]} rows")

flags = []

def flag(programme, issue_type, field, log_value, summary_value, note):
    flags.append({
        "oem_programme"  : programme,
        "issue_type"     : issue_type,
        "field"          : field,
        "log_value"      : log_value,
        "summary_value"  : summary_value,
        "note"           : note
    })
    print(f"  FLAG [{issue_type}] {programme}: {field}")

# ─── Check 1: Feature count reconciliation ─────────────────────────────────────
print("\nCHECK 1: Total delivered features — summary vs log")

log_total     = log[log["status"] == "delivered"]["feature_id"].nunique()
summary_total = summary["delivered_features"].sum() if "delivered_features" in summary.columns else None

if summary_total is not None:
    diff = abs(log_total - summary_total)
    if diff > 0:
        flag("ALL", "feature_count_mismatch", "delivered_features",
             log_total, summary_total,
             f"Row-level count ({log_total}) differs from summary total ({summary_total}) "
             f"by {diff}. Possible causes: version mismatch, estimated values in summary, "
             f"or features counted under different status definitions.")
    else:
        print(f"  OK: Feature count reconciles ({log_total})")

# ─── Check 2: Milestone basis consistency ──────────────────────────────────────
print("\nCHECK 2: On-time delivery basis — planned vs revised milestones")

if "milestone_type" in log.columns:
    basis_by_programme = log.groupby("oem_programme")["milestone_type"].unique()
    for prog, types in basis_by_programme.items():
        if "revised" in [t.lower() for t in types] and "planned" in [t.lower() for t in types]:
            # Both types present — check which one the OTD calculation uses
            flag(prog, "otd_basis_ambiguity", "milestone_type",
                 "mixed (planned + revised)", "not stated in summary",
                 f"Programme '{prog}' has both planned and revised milestones. "
                 f"If OTD is calculated against revised dates, it will appear better "
                 f"than a calculation against original planned dates. "
                 f"The summary does not state which basis is used.")

# ─── Check 3: Missing quarters ─────────────────────────────────────────────────
print("\nCHECK 3: Completeness — missing quarters per programme")

if "quarter" in log.columns:
    all_quarters  = sorted(log["quarter"].unique())
    all_programmes = log["oem_programme"].unique()

    for prog in all_programmes:
        present  = log[log["oem_programme"] == prog]["quarter"].unique()
        missing  = [q for q in all_quarters if q not in present]
        if missing:
            # Check if summary has values for these missing quarters
            if "oem_programme" in summary.columns and "quarter" in summary.columns:
                summary_has = summary[
                    (summary["oem_programme"] == prog) &
                    (summary["quarter"].isin(missing))
                ]
                if not summary_has.empty:
                    flag(prog, "estimated_values_in_summary", "quarter",
                         f"Missing in log: {missing}",
                         f"Present in summary: {missing}",
                         f"Programme '{prog}' has no raw data for {missing} "
                         f"but the summary shows values. These are likely estimates "
                         f"or carried-forward figures — not disclosed in summary.")

# ─── Check 4: Defect density snapshot consistency ──────────────────────────────
print("\nCHECK 4: Defect density — LOC snapshot date consistency")

if "loc_snapshot_date" in log.columns and "quarter" in log.columns:
    snapshot_by_prog = log.groupby("oem_programme")["loc_snapshot_date"].nunique()
    inconsistent = snapshot_by_prog[snapshot_by_prog > 1]
    if not inconsistent.empty:
        for prog in inconsistent.index:
            snapshots = log[log["oem_programme"] == prog]["loc_snapshot_date"].unique()
            flag(prog, "inconsistent_loc_snapshot", "loc_snapshot_date",
                 f"Multiple dates: {sorted(snapshots)}",
                 "single figure in summary",
                 f"Programme '{prog}' uses different LOC snapshot dates across quarters. "
                 f"Defect density comparisons across periods are not like-for-like.")

# ─── Check 5: Inter-programme comparison validity ──────────────────────────────
print("\nCHECK 5: Cross-programme comparison — team size normalisation")

if "team_size" in log.columns and "defect_count" in log.columns:
    # If defect counts are compared across programmes without normalising for team size,
    # the comparison is misleading. Flag programmes with substantially different team sizes.
    team_sizes = log.groupby("oem_programme")["team_size"].mean()
    max_size   = team_sizes.max()
    min_size   = team_sizes.min()
    ratio      = max_size / min_size if min_size > 0 else None

    if ratio and ratio > 2.0:
        flag("ALL", "cross_programme_comparison_invalid", "team_size",
             f"Range: {round(min_size,1)}–{round(max_size,1)}",
             "not normalised in summary",
             f"Team sizes vary by a factor of {round(ratio,1)}x across programmes. "
             f"Raw defect count comparisons are not valid without normalisation. "
             f"Summary does not note this.")

# ─── Write flag log ────────────────────────────────────────────────────────────
flag_df = pd.DataFrame(flags)
flag_df.to_csv(FLAG_FILE, index=False)
print(f"\n{len(flag_df)} issues flagged → {FLAG_FILE}")

print("\n--- REVIEW SUMMARY ---")
print(f"Total flags raised : {len(flag_df)}")
for issue_type in flag_df["issue_type"].unique():
    count = len(flag_df[flag_df["issue_type"] == issue_type])
    print(f"  {issue_type}: {count}")
print("\nAll flags logged. No values modified. Review note written separately.")
