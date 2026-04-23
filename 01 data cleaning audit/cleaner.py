"""
Data Cleaning & Audit Pipeline
JHC Consulting – Portfolio Project
Author: Nitish Kampagoudar
"""

import pandas as pd
import yaml
import argparse
import os
from datetime import datetime


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def log_action(audit_log: list, row_idx, column: str, original_value, action: str, reason: str):
    audit_log.append({
        "timestamp": datetime.now().isoformat(),
        "row_index": row_idx,
        "column": column,
        "original_value": original_value,
        "action": action,
        "reason": reason
    })


def check_missing_values(df: pd.DataFrame, audit_log: list) -> pd.DataFrame:
    """Flag and report missing values. Do not silently drop or fill."""
    missing = df.isnull()
    for col in df.columns:
        missing_rows = df[missing[col]].index.tolist()
        for idx in missing_rows:
            log_action(audit_log, idx, col, None, "FLAGGED_MISSING", "Value is null/empty")
    return df


def check_duplicates(df: pd.DataFrame, audit_log: list) -> pd.DataFrame:
    """Identify and flag exact duplicate rows."""
    duplicated_mask = df.duplicated(keep="first")
    duplicate_indices = df[duplicated_mask].index.tolist()
    for idx in duplicate_indices:
        log_action(audit_log, idx, "ALL_COLUMNS", df.loc[idx].to_dict(),
                   "FLAGGED_DUPLICATE", "Exact duplicate of an earlier row")
    if duplicate_indices:
        df = df[~duplicated_mask].copy()
    return df


def normalise_categories(df: pd.DataFrame, config: dict, audit_log: list) -> pd.DataFrame:
    """Standardise known category variants using config mapping."""
    mappings = config.get("category_mappings", {})
    for col, mapping in mappings.items():
        if col not in df.columns:
            continue
        for idx, val in df[col].items():
            if pd.isna(val):
                continue
            normalised = mapping.get(str(val).strip().lower())
            if normalised and str(val).strip() != normalised:
                log_action(audit_log, idx, col, val, f"NORMALISED → {normalised}",
                           "Category variant standardised per config mapping")
                df.at[idx, col] = normalised
    return df


def check_numeric_ranges(df: pd.DataFrame, config: dict, audit_log: list) -> pd.DataFrame:
    """Flag values outside expected numeric ranges defined in config."""
    ranges = config.get("numeric_ranges", {})
    for col, bounds in ranges.items():
        if col not in df.columns:
            continue
        min_val = bounds.get("min")
        max_val = bounds.get("max")
        for idx, val in df[col].items():
            if pd.isna(val):
                continue
            try:
                num = float(val)
            except (ValueError, TypeError):
                log_action(audit_log, idx, col, val, "FLAGGED_TYPE_ERROR",
                           f"Expected numeric value, got: {type(val).__name__}")
                continue
            if min_val is not None and num < min_val:
                log_action(audit_log, idx, col, val, "FLAGGED_BELOW_MIN",
                           f"Value {num} is below configured minimum {min_val}")
            if max_val is not None and num > max_val:
                log_action(audit_log, idx, col, val, "FLAGGED_ABOVE_MAX",
                           f"Value {num} is above configured maximum {max_val}")
    return df


def run_pipeline(input_path: str, config_path: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    config = load_config(config_path)
    audit_log = []

    print("Step 1: Checking missing values...")
    df = check_missing_values(df, audit_log)

    print("Step 2: Checking for duplicates...")
    df = check_duplicates(df, audit_log)

    print("Step 3: Normalising categories...")
    df = normalise_categories(df, config, audit_log)

    print("Step 4: Checking numeric ranges...")
    df = check_numeric_ranges(df, config, audit_log)

    # Write outputs
    clean_path = os.path.join(output_dir, "cleaned_data.csv")
    audit_path = os.path.join(output_dir, "audit_log.csv")

    df.to_csv(clean_path, index=False)
    pd.DataFrame(audit_log).to_csv(audit_path, index=False)

    print(f"\nDone.")
    print(f"  Cleaned data → {clean_path}")
    print(f"  Audit log    → {audit_path} ({len(audit_log)} entries)")

    if not audit_log:
        print("  Note: Audit log is empty — no issues detected or changes made.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Cleaning & Audit Pipeline")
    parser.add_argument("--input", required=True, help="Path to raw CSV input")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    args = parser.parse_args()

    run_pipeline(args.input, args.config, args.output_dir)
