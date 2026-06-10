# OHDSI FHIR-to-OMOP Showcase Demo

## Demo Title

**Synthetic FHIR Bulk Data to OMOP Analytics Using pyOMOP**

## Overview

This repository demonstrates a lightweight end-to-end interoperability workflow:

**Synthetic FHIR Bulk NDJSON → pyOMOP → SQLite OMOP CDM → Analytics Queries → Result Summaries**

The project shows how synthetic FHIR data can be transformed into a queryable OMOP Common Data Model database and used for basic observational health analytics.

## Goals

This demo focuses on practical interoperability engineering and analytics enablement. It demonstrates:

* Synthetic FHIR Bulk NDJSON data generation using Synthea
* FHIR-to-OMOP transformation using pyOMOP
* Local SQLite-based OMOP CDM querying
* Basic OMOP analytics outputs
* Athena vocabulary mapping summaries
* Lightweight result packaging for demonstration and review

## What This Demo Shows

The repository includes scripts and outputs for:

* Total patient counts
* Demographic summaries
* Condition prevalence summaries
* Drug exposure summaries
* Vocabulary mapping analytics
* Phase 4 analytical stability result artifacts

## Repository Structure

```text
ohdsi-fhir-omop-showcase-demo/
├── README.md
├── requirements.txt
├── run_showcase_demo.sh
├── scripts/
├── figures/
├── outputs/
│   └── queries/
└── results/
    └── phase4_analytical_stability/
```

## Athena Vocabulary Mapping Results

This demo loads OHDSI Athena Standardized Vocabulary files locally and applies concept mappings during the FHIR-to-OMOP import process.

Vocabulary CSV files are not included in this GitHub repository because they are large and may be subject to vocabulary-specific licensing.

### Loaded Vocabulary Tables

| Table                |  Row Count |
| -------------------- | ---------: |
| vocabulary           |         44 |
| concept              |  4,066,375 |
| concept_relationship | 34,078,766 |
| concept_ancestor     |  2,163,000 |
| concept_synonym      |  2,346,129 |
| drug_strength        |  3,020,774 |

### Mapping Summary

| OMOP Table           | Concept Column         | Mapped Percent |
| -------------------- | ---------------------- | -------------: |
| condition_occurrence | condition_concept_id   |        100.00% |
| drug_exposure        | drug_concept_id        |         78.12% |
| measurement          | measurement_concept_id |         99.99% |
| observation          | observation_concept_id |         99.99% |
| visit_occurrence     | visit_concept_id       |          0.00% |

Standard concept analytics outputs are included under `outputs/queries/`, including condition and drug exposure summaries joined to the OMOP concept table.

## Phase 4 Analytical Stability Outputs

This repository also includes Phase 4 analytical stability outputs under:

```text
results/phase4_analytical_stability/
```

These outputs summarize SQL-based analytical comparisons across controlled FHIR perturbation variants transformed into OMOP.

### Variants Evaluated

| Variant                    | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| V0_clean                   | Clean baseline                                                 |
| V1_missing_demographics    | Missing gender and birthDate for approximately 15% of patients |
| V2_duplicate_encounter_ids | Duplicate FHIR Encounter identifiers                           |
| V3_conflicting_codings     | Conflicting SNOMED/ICD condition coding patterns               |
| V4_missing_medications     | Medication-resource perturbation                               |

### Main Phase 4 Findings

Across all variants, structural OMOP row counts remained stable:

| OMOP Table           | Row Count |
| -------------------- | --------: |
| person               |     1,071 |
| visit_occurrence     |    25,000 |
| condition_occurrence |    25,000 |
| drug_exposure        |    25,000 |
| measurement          |    25,000 |
| observation          |    25,000 |
| procedure_occurrence |    25,000 |

However, analytical differences were still observed:

* **V1_missing_demographics** produced 15.03% demographic missingness in OMOP person-level attributes.
* **V2_duplicate_encounter_ids** did not create duplicate OMOP visit IDs because `visit_occurrence_id` was regenerated, indicating source-identity traceability loss.
* **V3_conflicting_codings** increased unique `condition_source_value` patterns from 247 to 412, introducing 170 new source-value patterns.
* **V4_missing_medications** kept total `drug_exposure` rows stable but changed person-level drug exposure and missing source-value completeness.

### Key Result

Structural row-count stability alone was insufficient to detect analytical instability. Although OMOP row counts remained stable across variants, downstream analytical behavior changed across demographic, identity, semantic, and medication exposure dimensions.

## Included Phase 4 Files

Important files include:

```text
phase4_main_result_summary_table.csv
phase4_publication_heatmap_numeric_table.csv
phase4_results_text_for_manuscript.txt
phase4_output_file_inventory.csv
figure_phase4_corrected_analytical_divergence_heatmap.png
phase4_analytical_stability_output_package.zip
```

## Figure

The corrected analytical divergence heatmap is available at:

```text
figures/figure_phase4_corrected_analytical_divergence_heatmap.png
```

This figure summarizes variant-specific analytical divergence across demographic, identity, semantic, and medication exposure metrics.

## Running the Showcase Demo

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_showcase_demo.sh
```

## Data and File Exclusions

The following files are intentionally excluded from GitHub:

* Raw FHIR NDJSON exports
* Large OMOP SQLite databases
* Athena vocabulary CSV files
* Synthea source repository
* Python virtual environments
* Temporary logs and cache files

These exclusions keep the repository lightweight and avoid distributing large or restricted vocabulary/data assets.

## Strategic Scope

This repository is primarily intended as a practical OHDSI-style interoperability demonstration. It shows how FHIR Bulk NDJSON can be transformed into OMOP and queried for analytics.

The deeper analytical stability results are included as output artifacts, while raw perturbation datasets and large transformation databases remain outside GitHub.
