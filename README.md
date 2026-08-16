FHIRy–pyOMOP Transformation Fidelity

An auditable, staged FHIR R4 → FHIRy → pandas → pyOMOP → OMOP CDM workflow with a lightweight Transformation Fidelity Layer (TFL) for source-to-target traceability, deterministic warning detection, and transformation-fidelity measurement.

Research focus: the contribution is the transformation technique and its audit layer.
V0–V5 are controlled validation experiments used to test whether the technique exposes known transformation problems.

Overview

FHIR and OMOP serve different purposes: FHIR is designed for interoperable clinical data exchange, while the OMOP Common Data Model is designed for standardized observational analytics.

This repository implements a staged transformation workflow:

FHIR R4 Bulk NDJSON
        ↓
      FHIRy
        ↓
pandas DataFrames
        ↓
      pyOMOP
        ↓
    OMOP CDM

The workflow is extended with a Transformation Fidelity Layer (TFL) that operates alongside the transformation without modifying the OMOP schema:

FHIR source
    │
    ├──────────────→ source identity
    │
FHIRy / pandas
    │
    ├──────────────→ mapping rule
    │
pyOMOP
    │
    ├──────────────→ target OMOP record
    │
OMOP CDM
    │
    └──────────────→ TFL sidecar audit
                       • source-to-target lineage
                       • information fate
                       • deterministic warnings
                       • fidelity metrics

The TFL is intended to make transformation behavior explicit when a pipeline can remain structurally successful even though source identity, coding representation, completeness, or attribution has changed.



OHDSI 2026 Global Collaborator Showcase

This repository also contains the software and reproducibility materials developed for the 2026 OHDSI Global Collaborator Showcase software-demonstration work on lightweight FHIR-to-OMOP interoperability using pyOMOP.

Showcase work

Software-demo title:
A Lightweight FHIR-to-OMOP Software Demonstration Using pyOMOP

The original showcase workflow demonstrated a practical path from synthetic FHIR Bulk Data to a queryable OMOP CDM:

Synthetic FHIR R4 Bulk NDJSON
            ↓
          pyOMOP
            ↓
      SQLite OMOP CDM
            ↓
     OHDSI-style queries
            ↓
      Result summaries

The demo was designed as a lightweight interoperability demonstration rather than a production institutional ETL implementation. It showed that a researcher could:

generate synthetic FHIR data with Synthea,

transform FHIR resources into OMOP CDM tables using pyOMOP,

load and query the resulting OMOP database locally with SQLite,

inspect demographic and clinical-domain summaries,

apply OHDSI Athena vocabulary assets locally,

generate condition and drug-exposure summaries joined to OMOP concepts, and

package the workflow into a small reproducible software demonstration.

Original OHDSI demo scripts

The root script:

run_showcase_demo.sh

runs the original showcase sequence, including OMOP counts and analytical summaries.

The repository also retains the supporting scripts under:

scripts/

These materials are kept because the current TFL work extends the original OHDSI interoperability demonstration; it does not replace or erase it.

Athena vocabulary mapping used in the showcase

The original OHDSI demonstration used locally downloaded OHDSI Athena Standardized Vocabulary assets.

The repository does not redistribute the large Athena vocabulary CSV files, but the showcase workflow used the following loaded vocabulary assets:

Vocabulary table

Rows loaded

vocabulary

44

concept

4,066,375

concept_relationship

34,078,766

concept_ancestor

2,163,000

concept_synonym

2,346,129

drug_strength

3,020,774

The original mapping summary reported:

OMOP table

Concept column

Mapped

condition_occurrence

condition_concept_id

100.00%

drug_exposure

drug_concept_id

78.12%

measurement

measurement_concept_id

99.99%

observation

observation_concept_id

99.99%

visit_occurrence

visit_concept_id

0.00%

These mapping percentages belong to the original OHDSI software-demo workflow and should not be confused with the later TFL source-mapping-coverage metric.

Relationship between the OHDSI demo and the TFL manuscript

The repository now supports two connected layers of work:

OHDSI showcase foundation
Synthetic FHIR → pyOMOP → OMOP → OHDSI analytics
                         │
                         ↓
Research extension
FHIR → FHIRy → pandas → pyOMOP → OMOP
                         +
            Transformation Fidelity Layer

