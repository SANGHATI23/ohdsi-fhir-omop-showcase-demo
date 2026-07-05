# FHIR-to-OMOP Analytical Stability Strengthening Analysis

This folder contains additional reviewer-strengthening analyses for the FHIRy-pyOMOP manuscript.

## Generated outputs

- `cohort_jaccard_downstream_shift.csv`
- `downstream_exposure_prevalence_shift.csv`
- `omop_table_row_counts_by_variant.csv`
- `distributional_drift_with_null_baseline.csv`
- `runtime_confidence_intervals.csv`

## Key interpretation

- V4 drug-exposed cohort Jaccard vs V0: 0.903; lost from V0: 4; gained vs V0: 61.
- V3 condition source-value JSD vs V0: 0.0524; null JSD 95th percentile: 0.0043; observed exceeds null p95: True.

These analyses help connect engineering-level perturbation metrics to downstream analytical consequences.


## Combined-perturbation extension

To address whether independently evaluated perturbations may co-occur, an additional combined variant was generated:

- **V5_missing_demographics_plus_conflicting_codings**: constructed by combining the V1 demographic-missingness perturbation with the V3 conflicting condition-coding perturbation.

V5 was created by using the V3 OMOP SQLite database as the base, preserving the conflicting condition-source-value representation, and applying the V1 PERSON-table demographic-missingness fields by `person_id`. This produced a combined perturbation with 161 persons having missing or unknown gender and missing or zero birth year, while retaining 412 unique `condition_source_value` categories.

The V5 results show that combined demographic incompleteness and condition-source coding heterogeneity did not alter broad cohort membership in this experiment, with Jaccard similarity remaining 1.000 for the evaluated condition, drug, and condition-drug cohorts. However, V5 produced simultaneous distributional signals in both PERSON and CONDITION_OCCURRENCE: gender-distribution divergence consistent with V1 and condition-source-value divergence consistent with V3. This supports the use of multi-metric validation because combined data-quality perturbations may remain invisible to row-count checks and broad cohort membership alone while still affecting semantic/source-value distributions.
