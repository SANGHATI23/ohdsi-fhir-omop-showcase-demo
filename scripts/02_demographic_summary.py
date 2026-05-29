import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

sql = """
SELECT
    CASE
        WHEN gender_concept_id = 8507 THEN 'Male'
        WHEN gender_concept_id = 8532 THEN 'Female'
        ELSE 'Unknown / Other'
    END AS gender,
    COUNT(*) AS person_count,
    MIN(year_of_birth) AS oldest_birth_year,
    MAX(year_of_birth) AS youngest_birth_year
FROM person
GROUP BY gender
ORDER BY person_count DESC;
"""

df = pd.read_sql_query(sql, conn)

print("\n--- Demographic Summary ---")
print(df)

output_path = OUTPUT_DIR / "demographic_summary.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")

conn.close()
