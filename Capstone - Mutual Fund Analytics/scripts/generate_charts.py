import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional charts
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Capstone - Mutual Fund Analytics"
data_raw_dir = os.path.join(base_dir, "data", "raw")
figures_dir = os.path.join(base_dir, "reports", "figures")
os.makedirs(figures_dir, exist_ok=True)

print("Reading datasets...")
df_nav = pd.read_csv(os.path.join(data_raw_dir, "nav_history_40.csv"))
df_schemes = pd.read_csv(os.path.join(data_raw_dir, "scheme_master_40.csv"))
df_aum = pd.read_csv(os.path.join(data_raw_dir, "aum_growth.csv"))
df_sip = pd.read_csv(os.path.join(data_raw_dir, "sip_inflow.csv"))
df_cat_inflow = pd.read_csv(os.path.join(data_raw_dir, "category_inflow.csv"))
df_demographics = pd.read_csv(os.path.join(data_raw_dir, "investor_demographics.csv"))
df_folio = pd.read_csv(os.path.join(data_raw_dir, "folio_growth.csv"))
df_holdings = pd.read_csv(os.path.join(data_raw_dir, "portfolio_holdings.csv"))

# Convert date columns
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_sip['month_dt'] = pd.to_datetime(df_sip['month'] + "-01")
df_folio['month_dt'] = pd.to_datetime(df_folio['month'] + "-01")

# Define HSL-like custom color palette for styling
c_primary = "#1f77b4"  # Muted Blue
c_secondary = "#aec7e8"
c_accent = "#d62728"   # Muted Red for highlights
c_dark = "#2c3e50"
c_light = "#f8f9fa"
c_green = "#2ca02c"    # Muted Green
colors_set = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# ---------------------------------------------------------
# Chart 1: NAV Trend Analysis (2022-2026)
# ---------------------------------------------------------
print("Plotting Chart 1: NAV Trend Analysis...")
fig, ax = plt.subplots(figsize=(12, 6.5))

# Plot all 40 schemes in light gray, but highlight 3 key schemes (one Equity, one Debt, one Hybrid)
selected_schemes = [
    (100000, "SBI Mutual Fund Equity Fund 1", "#1f77b4", "-"),
    (100020, "SBI Mutual Fund Debt Fund 21", "#ff7f0e", "--"),
    (100030, "SBI Mutual Fund Hybrid Fund 31", "#2ca02c", "-.")
]

for code in df_nav['scheme_code'].unique():
    subset = df_nav[df_nav['scheme_code'] == code]
    ax.plot(subset['date'], subset['nav'], color="lightgray", alpha=0.3, linewidth=0.8)

# Highlight selected
for code, name, color, style in selected_schemes:
    subset = df_nav[df_nav['scheme_code'] == code]
    ax.plot(subset['date'], subset['nav'], label=name, color=color, linestyle=style, linewidth=2.0)

