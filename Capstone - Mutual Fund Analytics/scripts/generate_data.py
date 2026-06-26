import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Capstone - Mutual Fund Analytics"
data_raw_dir = os.path.join(base_dir, "data", "raw")
os.makedirs(data_raw_dir, exist_ok=True)

print("Generating Capstone Mutual Fund Analytics Datasets...")

# ---------------------------------------------------------
# 1. generate_nav_history_40 (2022-2026)
# ---------------------------------------------------------
print("Generating NAV History for 40 schemes...")
dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="B")
num_days = len(dates)

# Define 40 schemes across categories
categories = ["Equity"] * 20 + ["Debt"] * 10 + ["Hybrid"] * 7 + ["Solution-Oriented"] * 3
fund_houses = [
    "SBI Mutual Fund", "HDFC Mutual Fund", "ICICI Prudential Mutual Fund",
    "Nippon India Mutual Fund", "Axis Mutual Fund", "Kotak Mahindra Mutual Fund",
    "DSP Mutual Fund", "Aditya Birla Sun Life Mutual Fund", "UTI Mutual Fund", "Tata Mutual Fund"
]

schemes = []
for i in range(40):
    cat = categories[i]
    fh = fund_houses[i % len(fund_houses)]
    schemes.append({
        "scheme_code": 100000 + i,
        "scheme_name": f"{fh} {cat} Fund {i+1}",
        "category": cat,
        "fund_house": fh,
        "base_nav": np.random.uniform(10.0, 150.0)
    })

df_schemes = pd.DataFrame(schemes)

nav_records = []
for idx, row in df_schemes.iterrows():
    code = row["scheme_code"]
    name = row["scheme_name"]
    cat = row["category"]
    current_nav = row["base_nav"]
    
    # Generate daily path
    nav_path = [current_nav]
    for d in dates[1:]:
        year = d.year
        # Define drift and volatility based on the year to simulate market regimes
        if year == 2022:
            # Volatile / sideways
            drift = 0.01 / 252 if cat == "Equity" else 0.05 / 252
            vol = 0.16 / np.sqrt(252) if cat == "Equity" else 0.03 / np.sqrt(252)
        elif year == 2023:
            # 2023 Bull Run
            drift = 0.36 / 252 if cat == "Equity" else 0.07 / 252
            vol = 0.11 / np.sqrt(252) if cat == "Equity" else 0.02 / np.sqrt(252)
        elif year == 2024:
            # 2024 Market Correction in mid-year
            # Drawdown from April to September, then recovery
            if 4 <= d.month <= 9:
                drift = -0.30 / 252 if cat == "Equity" else 0.04 / 252
                vol = 0.22 / np.sqrt(252) if cat == "Equity" else 0.04 / np.sqrt(252)
            else:
                drift = 0.15 / 252 if cat == "Equity" else 0.06 / 252
                vol = 0.14 / np.sqrt(252) if cat == "Equity" else 0.02 / np.sqrt(252)
        elif year == 2025:
            # Steady recovery and growth
            drift = 0.18 / 252 if cat == "Equity" else 0.06 / 252
            vol = 0.12 / np.sqrt(252) if cat == "Equity" else 0.02 / np.sqrt(252)
        else: # 2026
            # Moderate growth
            drift = 0.12 / 252 if cat == "Equity" else 0.05 / 252
            vol = 0.10 / np.sqrt(252) if cat == "Equity" else 0.02 / np.sqrt(252)
            
        # Adjust drift/vol for other categories
        if cat == "Hybrid":
            drift = drift * 0.7 + 0.02 / 252
            vol = vol * 0.6
        elif cat == "Solution-Oriented":
            drift = drift * 0.8
            vol = vol * 0.7
            
        # Random step
        pct_change = np.random.normal(drift, vol)
        current_nav = max(2.0, current_nav * (1.0 + pct_change))
        nav_path.append(current_nav)
        
    for d, nav in zip(dates, nav_path):
        nav_records.append({
            "date": d.strftime("%Y-%m-%d"),
            "scheme_code": code,
            "scheme_name": name,
            "nav": round(nav, 4)
        })

df_nav_history = pd.DataFrame(nav_records)
df_nav_history.to_csv(os.path.join(data_raw_dir, "nav_history_40.csv"), index=False)
print(f"Saved nav_history_40.csv with {len(df_nav_history)} rows.")

# Save scheme master data too for easy joins
df_schemes.to_csv(os.path.join(data_raw_dir, "scheme_master_40.csv"), index=False)

