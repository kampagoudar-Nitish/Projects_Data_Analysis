"""
Contract Data Reconciliation Pipeline
Author: Nitish Kampagoudar
GitHub: kampagoudar-Nitish/Projects_Data_Analysis

Reconciles three partial contract datasets from different source systems.
Does not silently prefer one source over another.
Documents every conflict for reviewer decision.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR    = "output"
CONFLICT_FILE = os.path.join(OUTPUT_DIR, "conflict_log.csv")
UNIFIED_FILE  = os.path.join(OUTPUT_DIR, "unified_contracts.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load three sources ────────────────────────────────────────────────────────
active   = pd.read_csv("active_contracts.csv")
expired  = pd.read_csv("expired_contracts.csv")
amend    = pd.read_csv("amendments.csv")

for df, label in [(active, "active"), (expired, "expired"), (amend, "amendments")]:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    print(f"Loaded [{label}]: {df.shape[0]} rows")

conflicts = []

# ─── Step 1: Identify contracts in both active and expired ─────────────────────
# A contract cannot be both active and expired. Flag for reviewer.
active_ids  = set(active["contract_id"].dropna().astype(str))
expired_ids = set(expired["contract_id"].dropna().astype(str))
both        = active_ids & expired_ids

print(f"\nConflict: {len(both)} contracts appear in both active and expired exports")
for cid in both:
    conflicts.append({
        "contract_id"   : cid,
        "conflict_type" : "status_conflict",
        "field"         : "contract_status",
        "source_a_value": "active",
        "source_b_value": "expired",
        "resolution"    : "unresolved – reviewer must determine correct status"
    })

# ─── Step 2: Merge all contracts ──────────────────────────────────────────────
active["source"]  = "active_export"
expired["source"] = "expired_export"
all_contracts = pd.concat([active, expired], ignore_index=True)

# ─── Step 3: Detect field-level conflicts ──────────────────────────────────────
# For contracts appearing in both sources, check key field values.
check_fields = ["contract_value", "counterparty_name", "start_date", "end_date"]

for cid in both:
    rows = all_contracts[all_contracts["contract_id"].astype(str) == str(cid)]
    for field in check_fields:
        if field not in rows.columns:
            continue
        values = rows[field].dropna().astype(str).unique()
        if len(values) > 1:
            conflicts.append({
                "contract_id"   : cid,
                "conflict_type" : "field_value_conflict",
                "field"         : field,
                "source_a_value": values[0],
                "source_b_value": values[1] if len(values) > 1 else "N/A",
                "resolution"    : "unresolved – reviewer must determine correct value"
            })

# ─── Step 4: Amendment orphan check ───────────────────────────────────────────
# Amendments should reference a known contract_id.
known_ids = active_ids | expired_ids
amend_ids = set(amend["contract_id"].dropna().astype(str))
orphan_ids = amend_ids - known_ids

print(f"Orphaned amendments: {len(orphan_ids)} amendment records reference unknown contract IDs")
for cid in orphan_ids:
    conflicts.append({
        "contract_id"   : cid,
        "conflict_type" : "orphaned_amendment",
        "field"         : "contract_id",
        "source_a_value": "not in any contract export",
        "source_b_value": "present in amendments",
        "resolution"    : "unresolved – possible deletion, ID mismatch, or data error"
    })

# ─── Step 5: Completeness audit ────────────────────────────────────────────────
# Find contracts with no counterparty name in any source
if "counterparty_name" in all_contracts.columns:
    no_counterparty = (
        all_contracts.groupby("contract_id")["counterparty_name"]
        .apply(lambda x: x.dropna().empty)
    )
    missing_cp = no_counterparty[no_counterparty].index.tolist()
    print(f"Missing counterparty: {len(missing_cp)} contracts have no counterparty name in any source")

# ─── Write outputs ─────────────────────────────────────────────────────────────
conflict_df = pd.DataFrame(conflicts)
conflict_df.to_csv(CONFLICT_FILE, index=False)
print(f"\nConflict log: {len(conflict_df)} entries → {CONFLICT_FILE}")

all_contracts.to_csv(UNIFIED_FILE, index=False)
print(f"Unified file: {all_contracts.shape[0]} rows → {UNIFIED_FILE}")

print("\n--- RECONCILIATION SUMMARY ---")
print(f"Status conflicts        : {len(both)}")
print(f"Field-level conflicts   : {len([c for c in conflicts if c['conflict_type']=='field_value_conflict'])}")
print(f"Orphaned amendments     : {len(orphan_ids)}")
print(f"Missing counterparties  : {len(missing_cp) if 'counterparty_name' in all_contracts.columns else 'N/A'}")
print("\nAll conflicts retained and logged. No source preference applied without documentation.")
