# Capstone Project I: Mutual Fund Analytics

This directory contains the complete implementation for **Capstone Project I - Mutual Fund Analytics** as part of the Bluestock Internship. It implements a complete, self-contained financial exploratory data analysis pipeline, generating 8 realistic datasets, plotting 16 professional, high-resolution charts, and compiling a pre-rendered Jupyter Notebook containing exactly 10 key findings.

## Directory Structure

```text
Capstone - Mutual Fund Analytics/
├── data/
│   ├── raw/                      # Generated CSV datasets (8 files + scheme master)
│   └── processed/                # Performance metrics and cleaned data
├── notebooks/
│   └── EDA_Analysis.ipynb        # Pre-rendered Jupyter Notebook with all 16 charts & 10 insights
├── reports/
│   ├── figures/                  # Exported high-resolution PNG charts (16 charts)
│   └── Capstone_EDA_Report.md    # Summary executive report of the analysis
├── scripts/
│   ├── generate_data.py          # Programmatic data generator
│   ├── generate_charts.py        # Professional chart generator (exports 16 PNGs)
│   └── compile_notebook.py       # Programmatic notebook compiler and executor
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation and execution instructions
```

## How to Execute the Pipeline

To run the entire pipeline from scratch and regenerate all data, charts, and the notebook:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the Datasets**:
   This script creates the 8 raw CSV datasets containing realistic financial trends and exact target figures.
   ```bash
   python scripts/generate_data.py
   ```

3. **Generate the Charts**:
   This script performs calculations (CAGR, daily returns, volatility) and exports 16 professional, publication-ready PNG charts to `reports/figures/`.
   ```bash
   python scripts/generate_charts.py
   ```

4. **Compile and Pre-render the Jupyter Notebook**:
   This script structures the Jupyter Notebook using `nbformat`, embeds all chart plotting codes (including interactive Plotly code), documents the 10 key insights, and runs the notebook to pre-render all cell outputs and charts.
   ```bash
   python scripts/compile_notebook.py
   ```

## Datasets Generated
1. `nav_history_40.csv`: Daily NAV time-series for 40 schemes (2022-2026), simulating the **2023 Bull Run** and the **2024 Market Correction**.
2. `aum_growth.csv`: Yearly AUM (2022-2025) for 6 major fund houses, with **SBI Mutual Fund peaking at exactly ₹12.5L Cr in 2025**.
3. `sip_inflow.csv`: Monthly SIP inflows (Jan 2022 - Dec 2025), peaking at an **all-time high of exactly ₹31,002 Cr in Dec 2025**.
4. `category_inflow.csv`: Monthly net inflows per category (Equity, Debt, Hybrid, etc.).
5. `investor_demographics.csv`: Demographic details of 10,000 active investors, with realistic age, gender, and ticket size distributions.
6. `geo_state_summary.csv` / `geo_tier_summary.csv`: State-wise and city-tier (T30 vs B30) contributions derived from demographic data for perfect consistency.
7. `folio_growth.csv`: Monthly mutual fund folios in India growing from **exactly 13.26 Cr in Jan 2022 to exactly 26.12 Cr in Dec 2025**.
8. `portfolio_holdings.csv`: Stock-level portfolio holdings across 10 sectors for equity schemes.

## The 16 Visualizations Created
1. **NAV Trend Analysis**: Daily NAV for 40 schemes (2022-2026), with shaded bands for the 2023 Bull Run and 2024 Correction.
2. **AUM Growth Bar Chart**: Grouped bar chart showing yearly AUM by fund house, highlighting SBI's dominance.
3. **SIP Inflow Time-Series**: Monthly SIP trend (Jan 2022 - Dec 2025) with a red annotation point for the ₹31,002 Cr peak in Dec 2025.
4. **Category Inflow Heatmap**: Inflow intensity by category and month (Jan 2022 - Dec 2025).
5. **Age Group Distribution**: Pie chart of investor age groups.
6. **SIP Amount Box Plot by Age Group**: Ticket size distributions across age groups.
7. **Gender Distribution Split**: Donut chart representing the gender split among active investors.
8. **State-wise SIP Contribution**: Horizontal bar chart showing total SIP volume by state.
9. **City Tier Contribution**: Donut chart showing the T30 (Top 30 cities) vs B30 (Beyond 30 cities) percentage distribution.
10. **Folio Count Growth**: Monthly line chart from 13.26 Cr to 26.12 Cr, marking major milestones.
11. **Daily Return Correlation Matrix**: Pairwise correlation heatmap of daily returns for 10 selected schemes.
12. **Sector Allocation Donut**: Consolidated sector weights across all equity portfolios.
13. **Risk vs. Return Frontier**: Scatter plot showing annualized volatility (Risk) vs. CAGR (Return) for all 40 schemes.
14. **Monthly Category Inflow Share**: Stacked area chart showing how investor allocation shifted dynamically over time.
15. **AUM Size Distribution in 2025**: Histogram showing the size distribution of the 40 schemes.
16. **Top 10 Stocks Held Across Equity Portfolios**: Aggregated weight of specific stock holdings across the equity mutual funds.
