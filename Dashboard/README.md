# Power BI Dashboard Development: Mutual Fund Analytics

This directory contains the prepared datasets, designed page layouts, compiled PDF, and step-by-step instructions to build the **Bluestock Mutual Fund Analytics Dashboard** in Power BI.

---

## 1. Directory Structure

```text
Dashboard/
├── data/
│   └── raw/                      # The 8 prepared CSV datasets for Power BI
│       ├── dim_fund.csv          # Fund metadata
│       ├── dim_date.csv          # Date dimension
│       ├── fact_nav.csv          # Daily NAV history (holidays filled)
│       ├── fact_transactions.csv  # Investor transactions (SIP/Lumpsum/Redemption)
│       ├── fact_performance.csv  # Fund CAGR and expense ratios
│       ├── fact_aum.csv          # Yearly AUM per AMC
│       ├── fact_market_index.csv  # Nifty 50 historical index (2022-2025)
│       └── investor_demographics.csv # Investor details (age, gender, city tier)
├── reports/
│   ├── figures/                  # Widescreen high-fidelity dashboard page layouts
│   │   ├── page1_industry_overview.png
│   │   ├── page2_fund_performance.png
│   │   ├── page3_investor_analytics.png
│   │   └── page4_market_trends.png
│   └── Dashboard.pdf             # Compiled 4-page dashboard report
└── scripts/
    ├── prepare_data.py           # Prepares and exports the 8 CSV tables
    └── compile_pdf.py            # Copies PNGs and compiles the PDF
```

---

## 2. Power BI Setup & Data Import Guide

Follow these steps to load the datasets and build the dashboard on your local PC:

### Step 2.1: Import the Data
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Navigate to `Dashboard/data/raw/` and import all **8 CSV files** one by one:
   - Click **Load** for each file.
4. Verify in the **Data Pane** (on the right) that all 8 tables are successfully loaded.

### Step 2.2: Set Up Relationships (Model View)
Go to the **Model View** (left sidebar icon) and configure the relationships. Power BI may auto-detect some, but verify and create them as follows:

1. **`dim_fund` to `fact_nav`**:
   - Relationship: `dim_fund[amfi_code]` (1) to `fact_nav[amfi_code]` (*)
   - Cross filter direction: **Single**
2. **`dim_fund` to `fact_transactions`**:
   - Relationship: `dim_fund[amfi_code]` (1) to `fact_transactions[amfi_code]` (*)
   - Cross filter direction: **Single**
3. **`dim_fund` to `fact_performance`**:
   - Relationship: `dim_fund[amfi_code]` (1) to `fact_performance[amfi_code]` (1)
   - Cross filter direction: **Both**
4. **`dim_date` to `fact_nav`**:
   - Relationship: `dim_date[date]` (1) to `fact_nav[date]` (*)
   - Cross filter direction: **Single**
5. **`dim_date` to `fact_transactions`**:
   - Relationship: `dim_date[date]` (1) to `fact_transactions[date]` (*)
   - Cross filter direction: **Single**
6. **`dim_date` to `fact_market_index`**:
   - Relationship: `dim_date[date]` (1) to `fact_market_index[date]` (*)
   - Cross filter direction: **Single**
7. **`investor_demographics` to `fact_transactions`**:
   - Relationship: `investor_demographics[investor_id]` (1) to `fact_transactions[investor_id]` (*)
   - Cross filter direction: **Single**

---

## 3. Dashboard Page Visualizations

Apply the **Bluestock Theme**: Use dark navy blue (`#0A192F` or `#0D1B2A`) for backgrounds, gold/yellow (`#F1C40F`) for accents/highlights, and white for text.

### Page 1: Industry Overview
* **KPI Cards**:
  - **Total AUM**: Create a card using `SUM(fact_aum[aum_cr])` (Format: Display unit = Lakh Crore, custom value = **₹81L Cr**).
  - **SIP Inflows**: Card using `SUM(fact_transactions[amount])` filtered for `transaction_type = "SIP"` (Format: **₹31K Cr**).
  - **Folios**: Card using a constant or count measure of folios (Format: **26.12 Cr**).
  - **Schemes**: Card using `DISTINCTCOUNT(dim_fund[amfi_code])` (Format: **1,908**).
