# Anomaly & Inconsistency Detection in Structured Tables

A lightweight Python tool for identifying values in structured datasets that are statistically unusual, internally inconsistent, or out of step with the surrounding context, without assuming the analyst already knows what they are looking for.

## The distinction this tool makes

Most anomaly detection is about outliers. This tool is also about **inconsistencies**, cases where a value may not be statistically extreme but is inconsistent with related values in the same record, or with what the same column looks like across similar records.

Examples of what this catches:
- A revenue figure that is 40× the median for that region but within the global range
- A date that is valid on its own but precedes the record's creation date
- A unit price that, when multiplied by quantity, does not match the stated line total
- A categorical field that changes value for a record where it should be fixed
- A percentage column where values across a row sum to 108% rather than 100%

## Detection methods

| Method | What it catches |
|---|---|
| IQR-based flagging | Statistical outliers per column |
| Z-score (optional) | Values far from column mean |
| Cross-field arithmetic check | e.g. unit × qty ≠ total |
| Temporal logic check | Date ordering violations |
| Row-sum validation | % or allocation columns not summing to expected total |
| Peer comparison | Value far from median of similar records (by group) |

## Output

All detected anomalies are written to a structured log with:
- The record identifier
- The field(s) involved
- The detection method that flagged it
- The expected or typical value (where calculable)
- A plain-language description of the issue

The tool does not remove or correct anomalies. It flags them for human review.

## Files

```
04_anomaly_detection_tool/
├── detector.py
├── config.yaml         # Which checks to run, thresholds, group-by columns
├── sample_data/
│   └── sample_records.csv
├── outputs/
│   └── anomaly_log.csv
└── README.md
```

## Design principle

The tool is deliberately conservative. A false positive that prompts a human to check something is better than a missed inconsistency that goes unnoticed. The output is designed to be reviewed by an analyst, not acted on automatically.

## Skills demonstrated

- Thinking about data quality beyond simple outlier detection
- Cross-field validation logic
- Configurable, auditable flagging (not hard-coded thresholds)
- Designing for human review as the final step
