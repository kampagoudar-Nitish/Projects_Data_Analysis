-- Insurance Risk Dataset – SQL Consistency Checks
-- Author: Nitish Kampagoudar
-- GitHub: kampagoudar-Nitish/Projects_Data_Analysis
--
-- Purpose: Verify category consistency and aggregate reconciliation
-- across the cleaned insurance dataset using SQL.
-- These queries are designed to be run in sequence as a validation checklist.

-- ─── 1. Category audit: product_type ──────────────────────────────────────────
-- Check that no unexpected category variants remain after cleaning.

SELECT
    product_type,
    COUNT(*)          AS row_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_of_total
FROM insurance_data
GROUP BY product_type
ORDER BY row_count DESC;


-- ─── 2. Aggregate reconciliation ──────────────────────────────────────────────
-- Compare the row-level sum of claim_amount against the expected summary total.
-- Expected total (from summary tab): 4,218,400
-- A non-zero difference requires investigation.

SELECT
    SUM(claim_amount)                    AS row_level_total,
    4218400                              AS summary_tab_total,
    SUM(claim_amount) - 4218400         AS discrepancy,
    ROUND(
        ABS(SUM(claim_amount) - 4218400) / 4218400.0 * 100, 2
    )                                    AS discrepancy_pct
FROM insurance_data;


-- ─── 3. Flag claim amounts exceeding sum insured ───────────────────────────────
-- These are not automatically removed — they are surfaced for reviewer decision.

SELECT
    policy_id,
    product_type,
    claim_amount,
    sum_insured,
    claim_amount - sum_insured   AS excess_amount
FROM insurance_data
WHERE claim_amount > sum_insured
ORDER BY excess_amount DESC;


-- ─── 4. Missing premium values ─────────────────────────────────────────────────
-- Count and list records where premium is null.

SELECT
    COUNT(*)  AS missing_premium_count
FROM insurance_data
WHERE premium IS NULL;

SELECT
    policy_id,
    product_type,
    policy_start,
    policy_end,
    premium
FROM insurance_data
WHERE premium IS NULL
ORDER BY policy_start;


-- ─── 5. Impossible date sequences ──────────────────────────────────────────────
-- Claim date should not precede policy start date.

SELECT
    policy_id,
    policy_start,
    claim_date,
    DATEDIFF(day, policy_start, claim_date)  AS days_before_start
FROM insurance_data
WHERE claim_date < policy_start
ORDER BY days_before_start;


-- ─── 6. Duplicate policy IDs ───────────────────────────────────────────────────
-- Check whether policy_id is a reliable unique identifier.

SELECT
    policy_id,
    COUNT(*) AS occurrence_count
FROM insurance_data
GROUP BY policy_id
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;


-- ─── 7. Null check across all key fields ──────────────────────────────────────
-- Quick summary of nulls per column. Run once after loading.

SELECT
    SUM(CASE WHEN policy_id     IS NULL THEN 1 ELSE 0 END) AS null_policy_id,
    SUM(CASE WHEN product_type  IS NULL THEN 1 ELSE 0 END) AS null_product_type,
    SUM(CASE WHEN premium       IS NULL THEN 1 ELSE 0 END) AS null_premium,
    SUM(CASE WHEN sum_insured   IS NULL THEN 1 ELSE 0 END) AS null_sum_insured,
    SUM(CASE WHEN claim_amount  IS NULL THEN 1 ELSE 0 END) AS null_claim_amount,
    SUM(CASE WHEN claim_date    IS NULL THEN 1 ELSE 0 END) AS null_claim_date,
    SUM(CASE WHEN policy_start  IS NULL THEN 1 ELSE 0 END) AS null_policy_start,
    SUM(CASE WHEN policy_end    IS NULL THEN 1 ELSE 0 END) AS null_policy_end,
    COUNT(*) AS total_rows
FROM insurance_data;