# ---------------------------------------------------------
# 2. generate_aum_growth (2022-2025)
# ---------------------------------------------------------
print("Generating AUM Growth data...")
# Years 2022 to 2025
# SBI must reach exactly 12.5L Cr in 2025. HDFC, ICICI, Nippon, Axis, Kotak.
aum_data = [
    # SBI Mutual Fund
    {"year": 2022, "fund_house": "SBI Mutual Fund", "aum_cr": 640000.0},
    {"year": 2023, "fund_house": "SBI Mutual Fund", "aum_cr": 820000.0},
    {"year": 2024, "fund_house": "SBI Mutual Fund", "aum_cr": 1010000.0},
    {"year": 2025, "fund_house": "SBI Mutual Fund", "aum_cr": 1250000.0}, # Target: 12.5L Cr
    
    # HDFC Mutual Fund
    {"year": 2022, "fund_house": "HDFC Mutual Fund", "aum_cr": 440000.0},
    {"year": 2023, "fund_house": "HDFC Mutual Fund", "aum_cr": 560000.0},
    {"year": 2024, "fund_house": "HDFC Mutual Fund", "aum_cr": 690000.0},
    {"year": 2025, "fund_house": "HDFC Mutual Fund", "aum_cr": 850000.0},
    
    # ICICI Prudential Mutual Fund
    {"year": 2022, "fund_house": "ICICI Prudential Mutual Fund", "aum_cr": 430000.0},
    {"year": 2023, "fund_house": "ICICI Prudential Mutual Fund", "aum_cr": 550000.0},
    {"year": 2024, "fund_house": "ICICI Prudential Mutual Fund", "aum_cr": 680000.0},
    {"year": 2025, "fund_house": "ICICI Prudential Mutual Fund", "aum_cr": 830000.0},
    
    # Nippon India Mutual Fund
    {"year": 2022, "fund_house": "Nippon India Mutual Fund", "aum_cr": 280000.0},
    {"year": 2023, "fund_house": "Nippon India Mutual Fund", "aum_cr": 350000.0},
    {"year": 2024, "fund_house": "Nippon India Mutual Fund", "aum_cr": 430000.0},
    {"year": 2025, "fund_house": "Nippon India Mutual Fund", "aum_cr": 530000.0},
    
    # Axis Mutual Fund
    {"year": 2022, "fund_house": "Axis Mutual Fund", "aum_cr": 250000.0},
    {"year": 2023, "fund_house": "Axis Mutual Fund", "aum_cr": 300000.0},
    {"year": 2024, "fund_house": "Axis Mutual Fund", "aum_cr": 340000.0},
    {"year": 2025, "fund_house": "Axis Mutual Fund", "aum_cr": 390000.0},
    
    # Kotak Mahindra Mutual Fund
    {"year": 2022, "fund_house": "Kotak Mahindra Mutual Fund", "aum_cr": 220000.0},
    {"year": 2023, "fund_house": "Kotak Mahindra Mutual Fund", "aum_cr": 280000.0},
    {"year": 2024, "fund_house": "Kotak Mahindra Mutual Fund", "aum_cr": 330000.0},
    {"year": 2025, "fund_house": "Kotak Mahindra Mutual Fund", "aum_cr": 410000.0},
]

df_aum = pd.DataFrame(aum_data)
df_aum.to_csv(os.path.join(data_raw_dir, "aum_growth.csv"), index=False)
print("Saved aum_growth.csv.")

# ---------------------------------------------------------
# 3. generate_sip_inflow (Jan 2022 - Dec 2025)
# ---------------------------------------------------------
print("Generating SIP Inflow data...")
# Start at 11,305 Cr in Jan 2022, peak at exactly 31,002 Cr in Dec 2025
months = pd.date_range(start="2022-01-01", end="2025-12-01", freq="MS")
n_months = len(months)

# Generate a steady upward trend with seasonal variation
trend = np.linspace(11305.0, 31002.0, n_months)
# Add some seasonal oscillations (higher inflows in March/April/October, lower in December usually, but here we peak in Dec 2025)
oscillation = 300.0 * np.sin(np.linspace(0, 4 * np.pi, n_months))
sip_values = trend + oscillation
# Force the exact end points
sip_values[0] = 11305.0
sip_values[-1] = 31002.0

sip_records = []
for m, val in zip(months, sip_values):
    sip_records.append({
        "month": m.strftime("%Y-%m"),
        "sip_inflow_cr": round(val, 2)
    })

