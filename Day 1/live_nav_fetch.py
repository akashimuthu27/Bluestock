import os
import sys
import logging
import requests
import pandas as pd

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scripts/live_nav_fetch.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("live_nav_fetch")

# Public API URL
API_URL = "https://api.mfapi.in/mf/{scheme_code}"

# Target scheme list
SCHEMES = {
    119551: "sbi_bluechip",
    120503: "icici_bluechip",
    118632: "nippon_large_cap",
    119092: "axis_bluechip",
    120841: "kotak_bluechip",
    125497: "hdfc_top_100"
}

def fetch_nav_data(scheme_code):
    """
    Fetches NAV records from the public API for a given scheme code.
    Returns metadata dict and a list of NAV records.
    """
    url = API_URL.format(scheme_code=scheme_code)
    logger.info(f"Fetching NAV data for scheme code: {scheme_code} from {url}")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        json_data = response.json()
        
        if not json_data or "data" not in json_data:
            logger.error(f"Invalid response structure from API for scheme: {scheme_code}")
            return None, None
            
        status = json_data.get("status")
        if status != "SUCCESS":
            logger.warning(f"API status was not SUCCESS: {status} for scheme: {scheme_code}")
            
        meta = json_data.get("meta", {})
        nav_records = json_data.get("data", [])
        
        logger.info(f"Successfully fetched {len(nav_records)} NAV records for scheme code: {scheme_code}")
        return meta, nav_records
        
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed for scheme {scheme_code}: {e}")
        return None, None
    except ValueError as e:
        logger.error(f"Failed to parse JSON response for scheme {scheme_code}: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error fetching scheme {scheme_code}: {e}")
        return None, None

def save_nav_to_csv(scheme_code, meta, nav_records):
    """
    Parses, formats, and saves NAV records into a CSV file in data/raw.
    """
    if not nav_records:
        logger.warning(f"No NAV records to save for scheme: {scheme_code}")
        return False
        
    try:
        df = pd.DataFrame(nav_records)
        
        # Verify required columns exist
        if "date" not in df.columns or "nav" not in df.columns:
            logger.error(f"Missing required columns in NAV records for scheme: {scheme_code}")
            return False
            
        # Convert values to correct types
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        # Parse DD-MM-YYYY dates and format as YYYY-MM-DD
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        
        # Add metadata columns
        df['scheme_code'] = scheme_code
        df['scheme_name'] = meta.get('scheme_name', 'Unknown Scheme')
        
        # Sort by date ascending
        df = df.sort_values(by='date', ascending=True)
        
        # Format date as YYYY-MM-DD
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Determine output filename
        custom_name = SCHEMES[scheme_code]
            
        output_dir = "data/raw"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{custom_name}_{scheme_code}.csv"
        filepath = os.path.join(output_dir, filename)
        
        df.to_csv(filepath, index=False)
        logger.info(f"Saved NAV data to {filepath}. Shape: {df.shape}")
        return True
        
    except Exception as e:
        logger.error(f"Error occurred while processing/saving scheme {scheme_code}: {e}")
        return False

def main():
    logger.info("Starting live NAV fetching task...")
    
    success_count = 0
    total_schemes = len(SCHEMES)
    
    for scheme_code in SCHEMES.keys():
        meta, nav_records = fetch_nav_data(scheme_code)
        if meta and nav_records:
            if save_nav_to_csv(scheme_code, meta, nav_records):
                success_count += 1
                
    logger.info(f"Live NAV fetching completed. Successfully processed {success_count}/{total_schemes} schemes.")
    
    if success_count == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
