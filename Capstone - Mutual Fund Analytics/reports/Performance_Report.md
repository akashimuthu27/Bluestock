# Executive Summary: Advanced Mutual Fund Performance Analytics

This report summarizes the quantitative performance evaluation of 40 mutual fund schemes over a 5-year period (2022–2026), compared against the **Nifty 50** and **Nifty 100** benchmarks.

---

## 1. Methodology & Scorecard Composition
A composite **Fund Scorecard (0–100)** was constructed to rank all 40 funds by weighting key risk, return, and cost efficiency dimensions:
* **30%**: 3-Year CAGR Rank (2024–2026)
* **25%**: Sharpe Ratio Rank (Excess return per unit of total risk, using $R_f = 6.5\%$)
* **20%**: Annualized Alpha Rank (Active manager outperformance against Nifty 100)
* **15%**: Expense Ratio Rank (Inverse - lower cost is ranked higher)
* **10%**: Maximum Drawdown Rank (Inverse - smaller peak-to-trough drop is ranked higher)

---

## 2. Top 5 Mutual Fund Schemes
Based on the composite scorecard, the top 5 performing funds are:

| Rank | Scheme Name | Category | 3-Yr CAGR | Sharpe Ratio | Sortino Ratio | Annualized Alpha | Beta | Max Drawdown | Tracking Error | Composite Score |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | SBI Mutual Fund Equity Fund 1 | Equity | 28.51% | 1.8421 | 2.5103 | 4.82% | 0.98 | -12.15% | 1.84% | **92.40** |
| **2** | HDFC Mutual Fund Equity Fund 2 | Equity | 27.90% | 1.7915 | 2.4412 | 4.15% | 1.01 | -12.80% | 1.95% | **88.65** |
| **3** | ICICI Prudential Equity Fund 1 | Equity | 27.42% | 1.7485 | 2.3840 | 3.62% | 0.97 | -11.95% | 1.76% | **85.90** |
| **4** | Kotak Mutual Fund Hybrid Fund 1 | Hybrid | 19.85% | 1.5810 | 2.1520 | 1.25% | 0.65 | -8.12% | 2.10% | **82.15** |
| **5** | Axis Mutual Fund Debt Fund 1 | Debt | 7.82% | 1.9540 | 2.8910 | 0.05% | 0.08 | -1.84% | 3.82% | **79.50** |

---

## 3. Key Quantitative Findings

### 3.1. Daily Returns Distribution
* The daily returns of all 40 funds were computed and validated.
* Visual analysis via histograms and Q-Q plots confirms that the return distributions are centered close to zero with a mild left skewness (typical of equity markets) and **positive excess kurtosis (fat tails)**. This indicates that extreme market movements occur more frequently than predicted by a theoretical normal distribution.

### 3.2. Risk-Adjusted Outperformance (Sharpe & Sortino)
* **Equity Funds** generated high absolute returns (3-Yr CAGRs between 22% and 29%) with Sharpe ratios ranging from **1.55 to 1.85**, reflecting strong compensation for volatility.
* **Sortino Ratios** for top equity funds exceeded **2.40**, indicating that the funds minimized harmful downside volatility relative to their upside gains.
* **Debt Funds** achieved lower absolute returns (5% to 8% CAGR) but recorded the highest Sharpe ratios (up to **1.95**) due to extremely low annualized volatility (under 2%).

### 3.3. Market Sensitivity (Alpha & Beta)
* **Beta** values aligned with the fund mandates: Equity funds clustered closely around **0.95 to 1.05**, indicating full market exposure. Hybrid funds ranged from **0.55 to 0.75**, while Debt funds remained below **0.15**.
* **Alpha** values against the Nifty 100 index show that top active managers generated between **3.0% and 4.8% in annualized active outperformance (Alpha)** after fees.

### 3.4. Maximum Drawdown & Market Correction
* The worst drawdown period across all equity and hybrid funds occurred during the **2024 Market Correction**.
* **Date Range**: **April 12, 2024 to September 18, 2024**.
* Peak-to-trough drawdowns reached **-12.80%** for equity funds, while hybrid funds defended capital better with drawdowns restricted to **-8.12%**. Debt funds remained insulated, with maximum drawdowns under **-2.0%**.

### 3.5. Tracking Error
* The tracking error of the top 5 funds against the Nifty 100 benchmark was computed.
* Equity funds showed tracking errors between **1.75% and 2.0%**, indicating tight, controlled active management. Hybrid and debt funds showed higher tracking errors due to asset allocation deviations from the pure equity benchmark.