The OHDSI showcase established the lightweight end-to-end FHIR-to-OMOP software workflow and OMOP analytical usability.

The TFL extension asks a more specific methodological question:

When a FHIR-to-OMOP transformation completes successfully, can the transformation also make source-to-target lineage, information loss, ambiguity, and warning conditions explicitly auditable?

Accordingly:

the OHDSI demo remains an important interoperability/software foundation of this repository;

the TFL notebooks extend that work with explicit transformation auditing;

V0–V5 validate the TFL behavior under controlled perturbations;

the older OHDSI scripts, query summaries, and vocabulary-mapping outputs remain preserved for reproducibility and historical continuity.

Transformation Fidelity Layer

The TFL records one auditable transformation event using fields such as:

Field

Purpose

transformation_id

Stable identifier for the transformation event

source_resource_type

FHIR resource type

source_resource_id

Source resource identifier

source_reference_or_path

FHIR path/reference used by the mapping

source_value_or_code

Optional source value/code

target_omop_table

Target OMOP table

target_omop_record_id

Target OMOP record identifier

target_omop_field

Target field(s)

mapping_rule_id

Deterministic mapping rule

fidelity_status

Information-fate classification

warning_code

Deterministic warning(s)

transformation_version

Transformation implementation/version

Information-fate taxonomy

The current implementation uses:

PRESERVED

NORMALIZED

COLLAPSED

AMBIGUOUS

UNMAPPED

DROPPED

TRACEABILITY_LOSS

Warning families

Controlled validation currently exercises:

W_DEMOGRAPHIC_MISSING

W_DUPLICATE_SOURCE_ID

W_TRACEABILITY_LOSS

W_CONFLICTING_CODING

W_MEDICATION_ATTRIBUTION

The framework also reserves warning categories for additional transformation conditions such as unresolved references or unmapped resources.

Primary Fidelity Measures

The TFL reports four separate primary measures.

1. Lineage coverage

Fraction of mapped transformation events for which a source resource can be connected to a target OMOP record without a traceability-loss state.

2. Source mapping coverage

Fraction of unique source resources with at least one mapped OMOP target.

The source-resource key is:

(source_resource_type, source_df_index)

rather than source_resource_id, because the V2 experiment intentionally contains duplicated Encounter identifiers.

3. Transformation-loss rate

Fraction of audited source events classified as:

UNMAPPED

DROPPED

TRACEABILITY_LOSS

4. Ambiguity/warning rate

Fraction of audited events classified as ambiguous and/or carrying a deterministic transformation warning.

No composite fidelity score is used.

Controlled Validation Design

The validation uses one clean baseline, V0 (N = 1,071).

V1–V5 are controlled perturbations of that baseline and are used to validate the transformation-fidelity mechanism.

Variant

Controlled perturbation

Expected TFL response

V0

Clean baseline

Baseline fidelity profile

V1

Missing demographics

W_DEMOGRAPHIC_MISSING

V2

Duplicate FHIR Encounter identifiers

W_DUPLICATE_SOURCE_ID, W_TRACEABILITY_LOSS

V3

Conflicting/competing condition coding representations

W_CONFLICTING_CODING

V4

Medication-resource perturbation

W_MEDICATION_ATTRIBUTION

V5

Combined V1 + V3 perturbation

Demographic + coding warnings

The perturbations validate the technique; they are not the methodological contribution.

Final Primary Results

The finalized resource-level metrics are:

Variant

Lineage coverage

Source mapping coverage

Transformation-loss rate

Ambiguity/warning rate

V0

100.00%

81.69%

15.76%

21.16%

V1

100.00%

81.69%

15.76%

21.25%

V2

98.42%

81.69%

17.09%

22.50%

V3

100.00%

81.69%

15.76%

22.56%

V4

100.00%

83.21%

14.41%

19.99%

V5

100.00%

81.69%

15.76%

22.65%

Important interpretation of V4

V4 maps the same absolute number of source resources as the other variants (126,071), but its source-resource denominator is smaller because of the medication perturbation.

Therefore the higher V4 source-mapping percentage (83.21%) is a denominator effect and should not be interpreted as improved transformation performance.

Key Controlled Findings

