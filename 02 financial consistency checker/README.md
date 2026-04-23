# Financial Consistency Checker

A SQL and Python tool for verifying whether figures in a financial summary or report are internally consistent with the underlying source data.

## The problem this solves

Summaries and reports frequently contain figures that do not match their source material, not through deliberate misrepresentation, but because totals are calculated differently, rounding conventions differ, or columns are misread. This tool checks whether the numbers in a summary document can actually be reconciled with the raw figures behind them.

## What it checks

- **Row and column totals**: Do stated totals match the sum of their components?
- **Cross-document consistency**: Does a figure appearing in two places agree with itself?
- **Category allocation**: Do all records fall into exactly one category (no overlaps, no gaps)?
- **Period alignment**: Are figures from the same time period being compared, or are dates mismatched?
- **Rounding audit**: Where figures are rounded, is rounding applied consistently?

## Approach

The tool ingests:
1. A **summary table** (Excel or CSV) containing the figures to be verified
2. A **source dataset** (CSV or database query result) containing the underlying records

It produces:
1. A **consistency report** — line-by-line comparison of summary vs source figures
2. A **discrepancy log** — flagging every figure that does not reconcile, with the magnitude of the gap
3. A **pass/fail verdict** per check — not a score, a clear binary result

## Files

```
02_financial_consistency_checker/
├── checker.py              # Main consistency logic
├── sql/
│   └── source_queries.sql  # SQL queries to extract source data
├── sample_data/
│   ├── summary_table.csv   # Example summary with intentional errors
│   └── source_records.csv  # Underlying transaction-level data
├── outputs/
│   ├── consistency_report.csv
│   └── discrepancy_log.csv
└── README.md
```

## Usage

```bash
python checker.py --summary sample_data/summary_table.csv \
                  --source sample_data/source_records.csv \
                  --output-dir outputs/
```

## Example output (discrepancy_log.csv)

| check_type | field | summary_value | source_value | difference | verdict |
|---|---|---|---|---|---|
| row_total | Q3_revenue | 142,500 | 141,800 | 700 | FAIL |
| category_sum | product_A | 38,200 | 38,200 | 0 | PASS |
| period_alignment | report_date | 2024-09 | 2024-10 | — | FAIL |

## Skills demonstrated

- SQL for source data extraction and aggregation
- Systematic cross-referencing of summary vs source figures
- Structured output designed for human review, not just programmatic use
- Thinking about where figures can go wrong, not just whether they add up
