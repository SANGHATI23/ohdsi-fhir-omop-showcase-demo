import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

queries = {
    "table_counts": """
        SELECT 'person' AS table_name, COUNT(*) AS row_count FROM person
        UNION ALL
        SELECT 'visit_occurrence', COUNT(*) FROM visit_occurrence
        UNION ALL
        SELECT 'condition_occurrence', COUNT(*) FROM condition_occurrence
        UNION ALL
        SELECT 'drug_exposure', COUNT(*) FROM drug_exposure
        UNION ALL
        SELECT 'observation', COUNT(*) FROM observation
        UNION ALL
        SELECT 'measurement', COUNT(*) FROM measurement
        ORDER BY row_count DESC;
    """,

    "gender_distribution": """
        SELECT
            gender_concept_id,
            COUNT(*) AS person_count
        FROM person
        GROUP BY gender_concept_id
        ORDER BY person_count DESC;
    """,

    "birth_year_distribution": """
        SELECT
            year_of_birth,
            COUNT(*) AS person_count
        FROM person
        GROUP BY year_of_birth
        ORDER BY year_of_birth;
    """
}

conn = sqlite3.connect(DB_PATH)

for name, sql in queries.items():
    print(f"\n--- {name} ---")
    df = pd.read_sql_query(sql, conn)
    print(df)

    output_path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")

conn.close()
