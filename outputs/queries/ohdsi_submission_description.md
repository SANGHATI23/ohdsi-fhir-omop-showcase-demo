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
