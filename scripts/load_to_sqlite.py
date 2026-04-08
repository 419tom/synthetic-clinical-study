import os
import sqlite3
import pandas as pd

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "clinical_study.db")

# ----------------------------
# Connect to SQLite
# ----------------------------
conn = sqlite3.connect(DB_PATH)

# ----------------------------
# Load CSVs into SQLite tables
# ----------------------------
files_to_tables = {
    "subjects.csv": "subjects",
    "sites.csv": "sites",
    "visits.csv": "visits",
    "labs.csv": "labs",
    "adverse_events.csv": "adverse_events",
    "conmeds.csv": "conmeds",
    "protocol_deviations.csv": "protocol_deviations",
    "data_queries.csv": "data_queries",
    "incident_change_log.csv": "incident_change_log"
}

for file_name, table_name in files_to_tables.items():
    file_path = os.path.join(RAW_DIR, file_name)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {file_name} -> {table_name}")
    else:
        print(f"Missing file: {file_name}")

conn.close()
print(f"\nSQLite database created at:\n{DB_PATH}")