# Analytical Note – International Trade Dataset Review

**Prepared by:** Nitish Kampagoudar
**Dataset:** Synthetic bilateral trade flows, 10 countries × 5 categories × 5 years
**Status:** Preliminary review complete — findings documented for researcher action

---

## Purpose

This note documents what the trade dataset supports analytically, what inconsistencies were found, and what a researcher should address before drawing conclusions or publishing figures from this data.

---

## Findings

### HS code formatting errors (estimated 23 records)
Approximately 23 records contain 5-digit HS codes where 6 digits are required by the Harmonized System standard. This is a formatting error, not a classification question — a 5-digit code does not map to a valid HS heading. Product category attribution for these records is unreliable. The records are flagged in `output/flagged_records.csv`.

### Mirror statistics gaps — most within normal range, four pairs require investigation
Mirror statistics gaps (difference between Country A's reported exports to Country B and Country B's reported imports from Country A) average 6.2% across all country pairs. This is consistent with known WTO/UN Comtrade data patterns, which routinely show gaps of 5–10% due to CIF/FOB valuation differences, timing, and re-export attribution.

Four country pairs show gaps above 18%:
- China → Germany
- USA → Japan
- India → UK
- Brazil → France

Gaps of this magnitude warrant investigation. Possible explanations include re-export misattribution (goods routed through a third country), significant timing differences between reporting periods, or data entry errors. These pairs should not be used in bilateral analysis without further investigation.

### Period mixing (estimated 12 records)
Twelve records have a reporting date that falls in a different calendar year from the stated trade year. These may represent revised estimates published in a subsequent year, or data extracted from a system that stamps extraction date rather than transaction year. They are flagged. If included in year-level analysis without adjustment, they may introduce noise in year-over-year comparisons.

### Implausible trade values (2 records)
Two records show trade values exceeding 50% of the exporting country's GDP for a single bilateral trade flow in a single product category. This is not plausible for any of the country pairs in this dataset. The most likely explanations are a unit inconsistency (USD vs thousands of USD) or a data entry error. These records are flagged and should be excluded or corrected before use.

---

## What the data supports — and what it does not

**Supported (after addressing the above):**
- Broad directional trends in bilateral trade flows across country pairs
- Category-level comparisons within the same country pair and year
- Multi-year trend analysis for country pairs where gaps are within normal range

**Not supported without further investigation:**
- Precise bilateral figures for the four high-gap country pairs
- Year-specific figures for the 12 period-mixed records
- Any analysis relying on the 23 incorrectly formatted HS code records

---

## Note on mirror statistics

Mirror statistics gaps are a well-documented feature of international trade statistics, not necessarily a data quality failure. The IMF, WTO, and UN all publish guidance on interpreting these gaps. A gap of 6% on average is unremarkable. The four pairs above 18% are the genuine concern, not the existence of gaps per se.
