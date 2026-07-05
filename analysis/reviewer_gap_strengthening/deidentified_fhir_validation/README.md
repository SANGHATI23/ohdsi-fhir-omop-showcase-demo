# Public or Deidentified FHIR Validation Scaffold

This folder contains a profiling workflow for future validation on public or governance-approved deidentified FHIR NDJSON exports.

The submitted manuscript evaluation used synthetic Synthea-generated data only. This scaffold does not change that claim. Instead, it provides a reproducible pathway for testing generalizability once appropriate public or deidentified FHIR data are available.

The profiling workflow reports:

- resource counts
- unique flattened field counts
- field presence fractions
- missing resource identifiers
- reference counts
- unresolved reference counts

No real patient data are committed to this repository.
