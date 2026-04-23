-- Financial Consistency Checker
-- Source Data Extraction Queries
-- Author: Nitish Kampagoudar

-- ─────────────────────────────────────────────
-- 1. Total revenue by category for a given period
-- Used to verify category-level figures in summary table
-- ─────────────────────────────────────────────
SELECT
    category,
    DATE_TRUNC('month', transaction_date) AS period,
    SUM(amount)                           AS total_amount,
    COUNT(*)                              AS record_count
FROM transactions
WHERE
    transaction_date BETWEEN :start_date AND :end_date
    AND status NOT IN ('cancelled', 'reversed')
GROUP BY
    category,
    DATE_TRUNC('month', transaction_date)
ORDER BY
    period,
    category;


-- ─────────────────────────────────────────────
-- 2. Check for category allocation gaps
-- Every transaction should belong to exactly one category.
-- Uncategorised or multi-categorised records are flagged.
-- ─────────────────────────────────────────────
SELECT
    t.transaction_id,
    t.amount,
    t.transaction_date,
    COUNT(tc.category_id) AS category_count,
    CASE
        WHEN COUNT(tc.category_id) = 0 THEN 'UNCATEGORISED'
        WHEN COUNT(tc.category_id) > 1 THEN 'MULTI_CATEGORISED'
        ELSE 'OK'
    END AS allocation_status
FROM transactions t
LEFT JOIN transaction_categories tc
    ON t.transaction_id = tc.transaction_id
GROUP BY
    t.transaction_id,
    t.amount,
    t.transaction_date
HAVING
    COUNT(tc.category_id) != 1
ORDER BY
    allocation_status,
    t.transaction_date;


-- ─────────────────────────────────────────────
-- 3. Period alignment check
-- Identifies records with a transaction_date outside the
-- stated reporting period — potential period-mismatch issues
-- ─────────────────────────────────────────────
SELECT
    transaction_id,
    transaction_date,
    report_period,
    amount,
    'PERIOD_MISMATCH' AS flag_reason
FROM transactions
WHERE
    DATE_TRUNC('month', transaction_date) != DATE_TRUNC('month', report_period::date)
    AND report_period IS NOT NULL
ORDER BY
    transaction_date;


-- ─────────────────────────────────────────────
-- 4. Row total verification
-- Compares stated subtotals against sum of line items
-- Tolerance: 0 (exact match required; rounding handled separately)
-- ─────────────────────────────────────────────
SELECT
    summary_group,
    SUM(line_item_amount)     AS computed_total,
    MAX(stated_group_total)   AS stated_total,
    MAX(stated_group_total)
        - SUM(line_item_amount) AS discrepancy,
    CASE
        WHEN ABS(MAX(stated_group_total) - SUM(line_item_amount)) = 0
            THEN 'PASS'
        WHEN ABS(MAX(stated_group_total) - SUM(line_item_amount)) <= 1
            THEN 'ROUNDING_FLAG'
        ELSE 'FAIL'
    END AS verdict
FROM line_items
GROUP BY
    summary_group
ORDER BY
    ABS(MAX(stated_group_total) - SUM(line_item_amount)) DESC;
