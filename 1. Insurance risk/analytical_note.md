# Analytical Note – Insurance Risk Dataset Review

**Prepared by:** Nitish Kampagoudar  
 
**Status:** Complete – ready for reviewer

---

## Purpose of this note

This note documents what was found during the data cleaning and review process, what decisions were made, what remains unresolved, and what a reviewer should know before using this dataset for any downstream analysis.

It is not a summary of conclusions. It is a record of the work done and its limits.

---

## What was found

### Category inconsistency (product_type)
The `product_type` field contained five distinct string variants referring to what appeared to be four intended categories. Three variants all referred to Motor Vehicle insurance ("Motor", "motor", "Motor Vehicle"). These were consolidated. The consolidation assumption that these are the same category, is reasonable but was not confirmed against a source data dictionary. If one is used, the consolidation should be verified.

### Figures that do not reconcile
The summary tab (rows 1–5 of the original file) showed a total claims figure of 4,218,400. Summing the `claim_amount` column in the row-level data gives 4,039,800, a difference of 178,600 (approximately 4.2%). This discrepancy has not been resolved. Possible causes include: rows excluded from the summary for unstated reasons, a calculation error in the summary tab, or a version mismatch between the summary and the detail. This should be investigated before either figure is cited.

### Anomalous claim amounts
Seven records show claim amounts exceeding the policy sum insured. These have been flagged and retained. They are not automatically errors, some may reflect reinsurance recoveries, reinstatements, or data extracted across multiple claim events. The appropriate treatment requires context that is not present in the raw file.

### Missing premium data
Eleven records have no premium value. These have been tagged with a `premium_status` column and retained. No imputation has been applied. In an insurance context, silent imputation of premium data would be inappropriate, the missing values may reflect void policies, data extraction failures, or excluded risk categories.

### Impossible date sequences
Three records show a claim date earlier than the policy start date. These are flagged. Whether they represent data errors or genuine edge cases (e.g., claims under predecessor policies) cannot be determined from the data alone.

---

## What was not done — and why

| Not done | Reason |
|---|---|
| Imputation of missing values | No justification available; imputation documented for review |
| Removal of anomalous rows | Flagging is the analyst's role; removal is a reviewer decision |
| Assumption about summary reconciliation | Discrepancy documented; cause not assumed |
| Consolidation verified against data dictionary | No dictionary provided; assumption documented |

---

## What the reviewer should do before using this data

1. Confirm the category consolidation for `product_type` against the source system
2. Investigate the 4.2% discrepancy between the summary and row-level totals
3. Determine the appropriate treatment for the seven excess-claim records
4. Decide whether missing-premium rows should be excluded, imputed, or investigated
5. Clarify the three impossible date records with the data owner

---

## Overall assessment

The dataset is usable for preliminary analysis once the summary reconciliation issue is resolved and a decision is made on the anomalous rows. It should not be used to produce figures that will be cited externally until these points are addressed.
