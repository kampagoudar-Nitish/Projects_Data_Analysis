# Review Note – OEM Software Delivery KPI Dashboard

**Prepared by:** Nitish Kampagoudar  
**Context:** Quarterly KPI review prior to OEM customer meeting  
**Status:** Findings documented — reviewer action required before distribution

---

## What was checked

This note covers the findings from a systematic consistency review of the quarterly KPI summary dashboard. The review was done before the figures are presented in the customer meeting. The goal was to identify anything that is unclear, inconsistent, or unsupported before the numbers are cited externally.

---

## Findings that require action before distribution

### 1. Feature count does not reconcile
The summary shows a total of 284 delivered features. The delivery log shows 271 unique delivered feature IDs. The difference of 13 features has not been explained. Possible causes include estimated values in the summary, features counted under different status definitions, or a version mismatch between the log and the summary. This should be resolved before the figure is cited to customers.

### 2. OTD basis not stated — and it matters
Two programmes calculate on-time delivery against original planned milestone dates. One programme calculates it against revised dates. The summary presents a single OTD figure for each programme without disclosing the basis. Against revised dates, the programme in question shows 91% OTD. Against original planned dates, it shows 78%. This is a material difference and the basis should be disclosed or standardised.

### 3. Estimated values in summary not flagged
One programme has no raw delivery data for Q3. The summary nonetheless shows Q3 figures for this programme. These appear to be estimated or carried-forward values. They are not labelled as estimates. Before circulation, either: (a) the estimates should be removed and the gap noted, or (b) they should be clearly labelled as estimates with the basis stated.

### 4. Cross-programme defect density comparison is not valid as presented
Team sizes across programmes range from 8 to 23 people, a factor of nearly 3×. The summary compares defect counts directly without normalising for team size or codebase size. A programme with a larger team and larger codebase will naturally produce more defects in absolute terms. The comparison as presented is misleading.

---

## Findings that do not block distribution but should be noted

- LOC snapshot dates differ within one programme across quarters. This means quarter-over-quarter defect density trends for that programme are not strictly comparable.
- Two programme names in the summary use different spellings from the delivery log ("OEM-3" vs "OEM3"). These appear to be the same programme. Should be standardised.

---

## Recommended actions before the customer meeting

1. Reconcile the 13-feature discrepancy with the delivery team
2. Standardise OTD calculation basis across all programmes, or disclose the basis per programme
3. Label estimated Q3 figures or remove them
4. Add a footnote to the defect comparison noting that figures are not normalised for team size
5. Standardise programme naming conventions between log and summary

---

## What is not in scope of this note

This review covers internal data consistency only. It does not assess whether the delivery performance shown is acceptable relative to contractual commitments — that is a separate question for the programme manager and customer relationship team.
