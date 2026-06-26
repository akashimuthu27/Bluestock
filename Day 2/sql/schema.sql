-- SQLite Star Schema DDL for Bluestock Mutual Fund Analytics Database

-- Drop tables if they exist to ensure clean initialization
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

-- 1. Dimension Table: Funds
CREATE TABLE dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT,
    risk_grade TEXT
);

-- 2. Dimension Table: Dates
CREATE TABLE dim_date (
    date TEXT PRIMARY KEY, -- Formatted as YYYY-MM-DD
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week TEXT NOT NULL
);

-- 3. Fact Table: NAV History
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    date TEXT NOT NULL,
    nav REAL NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

-- 4. Fact Table: Investor Transactions
CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id INTEGER NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    kyc_status TEXT NOT NULL,
    state TEXT NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
);

-- 5. Fact Table: Scheme Performance
CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    cagr_3yr REAL,
    cagr_5yr REAL,
    expense_ratio REAL NOT NULL,
    expense_ratio_anomaly INTEGER DEFAULT 0,
    return_anomaly INTEGER DEFAULT 0,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(scheme_code)
);

-- 6. Fact Table: Assets Under Management (AUM)
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT NOT NULL,
    year INTEGER NOT NULL,
    aum_cr REAL NOT NULL
);
