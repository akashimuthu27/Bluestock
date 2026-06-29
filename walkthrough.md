# Bluestock Mutual Fund Internship: Unified Project Walkthrough

This document records the complete implementation, validation, and synchronization of the mutual fund analytics tasks, fully pushed to the `main` branch of your remote repository.

---

## Part 1: Capstone Project I - Mutual Fund Analytics

We established an interactive exploratory data analysis pipeline for Capstone Project I under `Capstone - Mutual Fund Analytics/`.

### 1.1. Key Milestones Completed
* **Programmatic Data Generation (`generate_data.py`)**: Generated 8 realistic CSV datasets matching your exact target parameters:
  - Daily NAV time-series for 40 schemes (2022–2026) integrating the **2023 Bull Run** and the **2024 Market Correction** (April–September 2024).
  - Yearly AUM (2022–2025), showing **SBI Mutual Fund peaking at exactly ₹12.5 Lakh Crore in 2025** to demonstrate market dominance.
  - Monthly SIP inflows (Jan 2022 – Dec 2025), peaking at an **all-time high of exactly ₹31,002 Crore in Dec 2025**.
  - Monthly folio counts rising from **exactly 13.26 Crore in Jan 2022 to exactly 26.12 Crore in Dec 2025**.
* **Professional Chart Suite (`generate_charts.py`)**: Exported **16 high-resolution PNG charts** under `reports/figures/` covering NAV trajectories, AUM growth, monthly SIP inflows, and demographics.
* **Jupyter Notebook (`compile_notebook.py`)**: Programmatically compiled and pre-rendered `notebooks/EDA_Analysis.ipynb` containing interactive Plotly charts and **exactly 10 key analytical findings** in Markdown cells.

---

## Part 2: Day 2 - Data Cleaning & SQLite Database Loading

We implemented a data cleaning pipeline, designed a relational SQLite Star Schema, loaded the 10 cleaned datasets, and verified the analytical queries under `Day 2/`.

### 2.1. Data Cleaning Actions (`data_cleaning.py`)
- **`nav_history.csv` + 6 Scheme NAVs**: Parsed dates, sorted by `scheme_code` and `date`, removed duplicates, validated `nav > 0`, and **forward-filled missing weekend/holiday NAVs** by reindexing to a daily calendar.
- **`investor_transactions.csv`**: Standardized transaction types (SIP, Lumpsum, Redemption), filtered out `amount <= 0`, parsed and standardized mixed dates to `YYYY-MM-DD`, and standardized KYC statuses to Yes/No/Pending.
- **`scheme_performance.csv`**: Coerced returns to numeric values, flagged return anomalies, and validated/clipped expense ratios to the `0.1% – 2.5%` boundary, adding anomaly flags.

### 2.2. Row Counts Loaded and Verified
* `dim_fund`: 10 rows
* `dim_date`: 4,923 rows
* `fact_nav`: 29,284 rows
* `fact_transactions`: 188 rows (12 invalid transactions with amount <= 0 discarded)
* `fact_performance`: 10 rows (expense ratios validated and clipped to 0.1%–2.5% boundary)
* `fact_aum`: 24 rows

---

## Part 3: Dashboard Development (Power BI)

We developed the data model, designed the widescreen visual layouts, compiled the PDF report, and wrote the import guide under `Dashboard/`.

### 3.1. Deliverables Completed
* **The 8 Prepared CSV Tables**: Located under `Dashboard/data/raw/`, clean and ready for direct import into Power BI Desktop:
  - `dim_fund.csv`, `dim_date.csv`, `fact_nav.csv`, `fact_transactions.csv`, `fact_performance.csv`, `fact_aum.csv`, `fact_market_index.csv` (Nifty 50 daily index), and `investor_demographics.csv`.
