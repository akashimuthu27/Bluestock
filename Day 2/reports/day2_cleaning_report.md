# Data Cleaning and Financial EDA Report - Day 2

This report evaluates the execution, findings, and results of the **Day 2: Data Cleaning & Financial EDA** pipeline for the Bluestock project. 

---

## 1. Data Cleaning & Anomaly Resolution

During the profiling of the 10 raw datasets, two major data quality anomalies were identified and programmatically resolved:

1. **Zero NAV Anomaly (`icici_bluechip_120503.csv`)**:
   - **Problem**: A highly anomalous `0.0` NAV value was detected in the historical records, which completely distorted volatility calculations (reducing it to 0.00%) and max drawdown (dropping it to -100.00%).
   - **Resolution**: The pipeline now automatically treats NAV values $\leq 0$ as invalid, replaces them with `NaN`, and imputes them using timeseries forward-fill followed by backward-fill. Volatility and drawdown are now perfectly restored.
   
2. **Structural 100x Decimal Scale Break (`axis_bluechip_119092.csv`)**:
   - **Problem**: A sudden 100-fold jump in NAV was detected on `2015-08-30` (from `30.22` to `3023.47`), representing a historical redenomination or decimal placement error in the AMFI source dataset. This created an artificial +9,900% daily return, distorting volatility to `2628.45%`.
   - **Resolution**: The pipeline implements a programmatic structural break detector. If a daily return jumps by roughly 100x and stays at that level permanently, all historical NAVs prior to the break are scaled up by 100x. This smoothed the transition (reducing the daily jump to a normal +0.04%), restoring the true volatility to `0.54%`.

---

## 2. Ingestion & Cleaning Profiling
Below is the final profiling of the 10 cleaned datasets saved in `Day 2/data/processed/`:

| Dataset Name | Initial Rows | Cleaned Rows | Missing Values Resolved | Duplicates Removed | Key Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `fund_master` | 12 | 12 | 2 (`category`, `risk_grade`) | 0 | Clean & Complete |
| `nav_history` | 242 | 241 | 1 (`nav`) | 1 | Deduplicated & Filled |
| `user_portfolio` | 4 | 4 | 0 | 0 | Clean |
| `scheme_categories`| 4 | 4 | 0 | 0 | Clean |
| `sbi_bluechip_119551` | 3,250 | 3,250 | 0 | 0 | Outliers Checked |
| `icici_bluechip_120503` | 3,321 | 3,321 | 1 (`0.0` NAV resolved) | 0 | Restored & Cleaned |
| `nippon_large_cap_118632` | 3,312 | 3,312 | 0 | 0 | Outliers Checked |
| `axis_bluechip_119092` | 3,579 | 3,579 | 0 (100x break adjusted) | 0 | Volatility Restored |
| `kotak_bluechip_120841` | 3,315 | 3,315 | 0 | 0 | Outliers Checked |
| `hdfc_top_100_125497` | 3,105 | 3,105 | 0 | 0 | Outliers Checked |

---

## 3. Financial Performance Metrics Summary
We engineered key performance and risk indicators for each of the 6 large-cap funds based on their complete historical NAV curves:

| Fund Name (Scheme Code) | Duration (Years) | Start NAV | End NAV | Annualized CAGR | Ann. Volatility | Sharpe Ratio (Rf = 6%) | Max Drawdown |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **SBI Bluechip** (119551) | 13.48 | 103.01 | 103.20 | **0.21%** | 8.70% | -0.67 | -36.65% |
| **ICICI Bluechip** (120503) | 13.48 | 15.03 | 113.68 | **15.78%** | 15.31% | 0.64 | -33.51% |
| **Nippon India Large Cap** (118632) | 13.48 | 14.70 | 102.72 | **15.38%** | 16.69% | 0.56 | -39.96% |
| **HDFC Money Market (Axis)** (119092) | 13.48 | 2399.20 | 6195.78 | **7.30%** | 0.54% | 2.41 | -1.39% |
| **Kotak Bluechip** (120841) | 13.46 | 30.61 | 280.99 | **16.96%** | 15.42% | 0.71 | -33.43% |
| **HDFC Top 100** (125497) | 12.44 | 550.00 | 11846.74 | **24.30%** | 15.20% | 1.20 | -40.26% |

### Key Takeaways:
- **Best Performer (CAGR)**: **HDFC Top 100** leads with a spectacular **24.30%** annualized growth rate over 12.44 years.
- **Best Risk-Adjusted Returns (Sharpe)**: **HDFC Money Market (Axis 119092)** shows a Sharpe ratio of **2.41** due to its exceptionally low volatility (0.54%) and consistent 7.30% growth (typical for low-risk liquid debt funds).
- **Correlation Insight**: The correlation heatmap demonstrates that the equity large-cap funds (ICICI, Nippon, Kotak, HDFC Top 100) are **highly correlated (>0.85)** with each other, representing a high level of underlying market asset overlap.
