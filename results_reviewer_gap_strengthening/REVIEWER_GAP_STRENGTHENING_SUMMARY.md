# Reviewer Gap Strengthening Summary

This supplemental analysis addresses two likely reviewer concerns:

1. The submitted evaluation used synthetic Synthea-generated data only.
2. The submitted evaluation did not include a comparator benchmark.

## 1. Public or Deidentified FHIR Validation Scaffold

The repository now includes an executable profiling scaffold:

`analysis/reviewer_gap_strengthening/deidentified_fhir_validation/run_deidentified_fhir_profile.py`

This script can be run on public FHIR examples, governance-approved deidentified FHIR Bulk NDJSON exports, or institutional deidentified FHIR extracts when permitted.

The scaffold reports:

- resource counts
- unique flattened field counts
- field presence fractions
- missing resource identifiers
- reference counts
- unresolved reference counts

For the included synthetic smoke-test input, the scaffold processed 182 FHIR resources and detected 0 unresolved internal references.

Important: this does not claim that real patient data were used in the submitted evaluation. No real patient data are committed to this repository.

## 2. Comparator Benchmark Scaffold

The repository now includes a narrow comparator benchmark:

`analysis/reviewer_gap_strengthening/comparator_benchmark/run_comparator_benchmark.py`

The benchmark compares:

- deterministic FHIRy-style flattening
- generic JSON flattening baseline

For the included synthetic smoke-test input, both workflows preserved input row counts. Across the four tested resource types, the deterministic FHIRy-style workflow produced 31 total output columns compared with 37 total output columns for the generic JSON baseline.

This supports a modest interpretation: the deterministic FHIRy-style workflow produces a more compact analytics-oriented representation than a naive generic JSON flattening baseline on this smoke-test input.

Important: this is not a claim of superiority over mature external tools such as fhircrackr, FHIR-PYrate, FHIRpack, or production FHIR-to-OMOP ETL pipelines. A full external-framework head-to-head benchmark remains future work.

## Recommended Manuscript Interpretation

These analyses should be described as repository-level strengthening and reproducibility scaffolds, not as new main-study evidence unless additional public or deidentified FHIR data are actually run.

Suggested language:

> To improve reproducibility and support future generalizability testing, we added repository workflows for (i) profiling public or governance-approved deidentified FHIR NDJSON exports before transformation and (ii) running a narrow comparator benchmark against a generic JSON flattening baseline. These supplemental workflows do not change the submitted study's primary limitation that the reported evaluation used synthetic Synthea-generated data only, but they provide executable infrastructure for applying the same validation framework to real-world or deidentified FHIR exports when governance permits.