df_sip = pd.DataFrame(sip_records)
df_sip.to_csv(os.path.join(data_raw_dir, "sip_inflow.csv"), index=False)
print("Saved sip_inflow.csv.")

# ---------------------------------------------------------
# 4. generate_category_inflow (Jan 2022 - Dec 2025)
# ---------------------------------------------------------
print("Generating Category Inflow data...")
# Net inflows for categories: Equity, Debt, Hybrid, Solution-Oriented, Others
category_records = []
for m, tot_sip in zip(months, sip_values):
    # Total net inflow is typically higher or lower than SIP inflow due to lump sums, but let's base it on a multiplier
    # During bull markets, equity net inflow is extremely high. Debt fluctuates.
    year = m.year
    month_idx = m.month
    
    # Net inflow multipliers / shares
    if year == 2023:
        # Equity heavy bull run
        eq_share = np.random.uniform(0.60, 0.75)
        debt_share = np.random.uniform(-0.10, 0.10) # Outflows or low inflows
    elif year == 2024 and 4 <= month_idx <= 9:
        # Correction period
        eq_share = np.random.uniform(0.35, 0.45)
        debt_share = np.random.uniform(0.20, 0.35) # Safe haven
    else:
        eq_share = np.random.uniform(0.50, 0.60)
        debt_share = np.random.uniform(0.15, 0.25)
        
    hybrid_share = np.random.uniform(0.10, 0.15)
    sol_share = np.random.uniform(0.02, 0.05)
    other_share = 1.0 - (eq_share + debt_share + hybrid_share + sol_share)
    
    # Net inflow scale
    total_net_inflow = tot_sip * np.random.uniform(0.8, 1.3)
    
    category_records.append({"month": m.strftime("%Y-%m"), "category": "Equity", "net_inflow_cr": round(total_net_inflow * eq_share, 2)})
    category_records.append({"month": m.strftime("%Y-%m"), "category": "Debt", "net_inflow_cr": round(total_net_inflow * debt_share, 2)})
    category_records.append({"month": m.strftime("%Y-%m"), "category": "Hybrid", "net_inflow_cr": round(total_net_inflow * hybrid_share, 2)})
    category_records.append({"month": m.strftime("%Y-%m"), "category": "Solution-Oriented", "net_inflow_cr": round(total_net_inflow * sol_share, 2)})
    category_records.append({"month": m.strftime("%Y-%m"), "category": "Others", "net_inflow_cr": round(total_net_inflow * other_share, 2)})

df_category_inflow = pd.DataFrame(category_records)
df_category_inflow.to_csv(os.path.join(data_raw_dir, "category_inflow.csv"), index=False)
print("Saved category_inflow.csv.")

# ---------------------------------------------------------
# 5. generate_investor_demographics (10,000 records)
# ---------------------------------------------------------
print("Generating Investor Demographics (10,000 active investors)...")
n_investors = 10000

# Ages following a realistic distribution peaking in early 30s
ages = np.random.normal(loc=34, scale=10, size=n_investors).astype(int)
ages = np.clip(ages, 18, 80)

# Map to Age Groups
# Target shares: 26-35 (~42%), 36-50 (~30%), 18-25 (~15%), 50+ (~13%)
# Let's adjust ages slightly to hit these targets
age_groups = []
for a in ages:
    if a <= 25:
        age_groups.append("18-25")
    elif a <= 35:
        age_groups.append("26-35")
    elif a <= 50:
        age_groups.append("36-50")
    else:
        age_groups.append("50+")

# Gender shares: Male (~58%), Female (~40%), Other (~2%)
gender_choices = ["Male", "Female", "Other"]
gender_p = [0.58, 0.40, 0.02]
genders = np.random.choice(gender_choices, size=n_investors, p=gender_p)

# City Tier: T30 (~68%), B30 (~32%)
tier_choices = ["T30", "B30"]
tier_p = [0.68, 0.32]
tiers = np.random.choice(tier_choices, size=n_investors, p=tier_p)

# States distribution (Industrialized states having higher shares)
states_choices = [
    "Maharashtra", "Gujarat", "Karnataka", "Delhi", "Tamil Nadu",
    "Uttar Pradesh", "West Bengal", "Telangana", "Rajasthan", "Kerala",
    "Haryana", "Madhya Pradesh", "Andhra Pradesh", "Punjab", "Bihar"
]
# Probabilities summing to 1.0
states_p = [0.22, 0.16, 0.14, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.01, 0.01]
states = np.random.choice(states_choices, size=n_investors, p=states_p)

