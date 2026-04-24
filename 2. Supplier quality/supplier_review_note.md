# Supplier Quality Audit – Review Note

**Prepared by:** Nitish Kampagoudar
**Period covered:** Q1-2022 through Q4-2023 (8 quarters, 150 suppliers)
**Status:** Findings documented — reviewer action required before management distribution

---

## What was checked

This note covers findings from a structured review of the quarterly supplier quality export before it is used in a management review meeting. The review covers category consistency, figure reconciliation, data completeness, and cross-supplier comparison validity.

---

## Findings that require action

### 1. Supplier tier labels are inconsistent
The `supplier_tier` field contains five distinct label variants for three intended tiers (e.g., "Tier 1", "T1", "tier-1" all appear for the same tier). The cleaning pipeline has consolidated these. Before using tier-level aggregations, the consolidation should be confirmed against the source system's reference data.

### 2. On-time delivery figure does not reconcile with row-level data
The summary report states an aggregate OTD of 94.3%. The row-level average across all suppliers and quarters is 91.7% — a difference of 2.6 percentage points. This has not been explained. Possible causes: the summary excludes certain supplier tiers or status categories without disclosure, or the summary uses a weighted average with different weights than a simple mean. This should be resolved before the figure is cited.

### 3. Six suppliers report zero defects for every quarter
Six suppliers have a defect rate of exactly 0.0% across all eight quarters. While not impossible, this pattern is statistically unusual across a two-year window. These should be verified against source audit records before being cited as performance benchmarks.

### 4. Eleven suppliers have missing quarters
Eleven suppliers are missing data for at least one quarter. These gaps are documented in `output/gap_report.csv`. Suppliers with missing quarters have been excluded from trend analyses. The reason for the gaps (no audit conducted, data not submitted, system extraction failure) is not available from the dataset alone.

---

## Recommended actions before distribution

1. Confirm tier label consolidation against the source system's reference table
2. Investigate the 2.6 pp OTD discrepancy, determine whether summary uses a different denominator or scope
3. Verify zero-defect suppliers against source audit records
4. Obtain an explanation for the 11 suppliers with missing quarters before excluding them from benchmarking
