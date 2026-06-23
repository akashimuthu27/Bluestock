import os
import sys
import logging
import pandas as pd

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scripts/fund_master_exploration.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("fund_master_exploration")

def explore_fund_master(filepath):
    """
    Loads fund_master.csv and logs a detailed exploratory data analysis.
    """
    logger.info(f"Loading fund master file from: {filepath}")
    
    try:
        if not os.path.exists(filepath):
            logger.error(f"Fund master file not found: {filepath}")
            return False
            
        df = pd.read_csv(filepath)
        
        # 1. Total Records
        total_records = len(df)
        
        # 2. Unique counts
        unique_houses = df["fund_house"].nunique()
        unique_categories = df["category"].nunique()
        unique_sub_categories = df["sub_category"].nunique()
        unique_risk_grades = df["risk_grade"].nunique()
        
        logger.info("==================================================")
        logger.info("          MUTUAL FUND MASTER EXPLORATION          ")
        logger.info("==================================================")
        logger.info(f"Total Records: {total_records}")
        logger.info(f"Unique Fund Houses: {unique_houses}")
        logger.info(f"Unique Categories: {unique_categories}")
        logger.info(f"Unique Sub-Categories: {unique_sub_categories}")
        logger.info(f"Unique Risk Grades: {unique_risk_grades}")
        logger.info("==================================================\n")
        
        # 3. Distribution Summaries (Summary Statistics)
        logger.info("--- Fund Houses Distribution ---")
        house_counts = df["fund_house"].value_counts(dropna=False)
        for house, count in house_counts.items():
            logger.info(f"  - {house}: {count} schemes")
            
        logger.info("\n--- Category Distribution ---")
        category_counts = df["category"].value_counts(dropna=False)
        for cat, count in category_counts.items():
            logger.info(f"  - {cat}: {count} schemes")
            
        logger.info("\n--- Sub-Category Distribution ---")
        sub_cat_counts = df["sub_category"].value_counts(dropna=False)
        for sub_cat, count in sub_cat_counts.items():
            logger.info(f"  - {sub_cat}: {count} schemes")
            
        logger.info("\n--- Risk Grade Distribution ---")
        risk_counts = df["risk_grade"].value_counts(dropna=False)
        for risk, count in risk_counts.items():
            logger.info(f"  - {risk}: {count} schemes")
            
        # 4. Numeric and Date summaries (if any)
        # Note: In our mock fund_master we have scheme_code and other text fields.
        logger.info("\n--- Scheme Code Summary ---")
        code_min = df["scheme_code"].min()
        code_max = df["scheme_code"].max()
        logger.info(f"  - Scheme Code Range: {code_min} to {code_max}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during fund master exploration: {e}")
        return False

def main():
    filepath = os.path.join("data", "raw", "fund_master.csv")
    success = explore_fund_master(filepath)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