# SIP Amount by Age Group (reflecting ticket sizes)
# 18-25: median 2500, range 500 - 10k
# 26-35: median 5000, range 1k - 25k
# 36-50: median 8500, range 2k - 50k
# 50+: median 6000, range 1.5k - 40k
sip_amounts = []
for ag in age_groups:
    if ag == "18-25":
        val = np.random.lognormal(mean=7.7, sigma=0.5) # Median ~2200
        val = np.clip(val, 500, 10000)
    elif ag == "26-35":
        val = np.random.lognormal(mean=8.4, sigma=0.6) # Median ~4400
        val = np.clip(val, 1000, 25000)
    elif ag == "36-50":
        val = np.random.lognormal(mean=8.9, sigma=0.6) # Median ~7300
        val = np.clip(val, 2000, 50000)
    else: # 50+
        val = np.random.lognormal(mean=8.6, sigma=0.5) # Median ~5400
        val = np.clip(val, 1500, 40000)
    # Round to nearest 500 for realistic investment tickets
    sip_amounts.append(round(val / 500.0) * 500.0)

df_demographics = pd.DataFrame({
    "investor_id": range(100000, 100000 + n_investors),
    "age": ages,
    "age_group": age_groups,
    "gender": genders,
    "sip_amount": sip_amounts,
    "city_tier": tiers,
    "state": states
})
df_demographics.to_csv(os.path.join(data_raw_dir, "investor_demographics.csv"), index=False)
print("Saved investor_demographics.csv.")

# ---------------------------------------------------------
# 6. generate_geographic_distribution (Derived for 100% alignment)
# ---------------------------------------------------------
print("Generating Geographic Distribution from Demographics...")
# We aggregate the demographics dataset by state and city tier to create an aligned geographic_distribution.csv
df_geo_state = df_demographics.groupby("state").agg(
    total_sip_amount=("sip_amount", "sum"),
    investor_count=("investor_id", "count")
).reset_index().sort_values(by="total_sip_amount", ascending=False)

df_geo_tier = df_demographics.groupby("city_tier").agg(
    total_sip_amount=("sip_amount", "sum"),
    investor_count=("investor_id", "count")
).reset_index()

# Save them as separate tables or combined for ease
df_geo_state.to_csv(os.path.join(data_raw_dir, "geo_state_summary.csv"), index=False)
df_geo_tier.to_csv(os.path.join(data_raw_dir, "geo_tier_summary.csv"), index=False)
print("Saved geo summaries.")

# ---------------------------------------------------------
# 7. generate_folio_growth (Jan 2022 - Dec 2025)
# ---------------------------------------------------------
print("Generating Folio Growth data...")
# Start at 13.26 Crore in Jan 2022, grow to exactly 26.12 Crore in Dec 2025
start_folio = 13.26
end_folio = 26.12
folio_trend = np.linspace(start_folio, end_folio, n_months)
# Add minor fluctuations but keep it monotonically increasing
noise = np.random.uniform(-0.05, 0.05, n_months)
# Accumulate and smooth
folio_values = np.zeros(n_months)
folio_values[0] = start_folio
for idx in range(1, n_months - 1):
    folio_values[idx] = round(folio_trend[idx] + noise[idx], 2)
folio_values[-1] = end_folio

folio_records = []
for m, val in zip(months, folio_values):
    folio_records.append({
        "month": m.strftime("%Y-%m"),
        "folio_count_cr": round(val, 2)
    })

df_folio = pd.DataFrame(folio_records)
df_folio.to_csv(os.path.join(data_raw_dir, "folio_growth.csv"), index=False)
print("Saved folio_growth.csv.")

# ---------------------------------------------------------
# 8. generate_portfolio_holdings
# ---------------------------------------------------------
print("Generating Portfolio Holdings for Equity Funds...")
# Let's get the list of equity funds from df_schemes
equity_funds = df_schemes[df_schemes["category"] == "Equity"]["scheme_name"].tolist()

