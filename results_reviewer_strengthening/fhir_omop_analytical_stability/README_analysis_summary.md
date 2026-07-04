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
