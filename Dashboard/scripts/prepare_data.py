import os
import pandas as pd
import numpy as np

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK"
day2_processed = os.path.join(base_dir, "Day 2", "data", "processed")
capstone_raw = os.path.join(base_dir, "Capstone - Mutual Fund Analytics", "data", "raw")
dashboard_raw = os.path.join(base_dir, "Dashboard", "data", "raw")
os.makedirs(dashboard_raw, exist_ok=True)

print("Preparing datasets for Power BI...")

# 1. Load dim_fund (from Day 2 fund_master.csv)
print("Processing dim_fund...")
df_fund = pd.read_csv(os.path.join(day2_processed, "fund_master.csv"))
df_fund.drop_duplicates(subset=["scheme_code"], keep="first", inplace=True)
df_fund.rename(columns={"scheme_code": "amfi_code"}, inplace=True)
df_fund.to_csv(os.path.join(dashboard_raw, "dim_fund.csv"), index=False)

# 2. Load fact_performance (from Day 2 scheme_performance.csv)
print("Processing fact_performance...")
df_perf = pd.read_csv(os.path.join(day2_processed, "scheme_performance.csv"))
df_perf.rename(columns={"scheme_code": "amfi_code"}, inplace=True)
df_perf.to_csv(os.path.join(dashboard_raw, "fact_performance.csv"), index=False)

# 3. Load fact_transactions (from Day 2 investor_transactions.csv)
print("Processing fact_transactions...")
df_trans = pd.read_csv(os.path.join(day2_processed, "investor_transactions.csv"))
df_trans.rename(columns={"scheme_code": "amfi_code", "transaction_date": "date"}, inplace=True)
df_trans.to_csv(os.path.join(dashboard_raw, "fact_transactions.csv"), index=False)

# 4. Load fact_nav (combining nav_history.csv and the 6 scheme NAVs)
print("Processing fact_nav...")
nav_dfs = []
df_nav_hist = pd.read_csv(os.path.join(day2_processed, "nav_history.csv"))
nav_dfs.append(df_nav_hist)

scheme_files = [
    "axis_bluechip_119092.csv",
    "hdfc_top_100_125497.csv",
    "icici_bluechip_120503.csv",
    "kotak_bluechip_120841.csv",
    "nippon_large_cap_118632.csv",
    "sbi_bluechip_119551.csv"
]

for filename in scheme_files:
    filepath = os.path.join(day2_processed, filename)
    if os.path.exists(filepath):
        df_scheme = pd.read_csv(filepath)
        nav_dfs.append(df_scheme)

df_all_nav = pd.concat(nav_dfs, ignore_index=True)
df_all_nav.drop_duplicates(subset=["scheme_code", "date"], inplace=True)
df_all_nav.rename(columns={"scheme_code": "amfi_code"}, inplace=True)
df_all_nav.to_csv(os.path.join(dashboard_raw, "fact_nav.csv"), index=False)

# 5. Load fact_aum (from Capstone aum_growth.csv)
print("Processing fact_aum...")
df_aum = pd.read_csv(os.path.join(capstone_raw, "aum_growth.csv"))
df_aum.to_csv(os.path.join(dashboard_raw, "fact_aum.csv"), index=False)

# 6. Load investor_demographics (from Capstone investor_demographics.csv)
print("Processing investor_demographics...")
df_demo = pd.read_csv(os.path.join(capstone_raw, "investor_demographics.csv"))
df_demo.to_csv(os.path.join(dashboard_raw, "investor_demographics.csv"), index=False)

# 7. Generate fact_market_index (Nifty 50 index from 2022 to 2025)
print("Generating Nifty 50 market index data...")
dates = pd.date_range(start="2022-01-01", end="2025-12-31", freq="B")
np.random.seed(42)
n_days = len(dates)

# Generate a realistic Nifty 50 path: starting at 17,354, correcting in 2022, bull run in 2023, correction in 2024, rally in 2025
nifty_path = [17354.0]
for d in dates[1:]:
    year = d.year
    month = d.month
    if year == 2022:
        drift = -0.04 / 252  # Negative drift
        vol = 0.15 / np.sqrt(252)
    elif year == 2023:
        drift = 0.22 / 252  # Strong positive drift
        vol = 0.10 / np.sqrt(252)
    elif year == 2024:
        if 4 <= month <= 9:  # Correction period
            drift = -0.15 / 252
            vol = 0.16 / np.sqrt(252)
        else:
            drift = 0.18 / 252
            vol = 0.12 / np.sqrt(252)
    else:  # 2025
        drift = 0.15 / 252  # Steady growth
        vol = 0.11 / np.sqrt(252)
        
    pct_change = np.random.normal(drift, vol)
    nifty_path.append(nifty_path[-1] * (1.0 + pct_change))

df_nifty = pd.DataFrame({
    "date": dates.strftime("%Y-%m-%d"),
    "index_name": "Nifty 50",
    "close": np.round(nifty_path, 2)
})
df_nifty.to_csv(os.path.join(dashboard_raw, "fact_market_index.csv"), index=False)
print("Generated fact_market_index.csv.")

# 8. Generate dim_date (comprehensive date dimension from unique dates in NAV and transactions)
print("Generating dim_date...")
all_dates = pd.concat([
    df_all_nav['date'],
    df_trans['date'],
    df_nifty['date']
]).unique()

df_dates = pd.DataFrame({"date": all_dates})
df_dates['date_dt'] = pd.to_datetime(df_dates['date'])
df_dates.dropna(subset=['date_dt'], inplace=True)
df_dates.sort_values(by='date_dt', inplace=True)

df_dates['day'] = df_dates['date_dt'].dt.day
df_dates['month'] = df_dates['date_dt'].dt.month
df_dates['year'] = df_dates['date_dt'].dt.year
df_dates['quarter'] = df_dates['date_dt'].dt.quarter
df_dates['day_of_week'] = df_dates['date_dt'].dt.day_name()

df_dates_loaded = df_dates.drop(columns=['date_dt'])
df_dates_loaded.to_csv(os.path.join(dashboard_raw, "dim_date.csv"), index=False)
print(f"Generated dim_date.csv with {len(df_dates_loaded)} dates.")

print("\nAll 8 tables prepared and exported to Dashboard/data/raw/ successfully!")