# Define 40 major Indian stocks and their sectors
stocks_pool = [
    ("RELIANCE", "Reliance Industries Ltd", "Energy"),
    ("TCS", "Tata Consultancy Services Ltd", "IT"),
    ("INFY", "Infosys Ltd", "IT"),
    ("HDFCBANK", "HDFC Bank Ltd", "Banking & Financials"),
    ("ICICIBANK", "ICICI Bank Ltd", "Banking & Financials"),
    ("SBIN", "State Bank of India", "Banking & Financials"),
    ("KOTAKBANK", "Kotak Mahindra Bank Ltd", "Banking & Financials"),
    ("AXISBANK", "Axis Bank Ltd", "Banking & Financials"),
    ("ITC", "ITC Ltd", "FMCG"),
    ("HINDUNILVR", "Hindustan Unilever Ltd", "FMCG"),
    ("LTIM", "LTIMindtree Ltd", "IT"),
    ("WIPRO", "Wipro Ltd", "IT"),
    ("HCLTECH", "HCL Technologies Ltd", "IT"),
    ("SUNPHARMA", "Sun Pharmaceutical Industries Ltd", "Pharmaceuticals"),
    ("CIPLA", "Cipla Ltd", "Pharmaceuticals"),
    ("DRREDDY", "Dr. Reddy's Laboratories Ltd", "Pharmaceuticals"),
    ("APOLLOHOSP", "Apollo Hospitals Enterprise Ltd", "Pharmaceuticals"),
    ("TATAMOTORS", "Tata Motors Ltd", "Auto"),
    ("M&M", "Mahindra & Mahindra Ltd", "Auto"),
    ("MARUTI", "Maruti Suzuki India Ltd", "Auto"),
    ("EICHERMOT", "Eicher Motors Ltd", "Auto"),
    ("LT", "Larsen & Toubro Ltd", "Infrastructure"),
    ("ULTRACEMCO", "UltraTech Cement Ltd", "Infrastructure"),
    ("GRASIM", "Grasim Industries Ltd", "Infrastructure"),
    ("POWERGRID", "Power Grid Corp of India Ltd", "Energy"),
    ("NTPC", "NTPC Ltd", "Energy"),
    ("ONGC", "Oil & Natural Gas Corp Ltd", "Energy"),
    ("COALINDIA", "Coal India Ltd", "Energy"),
    ("BHARTIARTL", "Bharti Airtel Ltd", "Telecom"),
    ("JIOFIN", "Jio Financial Services Ltd", "Banking & Financials"),
    ("BAJFINANCE", "Bajaj Finance Ltd", "Banking & Financials"),
    ("BAJAJFINSV", "Bajaj Finserv Ltd", "Banking & Financials"),
    ("TATASTEEL", "Tata Steel Ltd", "Metals"),
    ("JSWSTEEL", "JSW Steel Ltd", "Metals"),
    ("HINDALCO", "Hindalco Industries Ltd", "Metals"),
    ("ASIANPAINT", "Asian Paints Ltd", "FMCG"),
    ("TITAN", "Titan Company Ltd", "FMCG"),
    ("NESTLEIND", "Nestle India Ltd", "FMCG"),
    ("TATACHEM", "Tata Chemicals Ltd", "Chemicals"),
    ("PIDILITIND", "Pidilite Industries Ltd", "Chemicals"),
]

holdings_records = []
for scheme_name in equity_funds:
    # Select a random subset of 15 to 22 stocks
    num_stocks = np.random.randint(15, 23)
    selected_stocks_idx = np.random.choice(len(stocks_pool), size=num_stocks, replace=False)
    
    # Generate weights
    raw_weights = np.random.dirichlet(np.ones(num_stocks))
    # Scale to 92% to 96%
    portfolio_weight_equity = np.random.uniform(0.92, 0.96)
    weights = raw_weights * portfolio_weight_equity
    
    for idx, w in zip(selected_stocks_idx, weights):
        ticker, name, sector = stocks_pool[idx]
        holdings_records.append({
            "scheme_name": scheme_name,
            "stock_ticker": ticker,
            "stock_name": name,
            "sector": sector,
            "weight_pct": round(w * 100, 2)
        })
    # Cash holding
    holdings_records.append({
        "scheme_name": scheme_name,
        "stock_ticker": "CASH",
        "stock_name": "Cash & Cash Equivalents",
        "sector": "Cash",
        "weight_pct": round((1.0 - portfolio_weight_equity) * 100, 2)
    })

df_holdings = pd.DataFrame(holdings_records)
df_holdings.to_csv(os.path.join(data_raw_dir, "portfolio_holdings.csv"), index=False)
print(f"Saved portfolio_holdings.csv with {len(df_holdings)} rows.")

print("\nAll datasets generated successfully!")
print("Paths:")
for f in os.listdir(data_raw_dir):
    print(f" - {os.path.join(data_raw_dir, f)}")
