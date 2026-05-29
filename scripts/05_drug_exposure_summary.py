import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

print("\n--- drug_exposure columns ---")
cols = pd.read_sql_query("PRAGMA table_info(drug_exposure);", conn)
print(cols[["name", "type"]])

sql = """
SELECT
    drug_source_value AS source_drug_code,
    COUNT(*) AS drug_record_count,
    COUNT(DISTINCT person_id) AS unique_patients,
    MIN(drug_exposure_start_date) AS first_exposure_date,
    MAX(drug_exposure_start_date) AS last_exposure_date
FROM drug_exposure
GROUP BY drug_source_value
ORDER BY unique_patients DESC, drug_record_count DESC
LIMIT 20;
"""

df = pd.read_sql_query(sql, conn)

print("\n--- Top Drug Exposures Using Source Values ---")
print(df)

output_path = OUTPUT_DIR / "drug_exposure_source_values_top20.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")

conn.close()
