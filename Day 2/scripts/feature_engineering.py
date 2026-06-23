import os
import sys
import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scripts/feature_engineering.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("feature_engineering")

def calculate_fund_metrics(filepath):
    """
    Loads a cleaned timeseries NAV dataset and computes:
    - CAGR (Compound Annual Growth Rate)
    - Annualized Volatility
    - Sharpe Ratio (using risk-free rate of 6.0%)
    - Max Drawdown
    """
    filename = os.path.basename(filepath)
    logger.info(f"Computing financial metrics for: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        if len(df) < 2:
            logger.warning(f"Not enough records in {filename} to compute metrics.")
            return None
            
        # Standardize date and sort
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values(by='date', ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # 1. Calculate CAGR
        start_date = df['date'].iloc[0]
        end_date = df['date'].iloc[-1]
        days = (end_date - start_date).days
        years = days / 365.25
        
        start_nav = df['nav'].iloc[0]
        end_nav = df['nav'].iloc[-1]
        
        if start_nav <= 0 or end_nav <= 0 or years <= 0:
            logger.warning(f"Invalid NAV values or duration in {filename}. Start: {start_nav}, End: {end_nav}, Years: {years}")
            cagr = np.nan
        else:
            cagr = (end_nav / start_nav) ** (1 / years) - 1
            
        # 2. Calculate Annual Volatility
        df['daily_return'] = df['nav'].pct_change()
        daily_std = df['daily_return'].std()
        # Annualized volatility (assuming 252 trading days per year)
        annual_volatility = daily_std * np.sqrt(252) if not np.isnan(daily_std) else 0.0
        
        # 3. Calculate Sharpe Ratio (Risk-free rate = 6% or 0.06)
        rf = 0.06
        if annual_volatility > 0 and not np.isnan(cagr):
            sharpe_ratio = (cagr - rf) / annual_volatility
        else:
            sharpe_ratio = np.nan
            
        # 4. Calculate Maximum Drawdown
        # Peak represents the running maximum of the NAV up to that point
        rolling_peak = df['nav'].cummax()
        drawdowns = (df['nav'] - rolling_peak) / rolling_peak
        max_drawdown = drawdowns.min()
        
        scheme_code = df['scheme_code'].iloc[0] if 'scheme_code' in df.columns else 'Unknown'
        scheme_name = df['scheme_name'].iloc[0] if 'scheme_name' in df.columns else filename.split('_')[0]
        
        metrics = {
            "scheme_code": scheme_code,
            "scheme_name": scheme_name,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "duration_years": round(years, 2),
            "start_nav": round(start_nav, 4),
            "end_nav": round(end_nav, 4),
            "cagr": round(cagr, 4) if not np.isnan(cagr) else np.nan,
            "annual_volatility": round(annual_volatility, 4),
            "sharpe_ratio": round(sharpe_ratio, 4) if not np.isnan(sharpe_ratio) else np.nan,
            "max_drawdown": round(max_drawdown, 4)
        }
        
        logger.info(f"  - CAGR: {metrics['cagr'] * 100:.2f}%, Volatility: {metrics['annual_volatility'] * 100:.2f}%, Sharpe: {metrics['sharpe_ratio']}, Max Drawdown: {metrics['max_drawdown'] * 100:.2f}%")
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating metrics for {filename}: {e}")
        return None

def main():
    logger.info("Starting Day 2 Feature Engineering & Metric Generation...")
    processed_dir = os.path.join("data", "processed")
    
    # We will compute metrics for the 6 live fetched schemes
    live_files = [
        "sbi_bluechip_119551.csv",
        "icici_bluechip_120503.csv",
        "nippon_large_cap_118632.csv",
        "axis_bluechip_119092.csv",
        "kotak_bluechip_120841.csv",
        "hdfc_top_100_125497.csv"
    ]
    
    results = []
    for filename in live_files:
        filepath = os.path.join(processed_dir, filename)
        if os.path.exists(filepath):
            metrics = calculate_fund_metrics(filepath)
            if metrics is not None:
                results.append(metrics)
        else:
            logger.warning(f"Processed file '{filename}' does not exist. Run data_cleaning.py first.")
            
    if results:
        df_metrics = pd.DataFrame(results)
        output_filepath = os.path.join(processed_dir, "fund_performance_metrics.csv")
        df_metrics.to_csv(output_filepath, index=False)
        logger.info(f"Feature engineering completed. Performance metrics saved to '{output_filepath}'.")
    else:
        logger.error("No metrics could be calculated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
