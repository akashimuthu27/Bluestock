import os
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Capstone - Mutual Fund Analytics"
notebook_path = os.path.join(base_dir, "notebooks", "Performance_Analytics.ipynb")
notebooks_dir = os.path.join(base_dir, "notebooks")

print("Initializing Jupyter Notebook compilation for Performance Analytics...")

nb = nbf.v4.new_notebook()

# ---------------------------------------------------------
# Cells definitions
# ---------------------------------------------------------
cells = []

# Title & Metadata
cells.append(nbf.v4.new_markdown_cell("""# Capstone Project I: Advanced Mutual Fund Performance Analytics
## Quantitative Evaluation of 40 Mutual Fund Schemes (2022 - 2026)

This notebook contains the advanced quantitative performance evaluation for **Capstone Project I - Mutual Fund Analytics**. The study covers daily returns distribution, 1Yr/3Yr/5Yr CAGR, risk-adjusted metrics (Sharpe and Sortino ratios), regression-based Alpha and Beta against Nifty 100, Maximum Drawdowns with their peak-to-trough date ranges, and a composite Fund Scorecard (0-100).

### Analytical Framework
- **Section 1: Data Ingestion & Return Computation**
- **Section 2: Daily Returns Distribution & Normality Validation**
- **Section 3: Multi-Period CAGR Comparison (1Yr, 3Yr, 5Yr)**
- **Section 4: Risk-Adjusted Ratios (Sharpe & Sortino Ratios)**
- **Section 5: Regression Analysis (Alpha, Beta, & R-Squared)**
- **Section 6: Maximum Drawdown & Peak-to-Trough Date Ranges**
- **Section 7: Composite Fund Scorecard (0 - 100)**
- **Section 8: 3-Year Benchmark Comparison & Tracking Error**

---
"""))

# Imports
cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Setup styles
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (11, 5.5)
plt.rcParams['figure.dpi'] = 120

# Define data paths
data_dir = r"../data"
print("Environment set up and libraries imported.")
"""))

# Data Loading
cells.append(nbf.v4.new_markdown_cell("""### Data Loading & Ingestion
We load the daily NAV history, benchmark index data, and computed performance summaries."""))

cells.append(nbf.v4.new_code_cell("""df_nav = pd.read_csv(os.path.join(data_dir, "raw", "nav_history_40.csv"))
df_schemes = pd.read_csv(os.path.join(data_dir, "raw", "scheme_master_40.csv"))
df_benchmarks = pd.read_csv(os.path.join(data_dir, "raw", "fact_benchmark_indices.csv"))
df_scorecard = pd.read_csv(os.path.join(data_dir, "processed", "fund_scorecard.csv"))
df_alpha_beta = pd.read_csv(os.path.join(data_dir, "processed", "alpha_beta.csv"))

# Parse dates
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_benchmarks['date'] = pd.to_datetime(df_benchmarks['date'])

print(f"Loaded NAV records: {df_nav.shape[0]}")
print(f"Loaded Benchmark index records: {df_benchmarks.shape[0]}")
print(f"Loaded Scorecard records: {df_scorecard.shape[0]}")
"""))

# Section 2: Returns Distribution
cells.append(nbf.v4.new_markdown_cell("""## Section 2: Daily Returns Distribution & Normality Validation

We compute the daily return:
$$R_t = \\frac{NAV_t}{NAV_{t-1}} - 1$$

We validate the distribution of returns for a representative fund (e.g., scheme 100000) using a histogram and a Q-Q plot to verify if they exhibit normal distribution properties with typical financial market fat tails."""))

cells.append(nbf.v4.new_code_cell("""# Select a representative fund (SBI Mutual Fund Equity Fund 1)
code_rep = 100000
df_rep = df_nav[df_nav['scheme_code'] == code_rep].copy().sort_values(by='date')
df_rep['daily_return'] = df_rep['nav'].pct_change()
df_rep_clean = df_rep.dropna()

