import os
import sys
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scripts/data_ingestion.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("data_ingestion")

def get_csv_files(directory):
    """
    Scans the specified directory and returns a list of absolute paths of CSV files.
    """
    if not os.path.exists(directory):
        logger.error(f"Directory '{directory}' does not exist.")
        return []
        
    csv_files = [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.lower().endswith('.csv')
    ]
    logger.info(f"Found {len(csv_files)} CSV file(s) in '{directory}'.")
    return csv_files

def ingest_and_analyze_dataset(filepath):
    """
    Loads a CSV file into a pandas DataFrame and logs/prints its structure and quality metrics.
    """
    filename = os.path.basename(filepath)
    dataset_name = os.path.splitext(filename)[0]
    
    logger.info(f"==================================================")
    logger.info(f"Ingesting Dataset: {filename}")
    logger.info(f"==================================================")
    
    try:
        # Load dataset
        df = pd.read_csv(filepath)
        logger.info(f"Successfully loaded '{filename}'.")
        
        # 1. Shape
        shape = df.shape
        logger.info(f"Dataset Name: {dataset_name}")
        logger.info(f"Shape (Rows, Columns): {shape}")
        
        # 2. Data Types
        logger.info("\nData Types:")
        for col, dtype in df.dtypes.items():
            logger.info(f"  - {col}: {dtype}")
            
        # 3. Missing Value Summary
        missing_summary = df.isnull().sum()
        logger.info("\nMissing Values Summary:")
        for col, missing_count in missing_summary.items():
            logger.info(f"  - {col}: {missing_count} missing values")
            
        # 4. Duplicate Rows Count
        duplicate_count = df.duplicated().sum()
        logger.info(f"\nDuplicate Row Count: {duplicate_count}")
        
        # 5. First Five Rows
        logger.info("\nFirst Five Rows:")
        # We can format the head as string for the logger
        head_str = df.head(5).to_string()
        logger.info(f"\n{head_str}\n")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"File not found error: '{filepath}' could not be located.")
    except pd.errors.EmptyDataError:
        logger.error(f"Empty data error: '{filename}' is empty or contains no columns.")
    except pd.errors.ParserError as e:
        logger.error(f"Parsing error: Failed to parse CSV for '{filename}': {e}")
    except Exception as e:
        logger.error(f"Unexpected error while reading '{filename}': {e}")
        
    return None

def main():
    logger.info("Starting Day 1 Data Ingestion process...")
    raw_data_dir = os.path.join("data", "raw")
    
    csv_files = get_csv_files(raw_data_dir)
    if not csv_files:
        logger.warning("No CSV files found to ingest.")
        sys.exit(0)
        
    loaded_count = 0
    for file_path in csv_files:
        df = ingest_and_analyze_dataset(file_path)
        if df is not None:
            loaded_count += 1
            
    logger.info(f"Data ingestion completed. Loaded and analyzed {loaded_count}/{len(csv_files)} datasets.")

if __name__ == "__main__":
    main()
