# Bluestock - Day 1 Data Ingestion System

A production-ready data ingestion, fetching, and validation pipeline for Mutual Fund Net Asset Value (NAV) datasets, built with Python, Pandas, and the AMFI API.

## Project Overview
This repository contains the implementation of the **Day 1 Data Ingestion** pipeline for the Bluestock project. The system is designed to:
1. Fetch live and historical NAV data directly from the public Association of Mutual Funds in India (AMFI) API.
2. Structure, parse, clean, and write records locally.
3. Profile and ingest raw datasets, logging key data properties (shape, types, missing values, duplicates).
4. Run exploratory analysis on fund master lists.
5. Validate code consistency (referential integrity) between fund master entries and NAV history files.
6. Generate automated data quality metrics.

---

## Folder Structure
The project folder structure is structured as follows:

```text
C:\Users\AKASH\Desktop\BLUESTOCK\
│
├── data/
│   ├── raw/                  # Source CSVs (mock and fetched live data)
│   └── processed/            # Cleaned/transformed data
│
├── notebooks/                # Jupyter Notebooks for analysis
├── sql/                      # SQL scripts for database operations
├── dashboard/                # Dash / Streamlit configuration files
├── reports/                  # Data Quality Reports
│   └── day1_data_quality.md  # Detailed data profiling and quality insights
│
├── scripts/                  # Supporting scripts (mock generator, logs)
│   ├── generate_mock_data.py # Programmatically populates data/raw/
│   ├── data_ingestion.log    # Log file for data_ingestion.py
│   ├── live_nav_fetch.log    # Log file for live_nav_fetch.py
│   ├── fund_master_exploration.log
│   └── amfi_validation.log
│
├── data_ingestion.py         # Loads and profiles all CSVs in data/raw/
├── live_nav_fetch.py         # Fetches real-time NAV records from AMFI
├── fund_master_exploration.py# Computes distributions and stats on fund_master.csv
├── amfi_validation.py        # Validates AMFI codes cross-referencing files
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project instructions and documentation
└── .gitignore                # Git ignore file
```

---

## Installation Steps
Follow these steps to set up the project on your local machine:

1. **Navigate to the Project Root**:
   ```powershell
   cd C:\Users\AKASH\Desktop\BLUESTOCK
   ```

2. **Set up a Virtual Environment** (Recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## Execution Steps

Execute the scripts in the following order to run the entire end-to-end data pipeline:

1. **Step 1: Populate Initial Master Datasets (Mock Data)**
   Generate the initial `fund_master.csv`, `nav_history.csv`, `user_portfolio.csv`, and `scheme_categories.csv` containing sample fund houses and historical data.
   ```powershell
   python scripts/generate_mock_data.py
   ```

2. **Step 2: Fetch Live NAV Data from AMFI**
   Fetch live data for HDFC Top 100 (125497) and the 5 key schemes and save them individually in `data/raw/`.
   ```powershell
   python live_nav_fetch.py
   ```

3. **Step 3: Run Ingestion and Profiling**
   Ingest all 10 CSVs, log dataset properties, missing records, and duplicate counts.
   ```powershell
   python data_ingestion.py
   ```

4. **Step 4: Explore Fund Master Details**
   Output distribution counts of unique fund houses, categories, subcategories, and risk grades.
   ```powershell
   python fund_master_exploration.py
   ```

5. **Step 5: Run AMFI Scheme Validation**
   Check for referential integrity between `fund_master.csv` and `nav_history.csv`.
   ```powershell
   python amfi_validation.py
   ```

---

## Data Ingestion Workflow
1. **Source Scanning**: The `data_ingestion.py` script reads the `data/raw` folder to locate all CSV files.
2. **Error-Resistant Loading**: Each file is loaded into a Pandas DataFrame inside `try-except` blocks to handle missing columns, corrupted rows, or file absence gracefully.
3. **Data Profiling**: Computes dataset shape, data types, missing records per column, duplicate counts, and extracts the first 5 records.
4. **Structured Logging**: Outputs results to both standard output and `scripts/data_ingestion.log`.

---

## NAV Fetching Workflow
1. **Dynamic Iteration**: The `live_nav_fetch.py` script loops through target scheme codes.
2. **REST API Invocations**: Communicates with `https://api.mfapi.in/mf/<scheme_code>` using the `requests` library.
3. **JSON Extraction**: Parses HTTP response body, checks if the status is SUCCESS, and separates the metadata (`meta`) from actual records (`data`).
4. **Parsing & Clean-up**: Translates API date values (`DD-MM-YYYY`) to standard format (`YYYY-MM-DD`), casts values to numeric, and sorts chronologically.
5. **File Serialization**: Writes individual records to `data/raw/<scheme_slug>_<scheme_code>.csv`.

---

## Git Setup and Commands
Run the following commands to initialize the repository, commit files, connect to your remote repository, and push the codebase:

```powershell
# 1. Initialize a new Git repository
git init

# 2. Add files to the staging area
git add .

# 3. Create your first commit
git commit -m "Day 1: Data ingestion complete"

# 4. Rename the default branch to main
git branch -M main

# 5. Connect the local repository to your remote GitHub repository
git remote add origin https://github.com/akashimuthu27/Bluestock.git

# 6. Push the code and set origin main as upstream
git push -u origin main
```