# Plot histogram of returns
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

sns.histplot(df_rep_clean['daily_return'], kde=True, ax=axes[0], color='royalblue', bins=50)
axes[0].set_title("Histogram of Daily Returns (Scheme 100000)", fontsize=11, fontweight='bold')
axes[0].set_xlabel("Daily Return")
axes[0].set_ylabel("Frequency")

# Q-Q Plot
stats.probplot(df_rep_clean['daily_return'], dist="norm", plot=axes[1])
axes[1].set_title("Normal Q-Q Plot", fontsize=11, fontweight='bold')
axes[1].get_lines()[0].set_color('royalblue')
axes[1].get_lines()[1].set_color('darkorange')

plt.tight_layout()
plt.show()

# Print skewness and kurtosis
skew = df_rep_clean['daily_return'].skew()
kurt = df_rep_clean['daily_return'].kurt()
print(f"Skewness: {skew:.4f} (Ideal normal = 0)")
print(f"Kurtosis: {kurt:.4f} (Ideal normal = 0, positive indicates fat tails)")
"""))

# Section 3: CAGR comparison
cells.append(nbf.v4.new_markdown_cell("""## Section 3: Multi-Period CAGR Comparison (1Yr, 3Yr, 5Yr)

We evaluate the Compound Annual Growth Rate (CAGR) across three horizons:
- **1-Year CAGR** (2026)
- **3-Year CAGR** (2024–2026)
- **5-Year CAGR** (2022–2026)

Formula:
$$CAGR = \\left(\\frac{NAV_{end}}{NAV_{start}}\\right)^{\\frac{1}{n}} - 1$$
"""))

cells.append(nbf.v4.new_code_cell("""# Display the top 10 funds by 3-Year CAGR
df_cagr_table = df_scorecard[['rank', 'scheme_name', 'category', 'cagr_1yr', 'cagr_3yr', 'cagr_5yr']].copy()
df_cagr_table.columns = ['Rank', 'Scheme Name', 'Category', '1-Yr CAGR (%)', '3-Yr CAGR (%)', '5-Yr CAGR (%)']
df_cagr_table.head(10)
"""))

# Section 4: Risk-adjusted ratios
cells.append(nbf.v4.new_markdown_cell("""## Section 4: Risk-Adjusted Ratios (Sharpe & Sortino Ratios)

We calculate the **Sharpe Ratio** (using standard deviation) and the **Sortino Ratio** (using downside standard deviation) to measure the risk-adjusted excess returns over the risk-free rate of **6.5%**:

$$\\text{Sharpe} = \\frac{R_p - R_f}{\\sigma_p} \\times \\sqrt{252}$$
$$\\text{Sortino} = \\frac{R_p - R_f}{\\sigma_{downside}} \\times \\sqrt{252}$$
"""))

cells.append(nbf.v4.new_code_cell("""# Display Sharpe and Sortino Ratios
df_ratios = df_scorecard[['rank', 'scheme_name', 'category', 'annualized_return', 'volatility', 'sharpe_ratio', 'sortino_ratio']].copy()
df_ratios.columns = ['Rank', 'Scheme Name', 'Category', 'Ann. Return (%)', 'Ann. Volatility (%)', 'Sharpe Ratio', 'Sortino Ratio']
df_ratios.head(10)
"""))

# Section 5: Regression Analysis
cells.append(nbf.v4.new_markdown_cell("""## Section 5: Regression Analysis (Alpha, Beta, & R-Squared)

Using Ordinary Least Squares (OLS) regression against the **Nifty 100** daily returns, we calculate the fund's **Beta** (market sensitivity) and **Alpha** (excess return relative to benchmark):

