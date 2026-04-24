"""
International Trade Dataset – Structural Review & Gap Analysis
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Background: MBA in International Trade, Hochschule Anhalt.
Module: International Economic Theory and Policy (grade 1.7),
        Economic Statistics & Empirical Methods (grade 1.3)

Purpose:
    Review a synthetic international trade dataset for structural
    inconsistencies before it is used in country-level trade analysis.
    The key questions:
      - Are HS codes valid and consistently formatted?
      - Do bilateral trade figures reconcile (mirror statistics)?
      - Have figures from different periods been combined without disclosure?
      - Are any values implausible relative to country-level context?
"""

import pandas as pd
import numpy as np
import os

TRADE_FILE = "raw_trade_data.csv"
HS_FILE    = "hs_reference.csv"
OUTPUT_DIR = "output"
FLAG_FILE  = os.path.join(OUTPUT_DIR, "flagged_records.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load ──────────────────────────────────────────────────────────────────────
trade = pd.read_csv(TRADE_FILE)
hs_ref = pd.read_csv(HS_FILE)

trade.columns  = [c.strip().lower().replace(" ", "_") for c in trade.columns]
hs_ref.columns = [c.strip().lower().replace(" ", "_") for c in hs_ref.columns]

print(f"Trade records : {trade.shape[0]} rows | "
      f"{trade['reporting_country'].nunique()} countries | "
      f"{trade['year'].nunique()} years")

flags = []

def flag(idx, reporter, partner, year, issue, field, value, note):
    flags.append({
        "record_index"      : idx,
        "reporting_country" : reporter,
        "partner_country"   : partner,
        "year"              : year,
        "issue_type"        : issue,
        "field"             : field,
        "value"             : value,
        "note"              : note
    })

# ─── Check 1: HS code format validation ───────────────────────────────────────
print("\nCHECK 1: HS code format validation")

if "hs_code" in trade.columns:
    # HS codes should be exactly 6 digits (numeric)
    def valid_hs(code):
        try:
            s = str(int(code)).zfill(6)
            return len(s) == 6
        except (ValueError, TypeError):
            return False

    invalid_hs = trade[~trade["hs_code"].apply(valid_hs)]
    print(f"  Invalid HS codes: {len(invalid_hs)}")

    for idx, row in invalid_hs.iterrows():
        flag(idx, row.get("reporting_country"), row.get("partner_country"),
             row.get("year"), "invalid_hs_code", "hs_code", row["hs_code"],
             f"HS code '{row['hs_code']}' is not a valid 6-digit code. "
             f"Product category attribution may be incorrect.")

# ─── Check 2: Mirror statistics gap ───────────────────────────────────────────
print("\nCHECK 2: Mirror statistics — export vs import reconciliation")

# For each country pair A→B, compare A's reported exports with B's reported imports from A
if all(c in trade.columns for c in ["reporting_country", "partner_country", "trade_value_usd", "flow_type", "year"]):

    exports = trade[trade["flow_type"] == "export"].copy()
    imports = trade[trade["flow_type"] == "import"].copy()

    # Merge: A's exports to B with B's imports from A
    merged = exports.merge(
        imports,
        left_on=["reporting_country", "partner_country", "year"],
        right_on=["partner_country", "reporting_country", "year"],
        suffixes=("_export", "_import")
    )

    if not merged.empty:
        merged["mirror_gap_pct"] = (
            abs(merged["trade_value_usd_export"] - merged["trade_value_usd_import"])
            / merged["trade_value_usd_export"] * 100
        ).round(1)

        avg_gap = merged["mirror_gap_pct"].mean()
        print(f"  Average mirror statistics gap: {round(avg_gap, 1)}%")

        # Flag pairs with gap > 15% (unusual; warrants investigation)
        large_gaps = merged[merged["mirror_gap_pct"] > 15]
        print(f"  Country pairs with gap > 15%: {len(large_gaps)}")
        for _, row in large_gaps.iterrows():
            flag(
                row.name,
                row["reporting_country_export"],
                row["partner_country_export"],
                row["year"],
                "large_mirror_statistics_gap",
                "trade_value_usd",
                f"{row['trade_value_usd_export']} vs {row['trade_value_usd_import']}",
                f"Gap of {row['mirror_gap_pct']}% between export and import reporting. "
                f"Possible causes: re-exports, CIF/FOB valuation differences, "
                f"timing differences, or data error. Investigate before citing."
            )

# ─── Check 3: Period mixing ────────────────────────────────────────────────────
print("\nCHECK 3: Reporting period consistency")

if "reporting_date" in trade.columns and "year" in trade.columns:
    trade["reporting_year"] = pd.to_datetime(
        trade["reporting_date"], errors="coerce"
    ).dt.year

    mixed_periods = trade[trade["reporting_year"] != trade["year"]]
    print(f"  Records where reporting date year ≠ stated year: {len(mixed_periods)}")

    for idx, row in mixed_periods.iterrows():
        flag(idx, row.get("reporting_country"), row.get("partner_country"),
             row.get("year"), "period_mismatch", "reporting_date / year",
             f"year={row['year']}, reporting_date={row['reporting_date']}",
             "Data for this record was reported in a different year from the "
             "stated trade year. May indicate revised estimates included without disclosure.")

# ─── Check 4: Implausible trade values ────────────────────────────────────────
print("\nCHECK 4: Plausibility check — trade value vs GDP")

if "trade_value_usd" in trade.columns and "exporter_gdp_usd" in trade.columns:
    # A bilateral trade flow exceeding 50% of exporter GDP is unusual for a single category
    trade["value_to_gdp_pct"] = trade["trade_value_usd"] / trade["exporter_gdp_usd"] * 100
    implausible = trade[trade["value_to_gdp_pct"] > 50]
    print(f"  Implausible trade values (>50% of exporter GDP): {len(implausible)}")

    for idx, row in implausible.iterrows():
        flag(idx, row.get("reporting_country"), row.get("partner_country"),
             row.get("year"), "implausible_value", "trade_value_usd",
             round(row["value_to_gdp_pct"], 1),
             f"Trade value is {round(row['value_to_gdp_pct'],1)}% of exporter GDP. "
             f"Possible re-export misattribution, data entry error, or unit inconsistency (USD vs '000 USD).")

# ─── Write flags ───────────────────────────────────────────────────────────────
flag_df = pd.DataFrame(flags)
flag_df.to_csv(FLAG_FILE, index=False)

print(f"\n{len(flag_df)} records flagged → {FLAG_FILE}")
print("\n--- REVIEW SUMMARY ---")
for issue in flag_df["issue_type"].unique():
    print(f"  {issue}: {len(flag_df[flag_df['issue_type']==issue])}")
print("\nAll flagged records retained. No values modified. See analytical_note.md.")
