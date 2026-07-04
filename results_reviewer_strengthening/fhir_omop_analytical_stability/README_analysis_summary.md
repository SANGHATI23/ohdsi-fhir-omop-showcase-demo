# FHIR-to-OMOP Analytical Stability Strengthening Analysis

This folder contains additional reviewer-strengthening analyses for the FHIRy-pyOMOP manuscript.

## Generated outputs

- `cohort_jaccard_downstream_shift.csv`
- `downstream_exposure_prevalence_shift.csv`
- `omop_table_row_counts_by_variant.csv`
- `distributional_drift_with_null_baseline.csv`
- `runtime_confidence_intervals.csv`

## Key interpretation

- V4 drug-exposed cohort Jaccard vs V0: 0.000; lost from V0: 609; gained vs V0: 0.
- V3 condition source-value JSD vs V0: nan; null JSD 95th percentile: 0.0043; observed exceeds null p95: False.

These analyses help connect engineering-level perturbation metrics to downstream analytical consequences.
