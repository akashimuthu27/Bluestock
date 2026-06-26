-- 10 Analytical SQL Queries for Bluestock Mutual Fund Database

-- 1. Top 5 funds by AUM (Latest year 2025)
SELECT fund_house, aum_cr AS AUM_Cr
FROM fact_aum
WHERE year = 2025
ORDER BY aum_cr DESC
LIMIT 5;

-- 2. Average NAV per month for each scheme
SELECT f.scheme_name, d.year, d.month, AVG(n.nav) AS avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.scheme_code
JOIN dim_date d ON n.date = d.date
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;

-- 3. Systematic Investment Plan (SIP) Year-over-Year (YoY) growth in inflow
WITH yearly_sip AS (
    SELECT d.year, SUM(t.amount) AS total_sip_amount
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT cur.year, cur.total_sip_amount,
       prev.total_sip_amount AS prev_year_sip,
       ROUND(((cur.total_sip_amount - prev.total_sip_amount) / prev.total_sip_amount) * 100, 2) AS yoy_growth_pct
FROM yearly_sip cur
LEFT JOIN yearly_sip prev ON cur.year = prev.year + 1;

-- 4. Total transaction count and sum grouped by investor state
SELECT state, COUNT(*) AS txn_count, SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. List of funds with an expense ratio less than 1.0%
SELECT f.scheme_name, p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.scheme_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. Total redemption amount per fund
SELECT f.scheme_name, SUM(t.amount) AS total_redemption_amount
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.scheme_code
WHERE t.transaction_type = 'Redemption'
GROUP BY f.scheme_name
ORDER BY total_redemption_amount DESC;

-- 7. Funds with 'Very High' risk grade and their average 3-year CAGR
SELECT f.scheme_name, f.risk_grade, p.cagr_3yr
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.scheme_code
WHERE f.risk_grade = 'Very High'
ORDER BY p.cagr_3yr DESC;

-- 8. Monthly transaction volume (count and sum) in 2026
SELECT d.month, COUNT(*) AS txn_count, SUM(t.amount) AS total_amount
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date
WHERE d.year = 2026
GROUP BY d.month
ORDER BY d.month;

-- 9. Top 3 fund houses by total transaction volume (amount)
SELECT f.fund_house, SUM(t.amount) AS total_txn_amount
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.scheme_code
GROUP BY f.fund_house
ORDER BY total_txn_amount DESC
LIMIT 3;

-- 10. NAV record completeness count per fund (demonstrates gap-filling completeness)
SELECT f.scheme_name, COUNT(n.nav) AS total_nav_records, MIN(n.date) AS start_date, MAX(n.date) AS end_date
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.scheme_code
GROUP BY f.scheme_name
ORDER BY total_nav_records DESC;