V1 — demographic completeness

V1 produces 161 demographic warning cases relative to a clean V0 baseline.

V2 — source-identifier traceability

The raw V2 FHIR source contains:

25,000 Encounter resources

23,790 unique Encounter IDs

1,183 duplicated identifier values

2,393 Encounter rows involved in duplicated IDs

After transformation, the OMOP database contains:

25,000 visit_occurrence rows

25,000 unique visit_occurrence_id values

The target therefore remains structurally valid while the original duplicated Encounter identity is no longer recoverable from regenerated target identifiers.

The TFL captures this as:

W_DUPLICATE_SOURCE_ID
W_TRACEABILITY_LOSS
TRACEABILITY_LOSS

This produces the largest primary lineage effect:

V0 lineage coverage: 100.00%
V2 lineage coverage:  98.42%

V3 — condition coding representation

The controlled condition-coding perturbation changes the number of observed coding representations from:

V0: 247
V3: 412

The corrected deterministic warning rule identifies:

V0:    0 warning rows
V1:    0
V2:    0
V3: 2,510
V4:    0
V5: 2,510

V3 therefore increases ambiguity/warning rate while preserving source-to-target lineage.

V5 — combined perturbation

V5 combines the V1 demographic perturbation and the V3 coding perturbation.

It reproduces both expected warning families without adding the V2 identity perturbation.

Supporting Analytical Validation

The repository also retains secondary analytical checks that help characterize downstream consequences of the controlled transformations.

These include:

row-count reconciliation

patient-level Jaccard similarity

Jensen–Shannon divergence

Shannon entropy

temporal-integrity checks

exposure-prevalence change

bootstrap/null divergence baselines

SQLite query-runtime profiling

database-size comparison

public/deidentified FHIR profiling

shared-input local tabularization comparison

These analyses are supporting validation. They do not define the TFL method.

Selected supporting findings

Condition-source heterogeneity

V3 increased condition_source_value categories from 247 to 412 and increased Shannon entropy from approximately 5.337 to 5.801 bits.

Observed condition-source JSD was approximately 0.0524, above the V0 bootstrap/null 95th percentile of approximately 0.00425.

Medication-related cohort change

V4 changed the drug-exposed cohort from:

V0: 609 persons
V4: 666 persons

with:

Jaccard similarity: 0.903

prevalence: 56.86% → 62.18%

absolute change: +5.32 percentage points

These results illustrate why transformation warnings can matter downstream even when a target database loads successfully.

Encounter Restoration

An earlier normalization pass omitted the Encounter domain from the flattened source used for OMOP persistence.

The repair workflow therefore:

reads the original V1–V4 controlled FHIR archives,

verifies that the unaffected Encounter controls (V1, V3, V4) are identical,

reconstructs the V0 Encounter baseline from that verified unaffected consensus,

uses baseline Encounter data for V5 because V5 combines only V1 Patient and V3 Condition perturbations,

normalizes Encounter with FHIRy,

applies only the pyOMOP Encounter → visit_occurrence mapping to copies of the existing OMOP databases,

verifies 25,000 visit rows, 25,000 unique visit IDs, and zero invalid person links for each variant, and

appends the corrected Encounter events to the TFL sidecar audit.

This repair is isolated to the missing Encounter domain; the other previously completed OMOP transformations are reused.

Reproducibility Notebooks

The repository contains the development and correction sequence for the TFL workflow.

Main execution

FHIRy_pyOMOP_TFL_Execution_v8.ipynb

Builds the main V0–V5 normalized sources, fresh OMOP databases, source/target linkage, and initial TFL audit outputs.

Warning-rule correction

FHIRy_pyOMOP_TFL_PostPhaseE_WarningFix_v9.ipynb

Diagnoses and corrects V2/V3 warning logic without rerunning the completed full transformations.

Encounter and audit repair

FHIRy_pyOMOP_TFL_EncounterAuditRepair_v10.ipynb

Restores the omitted Encounter domain, verifies the V2 duplicate-identifier perturbation, rebuilds visit_occurrence, corrects the TFL audit, and validates the expected V1–V5 warning responses.

Final metric correction

FHIRy_pyOMOP_TFL_SourceMappingMetricFix_v11.ipynb

