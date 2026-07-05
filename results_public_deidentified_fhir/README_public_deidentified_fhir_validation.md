# Public Deidentified FHIR Validation: MIMIC-IV Demo on FHIR

This folder contains aggregate validation outputs from the public/deidentified
MIMIC-IV Clinical Database Demo on FHIR v2.1.0.

This analysis was added to address the reviewer-facing limitation that the main
controlled perturbation experiment used synthetic Synthea data only.

## Dataset

Dataset: MIMIC-IV Clinical Database Demo on FHIR v2.1.0  
Source: PhysioNet  
Patient subset: 100 deidentified patients  
FHIR format: compressed NDJSON files by resource type

Raw patient-level FHIR files are intentionally not committed to this repository.
Only aggregate profiling outputs are committed.

## Validation purpose

This supplemental workflow does not replace the controlled synthetic perturbation
experiment. Instead, it provides a public/deidentified real-world FHIR validation
layer showing that the repository workflow can ingest and profile non-synthetic
FHIR resources.

The workflow reports:

- resource-level record counts
- flattened field-path coverage
- field-presence fractions
- missing FHIR resource identifiers
- internal FHIR reference counts
- unresolved internal references
- compact deterministic flattening versus generic JSON flattening
- source-value heterogeneity using Shannon entropy

## Summary

Files processed: 16  
Total FHIR resources processed: 858025  
Patient resources: 100  
Total internal FHIR references detected: 1860205  
Unresolved references detected: 112676  
Unresolved reference fraction: 0.060572

Across the processed files, the generic JSON flattening baseline produced
356 total columns, while the compact deterministic FHIR flattening
approximation produced 169 total columns, for a net column reduction
of 187 columns across files.

## Output files

- `mimic_demo_resource_counts.csv`: resource counts by input file and FHIR resource type
- `mimic_demo_field_presence.csv`: flattened field-path presence summary
- `mimic_demo_reference_integrity_summary.csv`: file-level internal reference integrity
- `mimic_demo_reference_integrity_overall.csv`: overall internal reference integrity
- `mimic_demo_compact_vs_generic_flattening_benchmark.csv`: compact flattening versus generic JSON flattening comparison
- `mimic_demo_source_value_entropy.csv`: source-value entropy summaries

## Interpretation

These outputs strengthen the manuscript by adding a real-world deidentified FHIR
validation layer. The main analytical-stability findings still come from the
controlled Synthea perturbation experiment because that design requires known
source-level modifications. The MIMIC-IV Demo on FHIR analysis demonstrates
workflow portability to public deidentified real clinical FHIR resources, but it
does not claim full institutional generalizability or production-scale
FHIR-to-OMOP validation.

Larger validation using the credentialed full MIMIC-IV on FHIR dataset and
governance-approved institutional deidentified FHIR exports remains future work.
