import os
import json

def main():
    print("Generating day2_eda.ipynb notebook...")
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Day 2: Financial Exploratory Data Analysis (EDA)\n",
                    "This notebook executes the Exploratory Data Analysis for the **Bluestock Mutual Fund Pipeline**.\n",
                    "\n",
                    "We will:\n",
                    "1. Load and inspect the cleaned datasets and performance metrics.\n",
                    "2. Visualize the historical Net Asset Value (NAV) trends for the 6 target schemes.\n",
                    "3. Compare key annualized performance metrics (CAGR, Volatility, Sharpe Ratio, and Maximum Drawdown).\n",
                    "4. Perform returns correlation analysis to evaluate portfolio overlap."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "# Set plots configuration\n",
                    "sns.set_theme(style=\"darkgrid\")\n",
                    "plt.rcParams[\"figure.figsize\"] = (12, 6)\n",
                    "\n",
                    "processed_dir = \"../data/processed\"\n",
                    "metrics_path = os.path.join(processed_dir, \"fund_performance_metrics.csv\")\n",
                    "df_metrics = pd.read_csv(metrics_path)\n",
                    "df_metrics"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Historical NAV Growth Trends\n",
                    "Let's plot the Net Asset Value (NAV) curves of all 6 mutual funds to visualize their growth trajectory over time."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "live_files = {\n",
                    "    119551: \"sbi_bluechip\",\n",
                    "    120503: \"icici_bluechip\",\n",
                    "    118632: \"nippon_large_cap\",\n",
                    "    119092: \"axis_bluechip\",\n",
                    "    120841: \"kotak_bluechip\",\n",
                    "    125497: \"hdfc_top_100\"\n",
                    "}\n",
                    "\n",
                    "plt.figure(figsize=(14, 7))\n",
                    "for code, name in live_files.items():\n",
                    "    filepath = os.path.join(processed_dir, f\"{name}_{code}.csv\")\n",
                    "    if os.path.exists(filepath):\n",
                    "        df = pd.read_csv(filepath)\n",
                    "        df['date'] = pd.to_datetime(df['date'])\n",
                    "        plt.plot(df['date'], df['nav'], label=f\"{name.replace('_', ' ').title()} ({code})\")\n",
                    "\n",
                    "plt.title(\"Historical Net Asset Value (NAV) Growth Trends\", fontsize=14, fontweight='bold')\n",
                    "plt.xlabel(\"Date\", fontsize=12)\n",
                    "plt.ylabel(\"NAV (INR)\", fontsize=12)\n",
                    "plt.legend(loc=\"upper left\")\n",
                    "plt.tight_layout()\n",
                    "os.makedirs(\"../reports\", exist_ok=True)\n",
                    "plt.savefig(\"../reports/nav_growth_trends.png\", dpi=300)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Annualized Return and Risk Metrics\n",
                    "Let's compare the annualized CAGR, Volatility, and Sharpe Ratio of the funds. Sharpe ratio measures risk-adjusted return (using a risk-free rate of 6%)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, axes = plt.subplots(1, 3, figsize=(20, 6))\n",
                    "\n",
                    "# CAGR Barplot\n",
                    "sns.barplot(data=df_metrics, x=\"scheme_name\", y=\"cagr\", ax=axes[0], hue=\"scheme_name\", palette=\"viridis\", legend=False)\n",
                    "axes[0].set_title(\"Compound Annual Growth Rate (CAGR)\", fontsize=12, fontweight='bold')\n",
                    "axes[0].set_ylabel(\"CAGR (Fraction)\")\n",
                    "axes[0].set_xlabel(\"\")\n",
                    "axes[0].tick_params(axis='x', rotation=30)\n",
                    "\n",
                    "# Volatility Barplot\n",
                    "sns.barplot(data=df_metrics, x=\"scheme_name\", y=\"annual_volatility\", ax=axes[1], hue=\"scheme_name\", palette=\"magma\", legend=False)\n",
                    "axes[1].set_title(\"Annualized Volatility\", fontsize=12, fontweight='bold')\n",
                    "axes[1].set_ylabel(\"Volatility (Fraction)\")\n",
                    "axes[1].set_xlabel(\"\")\n",
                    "axes[1].tick_params(axis='x', rotation=30)\n",
                    "\n",
                    "# Sharpe Ratio Barplot\n",
                    "sns.barplot(data=df_metrics, x=\"scheme_name\", y=\"sharpe_ratio\", ax=axes[2], hue=\"scheme_name\", palette=\"rocket\", legend=False)\n",
                    "axes[2].set_title(\"Sharpe Ratio (Risk-Free = 6%)\", fontsize=12, fontweight='bold')\n",
                    "axes[2].set_ylabel(\"Sharpe Ratio\")\n",
                    "axes[2].set_xlabel(\"\")\n",
                    "axes[2].tick_params(axis='x', rotation=30)\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig(\"../reports/performance_metrics_comparison.png\", dpi=300)\n",
                    "plt.show()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Mutual Fund Returns Correlation Analysis\n",
                    "A correlation heatmap helps us understand if the large-cap mutual funds are highly correlated. High correlation indicates high asset portfolio overlap."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "returns_dict = {}\n",
                    "for code, name in live_files.items():\n",
                    "    filepath = os.path.join(processed_dir, f\"{name}_{code}.csv\")\n",
                    "    if os.path.exists(filepath):\n",
                    "        df = pd.read_csv(filepath)\n",
                    "        df['date'] = pd.to_datetime(df['date'])\n",
                    "        df.set_index('date', inplace=True)\n",
                    "        df['daily_return'] = df['nav'].pct_change()\n",
                    "        returns_dict[name.replace('_', ' ').title()] = df['daily_return']\n",
                    "\n",
                    "df_returns = pd.DataFrame(returns_dict)\n",
                    "corr_matrix = df_returns.corr()\n",
                    "\n",
                    "plt.figure(figsize=(10, 8))\n",
                    "sns.heatmap(corr_matrix, annot=True, cmap=\"coolwarm\", fmt=\".2f\", vmin=0, vmax=1, linewidths=0.5)\n",
                    "plt.title(\"Correlation Matrix of Mutual Fund Daily Returns\", fontsize=14, fontweight='bold')\n",
                    "plt.tight_layout()\n",
                    "plt.savefig(\"../reports/returns_correlation_heatmap.png\", dpi=300)\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    output_dir = "notebooks"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "day2_eda.ipynb")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)
        
    print(f"Jupyter notebook successfully generated and saved to {output_path}")

if __name__ == "__main__":
    main()
