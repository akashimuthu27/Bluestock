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
        logging.FileHandler("scripts/data_cleaning.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("data_cleaning")

def clean_fund_master(filepath, output_dir):
    """
    Cleans fund_master.csv:
    - Deduplicates
    - Imputes missing category & risk_grade
    - Casts types
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning master dataset: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # 1. Deduplication
        df.drop_duplicates(inplace=True)
        
        # 2. Imputation of missing categorical variables
        df['category'] = df['category'].fillna("Equity")
        df['risk_grade'] = df['risk_grade'].fillna("Very High")
        
        # 3. Type Casting
        df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').dropna().astype(np.int64)
        
        final_shape = df.shape
        logger.info(f"Cleaned {filename}. Rows before: {initial_shape[0]}, after: {final_shape[0]}")
        
        # Save output
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_timeseries_nav(filepath, output_dir):
    """
    Cleans NAV historical CSVs:
    - Deduplicates
    - Imputes missing NAV values using ffill & bfill
    - Formats dates & casts types
    - Identifies and smooths outliers using a rolling Z-score (threshold=3.0)
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning NAV timeseries dataset: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # 1. Deduplication
        df.drop_duplicates(inplace=True)
        
        # 2. Type Casting
        if 'scheme_code' in df.columns:
            df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').astype(np.int64)
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        
        # Treat <= 0 NAVs as invalid/missing (Mutual Fund NAVs must be positive)
        zero_nav_mask = df['nav'] <= 0
        if zero_nav_mask.any():
            logger.warning(f"  - Found {zero_nav_mask.sum()} invalid NAV value(s) <= 0 in {filename}. Setting to NaN.")
            df.loc[zero_nav_mask, 'nav'] = np.nan
            
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Sort by date ascending to ensure proper timeseries imputation & rolling metrics
        df.sort_values(by='date', ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Detect and adjust structural scaling breaks (e.g., historical 100x decimal shift)
        # We look for a daily return ratio near 100 (between 90 and 110)
        for i in range(1, len(df)):
            prev_val = df.loc[i-1, 'nav']
            curr_val = df.loc[i, 'nav']
            if pd.notnull(prev_val) and pd.notnull(curr_val) and prev_val > 0:
                ratio = curr_val / prev_val
                if 90 <= ratio <= 110:
                    # Verify it's a permanent structural shift by checking means post and pre
                    post_mean = df.loc[i:i+10, 'nav'].mean()
                    pre_mean = df.loc[max(0, i-10):i-1, 'nav'].mean()
                    if pre_mean > 0 and 90 <= (post_mean / pre_mean) <= 110:
                        logger.info(f"  - Detected structural 100x scaling break on {df.loc[i, 'date'].strftime('%Y-%m-%d')} in {filename}. Scaling historical NAVs by 100x.")
                        df.loc[0:i-1, 'nav'] = df.loc[0:i-1, 'nav'] * 100
                        break
        
        # 3. Imputation of missing NAVs
        missing_count = df['nav'].isnull().sum()
        if missing_count > 0:
            logger.info(f"  - Imputing {missing_count} missing NAV values in {filename} using ffill/bfill")
            df['nav'] = df['nav'].ffill().bfill()
            
        # 4. Outlier Detection and Smoothing
        # We use a 7-day rolling window. If a NAV value deviates from the 7-day rolling mean
        # by more than 3 standard deviations, we replace it with the rolling mean.
        window = 7
        threshold = 3.0
        
        # Calculate rolling mean and standard deviation
        rolling_mean = df['nav'].rolling(window=window, min_periods=1).mean()
        rolling_std = df['nav'].rolling(window=window, min_periods=1).std().fillna(0)
        
        # Compute Z-score
        # Prevent division by zero if std dev is 0
        z_scores = np.zeros(len(df))
        non_zero_std_mask = rolling_std > 0
        z_scores[non_zero_std_mask] = np.abs(df['nav'][non_zero_std_mask] - rolling_mean[non_zero_std_mask]) / rolling_std[non_zero_std_mask]
        
        # Identify outliers
        outliers_mask = z_scores > threshold
        outlier_count = outliers_mask.sum()
        
        if outlier_count > 0:
            logger.info(f"  - Detected {outlier_count} NAV outlier(s) in {filename} (Z-score > {threshold})")
            # Smooth outliers by replacing them with the rolling mean
            df.loc[outliers_mask, 'nav'] = rolling_mean[outliers_mask]
            
        # Format date back as YYYY-MM-DD
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        final_shape = df.shape
        logger.info(f"Cleaned {filename}. Rows before: {initial_shape[0]}, after: {final_shape[0]}")
        
        # Save output
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_generic_dataset(filepath, output_dir):
    """
    Deduplicates and copies generic files (categories, portfolio).
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning generic dataset: {filename}")
    try:
        df = pd.read_csv(filepath)
        df.drop_duplicates(inplace=True)
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def main():
    logger.info("Starting Day 2 Data Cleaning pipeline...")
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")
    
    if not os.path.exists(raw_dir):
        logger.error(f"Raw data directory '{raw_dir}' does not exist.")
        sys.exit(1)
        
    files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.csv')]
    logger.info(f"Found {len(files)} datasets to clean.")
    
    cleaned_count = 0
    for filename in files:
        filepath = os.path.join(raw_dir, filename)
        
        if filename == "fund_master.csv":
            res = clean_fund_master(filepath, processed_dir)
        elif filename in ["user_portfolio.csv", "scheme_categories.csv"]:
            res = clean_generic_dataset(filepath, processed_dir)
        else:
            # All other files are NAV timeseries (nav_history + 6 fetched live files)
            res = clean_timeseries_nav(filepath, processed_dir)
            
        if res is not None:
            cleaned_count += 1
            
    logger.info(f"Data Cleaning completed. Processed and saved {cleaned_count}/{len(files)} datasets into '{processed_dir}'.")

if __name__ == "__main__":
    main()
