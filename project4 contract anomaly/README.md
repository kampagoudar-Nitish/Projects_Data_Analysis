# Contract Data Review – Anomaly Detection & Structured Notes

**Repository:** `kampagoudar-Nitish/Projects_Data_Analysis`  
**Project:** 04 – Contract Data Review: Organising Fragmented Information  
**Author:** Nitish Kampagoudar  
**Tools:** Python (pandas), SQL, Excel  

---

## Overview

This project addresses the messiest of real-world data situations: information that arrives in fragments — multiple partial sources, inconsistent formats, some fields populated in one file but not another, and needs to be unified into a working dataset before any analysis can begin.

The scenario: a contract management team provides three separate exports (active contracts, expired contracts, amendment records) that nominally refer to the same underlying contracts but were extracted from different systems on different dates. The task is to reconcile them into a single reliable working file.

---

## What the project covers

1. **Multi-source reconciliation** — joining three partial datasets on a shared key
2. **Conflict identification** — where the same field has different values across sources
3. **Completeness audit** — which contracts have critical fields missing across all sources
4. **Amendment logic check** — verifying that amendments are consistent with base contracts
5. **Structured notes output** — a working file with source annotations and a conflict log

---

## Files

| File | Description |
|---|---|
| `active_contracts.csv` | Active contract export (source A) |
| `expired_contracts.csv` | Expired contract export (source B) |
| `amendments.csv` | Amendment records (source C) |
| `reconcile.py` | Python: full reconciliation pipeline |
| `conflict_log.csv` | Output: every field-level conflict between sources |
| `reconciliation_note.md` | Written note: what was unified, what was not, decisions required |

---

## Key findings (synthetic scenario)

- 34 contracts appeared in both active and expired exports — status conflict not resolvable from data alone
- Contract value field had conflicting values in 12 records across sources (average discrepancy: €8,400)
- 6 amendment records referenced contract IDs not present in either main export — possible deletion, possible ID mismatch
- 28 contracts had no counterparty name in any source — critical gap for any downstream use

---

## Design note

When information is fragmented and incomplete, the worst response is to silently choose one source over another without documenting the decision. This project demonstrates the alternative: surface every conflict, document every choice, and give the reviewer enough information to make informed judgements.
