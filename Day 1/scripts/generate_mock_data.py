import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def main():
    print("Generating mock datasets for Bluestock project...")
    
    # Create directories if they don't exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # 1. Generate fund_master.csv
    # Scheme details
    schemes = [
        {"scheme_code": 119551, "scheme_name": "SBI Bluechip Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"scheme_code": 120503, "scheme_name": "ICICI Prudential Bluechip Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"scheme_code": 118632, "scheme_name": "Nippon India Large Cap Fund - Direct Plan - Growth", "fund_house": "Nippon India Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"scheme_code": 119092, "scheme_name": "Axis Bluechip Fund - Direct Plan - Growth", "fund_house": "Axis Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"scheme_code": 120841, "scheme_name": "Kotak Bluechip Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        # Additional schemes for exploration and validation
        {"scheme_code": 119999, "scheme_name": "HDFC Top 100 Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Equity", "sub_category": "Large Cap", "risk_grade": "Very High"},
        {"scheme_code": 120123, "scheme_name": "SBI Small Cap Fund - Direct Plan - Growth", "fund_house": "SBI Mutual Fund", "category": "Equity", "sub_category": "Small Cap", "risk_grade": "Very High"},
        {"scheme_code": 120456, "scheme_name": "ICICI Prudential Liquid Fund - Direct Plan - Growth", "fund_house": "ICICI Prudential Mutual Fund", "category": "Debt", "sub_category": "Liquid", "risk_grade": "Low to Moderate"},
        {"scheme_code": 120789, "scheme_name": "HDFC Balanced Advantage Fund - Direct Plan - Growth", "fund_house": "HDFC Mutual Fund", "category": "Hybrid", "sub_category": "Balanced Advantage", "risk_grade": "High"},
        {"scheme_code": 120999, "scheme_name": "Kotak Debt Hybrid Fund - Direct Plan - Growth", "fund_house": "Kotak Mahindra Mutual Fund", "category": "Hybrid", "sub_category": "Conservative Hybrid", "risk_grade": "Moderate"}
    ]
    
    df_master = pd.DataFrame(schemes)
    
    # Introduce a couple of duplicate rows to test data quality reports
    df_master = pd.concat([df_master, df_master.iloc[[0, 1]]], ignore_index=True)
    
    # Introduce some missing value fields to test missing value reporting
    df_master.loc[len(df_master)-1, "risk_grade"] = np.nan
    df_master.loc[len(df_master)-2, "category"] = np.nan
    
    df_master.to_csv("data/raw/fund_master.csv", index=False)
    print(f"Saved {len(df_master)} records to data/raw/fund_master.csv")
    
    # 2. Generate nav_history.csv
    # We will generate daily NAV records for the last 30 days for some of the schemes.
    # We intentionally exclude scheme_code 119999 (HDFC Top 100) and 120999 (Kotak Debt Hybrid) 
    # to test AMFI validation logic for missing codes.
    active_codes = [119551, 120503, 118632, 119092, 120841, 120123, 120456, 120789]
    
    base_navs = {
        119551: 75.5,
        120503: 82.3,
        118632: 64.2,
        119092: 52.1,
        120841: 48.9,
        120123: 135.2,
        120456: 320.4,
        120789: 385.6
    }
    
    history_records = []
    end_date = datetime.now()
    
    for code in active_codes:
        base_nav = base_navs[code]
        for day in range(30):
            date_val = (end_date - timedelta(days=day)).strftime("%Y-%m-%d")
            # add small random walk
            nav_val = round(base_nav + np.random.normal(0, base_nav * 0.01), 4)
            history_records.append({
                "scheme_code": code,
                "nav": nav_val,
                "date": date_val
            })
            
    df_history = pd.DataFrame(history_records)
    
    # Introduce a couple of duplicate records in nav_history
    df_history = pd.concat([df_history, df_history.iloc[[0, 1]]], ignore_index=True)
    
    # Introduce a few missing NAV values to test data quality check
    df_history.loc[len(df_history)-1, "nav"] = np.nan
    
    df_history.to_csv("data/raw/nav_history.csv", index=False)
    print(f"Saved {len(df_history)} records to data/raw/nav_history.csv")
    
    # 3. Generate user_portfolio.csv
    portfolio = [
        {"scheme_code": 119551, "units_held": 150.5, "purchase_nav": 72.1, "purchase_date": "2026-05-15"},
        {"scheme_code": 120503, "units_held": 200.0, "purchase_nav": 80.0, "purchase_date": "2026-05-20"},
        {"scheme_code": 118632, "units_held": 350.2, "purchase_nav": 61.5, "purchase_date": "2026-06-01"},
        {"scheme_code": 125497, "units_held": 100.0, "purchase_nav": 550.0, "purchase_date": "2026-06-10"}
    ]
    df_portfolio = pd.DataFrame(portfolio)
    df_portfolio.to_csv("data/raw/user_portfolio.csv", index=False)
    print(f"Saved {len(df_portfolio)} records to data/raw/user_portfolio.csv")

    # 4. Generate scheme_categories.csv
    categories = [
        {"category_id": "EQ_LC", "category_name": "Equity - Large Cap", "description": "Invests primarily in large-cap stocks for long-term growth."},
        {"category_id": "EQ_SC", "category_name": "Equity - Small Cap", "description": "Invests in small-cap companies with high growth potential and higher volatility."},
        {"category_id": "DB_LQ", "category_name": "Debt - Liquid", "description": "Low-risk debt instruments with short maturities."},
        {"category_id": "HY_BA", "category_name": "Hybrid - Balanced Advantage", "description": "Dynamically manages equity and debt allocation."}
    ]
    df_categories = pd.DataFrame(categories)
    df_categories.to_csv("data/raw/scheme_categories.csv", index=False)
    print(f"Saved {len(df_categories)} records to data/raw/scheme_categories.csv")
    
    # Create empty directories to complete folder structure
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("sql", exist_ok=True)
    os.makedirs("dashboard", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    print("Mock data generation and folder structure setup completed successfully.")

if __name__ == "__main__":
    main()
