import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Capstone - Mutual Fund Analytics"
data_raw_dir = os.path.join(base_dir, "data", "raw")
os.makedirs(data_raw_dir, exist_ok=True)

print("Generating daily benchmark index data (2022-2026)...")

# Generate daily business days from 2022-01-01 to 2026-12-31
dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="B")
num_days = len(dates)

# Generate Nifty 50 path
nifty50_path = [17354.0]
for d in dates[1:]:
    year = d.year
    month = d.month
    
    # Set market regimes
    if year == 2022:
        drift = -0.03 / 252
        vol = 0.15 / np.sqrt(252)
    elif year == 2023:
        # Bull run
        drift = 0.28 / 252
        vol = 0.10 / np.sqrt(252)
    elif year == 2024:
        # Correction in mid-year
        if 4 <= month <= 9:
            drift = -0.18 / 252
            vol = 0.18 / np.sqrt(252)
        else:
            drift = 0.15 / 252
            vol = 0.12 / np.sqrt(252)
    elif year == 2025:
        # Recovery
        drift = 0.16 / 252
        vol = 0.11 / np.sqrt(252)
    else: # 2026
        # Moderate growth
        drift = 0.12 / 252
        vol = 0.10 / np.sqrt(252)
        
    pct_change = np.random.normal(drift, vol)
    nifty50_path.append(nifty50_path[-1] * (1.0 + pct_change))

# Generate Nifty 100 path with a 98% correlation to Nifty 50
nifty50_returns = np.diff(nifty50_path) / nifty50_path[:-1]
# Generate noise
noise = np.random.normal(0, 0.002, len(nifty50_returns))
# Combine to get Nifty 100 returns (98% correlation)
nifty100_returns = 0.98 * nifty50_returns + 0.20 * noise

nifty100_path = [17620.0]
for ret in nifty100_returns:
    nifty100_path.append(nifty100_path[-1] * (1.0 + ret))

df_benchmarks = pd.DataFrame({
    "date": dates.strftime("%Y-%m-%d"),
    "nifty_50": np.round(nifty50_path, 2),
    "nifty_100": np.round(nifty100_path, 2)
})

output_path = os.path.join(data_raw_dir, "fact_benchmark_indices.csv")
df_benchmarks.to_csv(output_path, index=False)
print(f"Benchmark indices generated successfully. Saved to: {output_path}")
print(f"Total days: {len(df_benchmarks)}")
print(f"Nifty 50 range: {df_benchmarks['nifty_50'].iloc[0]} to {df_benchmarks['nifty_50'].iloc[-1]}")
print(f"Nifty 100 range: {df_benchmarks['nifty_100'].iloc[0]} to {df_benchmarks['nifty_100'].iloc[-1]}")
