import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("outputs/queries")
REPORT_PATH = OUTPUT_DIR / "ohdsi_showcase_summary.md"

sections = [
    ("Table Counts", "table_counts.csv"),
    ("Demographic Summary", "demographic_summary.csv"),
    ("Top Conditions Using Source Values", "condition_prevalence_source_values_top20.csv"),
    ("Top Drug Exposures Using Source Values", "drug_exposure_source_values_top20.csv"),
]

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# OHDSI Global Collaborator Showcase Demo Summary\n\n")
    f.write("## Demo Theme\n\n")
    f.write("Synthetic FHIR Bulk Data → pyOMOP → OMOP SQLite CDM → Analytics Queries\n\n")

    f.write("## Strategic Boundary\n\n")
    f.write(
        "This lightweight demonstration focuses only on operational interoperability, "
        "FHIR-to-OMOP transformation, and queryable OMOP analytics infrastructure. "
        "It intentionally excludes perturbation experiments, analytical drift evaluation, "
        "semantic robustness metrics, and the deeper journal-study framework.\n\n"
    )

    for title, filename in sections:
        path = OUTPUT_DIR / filename
        f.write(f"## {title}\n\n")

        if path.exists():
            df = pd.read_csv(path)
            f.write(df.head(10).to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write(f"Missing file: `{filename}`\n\n")

    f.write("## Demo Takeaway\n\n")
    f.write(
        "This demo shows that synthetic FHIR Bulk NDJSON records can be transformed into "
        "a queryable OMOP CDM database using pyOMOP, enabling basic observational analytics "
        "such as patient counts, demographics, condition prevalence, and drug exposure summaries.\n"
    )

print(f"Created: {REPORT_PATH}")
