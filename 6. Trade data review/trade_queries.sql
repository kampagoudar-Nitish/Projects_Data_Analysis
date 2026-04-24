-- International Trade Dataset – Verification Queries
-- Author: Nitish Kampagoudar

-- ─── 1. Mirror statistics gap by country pair and year ───────────────────────
SELECT
    e.reporting_country              AS exporter,
    e.partner_country                AS importer,
    e.year,
    e.trade_value_usd                AS reported_export_value,
    i.trade_value_usd                AS reported_import_value,
    ABS(e.trade_value_usd
        - i.trade_value_usd)         AS absolute_gap,
    ROUND(
        ABS(e.trade_value_usd - i.trade_value_usd)
        / NULLIF(e.trade_value_usd, 0) * 100, 1
    )                                AS gap_pct
FROM trade_data e
JOIN trade_data i
    ON  e.reporting_country = i.partner_country
    AND e.partner_country   = i.reporting_country
    AND e.year              = i.year
    AND e.flow_type         = 'export'
    AND i.flow_type         = 'import'
ORDER BY gap_pct DESC;


-- ─── 2. Invalid HS codes ──────────────────────────────────────────────────────
SELECT
    reporting_country,
    partner_country,
    year,
    hs_code,
    LENGTH(CAST(hs_code AS VARCHAR))  AS code_length,
    'invalid_format'                  AS issue
FROM trade_data
WHERE
    CAST(hs_code AS VARCHAR) NOT GLOB '[0-9][0-9][0-9][0-9][0-9][0-9]'
    OR LENGTH(CAST(hs_code AS VARCHAR)) <> 6
ORDER BY reporting_country, year;


-- ─── 3. Records where data year differs from reporting date year ─────────────
SELECT
    reporting_country,
    partner_country,
    year                         AS stated_trade_year,
    STRFTIME('%Y', reporting_date) AS reporting_date_year,
    trade_value_usd,
    flow_type
FROM trade_data
WHERE STRFTIME('%Y', reporting_date) <> CAST(year AS VARCHAR)
ORDER BY reporting_country, year;


-- ─── 4. Country pairs missing data for specific years ────────────────────────
WITH all_combos AS (
    SELECT DISTINCT
        p.reporting_country,
        p.partner_country,
        y.year
    FROM (SELECT DISTINCT reporting_country, partner_country FROM trade_data) p
    CROSS JOIN (SELECT DISTINCT year FROM trade_data) y
),
actuals AS (
    SELECT DISTINCT reporting_country, partner_country, year
    FROM trade_data
)
SELECT
    ac.reporting_country,
    ac.partner_country,
    ac.year,
    'missing' AS data_status
FROM all_combos ac
LEFT JOIN actuals a
    ON  ac.reporting_country = a.reporting_country
    AND ac.partner_country   = a.partner_country
    AND ac.year              = a.year
WHERE a.reporting_country IS NULL
ORDER BY ac.reporting_country, ac.partner_country, ac.year;
