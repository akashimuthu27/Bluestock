# Capstone Project I: Mutual Fund Analytics Executive Summary Report

## 1. Executive Summary
This report presents an in-depth analysis of the Indian Mutual Fund Industry over the period **2022–2026**. Utilizing a robust dataset comprising daily NAVs for 40 schemes, AUM data for major fund houses, monthly SIP inflows, folio counts, investor demographics, and stock-level portfolio holdings, we evaluate the market's trajectory through different macroeconomic regimes.

Our key findings highlight a **massive surge in retail participation**, driven by young professionals (ages 26–35) investing via systematic investment plans (SIPs), which culminated in an all-time high of **₹31,002 Crore in monthly inflows in December 2025**. Furthermore, the analysis of asset allocation shows a high concentration in financial and technology sectors, and the risk-return frontier highlights the superior risk-adjusted performance of diversified hybrid and equity funds.

---

## 2. Key Industry Metrics Summary

### 2.1. Systematic Investment Plan (SIP) & Folio Growth
Retail momentum has seen unprecedented growth over the 4-year period:
* **Monthly SIP Inflow**: Expanded from **₹11,305 Crore** in January 2022 to **₹31,002 Crore** in December 2025 (a **174% growth**).
* **Total Folios**: Rose from **13.26 Crore** in January 2022 to **26.12 Crore** in December 2025, showing a near doubling of active accounts.

### 2.2. AUM Concentration (2025)
SBI Mutual Fund remains the undisputed market leader, with HDFC and ICICI Prudential competing closely:
* **SBI Mutual Fund AUM**: Reached **₹12.5 Lakh Crore** in 2025.
* **HDFC Mutual Fund AUM**: Reached **₹8.5 Lakh Crore** in 2025.
* **ICICI Prudential Mutual Fund AUM**: Reached **₹8.3 Lakh Crore** in 2025.

---

## 3. The 10 Key EDA Findings

| # | Insight Domain | Analytical Finding | Supporting Visualization |
|---|---|---|---|
| 1 | **NAV Trajectory** | During the 2023 market expansion, equity fund NAVs grew by an average of 34.2%, while the mid-2024 correction induced an average drawdown of 12.8% before recovery commenced. | `chart01_nav_trends.png` |
| 2 | **AUM Concentration** | SBI Mutual Fund consolidated its market leadership by expanding its AUM to ₹12.5 Lakh Crore in 2025, outstripping its nearest competitor by over 45%. | `chart02_aum_growth.png` |
| 3 | **Retail Momentum** | Monthly SIP inflows experienced a continuous upward trajectory, starting at ₹11,305 Crore in January 2022 and culminating in an all-time high of ₹31,002 Crore in December 2025. | `chart03_sip_inflows.png` |
| 4 | **Category Dominance** | Heatmap analysis reveals that net inflows were heavily concentrated in Equity funds during the Q1-Q3 2023 bull market, while Debt funds experienced net outflows or stagnation during rate-hike cycles. | `chart04_category_heatmap.png` |
| 5 | **Demographic Engine** | Investors aged 26–35 constitute the largest segment at 42.1%, establishing young professionals as the primary driver of digital mutual fund adoption. | `chart05_age_pie.png` |
| 6 | **Investment Ticket Size** | The 36–50 age cohort exhibits the highest median monthly SIP contribution (₹8,500), reflecting higher disposable incomes compared to the 18–25 cohort (₹2,500). | `chart06_sip_box_plot.png` |
| 7 | **Geographical Footprint** | Maharashtra, Gujarat, and Karnataka collectively contribute 56.4% of total SIP volumes, illustrating a high concentration of financialization in industrialized states. | `chart08_state_sip.png` |
| 8 | **Urban-Rural Shift** | The B30 (Beyond 30) cities represent 31.8% of the total investor base, showing a steady expansion of retail investing into semi-urban and rural regions. | `chart09_city_tier.png` |
| 9 | **Folio Expansion** | Mutual fund folios expanded rapidly from 13.26 Crore in January 2022 to 26.12 Crore in December 2025, indicating a doubling of retail account penetration in 4 years. | `chart10_folio_growth.png` |
| 10 | **Sector Exposure** | Consolidated portfolio holdings across equity schemes show a significant concentration in the Banking & Financials (28.4%) and IT (18.6%) sectors, indicating high sensitivity to interest rate and global tech cycles. | `chart12_sector_allocation.png` |

---

## 4. Financial Performance & Risk-Return Analysis

### 4.1. The Risk-Return Frontier (`chart13_risk_return.png`)
By plotting the annualized CAGR against the annualized volatility of the 40 schemes over the 2022–2026 period:
* **Equity Funds**: Occupy the high-risk, high-return quadrant with CAGRs ranging between **14% to 19%** and volatilities of **12% to 16%**.
* **Hybrid Funds**: Offer optimized risk-adjusted profiles (Sharpe ratios) with CAGRs of **10% to 13%** and significantly lower volatilities (**6% to 8%**).
* **Debt Funds**: Cluster in the low-risk quadrant with steady, predictable CAGRs of **5.5% to 6.5%** and minimal volatility (**1.5% to 2.5%**).

### 4.2. Daily Return Correlation (`chart11_correlation_matrix.png`)
* Pairwise return correlation of large-cap equity funds is extremely high (ranging between **0.88 to 0.96**), showing that passive and active large-cap equity strategies move in tandem.
* Debt funds show very low correlation with equity funds (ranging between **-0.05 to 0.12**), validating their role as a strong diversification tool during equity drawdowns.

---

## 5. Portfolio Sector Allocation & Stock Concentration

### 5.1. Sector Exposure (`chart12_sector_allocation.png`)
The consolidated portfolio holdings across equity funds indicate the following sector distributions:
1. **Banking & Financials**: **28.4%** (core driver of the Indian economy and major index weight).
2. **Information Technology (IT)**: **18.6%** (global tech exposure and defensive cash generator).
3. **FMCG**: **11.2%** (consumption-driven stability).
4. **Pharmaceuticals & Healthcare**: **9.4%** (defensive defensive growth).
5. **Auto & Energy**: **15.8%** (cyclical and infrastructure plays).
6. **Others & Cash**: **16.6%** (metals, chemicals, and liquid cash reserves).

### 5.2. Top Stock Holdings (`chart16_top_stocks.png`)
The top 5 stocks held across all equity mutual fund portfolios by aggregated weight are:
1. **HDFC Bank Ltd (HDFCBANK)** (Sector: Banking & Financials)
2. **Reliance Industries Ltd (RELIANCE)** (Sector: Energy)
3. **ICICI Bank Ltd (ICICIBANK)** (Sector: Banking & Financials)
4. **Infosys Ltd (INFY)** (Sector: IT)
5. **Tata Consultancy Services Ltd (TCS)** (Sector: IT)

---

## 6. Conclusion & Strategic Takeaways
The data paints a clear picture of a **maturing and financializing Indian economy**. Retail money, flowing steadily through monthly SIPs, has become a formidable force, acting as a buffer against foreign institutional investor (FII) outflows (as seen during the 2024 market correction). The rise of the B30 (Beyond 30) cities highlights that the next wave of growth will come from tier-2 and tier-3 locations. For asset management companies (AMCs), key strategic focus areas should include expanding digital distribution in B30 cities and designing hybrid products that appeal to the risk-averse, emerging retail segment.
