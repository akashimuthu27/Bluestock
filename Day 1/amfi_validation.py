import os
import sys
import logging
import pandas as pd

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scripts/amfi_validation.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("amfi_validation")

def validate_amfi_codes(master_path, history_path):
    """
    Validates that all scheme codes in fund_master.csv exist in nav_history.csv.
    Identifies, counts, and summaries missing scheme codes.
    """
    logger.info(f"Loading Master from: {master_path}")
    logger.info(f"Loading History from: {history_path}")
    
    try:
        # Load datasets
        if not os.path.exists(master_path) or not os.path.exists(history_path):
            logger.error("One or both input files do not exist.")
            return None
            
        df_master = pd.read_csv(master_path)
        df_history = pd.read_csv(history_path)
        
        # Verify columns exist
        if "scheme_code" not in df_master.columns:
            logger.error("Missing 'scheme_code' column in fund_master.csv")
            return None
            
        if "scheme_code" not in df_history.columns:
            logger.error("Missing 'scheme_code' column in nav_history.csv")
            return None
            
        # Clean and find unique scheme codes
        master_codes = set(pd.to_numeric(df_master["scheme_code"], errors="coerce").dropna().astype(int))
        history_codes = set(pd.to_numeric(df_history["scheme_code"], errors="coerce").dropna().astype(int))
        
        # Find missing scheme codes (codes in master but not in history)
        missing_codes = master_codes - history_codes
        matching_codes = master_codes & history_codes
        
        total_master = len(master_codes)
        total_history = len(history_codes)
        missing_count = len(missing_codes)
        matching_count = len(matching_codes)
        
        logger.info("==================================================")
        logger.info("             AMFI SCHEME CODE VALIDATION          ")
        logger.info("==================================================")
        logger.info(f"Total Unique Scheme Codes in Master: {total_master}")
        logger.info(f"Total Unique Scheme Codes in History: {total_history}")
        logger.info(f"Matching Scheme Codes: {matching_count} / {total_master} ({matching_count / total_master * 100:.2f}%)")
        logger.info(f"Missing Scheme Codes in History: {missing_count}")
        logger.info("==================================================\n")
        
        summary_details = []
        
        if missing_count > 0:
            logger.info("--- Details of Missing Scheme Codes ---")
            # Lookup scheme names for the missing codes
            for code in sorted(missing_codes):
                # find matching records in master to get scheme name
                matching_rows = df_master[df_master["scheme_code"] == code]
                scheme_name = "Unknown Name"
                fund_house = "Unknown Fund House"
                if not matching_rows.empty:
                    # Drop duplicates if any and get the first one
                    scheme_name = matching_rows.iloc[0].get("scheme_name", "Unknown Name")
                    fund_house = matching_rows.iloc[0].get("fund_house", "Unknown Fund House")
                    
                logger.info(f"  - Code: {code} | {scheme_name} ({fund_house})")
                summary_details.append({
                    "scheme_code": code,
                    "scheme_name": scheme_name,
                    "fund_house": fund_house
                })
        else:
            logger.info("Success: All scheme codes in Master are present in History!")
            
        validation_summary = {
            "total_master_codes": total_master,
            "total_history_codes": total_history,
            "matching_codes_count": matching_count,
            "missing_codes_count": missing_count,
            "missing_codes": summary_details
        }
        
        return validation_summary
        
    except Exception as e:
        logger.error(f"Error during AMFI validation: {e}")
        return None

def main():
    master_path = os.path.join("data", "raw", "fund_master.csv")
    history_path = os.path.join("data", "raw", "nav_history.csv")
    
    summary = validate_amfi_codes(master_path, history_path)
    if summary is None:
        sys.exit(1)

if __name__ == "__main__":
    main()