* **Line Chart (AUM Trend)**:
  - **X-axis**: `dim_date[year]`
  - **Y-axis**: `SUM(fact_aum[aum_cr])`
* **Bar Chart (AUM by AMC)**:
  - **Y-axis (axis)**: `fact_aum[fund_house]`
  - **X-axis (values)**: `SUM(fact_aum[aum_cr])` (Sort descending, highlight SBI).

### Page 2: Fund Performance
* **Slicers (Top/Left)**: `dim_fund[fund_house]`, `dim_fund[category]`, `dim_fund[sub_category]`
* **Scatter Plot (Risk vs. Return)**:
  - **X-axis**: `cagr_3yr` (Return)
  - **Y-axis**: `expense_ratio` or standard deviation volatility (Risk)
  - **Bubble Size**: `SUM(fact_aum[aum_cr])` (linked via fund house)
  - **Details**: `dim_fund[scheme_name]`
* **Fund Scorecard Table**:
  - Add a **Table** visual: `dim_fund[scheme_name]`, `dim_fund[category]`, `fact_performance[cagr_3yr]`, `fact_performance[cagr_5yr]`, `fact_performance[expense_ratio]`. Enable sorting on columns.
* **Line Chart (NAV vs. Benchmark)**:
  - **X-axis**: `dim_date[date]`
  - **Y-axis**: `AVG(fact_nav[nav])` and `AVG(fact_market_index[close])` (Dual-axis or scaled).

### Page 3: Investor Analytics
* **Slicers**: `fact_transactions[state]`, `investor_demographics[age_group]`, `investor_demographics[city_tier]`
* **Horizontal Bar Chart (Transactions by State)**:
  - **Y-axis**: `fact_transactions[state]`
  - **X-axis**: `SUM(fact_transactions[amount])`
* **Donut Chart (Transaction Type Split)**:
  - **Legend**: `fact_transactions[transaction_type]`
  - **Values**: `COUNT(fact_transactions[transaction_id])` or `SUM(fact_transactions[amount])`
* **Grouped Column Chart (Age vs. Avg SIP)**:
  - **X-axis**: `investor_demographics[age_group]`
  - **Y-axis**: `AVERAGE(fact_transactions[amount])` (filtered for `transaction_type = "SIP"`)
* **Line Chart (Monthly Volume)**:
  - **X-axis**: `dim_date[month]` (or Year-Month)
  - **Y-axis**: `COUNT(fact_transactions[transaction_id])`

### Page 4: SIP & Market Trends
* **Dual-Axis Chart (SIP vs. Nifty)**:
  - **X-axis**: `dim_date[date]` (grouped by Month)
  - **Column Y-axis**: `SUM(fact_transactions[amount])` (filtered for "SIP")
  - **Line Y-axis**: `AVERAGE(fact_market_index[close])`
* **Heatmap (Category Inflows)**:
  - Use a **Matrix** visual:
    - **Rows**: `dim_fund[category]`
    - **Columns**: `dim_date[month]`
    - **Values**: `SUM(fact_transactions[amount])`
    - **Conditional Formatting**: Apply a **color scale** (background color) to represent net inflow intensity.
* **Bar Chart (Top 5 Categories)**:
  - **Y-axis**: `dim_fund[category]`
  - **X-axis**: `SUM(fact_transactions[amount])` (Filter Top 5 by amount).

---

## 4. Interactivity & Enhancements
1. **Drill-Through**:
   - Create a new page named **NAV Detail**.
   - Add `dim_fund[scheme_name]` to the **Drill-through fields** pane.
   - Design a historical line chart of NAV on this page. Now, when a user right-clicks a fund name in the Page 2 scorecard table, they can select **Drillthrough -> NAV Detail** to view its history.
2. **Tooltips**:
   - Ensure tooltips are enabled on all charts to display exact numbers (e.g., hover over a scatter plot bubble to see the fund name, AUM, CAGR, and expense ratio).
3. **Bluestock Theme**:
   - Import a custom JSON theme or manually configure the background of the pages to dark navy and chart series to navy blue, gold, and teal.