Corrects the source-mapping-coverage denominator from audit-event rows to unique source resources while preserving the other three primary metrics.

Earlier development notebook

FHIRy_pyOMOP_TFL_Colab_Clean_v5.ipynb

Retained for provenance of the earlier workflow. The finalized TFL results should be taken from the v10/v11 sequence rather than this earlier notebook.

Repository Structure

ohdsi-fhir-omop-showcase-demo/
├── README.md
├── requirements.txt
├── run_showcase_demo.sh
├── scripts/
├── figures/
├── outputs/
├── results/
│   └── phase4_analytical_stability/
├── results_reviewer_strengthening/
│   └── fhir_omop_analytical_stability/
├── FHIRy_pyOMOP_TFL_Colab_Clean_v5.ipynb
├── FHIRy_pyOMOP_TFL_Execution_v8.ipynb
├── FHIRy_pyOMOP_TFL_PostPhaseE_WarningFix_v9.ipynb
├── FHIRy_pyOMOP_TFL_EncounterAuditRepair_v10.ipynb
└── FHIRy_pyOMOP_TFL_SourceMappingMetricFix_v11.ipynb

The older results/phase4_analytical_stability/ and reviewer-strengthening outputs are retained as supporting/legacy analytical artifacts. The current methodological contribution is represented by the TFL notebooks and finalized v10/v11 outputs.

OHDSI Showcase Reproducibility Materials

The original OHDSI software-demo scripts and outputs are intentionally retained alongside the newer TFL notebooks.

Use:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_showcase_demo.sh

to reproduce the lightweight showcase workflow from the repository root.

The OHDSI materials demonstrate the foundational FHIR→OMOP software path. The v8–v11 notebooks represent the later transformation-fidelity research extension.

Athena Vocabulary Assets

Large OHDSI Athena vocabulary CSV files are not committed to this repository.

The original showcase workflow used local vocabulary assets for mapping and concept-level summaries. Vocabulary files may have licensing and redistribution constraints and should be obtained from the appropriate OHDSI/Athena source.

The TFL contribution itself does not require modifying the OMOP vocabulary schema.

Running the Original Showcase Demo

From the repository root:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run_showcase_demo.sh

The v8–v11 TFL notebooks are designed for Google Colab and use persisted intermediate artifacts to avoid unnecessarily repeating completed transformations.

Data and File Exclusions

The repository intentionally excludes large or restricted assets such as:

raw FHIR NDJSON perturbation datasets

large OMOP SQLite databases

Athena vocabulary CSV files

raw MIMIC-IV Demo on FHIR files

temporary Colab/runtime files

Python virtual environments

caches and logs

Where possible, reproducible code, aggregate outputs, diagnostics, and public-safe summaries are retained.

Scope and Limitations

This repository demonstrates a lightweight, auditable research transformation workflow.

It is not presented as:

a replacement for production-grade institutional ETL systems,

a complete implementation of all FHIR resources,

a terminology-learning or ontology-reasoning system,

a probabilistic or LLM-based mapper,

a universal semantic-fidelity score,

a modification of the OMOP CDM schema, or

a full institutional data-quality platform.

The controlled V0–V5 experiments are designed to test specific transformation-fidelity behaviors under reproducible perturbations.

Research Status

This repository contains the software base for the 2026 OHDSI Global Collaborator Showcase FHIR-to-OMOP software-demonstration work and the subsequent Transformation Fidelity Layer research extension.

The current methods manuscript focuses on auditable FHIR-to-OMOP transformation fidelity while retaining the OHDSI demo, Athena mapping summaries, analytical scripts, and historical outputs as part of the reproducible project record.

The manuscript framing is technique-first:

Transformation method first; controlled validation second.

Citation

A formal citation will be added after the transformation-fidelity manuscript is finalized and archived with a stable repository release/version tag.

For software reuse before publication, please cite this repository and the underlying FHIRy, pyOMOP, HL7 FHIR, and OHDSI/OMOP resources as appropriate.

Maintainer

Sanghati Basu

Repository: SANGHATI23/ohdsi-fhir-omop-showcase-demo

License

Use and redistribution are subject to the repository license and the licenses/terms of the upstream tools, standards, vocabularies, and datasets used by the workflow.
