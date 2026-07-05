# Comparator Benchmark

This benchmark addresses the reviewer-facing limitation that the current study does not include a head-to-head comparator.

The included script compares the proposed deterministic FHIRy-style flattening behavior with a simple generic JSON flattening baseline on the same FHIR NDJSON input files.

This benchmark is intentionally narrow. It does not claim superiority over fhircrackr, FHIR-PYrate, FHIRpack, or production FHIR-to-OMOP ETL frameworks. Instead, it provides a reproducible comparator scaffold reporting:

- input records
- output rows
- output columns
- missing-cell fraction
- non-null cell count
- wall-clock runtime
- preview outputs for manual inspection

No real patient data are committed to this repository.