$$R_{fund} = \\alpha + \\beta \\times R_{Nifty100} + \\epsilon$$
$$\\text{Annualized Alpha} = \\alpha_{daily} \\times 252$$
"""))

cells.append(nbf.v4.new_code_cell("""# Display Alpha, Beta and R-Squared
df_regression = df_scorecard[['rank', 'scheme_name', 'category', 'alpha_pct', 'beta']].copy()
df_regression.columns = ['Rank', 'Scheme Name', 'Category', 'Annualized Alpha (%)', 'Beta']
df_regression.head(10)
"""))

# Section 6: Maximum Drawdown
cells.append(nbf.v4.new_markdown_cell("""## Section 6: Maximum Drawdown & Peak-to-Trough Date Ranges

**Maximum Drawdown** represents the largest peak-to-trough drop in a fund's NAV before a new peak is achieved:
$$MDD = \\min\\left(\\frac{NAV_t}{\\text{Running Max } NAV} - 1\\right)$$
"""))

cells.append(nbf.v4.new_code_cell("""# Display Maximum Drawdown and Date Ranges
df_drawdown = df_scorecard[['rank', 'scheme_name', 'category', 'max_drawdown_pct', 'drawdown_peak', 'drawdown_trough']].copy()
df_drawdown.columns = ['Rank', 'Scheme Name', 'Category', 'Max Drawdown (%)', 'Worst Peak Date', 'Worst Trough Date']
df_drawdown.head(10)
"""))

# Section 7: Composite Scorecard
cells.append(nbf.v4.new_markdown_cell("""## Section 7: Composite Fund Scorecard (0 - 100)

The **Fund Scorecard** is a composite metric from 0 to 100 based on weighted percentile ranks:
- **30%**: 3-Year CAGR Rank
- **25%**: Sharpe Ratio Rank
- **20%**: Annualized Alpha Rank
- **15%**: Expense Ratio Rank (inverse)
- **10%**: Maximum Drawdown Rank (inverse)
"""))

cells.append(nbf.v4.new_code_cell("""# Display Top 15 Funds by Scorecard
df_score_table = df_scorecard[['rank', 'scheme_name', 'category', 'composite_score', 'expense_ratio', 'max_drawdown_pct', 'sharpe_ratio']].copy()
df_score_table.columns = ['Rank', 'Scheme Name', 'Category', 'Composite Score (0-100)', 'Expense Ratio (%)', 'Max Drawdown (%)', 'Sharpe Ratio']
df_score_table.head(15)
"""))

# Section 8: Benchmark Comparison Plot
cells.append(nbf.v4.new_markdown_cell("""## Section 8: 3-Year Benchmark Comparison & Tracking Error

We plot the 3-year cumulative returns (2024–2026) for the **top 5 funds** against the **Nifty 50** and **Nifty 100** indexes. We also calculate the **Tracking Error** against Nifty 100:

$$\\text{Tracking Error} = \\sigma(R_p - R_b) \\times \\sqrt{252}$$
"""))

cells.append(nbf.v4.new_code_cell("""# Display pre-generated chart
from IPython.display import Image, display
chart_path = os.path.join("..", "reports", "figures", "benchmark_comparison.png")
if os.path.exists(chart_path):
    display(Image(filename=chart_path))
else:
    print("Benchmark comparison chart not found. Please run the analytics script.")
"""))

# End note
cells.append(nbf.v4.new_markdown_cell("""---
### Conclusion
This concludes the Advanced Mutual Fund Performance Analytics. The composite scorecard highlights the funds that optimized risk-adjusted returns (high Sharpe/Sortino), generated positive active manager alpha, and minimized downside drawdowns during market corrections.
"""))

# Add cells to notebook
nb['cells'] = cells

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print(f"Notebook created at {notebook_path}.")

# ---------------------------------------------------------
# Run execution to pre-render
# ---------------------------------------------------------
print("Executing notebook to pre-render cell outputs...")
try:
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': notebooks_dir}})
    
    # Save the executed notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Notebook executed and pre-rendered successfully!")
except Exception as e:
    print(f"Error executing notebook: {e}")
    print("Saving unexecuted notebook so it is still present.")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
