import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

sql = """
SELECT
    condition_concept_id,
    COUNT(*) AS condition_record_count,
    COUNT(DISTINCT person_id) AS unique_patients
FROM condition_occurrence
GROUP BY condition_concept_id
ORDER BY unique_patients DESC, condition_record_count DESC
LIMIT 15;
"""

df = pd.read_sql_query(sql, conn)

print("\n--- Top Condition Prevalence ---")
print(df)

output_path = OUTPUT_DIR / "condition_prevalence_top15.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")

conn.close()
