# OHDSI Showcase Demo Asset Checklist

## 1. Core Demo Files

Confirm these files exist:

README.md
run_showcase_demo.sh
outputs/queries/ohdsi_showcase_summary.md
outputs/queries/ohdsi_submission_description.md
outputs/queries/ohdsi_demo_narration_script.md
outputs/queries/ohdsi_architecture_diagram.mmd

## 2. Data Transformation Evidence

Capture screenshots showing:

- FHIR NDJSON files in data/fhir_input/fhir/
- OMOP SQLite database file in data/omop_db/
- Successful pyomop input execution
- OMOP table counts after import

## 3. Analytics Evidence

Capture screenshots showing:

- person table count
- visit_occurrence count
- condition_occurrence count
- drug_exposure count
- demographic summary output
- condition prevalence output
- drug exposure output

## 4. Natural-Language Query Evidence

Capture screenshots showing:

- Question: How many male patients are there?
- Generated SQL
- Result table
- Question: Show top drug exposures
- Generated SQL
- Result table

## 5. Demo Storyline

Synthetic patients were generated using Synthea.
FHIR Bulk NDJSON files were imported using pyOMOP.
The data was transformed into OMOP CDM tables.
Basic analytics were executed on the OMOP database.
A lightweight natural-language-to-SQL layer demonstrated simple AI-assisted querying.

## 6. Strategic Boundary Reminder

Do not include:

- perturbation experiments
- analytical drift
- semantic robustness
- stability metrics
- journal-specific methodological framework

Keep the showcase focused on:

- interoperability workflow
- FHIR-to-OMOP transformation
- queryable OMOP analytics
- lightweight AI-assisted querying

## 7. Final Files to Share or Submit

Recommended files:

README.md
outputs/queries/ohdsi_submission_description.md
outputs/queries/ohdsi_showcase_summary.md
outputs/queries/ohdsi_demo_narration_script.md
outputs/queries/ohdsi_architecture_diagram.mmd

Optional files:

outputs/queries/table_counts.csv
outputs/queries/demographic_summary.csv
outputs/queries/condition_prevalence_source_values_top20.csv
outputs/queries/drug_exposure_source_values_top20.csv
