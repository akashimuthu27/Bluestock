import os
import sys
import logging
import pandas as pd
import numpy as np

# Configure logging
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Day 2"
log_filepath = os.path.join(base_dir, "scripts", "data_cleaning.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("data_cleaning")

def clean_nav_history_file(filepath, output_dir):
    """
    Cleans nav_history.csv or individual scheme NAV files:
    - Parses dates to datetime.
    - Removes duplicate records.
    - Validates NAV > 0 (removes <= 0).
    - Sorts by scheme_code + date.
    - Forward-fills missing NAV for holidays/weekends.
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning NAV history dataset: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # 1. Deduplication
        df.drop_duplicates(inplace=True)
        
        # 2. Type casting and validation
        df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').astype(np.int64)
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        
        # Filter out NAV <= 0
        df = df[df['nav'] > 0]
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.dropna(subset=['date', 'nav'], inplace=True)
        
        # 3. Sort by scheme_code and date
        df.sort_values(by=['scheme_code', 'date'], ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # 4. Forward-fill missing NAV for holidays/weekends
        # We group by scheme_code and reindex to a daily date range, then ffill
        filled_dfs = []
        for code, group in df.groupby('scheme_code'):
            group = group.set_index('date')
            # Generate complete daily date range
            daily_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
            # Reindex and forward-fill
            group_filled = group.reindex(daily_range)
            group_filled['scheme_code'] = code
            group_filled['nav'] = group_filled['nav'].ffill().bfill()
            group_filled = group_filled.reset_index().rename(columns={'index': 'date'})
            filled_dfs.append(group_filled)
            
        if filled_dfs:
            df_cleaned = pd.concat(filled_dfs, ignore_index=True)
        else:
            df_cleaned = df.copy()
            
        # Format date as YYYY-MM-DD
        df_cleaned['date'] = df_cleaned['date'].dt.strftime('%Y-%m-%d')
        
        final_shape = df_cleaned.shape
        logger.info(f"Cleaned {filename}. Rows before: {initial_shape[0]}, after: {final_shape[0]} (holiday-filled)")
        
        # Save output
        os.makedirs(output_dir, exist_ok=True)
        df_cleaned.to_csv(os.path.join(output_dir, filename), index=False)
        return df_cleaned
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_investor_transactions(filepath, output_dir):
    """
    Cleans investor_transactions.csv:
    - Standardises transaction_type to ['SIP', 'Lumpsum', 'Redemption'].
    - Validates amount > 0.
    - Fixes various date formats to YYYY-MM-DD.
    - Maps and checks KYC status enum values to ['Yes', 'No', 'Pending'].
    - Deduplicates.
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning investor transactions dataset: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # 1. Deduplication
        df.drop_duplicates(inplace=True)
        
        # 2. Standardise transaction_type
        # Map dirty values to standard ones
        tx_mapping = {
            'SIP': 'SIP', 'sip': 'SIP', 'Sip': 'SIP',
            'Lumpsum': 'Lumpsum', 'lumpsum': 'Lumpsum', 'LUMP-SUM': 'Lumpsum', 'PURCHASE': 'Lumpsum',
            'Redemption': 'Redemption', 'redemption': 'Redemption'
        }
        df['transaction_type'] = df['transaction_type'].str.strip().map(tx_mapping).fillna('Lumpsum')
        
        # 3. Validate amount > 0
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        # Log rows being dropped
        invalid_amount_count = (df['amount'] <= 0).sum() + df['amount'].isnull().sum()
        if invalid_amount_count > 0:
            logger.warning(f"  - Dropping {invalid_amount_count} transactions with invalid amount <= 0 or null in {filename}")
        df = df[df['amount'] > 0]
        
        # 4. Fix date formats
        # pd.to_datetime handles mixed formats elegantly when format='mixed' is used
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='mixed', errors='coerce')
        df.dropna(subset=['transaction_date'], inplace=True)
        df['transaction_date'] = df['transaction_date'].dt.strftime('%Y-%m-%d')
        
        # 5. KYC Status mapping
        kyc_mapping = {
            'Yes': 'Yes', 'yes': 'Yes', 'Y': 'Yes',
            'No': 'No', 'no': 'No', 'N': 'No',
            'Pending': 'Pending', 'PENDING': 'Pending'
        }
        df['kyc_status'] = df['kyc_status'].str.strip().map(kyc_mapping).fillna('Pending')
        
        # Cast ids
        df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').astype(np.int64)
        df['investor_id'] = pd.to_numeric(df['investor_id'], errors='coerce').astype(np.int64)
        
        final_shape = df.shape
        logger.info(f"Cleaned {filename}. Rows before: {initial_shape[0]}, after: {final_shape[0]}")
        
        # Save output
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_scheme_performance(filepath, output_dir):
    """
    Cleans scheme_performance.csv:
    - Validates all return values are numeric (converts '%' and string 'N/A').
    - Flags anomalies in returns.
    - Validates expense_ratio is in range 0.1% to 2.5% (represented as 0.1 to 2.5).
    - Adds anomaly flag columns.
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning scheme performance dataset: {filename}")
    
    try:
        df = pd.read_csv(filepath)
        initial_shape = df.shape
        
        # Deduplicate
        df.drop_duplicates(inplace=True)
        
        # Function to clean percentage strings to float
        def clean_pct_string(val):
            if pd.isnull(val):
                return np.nan
            val_str = str(val).strip().replace('%', '')
            if val_str == 'N/A' or val_str == 'nan' or val_str == '':
                return np.nan
            try:
                return float(val_str)
            except ValueError:
                return np.nan
                
        df['cagr_3yr'] = df['cagr_3yr'].apply(clean_pct_string)
        df['cagr_5yr'] = df['cagr_5yr'].apply(clean_pct_string)
        
        # Fill missing returns with median
        df['cagr_3yr'] = df['cagr_3yr'].fillna(df['cagr_3yr'].median())
        df['cagr_5yr'] = df['cagr_5yr'].fillna(df['cagr_5yr'].median())
        
        # Check expense_ratio range (0.1% to 2.5%, which is 0.1 to 2.5)
        df['expense_ratio'] = pd.to_numeric(df['expense_ratio'], errors='coerce')
        
        # Add anomaly flag columns
        df['expense_ratio_anomaly'] = 0
        df['return_anomaly'] = 0
        
        # Flag expense ratio anomalies
        ratio_out_of_bounds = (df['expense_ratio'] < 0.1) | (df['expense_ratio'] > 2.5)
        df.loc[ratio_out_of_bounds, 'expense_ratio_anomaly'] = 1
        
        for idx, row in df[ratio_out_of_bounds].iterrows():
            logger.warning(f"  - Expense ratio anomaly flagged for scheme {row['scheme_code']}: {row['expense_ratio']}% (out of bounds 0.1% - 2.5%)")
            
        # Clip/correct expense ratios to boundary if they are out of bounds
        df['expense_ratio'] = df['expense_ratio'].clip(lower=0.1, upper=2.5)
        
        # Flag return anomalies (e.g. returns > 50% or < -20% which is unusual for large caps)
        return_outliers = (df['cagr_3yr'] > 50.0) | (df['cagr_3yr'] < -20.0) | (df['cagr_5yr'] > 50.0) | (df['cagr_5yr'] < -20.0)
        df.loc[return_outliers, 'return_anomaly'] = 1
        
        # Cast ids
        df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').astype(np.int64)
        
        final_shape = df.shape
        logger.info(f"Cleaned {filename}. Rows before: {initial_shape[0]}, after: {final_shape[0]}")
        
        # Save output
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_fund_master_simple(filepath, output_dir):
    """
    Cleans fund_master.csv:
    - Deduplicates.
    - Imputes category and risk_grade.
    """
    filename = os.path.basename(filepath)
    logger.info(f"Cleaning fund master: {filename}")
    try:
        df = pd.read_csv(filepath)
        df.drop_duplicates(inplace=True)
        df['category'] = df['category'].fillna("Equity")
        df['risk_grade'] = df['risk_grade'].fillna("Very High")
        df['scheme_code'] = pd.to_numeric(df['scheme_code'], errors='coerce').astype(np.int64)
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, filename), index=False)
        return df
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")
        return None

def clean_generic(filepath, output_dir):
    """
    Deduplicates and copies generic CSV files.
    """
    filename = os.path.basename(filepath)
    logger.info(f"Deduplicating generic file: {filename}")
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
    logger.info("Starting Day 2 Data Cleaning Pipeline...")
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    
    if not os.path.exists(raw_dir):
        logger.error(f"Raw data directory '{raw_dir}' does not exist.")
        sys.exit(1)
        
    # We define the 10 target files we want to process
    target_files = [
        "axis_bluechip_119092.csv",
        "hdfc_top_100_125497.csv",
        "icici_bluechip_120503.csv",
        "kotak_bluechip_120841.csv",
        "nippon_large_cap_118632.csv",
        "sbi_bluechip_119551.csv",
        "fund_master.csv",
        "nav_history.csv",
        "investor_transactions.csv",
        "scheme_performance.csv"
    ]
    
    # Check if they exist
    existing_files = [f for f in target_files if os.path.exists(os.path.join(raw_dir, f))]
    logger.info(f"Found {len(existing_files)} out of 10 target datasets to clean.")
    
    cleaned_count = 0
    for filename in target_files:
        filepath = os.path.join(raw_dir, filename)
        if not os.path.exists(filepath):
            logger.warning(f"Target file '{filename}' is missing in raw folder.")
            continue
            
        if filename == "fund_master.csv":
            res = clean_fund_master_simple(filepath, processed_dir)
        elif filename == "investor_transactions.csv":
            res = clean_investor_transactions(filepath, processed_dir)
        elif filename == "scheme_performance.csv":
            res = clean_scheme_performance(filepath, processed_dir)
        elif filename in ["nav_history.csv"] or filename.endswith("_119092.csv") or filename.endswith("_125497.csv") or filename.endswith("_120503.csv") or filename.endswith("_120841.csv") or filename.endswith("_118632.csv") or filename.endswith("_119551.csv"):
            res = clean_nav_history_file(filepath, processed_dir)
        else:
            res = clean_generic(filepath, processed_dir)
            
        if res is not None:
            cleaned_count += 1
            
    logger.info(f"Data Cleaning Pipeline completed. Successfully processed and saved {cleaned_count}/{len(target_files)} datasets to '{processed_dir}'.")

if __name__ == "__main__":
    main()
