# Day 2: Data Cleaning and Financial EDA

This sub-repository folder contains the pipeline and notebooks for **Day 2: Data Cleaning & Financial EDA** of the Bluestock project.

## Objectives
1. **Deduplication**: Clean all duplicate rows from datasets.
2. **Missing Value Imputation**: Handle missing fields in metadata and continuous timeseries NAV nulls.
3. **Outlier Detection**: Filter out extreme NAV data spikes using rolling Z-scores.
4. **Structural Anomaly Resolution**: Programmatically scale historical decimals (100x shift breaks).
5. **Feature Engineering**: Compute Compound Annual Growth Rate (CAGR), Annualized Volatility, Sharpe Ratio, and Maximum Drawdown.
6. **Exploratory Data Analysis (EDA)**: Produce visual insights in an interactive Jupyter Notebook.

---

## Folder Structure
```text
Day 2/
├── data/
│   ├── raw/                  # 10 raw CSV datasets copied from Day 1
│   └── processed/            # Cleaned datasets + computed performance metrics
├── notebooks/
│   └── day2_eda.ipynb        # Jupyter Notebook executing financial EDA
├── reports/
│   ├── day2_cleaning_report.md  # Profiling, outlier, and CAGR summary report
│   ├── nav_growth_trends.png
│   ├── performance_metrics_comparison.png
│   └── returns_correlation_heatmap.png
├── scripts/
│   ├── data_cleaning.py      # Cleans datasets, handles zero NAVs & 100x jumps
│   ├── feature_engineering.py # Computes CAGR, Volatility, Sharpe, and Drawdowns
│   └── generate_charts.py    # Generates PNG plots for report embedding
├── requirements.txt          # Python packages
└── README.md                 # Local documentation
```

---

## Technical Implementations

### 1. CAGR (Compound Annual Growth Rate)
We annualize the total return of each fund over its active lifespan:
$$CAGR = \left(\frac{\text{Ending NAV}}{\text{Beginning NAV}}\right)^{\frac{365.25}{\text{Days Active}}} - 1$$

### 2. Annualized Volatility
Measures timeseries dispersion (daily standard deviation annualized):
$$\text{Volatility} = \text{StDev}(R_t) \times \sqrt{252}$$
Where $R_t$ represents the daily percentage returns of NAV.

### 3. Sharpe Ratio
Measures risk-adjusted performance using an Indian market risk-free rate ($R_f = 6.0\%$):
$$\text{Sharpe} = \frac{\text{CAGR} - R_f}{\text{Volatility}}$$

---

## How to Run

Navigate to the `Day 2` folder:
```powershell
cd "C:\Users\AKASH\Desktop\BLUESTOCK\Day 2"
```

Execute the pipeline in sequence:
```powershell
# 1. Clean data, impute nulls, resolve zero NAVs and 100x breaks
python scripts/data_cleaning.py

# 2. Compute CAGR, Volatility, Sharpe, and Drawdowns
python scripts/feature_engineering.py

# 3. Generate PNG visualizations for reports
python scripts/generate_charts.py
```
*Note: You can open and run `notebooks/day2_eda.ipynb` directly in VS Code to interactively view the plots.*
