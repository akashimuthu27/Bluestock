# Data Quality Report - Day 1 Ingestion

This report evaluates the quality, completeness, and integrity of the datasets loaded during the Day 1 Data Ingestion phase of the Bluestock project.

## 1. Executive Summary
During this ingestion cycle, a total of **10 datasets** were loaded and analyzed. This includes **4 local datasets** (fund master, historical NAVs, user portfolio, and scheme categories) and **6 live NAV datasets** fetched directly from the AMFI API. While the live data is clean and consistent, structural and quality issues (duplicates, missing fields, and scheme discrepancies) were discovered in the master files.

---

## 2. Ingestion Profile
Below is a summary of all 10 datasets processed during the ingestion phase:

| Dataset Name | Source Type | Row Count | Column Count | Missing Values | Duplicate Rows | Key Fields |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fund_master` | Local CSV | 12 | 6 | 2 | 2 | `scheme_code`, `scheme_name`, `fund_house`, `category` |
| `nav_history` | Local CSV | 242 | 3 | 1 | 1 | `scheme_code`, `nav`, `date` |
| `user_portfolio` | Local CSV | 4 | 4 | 0 | 0 | `scheme_code`, `units_held`, `purchase_nav`, `purchase_date` |
| `scheme_categories`| Local CSV | 4 | 3 | 0 | 0 | `category_id`, `category_name`, `description` |
| `sbi_bluechip_119551` | Live API | 3,250 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |
| `icici_bluechip_120503` | Live API | 3,321 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |
| `nippon_large_cap_118632` | Live API | 3,312 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |
| `axis_bluechip_119092` | Live API | 3,579 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |
| `kotak_bluechip_120841` | Live API | 3,315 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |
| `hdfc_top_100_125497` | Live API | 3,105 | 4 | 0 | 0 | `date`, `nav`, `scheme_code`, `scheme_name` |

---

## 3. Data Quality Findings

### A. Missing Value Observations
- **`fund_master`**:
  - `category` contains **1 missing value**.
  - `risk_grade` contains **1 missing value**.
- **`nav_history`**:
  - `nav` contains **1 missing value** (a null value in the historical timeseries).
- **Live NAV & Other Files**:
  - No missing values found.

### B. Duplicate Observations
- **`fund_master`**: Contains **2 duplicate rows** (exact copies of scheme rows injected to test robustness).
- **`nav_history`**: Contains **1 duplicate row**.
- **Live NAV & Other Files**: No duplicates found.

### C. Data Type Issues
- **Date Format**: The `date` and `purchase_date` columns in the CSVs are currently stored as strings (`str`/`object`). For timeseries analysis, this needs to be parsed as a native `datetime64[ns]` format.
- **Scheme Code Type**: Scheme codes are integers, but in scenarios with poor formatting, they risk being read as floats. They must be explicitly cast to `int64`.

---

## 4. AMFI Validation Findings
We verified whether every `scheme_code` in the `fund_master` dataset had matching historical records in `nav_history`.

- **Total Unique Scheme Codes in Master**: 10
- **Total Unique Scheme Codes in History**: 8
- **Matching Scheme Codes**: 8 (80.00%)
- **Missing Scheme Codes in History**: 2

### Missing Scheme Details:
The following schemes exist in the master record but have **no corresponding NAV history** in `nav_history.csv`:

1. **Scheme Code 119999**: HDFC Top 100 Fund - Direct Plan - Growth (HDFC Mutual Fund)
2. **Scheme Code 120999**: Kotak Debt Hybrid Fund - Direct Plan - Growth (Kotak Mahindra Mutual Fund)

---

## 5. Recommendations for Data Cleaning

1. **Deduplication**: 
   - Apply `.drop_duplicates(inplace=True)` on the `fund_master` and `nav_history` datasets before running downstream analytics to prevent inflated records.
2. **Missing Value Imputation**:
   - **Categorical fields in master**: Manually research and fill missing values for `category` and `risk_grade` or drop them if they are non-critical.
   - **NAV timeseries**: Impute missing `nav` values in `nav_history` using forward-fill (`ffill()`) or linear interpolation since NAV is continuous and sequential.
3. **Data Type Standardization**:
   - Explicitly cast date strings using `pd.to_datetime(df['date'], format='%Y-%m-%d')`.
   - Cast scheme codes using `df['scheme_code'].astype(int)`.
4. **Referential Integrity Remediation**:
   - Investigate why historical NAV records for scheme codes `119999` and `120999` are absent. 
   - Fetch the missing historical data from the AMFI API (using `live_nav_fetch.py`) to reconcile the validation gaps.
