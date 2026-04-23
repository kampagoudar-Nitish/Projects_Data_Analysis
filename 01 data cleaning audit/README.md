# Data Cleaning & Audit Pipeline

A structured Python workflow for cleaning, validating and auditing raw datasets before analysis. Designed around the principle that reliable analysis begins with reliable inputs.

## What this does

Takes a raw CSV (e.g. from a spreadsheet export, survey tool or operational system) and:

1. Detects and flags missing values by column and row
2. Identifies duplicate records (exact and near-duplicate)
3. Checks for category inconsistencies (e.g. "UK" vs "United Kingdom" vs "u.k.")
4. Validates numeric ranges against user-defined thresholds
5. Flags rows where figures appear implausible given the surrounding data
6. Outputs a clean working file and a separate **audit log** documenting every change made

The audit log is the point. Every transformation is recorded with the original value, the action taken, and the reason — so the cleaned output can be checked and challenged, not just trusted.

## Why this exists

Most data cleaning tutorials focus on getting to a clean file quickly. This project focuses on **accountability** — making the cleaning process itself transparent and reviewable.

## Files

```
01_data_cleaning_audit/
├── cleaner.py          # Main cleaning and audit logic
├── config.yaml         # Column types, expected ranges, category mappings
├── sample_data/
│   ├── raw_input.csv   # Example messy dataset (synthetic)
│   └── expected_output.csv
├── outputs/
│   ├── cleaned_data.csv
│   └── audit_log.csv
└── tests/
    └── test_cleaner.py
```

## Usage

```bash
pip install -r requirements.txt
python cleaner.py --input sample_data/raw_input.csv --config config.yaml
```

Outputs are written to `/outputs/`. The audit log is always generated, even if no changes were made (a null audit log is itself informative).

## Skills demonstrated

- Structured data handling in Python (pandas)
- Systematic approach to data quality
- Audit-trail thinking — not just cleaning, but documenting cleaning
- Attention to detail in edge cases (whitespace, encoding issues, mixed types)

## Notes

Sample data is fully synthetic and does not represent any real individuals or organisations.