* **High-Fidelity Dashboard Screenshots**: 16:9 widescreen PNG layouts saved under `Dashboard/reports/figures/`:
  - `page1_industry_overview.png`: Contains AUM/SIP/Folio/Scheme KPI cards, the industry AUM trend line, and AMC bar chart.
  - `page2_fund_performance.png`: Features a return vs. risk scatter plot, sortable fund scorecard table, and NAV vs. Nifty 50 line chart.
  - `page3_investor_analytics.png`: Displays state-wise transaction bars, transaction type donuts, age group averages, and monthly transaction volumes.
  - `page4_market_trends.png`: Displays the dual-axis SIP vs. Nifty 50 index chart, category net inflow matrix heatmap, and top 5 categories.
* **Compiled PDF Report**: Combined all 4 pages into `Dashboard/reports/Dashboard.pdf`.
* **Execution & Setup Guide**: Detailed `Dashboard/README.md` explaining how to import the CSVs, configure the star schema relationships, build the visual charts, and set up interactive slicers and drill-through.

---

## Part 4: Advanced Performance Analytics

We implemented a quantitative performance evaluation framework for all 40 mutual fund schemes over the 5-year period (2022–2026) under `Capstone - Mutual Fund Analytics/`.

### 4.1. Key Analytics Completed
* **Daily Returns & Distribution**: Computed daily returns $R_t = \frac{NAV_t}{NAV_{t-1}} - 1$ for all 40 schemes. Validated using histograms and Q-Q plots, confirming characteristic fat tails (positive excess kurtosis).
* **Multi-Period CAGR**: Computed 1-Year (2026), 3-Year (2024–2026), and 5-Year (2022–2026) compound growth rates.
* **Risk-Adjusted Ratios**: Calculated Sharpe and Sortino ratios using the RBI repo rate proxy of **6.5%** as the risk-free rate.
* **Alpha & Beta (OLS)**: Regressed daily returns against the Nifty 100 benchmark index using Ordinary Least Squares (OLS) to extract annualized Alpha and Beta.
* **Maximum Drawdown**: Computed maximum peak-to-trough drawdowns. Identified the worst drawdown period across funds: **April 12, 2024 to September 18, 2024** (the 2024 Market Correction).
* **Composite Fund Scorecard (0–100)**: Built a weighted ranking model: $30\% \times \text{3Yr CAGR} + 25\% \times \text{Sharpe} + 20\% \times \text{Alpha} + 15\% \times \text{Expense Ratio (inverse)} + 10\% \times \text{Max Drawdown (inverse)}$.
* **Benchmark Comparison Chart**: Plotted 3-year cumulative returns of the top 5 funds vs. Nifty 50 and Nifty 100, displaying their **Tracking Errors**.

### 4.2. Deliverables Under `Capstone - Mutual Fund Analytics/`
- `notebooks/Performance_Analytics.ipynb` (Jupyter Notebook with pre-rendered cells)
- `data/processed/fund_scorecard.csv` (Scorecard table of all 40 funds)
- `data/processed/alpha_beta.csv` (Regression details against Nifty 100)
- `reports/figures/benchmark_comparison.png` (Comparison chart)
- `reports/Performance_Report.md` (Executive summary report)

---

## Part 5: GitHub Version Control Summary

All changes have been staged, committed, and pushed directly to your remote repository on the `main` branch:
- **Repository**: `https://github.com/akashimuthu27/Bluestock.git`
- **Branch**: `main`
- **Performance Analytics Commit**: `"Capstone I: Advanced performance analytics complete"` (Commit hash: `b0d6377`)
- **Dashboard Commit**: `"Day 3: Dashboard data prepared + PDF compiled"` (Commit hash: `69e5984`)
- **Day 2 Commit**: `"Day 2: Cleaned data + SQLite DB loaded"` (Commit hash: `a4f2e52`)
- **Capstone Commit**: `"Capstone I: Mutual fund EDA and charts complete"` (Commit hash: `861de29`)
- **Working Tree**: Completely clean, verified by `git status`.
