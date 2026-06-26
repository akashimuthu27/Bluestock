import os
import sqlite3
import pandas as pd

# Define paths
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Day 2"
db_path = os.path.join(base_dir, "bluestock_mf.db")
queries_path = os.path.join(base_dir, "sql", "queries.sql")

print("Initializing Query Verification System...")
print(f"Connecting to database: {db_path}")

conn = sqlite3.connect(db_path)

# Read queries
with open(queries_path, 'r', encoding='utf-8') as f:
    sql_text = f.read()

# Split queries by semicolon (excluding comments and empty statements)
raw_queries = sql_text.split(";")
queries = []
current_query = []

for line in sql_text.split("\n"):
    if line.strip().startswith("--"):
        # If we have a query title, print it
        if current_query:
            queries.append("\n".join(current_query))
            current_query = []
        print(f"\n{line}")
    elif line.strip():
        current_query.append(line)
if current_query:
    queries.append("\n".join(current_query))

# Execute the 10 queries using pandas for beautiful tabular output
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# We can also parse the queries by splitting on semicolon and filter out empty ones
queries_list = [q.strip() for q in sql_text.split(";") if q.strip()]

print("\nExecuting the 10 analytical queries against bluestock_mf.db:")
for i, query in enumerate(queries_list, 1):
    print(f"\n=========================================================")
    print(f"QUERY {i}:")
    print("---------------------------------------------------------")
    # Extract the query title comment if present
    print(query)
    print("---------------------------------------------------------")
    try:
        df_result = pd.read_sql_query(query, conn)
        print("RESULT:")
        if len(df_result) == 0:
            print("(No rows returned)")
        else:
            print(df_result.to_string(index=False))
    except Exception as e:
        print(f"ERROR executing query: {e}")
    print("=========================================================")

conn.close()
print("\nQuery verification complete!")
