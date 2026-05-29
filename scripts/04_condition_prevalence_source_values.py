import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

sql = """
SELECT
    condition_source_value AS source_condition_code,
    condition_status_source_value AS condition_status,
    COUNT(*) AS condition_record_count,
    COUNT(DISTINCT person_id) AS unique_patients,
    MIN(condition_start_date) AS first_observed_date,
    MAX(condition_start_date) AS last_observed_date
FROM condition_occurrence
GROUP BY
    condition_source_value,
    condition_status_source_value
ORDER BY
    unique_patients DESC,
    condition_record_count DESC
LIMIT 20;
"""

df = pd.read_sql_query(sql, conn)

print("\n--- Top Conditions Using Source Values ---")
print(df)

output_path = OUTPUT_DIR / "condition_prevalence_source_values_top20.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")

conn.close()
