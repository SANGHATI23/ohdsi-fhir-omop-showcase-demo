import sqlite3
import pandas as pd

DB_PATH = "data/omop_db/ohdsi_demo.sqlite"

def generate_sql(question: str) -> str:
    q = question.lower().strip()

    if "how many" in q and "male" in q and "patient" in q:
        return """
        SELECT COUNT(*) AS male_patient_count
        FROM person
        WHERE gender_concept_id = 8507;
        """

    if "how many" in q and "female" in q and "patient" in q:
        return """
        SELECT COUNT(*) AS female_patient_count
        FROM person
        WHERE gender_concept_id = 8532;
        """

    if "total" in q and ("patient" in q or "person" in q):
        return """
        SELECT COUNT(*) AS total_patients
        FROM person;
        """

    if "condition" in q and ("top" in q or "prevalence" in q):
        return """
        SELECT
            condition_source_value AS source_condition_code,
            COUNT(*) AS condition_record_count,
            COUNT(DISTINCT person_id) AS unique_patients
        FROM condition_occurrence
        GROUP BY condition_source_value
        ORDER BY unique_patients DESC, condition_record_count DESC
        LIMIT 10;
        """

    if "drug" in q or "medication" in q:
        return """
        SELECT
            drug_source_value AS source_drug_code,
            COUNT(*) AS drug_record_count,
            COUNT(DISTINCT person_id) AS unique_patients
        FROM drug_exposure
        GROUP BY drug_source_value
        ORDER BY unique_patients DESC, drug_record_count DESC
        LIMIT 10;
        """

    raise ValueError(
        "Sorry, this demo question is not supported yet. "
        "Try: total patients, male patients, female patients, top conditions, or top drugs."
    )

def run_question(question: str):
    print("\nQuestion:")
    print(question)

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql.strip())

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()

    print("\nResult:")
    print(df)

questions = [
    "How many male patients are there?",
    "How many female patients are there?",
    "What is the total number of patients?",
    "Show top condition prevalence",
    "Show top drug exposures"
]

for question in questions:
    run_question(question)
    print("\n" + "=" * 70)
