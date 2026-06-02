import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"
OUTPUT_DIR = Path("outputs/queries")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# 1. Check vocabulary table counts
vocab_count_sql = """
SELECT 'vocabulary' AS table_name, COUNT(*) AS row_count FROM vocabulary
UNION ALL
SELECT 'concept' AS table_name, COUNT(*) AS row_count FROM concept
UNION ALL
SELECT 'concept_relationship' AS table_name, COUNT(*) AS row_count FROM concept_relationship
UNION ALL
SELECT 'concept_ancestor' AS table_name, COUNT(*) AS row_count FROM concept_ancestor
UNION ALL
SELECT 'concept_synonym' AS table_name, COUNT(*) AS row_count FROM concept_synonym
UNION ALL
SELECT 'drug_strength' AS table_name, COUNT(*) AS row_count FROM drug_strength;
"""

vocab_counts = pd.read_sql_query(vocab_count_sql, conn)
vocab_counts.to_csv(OUTPUT_DIR / "vocabulary_table_counts.csv", index=False)

print("\n=== Vocabulary Table Counts ===")
print(vocab_counts)


# 2. Mapping summary for major OMOP clinical tables
mapping_queries = []

table_columns = [
    ("condition_occurrence", "condition_concept_id"),
    ("drug_exposure", "drug_concept_id"),
    ("measurement", "measurement_concept_id"),
    ("observation", "observation_concept_id"),
    ("visit_occurrence", "visit_concept_id")
]

for table, col in table_columns:
    sql = f"""
    SELECT
        '{table}' AS omop_table,
        '{col}' AS concept_column,
        COUNT(*) AS total_rows,
        SUM(CASE WHEN {col} = 0 THEN 1 ELSE 0 END) AS unmapped_rows,
        SUM(CASE WHEN {col} <> 0 THEN 1 ELSE 0 END) AS mapped_rows,
        ROUND(
            100.0 * SUM(CASE WHEN {col} <> 0 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
            2
        ) AS mapped_percent
    FROM {table};
    """
    mapping_queries.append(pd.read_sql_query(sql, conn))

mapping_summary = pd.concat(mapping_queries, ignore_index=True)
mapping_summary.to_csv(OUTPUT_DIR / "vocabulary_mapping_summary.csv", index=False)

print("\n=== Vocabulary Mapping Summary ===")
print(mapping_summary)


# 3. Standard concept-based condition analytics
condition_sql = """
SELECT
    c.concept_name,
    c.domain_id,
    c.vocabulary_id,
    co.condition_concept_id,
    COUNT(*) AS condition_record_count,
    COUNT(DISTINCT co.person_id) AS unique_patients
FROM condition_occurrence co
LEFT JOIN concept c
    ON co.condition_concept_id = c.concept_id
WHERE co.condition_concept_id <> 0
GROUP BY
    c.concept_name,
    c.domain_id,
    c.vocabulary_id,
    co.condition_concept_id
ORDER BY unique_patients DESC, condition_record_count DESC
LIMIT 20;
"""

standard_conditions = pd.read_sql_query(condition_sql, conn)
standard_conditions.to_csv(
    OUTPUT_DIR / "standard_condition_concepts_top20.csv",
    index=False
)

print("\n=== Top Standard Condition Concepts ===")
print(standard_conditions)


# 4. Standard concept-based drug analytics
drug_sql = """
SELECT
    c.concept_name,
    c.domain_id,
    c.vocabulary_id,
    de.drug_concept_id,
    COUNT(*) AS drug_record_count,
    COUNT(DISTINCT de.person_id) AS unique_patients
FROM drug_exposure de
LEFT JOIN concept c
    ON de.drug_concept_id = c.concept_id
WHERE de.drug_concept_id <> 0
GROUP BY
    c.concept_name,
    c.domain_id,
    c.vocabulary_id,
    de.drug_concept_id
ORDER BY unique_patients DESC, drug_record_count DESC
LIMIT 20;
"""

standard_drugs = pd.read_sql_query(drug_sql, conn)
standard_drugs.to_csv(
    OUTPUT_DIR / "standard_drug_concepts_top20.csv",
    index=False
)

print("\n=== Top Standard Drug Concepts ===")
print(standard_drugs)

conn.close()

print("\nDone.")
print("Created:")
print("- outputs/queries/vocabulary_table_counts.csv")
print("- outputs/queries/vocabulary_mapping_summary.csv")
print("- outputs/queries/standard_condition_concepts_top20.csv")
print("- outputs/queries/standard_drug_concepts_top20.csv")
