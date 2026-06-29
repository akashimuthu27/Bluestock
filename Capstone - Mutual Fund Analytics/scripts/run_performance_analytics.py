import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting styles
plt.rcParams['font.family'] = 'sans-serif'
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (11, 6)
plt.rcParams['figure.dpi'] = 150

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Capstone - Mutual Fund Analytics"
data_raw_dir = os.path.join(base_dir, "data", "raw")
data_processed_dir = os.path.join(base_dir, "data", "processed")
figures_dir = os.path.join(base_dir, "reports", "figures")
os.makedirs(data_processed_dir, exist_ok=True)
os.makedirs(figures_dir, exist_ok=True)

print("Starting Advanced Performance Analytics...")

# Load datasets
df_nav = pd.read_csv(os.path.join(data_raw_dir, "nav_history_40.csv"))
df_schemes = pd.read_csv(os.path.join(data_raw_dir, "scheme_master_40.csv"))
df_benchmarks = pd.read_csv(os.path.join(data_raw_dir, "fact_benchmark_indices.csv"))

# Parse dates
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_benchmarks['date'] = pd.to_datetime(df_benchmarks['date'])

# Sort dates
df_nav.sort_values(by=['scheme_code', 'date'], inplace=True)
df_benchmarks.sort_values(by='date', inplace=True)

# Compute daily returns for benchmarks
df_benchmarks['nifty50_ret'] = df_benchmarks['nifty_50'].pct_change()
df_benchmarks['nifty100_ret'] = df_benchmarks['nifty_100'].pct_change()
df_benchmarks.dropna(inplace=True)

# Risk-free rate (RBI repo rate proxy)
rf_annual = 0.065
rf_daily = rf_annual / 252

performance_results = []
alpha_beta_results = []

# List of all schemes
scheme_codes = df_schemes['scheme_code'].unique()

