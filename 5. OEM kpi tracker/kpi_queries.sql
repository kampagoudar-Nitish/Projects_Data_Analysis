-- OEM Software Delivery – KPI Verification Queries
-- Author: Nitish Kampagoudar
-- GitHub: kampagoudar-Nitish/Projects_Data_Analysis

-- ─── 1. Feature count reconciliation ──────────────────────────────────────────
-- Compare delivered feature counts by programme between log and summary.

SELECT
    l.oem_programme,
    COUNT(DISTINCT l.feature_id)       AS log_delivered_count,
    s.delivered_features               AS summary_count,
    COUNT(DISTINCT l.feature_id)
        - s.delivered_features         AS discrepancy
FROM delivery_log l
JOIN kpi_summary s
    ON l.oem_programme = s.oem_programme
WHERE l.status = 'delivered'
GROUP BY l.oem_programme, s.delivered_features
HAVING ABS(COUNT(DISTINCT l.feature_id) - s.delivered_features) > 0
ORDER BY ABS(discrepancy) DESC;


-- ─── 2. On-time delivery rate — planned vs revised basis ──────────────────────
-- Calculate OTD two ways: against planned date and against revised date.
-- A material difference indicates the summary choice of basis matters.

SELECT
    oem_programme,
    ROUND(
        SUM(CASE WHEN actual_date <= planned_milestone_date THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 1
    ) AS otd_pct_vs_planned,
    ROUND(
        SUM(CASE WHEN actual_date <= revised_milestone_date THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 1
    ) AS otd_pct_vs_revised,
    ROUND(
        SUM(CASE WHEN actual_date <= revised_milestone_date THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 1
    ) -
    ROUND(
        SUM(CASE WHEN actual_date <= planned_milestone_date THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 1
    )                               AS basis_difference_pp
FROM delivery_log
WHERE status IN ('delivered', 'late')
GROUP BY oem_programme
ORDER BY ABS(basis_difference_pp) DESC;


-- ─── 3. Missing quarters per programme ───────────────────────────────────────
-- Identify programmes with no data for a quarter that other programmes report.

WITH all_combos AS (
    SELECT DISTINCT
        p.oem_programme,
        q.quarter
    FROM (SELECT DISTINCT oem_programme FROM delivery_log) p
    CROSS JOIN (SELECT DISTINCT quarter FROM delivery_log) q
),
actuals AS (
    SELECT DISTINCT oem_programme, quarter
    FROM delivery_log
)
SELECT
    ac.oem_programme,
    ac.quarter,
    'missing from log' AS status
FROM all_combos ac
LEFT JOIN actuals a
    ON ac.oem_programme = a.oem_programme
    AND ac.quarter = a.quarter
WHERE a.oem_programme IS NULL
ORDER BY ac.oem_programme, ac.quarter;


-- ─── 4. Defect density — check for multiple LOC snapshot dates ────────────────

SELECT
    oem_programme,
    COUNT(DISTINCT loc_snapshot_date)  AS distinct_snapshots,
    MIN(loc_snapshot_date)             AS earliest_snapshot,
    MAX(loc_snapshot_date)             AS latest_snapshot
FROM delivery_log
GROUP BY oem_programme
HAVING COUNT(DISTINCT loc_snapshot_date) > 1
ORDER BY distinct_snapshots DESC;


-- ─── 5. Grand total cross-check ───────────────────────────────────────────────

SELECT
    SUM(d.delivered_features) AS log_total,
    s.grand_total              AS summary_grand_total,
    SUM(d.delivered_features) - s.grand_total AS discrepancy
FROM (
    SELECT oem_programme, COUNT(DISTINCT feature_id) AS delivered_features
    FROM delivery_log
    WHERE status = 'delivered'
    GROUP BY oem_programme
) d
CROSS JOIN (
    SELECT SUM(delivered_features) AS grand_total FROM kpi_summary
) s;
