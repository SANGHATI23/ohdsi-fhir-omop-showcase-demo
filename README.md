# OHDSI Global Collaborator Showcase Demo

## Demo Title

Synthetic FHIR Bulk Data to OMOP Analytics Using pyOMOP

## Demo Theme

This project demonstrates a lightweight end-to-end interoperability workflow:

Synthetic FHIR Bulk NDJSON → pyOMOP → SQLite OMOP CDM → Analytics Queries → Lightweight Natural-Language Querying

## Goal

The goal is to show how synthetic FHIR data can be transformed into a queryable OMOP Common Data Model database and used for basic observational health analytics.

## What This Demo Shows

1. Generation of synthetic FHIR Bulk NDJSON data using Synthea
2. Creation of an OMOP CDM SQLite database
3. Import of FHIR NDJSON files into OMOP using pyOMOP
4. Basic OMOP analytics:
   - Total patient counts
   - Demographic summaries
   - Condition prevalence
   - Drug exposure summaries
5. Lightweight natural-language-to-SQL querying for simple OMOP questions

## Strategic Scope

This demo focuses only on practical interoperability engineering and analytics enablement.

It intentionally does not include:

- Perturbation experiments
- Analytical drift evaluation
- Semantic robustness framework
- Full stability metrics
- Deeper methodological analysis

Those components are reserved for a separate research manuscript.

## Project Structure

```text
ohdsi_fhir_omop_demo/
├── data/
│   ├── fhir_input/
│   ├── omop_db/
│   └── vocabulary/
├── outputs/
│   ├── queries/
│   └── screenshots/
├── scripts/
│   ├── 01_basic_omop_counts.py
│   ├── 02_demographic_summary.py
│   ├── 03_condition_prevalence.py
│   ├── 04_condition_prevalence_source_values.py
│   ├── 05_drug_exposure_summary.py
│   ├── 06_create_showcase_summary.py
│   └── 07_nl_to_sql_demo.py
├── run_showcase_demo.sh
└── README.md
cd ~/ohdsi_fhir_omop_demo
source .venv/bin/activate
./run_showcase_demo.sh
cd ~/ohdsi_fhir_omop_demo
source .venv/bin/activate

cat > outputs/queries/ohdsi_submission_description.md <<'MD'
# OHDSI Global Collaborator Showcase Submission Description

## Proposed Demo Title

Synthetic FHIR Bulk Data to OMOP Analytics Using pyOMOP

## Short Description

This demonstration presents a lightweight end-to-end workflow for transforming synthetic FHIR Bulk NDJSON data into a queryable OMOP Common Data Model database using pyOMOP. The demo highlights practical interoperability engineering, OMOP CDM creation, FHIR resource ingestion, and basic observational analytics including patient counts, demographics, condition prevalence, and drug exposure summaries.

## Demo Overview

The workflow begins with synthetic patient data generated using Synthea in FHIR Bulk NDJSON format. The generated FHIR resources are imported into a SQLite-based OMOP CDM database using pyOMOP. Once loaded, the database is queried using simple Python and SQL scripts to demonstrate how transformed clinical data can support observational analytics.

The demonstration also includes a lightweight natural-language-to-SQL layer that converts simple analytical questions, such as “How many male patients are there?” or “Show top drug exposures,” into SQL queries executed against the OMOP database.

## Demonstrated Workflow

1. Generate synthetic FHIR Bulk NDJSON records using Synthea
2. Create a SQLite OMOP CDM database
3. Import FHIR NDJSON resources into OMOP using pyOMOP
4. Execute OMOP analytics queries
5. Demonstrate lightweight natural-language-assisted querying

## Example Analytics Outputs

The demo includes:

- Total patient count
- Demographic summary by gender and birth year
- Condition prevalence using source condition codes
- Drug exposure summaries using source drug codes
- Simple natural-language question answering over OMOP tables

## Intended Audience

This demo is intended for OHDSI collaborators, clinical informatics researchers, interoperability engineers, and healthcare analytics teams interested in practical FHIR-to-OMOP workflows and AI-ready observational health data infrastructure.

## Value to the OHDSI Community

This demonstration provides a compact and reproducible example of how synthetic FHIR data can be transformed into OMOP and used for analytics. It may be useful for teaching, prototyping, onboarding new collaborators, and exploring future extensions involving vocabulary enrichment, broader OMOP domain coverage, and AI-assisted analytics.

## Strategic Scope

This showcase focuses on operational interoperability and analytics enablement. It intentionally excludes deeper methodological evaluation, perturbation experiments, robustness testing, and analytical stability metrics, which are reserved for separate research work.

## Demo Takeaway

Synthetic FHIR Bulk NDJSON data can be transformed into a queryable OMOP CDM database using pyOMOP, enabling a practical bridge from interoperable clinical data exchange formats to observational analytics workflows.
