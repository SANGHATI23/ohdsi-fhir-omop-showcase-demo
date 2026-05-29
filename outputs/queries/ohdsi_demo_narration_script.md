# OHDSI Showcase Demo Narration Script

## Opening

Hello, my name is Deb. In this demo, I will present a lightweight end-to-end workflow that transforms synthetic FHIR Bulk Data into a queryable OMOP Common Data Model database using pyOMOP.

The goal of this demo is to show a practical interoperability pipeline from FHIR to OMOP, followed by basic analytics and a lightweight natural-language query layer.

## Demo Architecture

The workflow has five simple steps.

First, I generate synthetic patient data using Synthea.

Second, the data is exported in FHIR Bulk NDJSON format.

Third, I create a SQLite-based OMOP CDM database.

Fourth, I use pyOMOP to import the FHIR resources into OMOP clinical tables.

Finally, I run basic analytics queries over the transformed OMOP database.

## FHIR Input

The synthetic FHIR dataset includes common healthcare resources such as Patient, Encounter, Condition, Observation, MedicationRequest, Procedure, and Immunization.

These files are stored as NDJSON files, which makes them suitable for FHIR Bulk Data workflows.

## OMOP Transformation

Using pyOMOP, the FHIR NDJSON files are imported into OMOP tables such as person, visit_occurrence, condition_occurrence, drug_exposure, observation, and measurement.

This demonstrates how FHIR resources can be transformed into an analytics-ready OMOP database.

## Analytics Layer

After the import, I run several basic analytics queries.

These include total patient counts, demographic summaries, condition prevalence, and drug exposure summaries.

For this lightweight demo, source values are used where full Athena vocabulary enrichment has not yet been loaded.

## Natural-Language Query Layer

I also include a small natural-language-to-SQL demonstration.

For example, a question like “How many male patients are there?” is converted into SQL and executed against the OMOP database.

This shows how OMOP can support simple AI-assisted analytical querying.

## Key Takeaway

The key takeaway is that synthetic FHIR Bulk Data can be transformed into a queryable OMOP CDM database using pyOMOP.

This creates a practical bridge from interoperable clinical data exchange formats to observational analytics workflows.

## Scope Boundary

This showcase focuses only on operational interoperability and analytics enablement.

It does not include deeper methodological evaluation, perturbation analysis, robustness testing, or analytical stability metrics.

Those are intentionally outside the scope of this demonstration.
