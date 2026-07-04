# FHIR-to-OMOP Analytical Stability Strengthening Analysis

This folder contains additional reviewer-strengthening analyses for the FHIRy-pyOMOP manuscript.

## Purpose

These analyses connect transformation-level perturbation metrics to downstream analytical consequences. The goal is to show that identical OMOP row counts do not necessarily imply analytical equivalence.

## Validated SQLite Inputs

The analysis uses the non-empty 25k OMOP SQLite databases:

- V0: `/content/drive/MyDrive/fhir_omop_colab/results_25k/V0_clinical_core_25k.sqlite`
- V1: `/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V1_missing_demographics_clinical_core_25k.sqlite`
- V2: `/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V2_duplicate_encounter_ids_clinical_core_25k.sqlite`
- V3: `/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V3_conflicting_codings_clinical_core_25k.sqlite`
- V4: `/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V4_missing_medications_clinical_core_25k.sqlite`

Zero-byte placeholder SQLite files in `results_combined_25k/` were intentionally excluded.

## Generated Outputs

- `cohort_jaccard_downstream_shift.csv`  
  Patient-level cohort preservation and Jaccard similarity versus V0.

- `downstream_exposure_prevalence_shift.csv`  
  Downstream condition/drug exposure prevalence changes across V0-V4.

- `omop_table_row_counts_by_variant.csv`  
  Structural row-count comparison across OMOP tables and variants.

- `distributional_drift_with_null_baseline.csv`  
  Jensen-Shannon divergence, Shannon entropy, and bootstrap/null JSD baseline.

- `runtime_confidence_intervals.csv`  
  Runtime mean, standard deviation, and 95% confidence intervals for standard OMOP analytical queries.

## Key Findings

- V4_missing_medications changed the drug-exposed cohort from 609 to 666 persons.
- V4 drug cohort Jaccard similarity versus V0 was 0.903, with 4 baseline patients lost and 61 patients gained.
- V4 increased drug exposure prevalence from 56.86% to 62.18%, a +5.32 percentage-point shift and +9.36% relative increase.
- V3_conflicting_codings increased condition_source_value categories from 247 to 412.
- V3 condition-source JSD versus V0 was 0.0524, exceeding the V0 bootstrap/null 95th percentile of 0.00425.
- V3 condition-source entropy increased by 0.464 bits.