print("Calculating financial metrics for all 40 funds...")
for code in scheme_codes:
    scheme_name = df_schemes[df_schemes['scheme_code'] == code]['scheme_name'].values[0]
    category = df_schemes[df_schemes['scheme_code'] == code]['category'].values[0]
    
    # Get NAV series
    df_fund_nav = df_nav[df_nav['scheme_code'] == code].copy().sort_values(by='date')
    df_fund_nav['daily_return'] = df_fund_nav['nav'].pct_change()
    
    # Drop first row since it's NaN
    df_fund_clean = df_fund_nav.dropna(subset=['daily_return'])
    
    if len(df_fund_clean) < 100:
        print(f"Skipping scheme {code} due to insufficient data.")
        continue
        
    # 1. Daily Returns Distribution check
    # (We will plot this in the notebook)
    
    # 2. Compute CAGR (1yr, 3yr, 5yr)
    # 5Yr: Jan 2022 to Dec 2026
    nav_start_5y = df_fund_nav['nav'].iloc[0]
    nav_end_5y = df_fund_nav['nav'].iloc[-1]
    cagr_5yr = (nav_end_5y / nav_start_5y) ** (1.0 / 5.0) - 1.0
    
    # 3Yr: Dec 2023 to Dec 2026
    df_3y = df_fund_nav[(df_fund_nav['date'] >= '2023-12-31') & (df_fund_nav['date'] <= '2026-12-31')]
    nav_start_3y = df_3y['nav'].iloc[0]
    nav_end_3y = df_3y['nav'].iloc[-1]
    cagr_3yr = (nav_end_3y / nav_start_3y) ** (1.0 / 3.0) - 1.0
    
    # 1Yr: Dec 2025 to Dec 2026
    df_1y = df_fund_nav[(df_fund_nav['date'] >= '2025-12-31') & (df_fund_nav['date'] <= '2026-12-31')]
    nav_start_1y = df_1y['nav'].iloc[0]
    nav_end_1y = df_1y['nav'].iloc[-1]
    cagr_1yr = (nav_end_1y / nav_start_1y) ** (1.0 / 1.0) - 1.0
    
    # 3. Sharpe Ratio
    mean_daily_ret = df_fund_clean['daily_return'].mean()
    std_daily_ret = df_fund_clean['daily_return'].std()
    annualized_return = mean_daily_ret * 252
    annualized_vol = std_daily_ret * np.sqrt(252)
    
    sharpe = (annualized_return - rf_annual) / annualized_vol if annualized_vol > 0 else 0
    
    # 4. Sortino Ratio
    downside_returns = df_fund_clean['daily_return'].copy()
    downside_returns[downside_returns > 0] = 0
    downside_vol = np.sqrt(np.mean(downside_returns ** 2)) * np.sqrt(252)
    
    sortino = (annualized_return - rf_annual) / downside_vol if downside_vol > 0 else 0
    
    # 5. Alpha and Beta (OLS against Nifty 100)
    # Align dates
    df_aligned = pd.merge(df_fund_clean, df_benchmarks, on='date', how='inner')
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_aligned['nifty100_ret'], df_aligned['daily_return']
    )
    beta = slope
    alpha_annual = intercept * 252
    r_squared = r_value ** 2
    
    alpha_beta_results.append({
        "scheme_code": code,
        "scheme_name": scheme_name,
        "beta": round(beta, 4),
        "alpha_annual": round(alpha_annual * 100, 2), # in percentage
        "r_squared": round(r_squared, 4),
        "p_value": round(p_value, 6)
    })
    
    # 6. Maximum Drawdown & worst drawdown date range
    df_fund_nav['running_max'] = df_fund_nav['nav'].cummax()
    df_fund_nav['drawdown'] = df_fund_nav['nav'] / df_fund_nav['running_max'] - 1.0
    
    max_dd = df_fund_nav['drawdown'].min()
    trough_idx = df_fund_nav['drawdown'].idxmin()
    trough_date = df_fund_nav.loc[trough_idx, 'date']
    
    # Peak date is the date of the running max at the trough date
    peak_date = df_fund_nav.loc[:trough_idx, 'nav'].idxmax()
    peak_date = df_fund_nav.loc[peak_date, 'date']
    
    # Generate expense ratio (simulated between 0.1% and 2.2% based on category)
    if category == "Equity":
        expense_ratio = np.random.uniform(1.2, 2.2)
    elif category == "Hybrid":
        expense_ratio = np.random.uniform(0.8, 1.6)
    else: # Debt / Sol oriented
        expense_ratio = np.random.uniform(0.2, 0.9)
    expense_ratio = round(expense_ratio, 2)
    
    performance_results.append({
        "scheme_code": code,
        "scheme_name": scheme_name,
        "category": category,
        "cagr_1yr": round(cagr_1yr * 100, 2),
        "cagr_3yr": round(cagr_3yr * 100, 2),
        "cagr_5yr": round(cagr_5yr * 100, 2),
        "annualized_return": round(annualized_return * 100, 2),
        "volatility": round(annualized_vol * 100, 2),
        "sharpe_ratio": round(sharpe, 4),
        "sortino_ratio": round(sortino, 4),
        "alpha_pct": round(alpha_annual * 100, 2),
        "beta": round(beta, 4),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "drawdown_peak": peak_date.strftime("%Y-%m-%d"),
        "drawdown_trough": trough_date.strftime("%Y-%m-%d"),
        "expense_ratio": expense_ratio
    })

df_perf_results = pd.DataFrame(performance_results)
df_alpha_beta = pd.DataFrame(alpha_beta_results)

# 7. Fund Scorecard (0-100)
print("Building composite Fund Scorecard...")
# Calculate percentile ranks (higher is better for cagr, sharpe, alpha, max_dd)
df_perf_results['cagr_3yr_rank'] = df_perf_results['cagr_3yr'].rank(pct=True) * 100.0
df_perf_results['sharpe_rank'] = df_perf_results['sharpe_ratio'].rank(pct=True) * 100.0
df_perf_results['alpha_rank'] = df_perf_results['alpha_pct'].rank(pct=True) * 100.0
# Max drawdown is negative, so higher value (closer to 0) is better
df_perf_results['max_dd_rank'] = df_perf_results['max_drawdown_pct'].rank(pct=True) * 100.0
# Expense ratio is lower is better, so we rank in descending order
df_perf_results['expense_ratio_rank'] = df_perf_results['expense_ratio'].rank(pct=True, ascending=False) * 100.0

