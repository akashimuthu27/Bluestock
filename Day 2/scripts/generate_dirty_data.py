import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Day 2"
data_raw_dir = os.path.join(base_dir, "data", "raw")
os.makedirs(data_raw_dir, exist_ok=True)

print("Generating dirty raw datasets for Day 2...")

# 1. investor_transactions.csv (dirty dates, transaction types, amounts, kyc status)
# We will generate 200 transaction records
n_records = 200

# Scheme codes from fund_master
scheme_codes = [119551, 120503, 118632, 119092, 120841, 119999, 120123, 120456, 120789, 120999]

# Transaction types with mixed casing and invalid values
tx_types_pool = ["SIP", "sip", "Sip", "Lumpsum", "lumpsum", "LUMP-SUM", "Redemption", "redemption", "PURCHASE"]
tx_types = np.random.choice(tx_types_pool, size=n_records)

# Amounts, with some negative and zero values (anomalies)
amounts = np.random.normal(loc=15000, scale=10000, size=n_records)
# Inject anomalies
amounts[10] = -5000.0
amounts[25] = 0.0
amounts[50] = -1200.0
amounts = np.round(amounts, 2)

# Transaction dates with various formats
dates_pool = [
    "2026-05-15", "15-05-2026", "2026/05/15", "2026-05-20", "20-05-2026", 
    "2026/05/20", "2026-06-01", "01-06-2026", "2026/06/01", "2026-06-10", 
    "10-06-2026", "2026/06/10", "2026-06-15", "15-06-2026", "2026/06/15"
]
tx_dates = np.random.choice(dates_pool, size=n_records)

# KYC status with mixed casing, shorthand, and invalid values
kyc_pool = ["Yes", "No", "Pending", "Y", "N", "PENDING", "yes", "no"]
kyc_statuses = np.random.choice(kyc_pool, size=n_records)

# States
states_pool = ["Maharashtra", "Gujarat", "Karnataka", "Delhi", "Tamil Nadu", "Uttar Pradesh", "West Bengal"]
states = np.random.choice(states_pool, size=n_records)

df_transactions = pd.DataFrame({
    "transaction_id": [f"TXN{10000 + i}" for i in range(n_records)],
    "investor_id": np.random.randint(500000, 501000, size=n_records),
    "scheme_code": np.random.choice(scheme_codes, size=n_records),
    "transaction_type": tx_types,
    "amount": amounts,
    "transaction_date": tx_dates,
    "kyc_status": kyc_statuses,
    "state": states
})

df_transactions.to_csv(os.path.join(data_raw_dir, "investor_transactions.csv"), index=False)
print(f"Generated investor_transactions.csv with {n_records} rows.")

# 2. scheme_performance.csv (non-numeric returns, out-of-bounds expense ratios)
# We will generate one performance record for each of our 10 schemes
scheme_names = [
    "SBI Bluechip Fund - Direct Plan - Growth",
    "ICICI Prudential Bluechip Fund - Direct Plan - Growth",
    "Nippon India Large Cap Fund - Direct Plan - Growth",
    "Axis Bluechip Fund - Direct Plan - Growth",
    "Kotak Bluechip Fund - Direct Plan - Growth",
    "HDFC Top 100 Fund - Direct Plan - Growth",
    "SBI Small Cap Fund - Direct Plan - Growth",
    "ICICI Prudential Liquid Fund - Direct Plan - Growth",
    "HDFC Balanced Advantage Fund - Direct Plan - Growth",
    "Kotak Debt Hybrid Fund - Direct Plan - Growth"
]

# CAGR 3Yr with dirty strings ("%", "N/A", etc.)
cagr_3yr_pool = ["15.5%", "12.4", "N/A", "18.2%", "10.1", "14.8%", "11.2", "6.5%", "13.9%", "8.2"]
# CAGR 5Yr
cagr_5yr_pool = ["14.2", "11.8%", "16.5", "15.9%", "9.5", "13.4%", "10.5", "N/A", "12.8%", "7.5"]

# Expense ratios, with some out-of-bounds values (valid is 0.1% to 2.5%, representing 0.1 to 2.5)
# Let's put some anomalies: 3.2 (too high), 0.05 (too low), 1.2, 1.8, 0.85
expense_ratios = [1.2, 1.8, 0.85, 3.2, 0.05, 1.1, 1.5, 0.25, 0.95, 0.65]

df_performance = pd.DataFrame({
    "scheme_code": scheme_codes,
    "scheme_name": scheme_names,
    "cagr_3yr": cagr_3yr_pool,
    "cagr_5yr": cagr_5yr_pool,
    "expense_ratio": expense_ratios
})

df_performance.to_csv(os.path.join(data_raw_dir, "scheme_performance.csv"), index=False)
print(f"Generated scheme_performance.csv with {len(df_performance)} rows.")

print("Dirty datasets generated successfully under data/raw/!")
