# Day 2: Data Cleaning & SQLite Database Loading

This sub-repository contains the pipeline, SQL scripts, database, and documentation for **Day 2: Data Cleaning & SQLite Database Loading** of the Bluestock Internship.

## Objectives
1. **Data Cleaning**: Parse dates, sort, forward-fill missing NAV values for weekends/holidays, deduplicate, validate amounts/NAVs, coerce return types, and flag expense ratio anomalies.
2. **Star Schema Database**: Design a relational star schema database (`bluestock_mf.db`) with 2 dimension tables and 4 fact tables, maintaining full key relationships and constraints.
3. **Automated Loading**: Implement a Python script using SQLAlchemy to create the schema and load the 10 cleaned datasets, verifying row count integrity.
4. **SQL Analytics**: Write and verify 10 analytical SQL queries covering fund performance, retail transaction trends, geographical contributions, and database completeness.
5. **Documentation**: Create a comprehensive data dictionary defining tables, data types, business logic, and cleaning rules.

---

## Folder Structure

```text
Day 2/
├── data/
│   ├── raw/                      # Raw dirty CSV datasets (10 files)
│   └── processed/                # 10 cleaned CSV datasets
├── sql/
│   ├── schema.sql                # SQLite Star Schema DDL
│   └── queries.sql               # 10 analytical SQL queries
├── reports/
│   └── data_dictionary.md        # Column-level database documentation
├── scripts/
│   ├── generate_dirty_data.py    # Generates raw dirty datasets for transactions & performance
│   ├── data_cleaning.py          # Cleans all 10 datasets according to rules
│   ├── load_to_sqlite.py         # Connects to SQLite and loads data via SQLAlchemy
│   └── test_queries.py           # Verification script running the 10 analytical queries
├── bluestock_mf.db               # Pre-loaded SQLite Database
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

---

## Execution Guide

### 1. Install Dependencies
Ensure you have the required packages installed:
```bash
pip install -r requirements.txt
pip install sqlalchemy
```

### 2. Generate Raw Dirty Data
Create the raw datasets containing realistic anomalies:
```bash
python scripts/generate_dirty_data.py
```

### 3. Run Data Cleaning Pipeline
Clean all 10 datasets, forward-filling NAV gaps and standardizing columns:
```bash
python scripts/data_cleaning.py
```

### 4. Load Data into SQLite Database
Initialize the star schema and load the cleaned CSV data:
```bash
python scripts/load_to_sqlite.py
```

### 5. Verify SQL Queries
Execute and print the output of the 10 analytical queries:
```bash
python scripts/test_queries.py
```

---

## Star Schema Architecture

The SQLite database `bluestock_mf.db` implements the following relational star schema:
* **`dim_fund`**: Scheme codes, names, fund house, categories, and risk grades.
* **`dim_date`**: Calendar dates broken down by day, month, year, quarter, and day name.
* **`fact_nav`**: Daily Net Asset Value (NAV) records, with weekend gaps forward-filled.
* **`fact_transactions`**: Aligned investor purchase, SIP, and redemption transactions.
* **`fact_performance`**: Coerced annualized returns (CAGR) and expense ratios with anomaly flags.
* **`fact_aum`**: Consolidated yearly Assets Under Management (AUM) per fund house.

---

## Deliverables Completed
- **10 Cleaned CSVs**: Located in `data/processed/`
- **SQLite Database**: `bluestock_mf.db` (fully populated and verified)
- **Star Schema DDL**: `sql/schema.sql`
- **10 Analytical Queries**: `sql/queries.sql`
- **Data Dictionary**: `reports/data_dictionary.md`
- **Git Commit & Sync**: Pushed to the remote repository