# Composite score formula:
# 30% * 3Yr return rank + 25% * Sharpe rank + 20% * Alpha rank + 15% * expense rank + 10% * max DD rank
df_perf_results['composite_score'] = (
    0.30 * df_perf_results['cagr_3yr_rank'] +
    0.25 * df_perf_results['sharpe_rank'] +
    0.20 * df_perf_results['alpha_rank'] +
    0.15 * df_perf_results['expense_ratio_rank'] +
    0.10 * df_perf_results['max_dd_rank']
)
df_perf_results['composite_score'] = np.round(df_perf_results['composite_score'], 2)

# Sort by composite score
df_scorecard = df_perf_results.sort_values(by='composite_score', ascending=False).copy()
df_scorecard['rank'] = range(1, len(df_scorecard) + 1)

# Save deliverables
scorecard_path = os.path.join(data_processed_dir, "fund_scorecard.csv")
alpha_beta_path = os.path.join(data_processed_dir, "alpha_beta.csv")

df_scorecard.to_csv(scorecard_path, index=False)
df_alpha_beta.to_csv(alpha_beta_path, index=False)

print(f"Saved fund_scorecard.csv with {len(df_scorecard)} funds.")
print(f"Saved alpha_beta.csv with {len(df_alpha_beta)} funds.")

# 8. Benchmark Comparison Chart
print("Plotting Benchmark Comparison Chart for Top 5 Funds vs Nifty 50 & Nifty 100 over 3 years...")
top_5_schemes = df_scorecard.head(5)['scheme_code'].tolist()
top_5_names = df_scorecard.head(5)['scheme_name'].tolist()

# Filter NAV and benchmarks for the 3-year period (2024-01-01 to 2026-12-31)
start_date_3y = '2024-01-01'
end_date_3y = '2026-12-31'

df_bench_3y = df_benchmarks[(df_benchmarks['date'] >= start_date_3y) & (df_benchmarks['date'] <= end_date_3y)].copy().sort_values(by='date')
df_bench_3y['nifty50_cum_ret'] = (1.0 + df_bench_3y['nifty50_ret']).cumprod() - 1.0
df_bench_3y['nifty100_cum_ret'] = (1.0 + df_bench_3y['nifty100_ret']).cumprod() - 1.0

plt.figure(figsize=(12, 6.5))

# Plot Nifty 50 and Nifty 100
plt.plot(df_bench_3y['date'], df_bench_3y['nifty50_cum_ret'] * 100.0, label="Nifty 50 (Benchmark)", color='black', linewidth=2.0, linestyle='--')
plt.plot(df_bench_3y['date'], df_bench_3y['nifty100_cum_ret'] * 100.0, label="Nifty 100 (Benchmark)", color='dimgray', linewidth=2.0, linestyle=':')

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for idx, (code, name) in enumerate(zip(top_5_schemes, top_5_names)):
    df_fund_nav = df_nav[(df_nav['scheme_code'] == code) & (df_nav['date'] >= start_date_3y) & (df_nav['date'] <= end_date_3y)].copy().sort_values(by='date')
    df_fund_nav['daily_return'] = df_fund_nav['nav'].pct_change()
    df_fund_nav['cum_return'] = (1.0 + df_fund_nav['daily_return'].fillna(0)).cumprod() - 1.0
    
    # Calculate Tracking Error against Nifty 100
    df_aligned = pd.merge(df_fund_nav.dropna(subset=['daily_return']), df_bench_3y, on='date', how='inner')
    tracking_error = np.std(df_aligned['daily_return'] - df_aligned['nifty100_ret']) * np.sqrt(252.0)
    
    # Clean name for legend
    short_name = name.replace(" Mutual Fund", "").replace(" Fund", "")
    plt.plot(
        df_fund_nav['date'], df_fund_nav['cum_return'] * 100.0,
        label=f"{short_name} (TE: {tracking_error*100.0:.2f}%)",
        color=colors[idx], linewidth=1.8
    )

plt.title("3-Year Cumulative Returns: Top 5 Funds vs. Benchmarks (2024-2026)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Date", fontsize=11, labelpad=10)
plt.ylabel("Cumulative Return (%)", fontsize=11, labelpad=10)
plt.legend(loc="upper left", frameon=True, shadow=True, title="Schemes & Tracking Error (TE)")
plt.tight_layout()

chart_path = os.path.join(figures_dir, "benchmark_comparison.png")
plt.savefig(chart_path, dpi=150)
plt.close()

print(f"Benchmark comparison chart saved successfully at: {chart_path}")
print("Advanced Performance Analytics completed successfully!")