# Shade 2023 Bull Run
ax.axvspan(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31"), color="#2ca02c", alpha=0.08, label="2023 Bull Run")
# Shade 2024 Market Correction (April to Sept)
ax.axvspan(pd.to_datetime("2024-04-01"), pd.to_datetime("2024-09-30"), color="#d62728", alpha=0.08, label="2024 Market Correction")

ax.set_title("NAV Trend Analysis (2022-2026) - Shaded Market Regimes", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Date", fontsize=11, labelpad=10)
ax.set_ylabel("NAV (₹)", fontsize=11, labelpad=10)
ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none", shadow=True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart01_nav_trends.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 2: AUM Growth Bar Chart (2022-2025)
# ---------------------------------------------------------
print("Plotting Chart 2: AUM Growth Bar Chart...")
fig, ax = plt.subplots(figsize=(11, 6))

# Melt or Pivot is not needed, seaborn accepts this grouped bar directly
df_aum_lakh_cr = df_aum.copy()
df_aum_lakh_cr['aum_lakh_cr'] = df_aum_lakh_cr['aum_cr'] / 100000.0

sns.barplot(
    data=df_aum_lakh_cr,
    x="year",
    y="aum_lakh_cr",
    hue="fund_house",
    palette="viridis",
    ax=ax
)

# Highlight SBI in 2025 at 12.5L Cr
ax.annotate(
    "SBI Dominance: ₹12.5L Cr",
    xy=(3.0 - 0.23, 12.5),  # 3.0 is the 2025 x-position, -0.23 is the SBI hue offset
    xytext=(1.8, 11.5),
    arrowprops=dict(facecolor=c_accent, shrink=0.08, width=1.5, headwidth=6),
    fontsize=11,
    color=c_accent,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3, ec="none")
)

ax.set_title("Asset Under Management (AUM) Growth by Fund House (2022-2025)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("AUM (₹ Lakh Crore)", fontsize=11)
ax.legend(title="Fund House", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart02_aum_growth.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 3: SIP Inflow Time-Series (2022-2025)
# ---------------------------------------------------------
print("Plotting Chart 3: SIP Inflow Time-Series...")
fig, ax = plt.subplots(figsize=(11, 5.5))

ax.plot(df_sip['month_dt'], df_sip['sip_inflow_cr'], color="#1f77b4", linewidth=2.5, marker="o", markersize=4, label="Monthly SIP Inflow")
ax.fill_between(df_sip['month_dt'], df_sip['sip_inflow_cr'], color="#1f77b4", alpha=0.1)

# Annotate Start: 11,305 Cr
ax.annotate(
    "Start: ₹11,305 Cr\n(Jan 2022)",
    xy=(df_sip['month_dt'].iloc[0], df_sip['sip_inflow_cr'].iloc[0]),
    xytext=(df_sip['month_dt'].iloc[0] + pd.Timedelta(days=60), df_sip['sip_inflow_cr'].iloc[0] + 1500),
    arrowprops=dict(arrowstyle="->", color=c_dark, connectionstyle="arc3,rad=.2"),
    fontsize=9,
    color=c_dark
)

# Annotate Peak: 31,002 Cr in Dec 2025
peak_idx = len(df_sip) - 1
ax.annotate(
    "All-Time High: ₹31,002 Cr\n(Dec 2025)",
    xy=(df_sip['month_dt'].iloc[peak_idx], df_sip['sip_inflow_cr'].iloc[peak_idx]),
    xytext=(df_sip['month_dt'].iloc[peak_idx] - pd.Timedelta(days=450), df_sip['sip_inflow_cr'].iloc[peak_idx] - 3000),
    arrowprops=dict(facecolor=c_accent, shrink=0.08, width=1.5, headwidth=6),
    fontsize=11,
    color=c_accent,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="gray", lw=0.5)
)

ax.set_title("Monthly SIP Inflow Trajectory (Jan 2022 - Dec 2025)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("SIP Inflow (₹ Crore)", fontsize=11)
ax.set_ylim(8000, 35000)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart03_sip_inflows.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 4: Category Inflow Heatmap
# ---------------------------------------------------------
print("Plotting Chart 4: Category Inflow Heatmap...")
fig, ax = plt.subplots(figsize=(12, 5))

# Pivot category inflow
df_cat_pivot = df_cat_inflow.pivot(index="category", columns="month", values="net_inflow_cr")
# Sort categories for logical display
cat_order = ["Equity", "Hybrid", "Solution-Oriented", "Others", "Debt"]
df_cat_pivot = df_cat_pivot.reindex(cat_order)

sns.heatmap(
    df_cat_pivot,
    cmap="RdYlGn",
    center=0,
    cbar_kws={'label': 'Net Monthly Inflow (₹ Crore)'},
    linewidths=0.2,
    ax=ax
)

ax.set_title("Net Inflow Intensity by Fund Category (Jan 2022 - Dec 2025)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Category", fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart04_category_heatmap.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 5: Age Group Distribution Pie Chart
# ---------------------------------------------------------
print("Plotting Chart 5: Age Group Distribution...")
fig, ax = plt.subplots(figsize=(7, 7))

age_dist = df_demographics['age_group'].value_counts().reindex(["18-25", "26-35", "36-50", "50+"])
labels = [f"{g}\n({count:,})" for g, count in zip(age_dist.index, age_dist.values)]
colors_pie = ["#9467bd", "#1f77b4", "#ff7f0e", "#e377c2"]

wedges, texts, autotexts = ax.pie(
    age_dist,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors_pie,
    explode=(0, 0.05, 0, 0),  # explode the largest segment (26-35)
    textprops=dict(color=c_dark, fontsize=10),
    wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2)  # Donut chart
)

plt.setp(autotexts, size=10, weight="bold")
ax.set_title("Investor Demographics: Age Group Distribution", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart05_age_pie.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 6: SIP Amount Box Plot by Age Group
# ---------------------------------------------------------
print("Plotting Chart 6: SIP Amount Box Plot by Age Group...")
fig, ax = plt.subplots(figsize=(9, 6))

sns.boxplot(
    data=df_demographics,
    x="age_group",
    y="sip_amount",
    order=["18-25", "26-35", "36-50", "50+"],
    palette="muted",
    showmeans=True,
    meanprops={"marker":"D","markerfacecolor":"white", "markeredgecolor":"black", "markersize":"6"},
    ax=ax
)

ax.set_title("SIP Investment Ticket Size Distribution by Age Group", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Monthly SIP Amount (₹)", fontsize=11)
# Use a log scale or sensible tick marks because of outliers
ax.set_yscale('log')
import matplotlib.ticker as ticker
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.set_yticks([500, 1000, 2000, 5000, 10000, 20000, 50000])

plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart06_sip_box_plot.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 7: Gender Split
# ---------------------------------------------------------
print("Plotting Chart 7: Gender Split...")
fig, ax = plt.subplots(figsize=(7, 7))

gender_dist = df_demographics['gender'].value_counts()
colors_gender = ["#1f77b4", "#e377c2", "#bcbd22"]

wedges, texts, autotexts = ax.pie(
    gender_dist,
    labels=gender_dist.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_gender,
    textprops=dict(color=c_dark, fontsize=10),
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)  # Donut chart
)

plt.setp(autotexts, size=10, weight="bold")
ax.set_title("Investor Demographics: Gender Split", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart07_gender_donut.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 8: State-wise SIP Contribution
# ---------------------------------------------------------
print("Plotting Chart 8: State-wise SIP Contribution...")
df_geo_state = pd.read_csv(os.path.join(data_raw_dir, "geo_state_summary.csv"))
fig, ax = plt.subplots(figsize=(10, 6.5))

# Convert total SIP to Crores for plotting
df_geo_state['total_sip_cr'] = df_geo_state['total_sip_amount'] / 10000000.0

sns.barplot(
    data=df_geo_state,
    x="total_sip_cr",
    y="state",
    palette="plasma",
    ax=ax
)

ax.set_title("State-wise Monthly SIP Contribution Volume (₹ Crore)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Total SIP Volume (₹ Crore)", fontsize=11)
ax.set_ylabel("State", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart08_state_sip.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 9: City Tier (T30 vs B30)
# ---------------------------------------------------------
print("Plotting Chart 9: City Tier Distribution...")
df_geo_tier = pd.read_csv(os.path.join(data_raw_dir, "geo_tier_summary.csv"))
fig, ax = plt.subplots(figsize=(6.5, 6.5))

labels = [f"T30 (Top 30 Cities)\n{df_geo_tier.loc[df_geo_tier['city_tier']=='T30', 'investor_count'].values[0]:,} investors",
          f"B30 (Beyond 30 Cities)\n{df_geo_tier.loc[df_geo_tier['city_tier']=='B30', 'investor_count'].values[0]:,} investors"]
colors_tier = ["#2ca02c", "#ff7f0e"]

ax.pie(
    df_geo_tier['investor_count'],
    labels=labels,
    autopct='%1.1f%%',
    startangle=120,
    colors=colors_tier,
    textprops=dict(color=c_dark, fontsize=10),
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
)

ax.set_title("Geographic Demographics: T30 vs B30 Market Share", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart09_city_tier.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 10: Folio Count Growth
# ---------------------------------------------------------
print("Plotting Chart 10: Folio Count Growth...")
fig, ax = plt.subplots(figsize=(11, 5.5))

ax.plot(df_folio['month_dt'], df_folio['folio_count_cr'], color="#2ca02c", linewidth=2.5, marker="s", markersize=4, label="Folio Count")
ax.fill_between(df_folio['month_dt'], df_folio['folio_count_cr'], color="#2ca02c", alpha=0.1)

# Annotate milestones
milestones = [
    ("Jan 2022", "13.26 Cr", df_folio['month_dt'].iloc[0], 13.26, "Start"),
    ("Nov 2023", "20.00 Cr", df_folio[df_folio['month'] == "2023-11"]['month_dt'].values[0], 19.98, "Crossed 20 Cr"),
    ("Dec 2025", "26.12 Cr", df_folio['month_dt'].iloc[-1], 26.12, "Peak")
]

for date_lbl, val_lbl, dt, val, label in milestones:
    ax.axvline(dt, color="gray", linestyle=":", alpha=0.5)
    ax.plot(dt, val, 'ro', markersize=6)
    ax.annotate(
        f"{label}\n{val_lbl}\n({date_lbl})",
        xy=(dt, val),
        xytext=(dt + pd.Timedelta(days=30) if date_lbl != "Dec 2025" else dt - pd.Timedelta(days=250), val - 1.5 if date_lbl != "Jan 2022" else val + 1.0),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="lightgray"),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="gray", connectionstyle="arc3,rad=.1")
    )

ax.set_title("Growth of Mutual Fund Folios in India (Jan 2022 - Dec 2025)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Total Folio Count (Crore)", fontsize=11)
ax.set_ylim(10, 29)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart10_folio_growth.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 11: NAV Return Correlation Matrix
# ---------------------------------------------------------
print("Plotting Chart 11: NAV Return Correlation...")
# Select 10 funds (5 Equity, 3 Debt, 2 Hybrid)
selected_codes = [100000, 100001, 100002, 100003, 100004, 100020, 100021, 100022, 100030, 100031]
df_subset_nav = df_nav[df_nav['scheme_code'].isin(selected_codes)].copy()

# Pivot to have dates as index, scheme names as columns, nav as values
df_pivot_nav = df_subset_nav.pivot(index="date", columns="scheme_name", values="nav")
# Compute daily returns
df_returns = df_pivot_nav.pct_change().dropna()
# Shorten names for the heatmap
short_names = {name: name.replace(" Mutual Fund", "").replace(" Fund", "") for name in df_returns.columns}
df_returns = df_returns.rename(columns=short_names)

# Compute correlation matrix
corr_matrix = df_returns.corr()

fig, ax = plt.subplots(figsize=(10, 8.5))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=0.5, vmax=1.0,  # Since they are mostly positively correlated during bull/bear markets
    linewidths=0.5,
    ax=ax
)
ax.set_title("Pairwise Daily Return Correlation Matrix (10 Selected Funds)", fontsize=13, fontweight="bold", pad=15)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart11_correlation_matrix.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 12: Sector Allocation Donut
# ---------------------------------------------------------
print("Plotting Chart 12: Sector Allocation Donut...")
# Aggregate portfolio holdings sector weights across all equity funds
df_equity_holdings = df_holdings[df_holdings['stock_ticker'] != 'CASH']
sector_weights = df_equity_holdings.groupby("sector")["weight_pct"].sum()
sector_weights = sector_weights / sector_weights.sum() * 100.0  # Normalize to 100% of equity portion
sector_weights = sector_weights.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(7.5, 7.5))
colors_sector = sns.color_palette("tab20", len(sector_weights))

wedges, texts, autotexts = ax.pie(
    sector_weights,
    labels=sector_weights.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors_sector,
    textprops=dict(color=c_dark, fontsize=9),
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=1.5)
)

plt.setp(autotexts, size=8, weight="bold")
ax.set_title("Consolidated Sector Allocation Across All Equity Funds", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart12_sector_allocation.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 13: Risk vs. Return Frontier Scatter Plot
# ---------------------------------------------------------
print("Plotting Chart 13: Risk vs. Return Scatter...")
# We need to compute CAGR and Volatility for all 40 schemes over the 5-year period
performance_records = []
for idx, row in df_schemes.iterrows():
    code = row["scheme_code"]
    name = row["scheme_name"]
    cat = row["category"]
    
    # Get NAV series
    subset = df_nav[df_nav['scheme_code'] == code].sort_values(by="date")
    beg_nav = subset['nav'].iloc[0]
    end_nav = subset['nav'].iloc[-1]
    n_days = len(subset)
    
    # CAGR formula
    cagr = (end_nav / beg_nav) ** (252.0 / n_days) - 1.0
    
    # Daily returns volatility
    daily_ret = subset['nav'].pct_change().dropna()
    vol = daily_ret.std() * np.sqrt(252.0)
    
    performance_records.append({
        "scheme_code": code,
        "scheme_name": name,
        "category": cat,
        "cagr": cagr * 100,
        "volatility": vol * 100
    })

df_perf = pd.DataFrame(performance_records)
df_perf.to_csv(os.path.join(base_dir, "data", "processed", "fund_performance_metrics.csv"), index=False)

fig, ax = plt.subplots(figsize=(10, 6.5))
sns.scatterplot(
    data=df_perf,
    x="volatility",
    y="cagr",
    hue="category",
    style="category",
    s=100,
    palette="Set1",
    ax=ax
)

ax.set_title("Risk-Return Frontier: Annualized Volatility vs. CAGR (2022-2026)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Annualized Volatility (Risk %)", fontsize=11)
ax.set_ylabel("Annualized CAGR (Return %)", fontsize=11)
ax.legend(title="Fund Category", frameon=True, shadow=True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart13_risk_return.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 14: Monthly Category Inflow Share (Stacked Area)
# ---------------------------------------------------------
print("Plotting Chart 14: Category Inflow Share Stacked Area...")
# Prepare category inflow data: Pivot month as index, category as column, inflow as value
df_inflow_pivot = df_cat_inflow.pivot(index="month", columns="category", values="net_inflow_cr")
df_inflow_pivot = df_inflow_pivot.reindex(columns=cat_order)
# Convert index to datetime
df_inflow_pivot.index = pd.to_datetime(df_inflow_pivot.index + "-01")

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.stackplot(
    df_inflow_pivot.index,
    [df_inflow_pivot[c] for c in cat_order],
    labels=cat_order,
    colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    alpha=0.85
)

ax.set_title("Monthly Net Inflow Composition by Fund Category (Jan 2022 - Dec 2025)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Net Monthly Inflow (₹ Crore)", fontsize=11)
ax.legend(loc="upper left", title="Category", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart14_category_share.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 15: Distribution of Fund Sizes (AUM) in 2025
# ---------------------------------------------------------
print("Plotting Chart 15: Distribution of Fund Sizes...")
# Filter 2025 AUM
df_aum_2025 = df_aum_lakh_cr[df_aum_lakh_cr['year'] == 2025]

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(
    data=df_aum_2025.sort_values(by="aum_lakh_cr", ascending=False),
    x="aum_lakh_cr",
    y="fund_house",
    palette="viridis",
    ax=ax
)

ax.set_title("Consolidated Fund House AUM Size in 2025 (₹ Lakh Crore)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("AUM (₹ Lakh Crore)", fontsize=11)
ax.set_ylabel("Fund House", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart15_aum_dist_2025.png"), dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 16: Top 10 Stock Holdings Across Equity Portfolios
# ---------------------------------------------------------
print("Plotting Chart 16: Top 10 Stock Holdings...")
# Sum weights across all equity schemes, excluding CASH
df_stock_weights = df_equity_holdings.groupby(["stock_ticker", "stock_name", "sector"])["weight_pct"].sum().reset_index()
df_stock_weights = df_stock_weights.sort_values(by="weight_pct", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df_stock_weights,
    x="weight_pct",
    y="stock_ticker",
    hue="sector",
    dodge=False,
    palette="tab10",
    ax=ax
)

ax.set_title("Top 10 Most Widely Held Stocks Across Equity Portfolios (Aggregated Weights)", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Aggregated Weight (Sum of % across all portfolios)", fontsize=11)
ax.set_ylabel("Stock Ticker", fontsize=11)
ax.legend(title="Sector", loc="lower right", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, "chart16_top_stocks.png"), dpi=150)
plt.close()

print("\nAll 16 professional charts plotted and saved successfully under reports/figures/!")
