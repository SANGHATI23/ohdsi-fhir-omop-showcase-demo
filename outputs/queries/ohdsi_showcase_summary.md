# OHDSI Global Collaborator Showcase Demo Summary

## Demo Theme

Synthetic FHIR Bulk Data → pyOMOP → OMOP SQLite CDM → Analytics Queries

## Strategic Boundary

This lightweight demonstration focuses only on operational interoperability, FHIR-to-OMOP transformation, and queryable OMOP analytics infrastructure. It intentionally excludes perturbation experiments, analytical drift evaluation, semantic robustness metrics, and the deeper journal-study framework.

## Table Counts

| table_name           |   row_count |
|:---------------------|------------:|
| observation          |       14168 |
| measurement          |       14150 |
| visit_occurrence     |        1386 |
| drug_exposure        |        1275 |
| condition_occurrence |         983 |
| person               |          27 |

## Demographic Summary

| gender   |   person_count |   oldest_birth_year |   youngest_birth_year |
|:---------|---------------:|--------------------:|----------------------:|
| Male     |             19 |                1953 |                  2024 |
| Female   |              8 |                1953 |                  2005 |

## Top Conditions Using Source Values

|   source_condition_code | condition_status   |   condition_record_count |   unique_patients | first_observed_date   | last_observed_date   |
|------------------------:|:-------------------|-------------------------:|------------------:|:----------------------|:---------------------|
|               314529007 | resolved           |                      202 |                26 | 1965-06-18            | 2026-05-01           |
|                66383009 | resolved           |                       71 |                19 | 1973-07-13            | 2025-11-24           |
|               160903007 | resolved           |                       67 |                18 | 2008-05-23            | 2026-03-06           |
|                73595000 | resolved           |                       63 |                18 | 2007-03-22            | 2026-03-06           |
|               314529007 | active             |                       17 |                17 | 1976-07-30            | 2026-05-08           |
|               160904001 | resolved           |                       38 |                16 | 2016-04-28            | 2025-01-24           |
|               444814009 | resolved           |                       26 |                16 | 2016-07-17            | 2025-07-26           |
|               162864005 | active             |                       16 |                16 | 1991-01-06            | 2024-03-18           |
|                18718003 | resolved           |                       22 |                14 | 1975-08-01            | 2025-05-04           |
|               741062008 | resolved           |                       25 |                13 | 2012-06-21            | 2026-01-30           |

## Top Drug Exposures Using Source Values

|   source_drug_code |   drug_record_count |   unique_patients | first_exposure_date   | last_exposure_date   |
|-------------------:|--------------------:|------------------:|:----------------------|:---------------------|
|                140 |                 220 |                27 | 1967-06-16            | 2026-05-16           |
|                nan |                 232 |                25 | 1967-12-22            | 2026-05-15           |
|                113 |                  18 |                18 | 2017-05-22            | 2025-10-24           |
|                208 |                  28 |                14 | 2021-02-15            | 2022-01-09           |
|             313782 |                  13 |                10 | 2016-10-21            | 2024-08-28           |
|             562251 |                   8 |                 7 | 2016-08-26            | 2025-07-26           |
|                121 |                  11 |                 6 | 2017-05-22            | 2024-07-30           |
|                114 |                  10 |                 6 | 2016-06-23            | 2026-02-27           |
|                 62 |                  15 |                 5 | 2016-06-23            | 2023-11-19           |
|                133 |                  14 |                 5 | 2018-08-10            | 2025-09-08           |

## Demo Takeaway

This demo shows that synthetic FHIR Bulk NDJSON records can be transformed into a queryable OMOP CDM database using pyOMOP, enabling basic observational analytics such as patient counts, demographics, condition prevalence, and drug exposure summaries.
