import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Generating chart images for Day 2 report...")
    
    # Configure styling
    sns.set_theme(style="darkgrid")
    plt.rcParams["figure.figsize"] = (12, 6)
    
    processed_dir = "data/processed"
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    metrics_path = os.path.join(processed_dir, "fund_performance_metrics.csv")
    if not os.path.exists(metrics_path):
        print(f"Metrics file {metrics_path} not found.")
        return
        
    df_metrics = pd.read_csv(metrics_path)
    
    # 1. Historical NAV Growth Trends
    live_files = {
        119551: "sbi_bluechip",
        120503: "icici_bluechip",
        118632: "nippon_large_cap",
        119092: "axis_bluechip",
        120841: "kotak_bluechip",
        125497: "hdfc_top_100"
    }

    plt.figure(figsize=(14, 7))
    for code, name in live_files.items():
        filepath = os.path.join(processed_dir, f"{name}_{code}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            plt.plot(df['date'], df['nav'], label=f"{name.replace('_', ' ').title()} ({code})")

    plt.title("Historical Net Asset Value (NAV) Growth Trends", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("NAV (INR)", fontsize=12)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "nav_growth_trends.png"), dpi=300)
    plt.close()
    print("  - Generated nav_growth_trends.png")
    
    # 2. Annualized Return and Risk Metrics Comparison
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    # CAGR Barplot
    sns.barplot(data=df_metrics, x="scheme_name", y="cagr", ax=axes[0], hue="scheme_name", palette="viridis", legend=False)
    axes[0].set_title("Compound Annual Growth Rate (CAGR)", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("CAGR (Fraction)")
    axes[0].set_xlabel("")
    axes[0].tick_params(axis='x', rotation=30)

    # Volatility Barplot
    sns.barplot(data=df_metrics, x="scheme_name", y="annual_volatility", ax=axes[1], hue="scheme_name", palette="magma", legend=False)
    axes[1].set_title("Annualized Volatility", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("Volatility (Fraction)")
    axes[1].set_xlabel("")
    axes[1].tick_params(axis='x', rotation=30)

    # Sharpe Ratio Barplot
    sns.barplot(data=df_metrics, x="scheme_name", y="sharpe_ratio", ax=axes[2], hue="scheme_name", palette="rocket", legend=False)
    axes[2].set_title("Sharpe Ratio (Risk-Free = 6%)", fontsize=12, fontweight='bold')
    axes[2].set_ylabel("Sharpe Ratio")
    axes[2].set_xlabel("")
    axes[2].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "performance_metrics_comparison.png"), dpi=300)
    plt.close()
    print("  - Generated performance_metrics_comparison.png")
    
    # 3. Mutual Fund Returns Correlation Analysis
    returns_dict = {}
    for code, name in live_files.items():
        filepath = os.path.join(processed_dir, f"{name}_{code}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['daily_return'] = df['nav'].pct_change()
            returns_dict[name.replace('_', ' ').title()] = df['daily_return']

    df_returns = pd.DataFrame(returns_dict)
    corr_matrix = df_returns.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=0, vmax=1, linewidths=0.5)
    plt.title("Correlation Matrix of Mutual Fund Daily Returns", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, "returns_correlation_heatmap.png"), dpi=300)
    plt.close()
    print("  - Generated returns_correlation_heatmap.png")
    print("All chart images successfully generated on disk.")

if __name__ == "__main__":
    main()
