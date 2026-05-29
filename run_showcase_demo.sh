#!/bin/bash

echo "============================================================"
echo "OHDSI Global Collaborator Showcase Demo"
echo "Synthetic FHIR Bulk Data → pyOMOP → OMOP Analytics"
echo "============================================================"

echo ""
echo "Step 1: Checking OMOP table counts..."
python scripts/01_basic_omop_counts.py

echo ""
echo "Step 2: Running demographic summary..."
python scripts/02_demographic_summary.py

echo ""
echo "Step 3: Running condition prevalence summary..."
python scripts/04_condition_prevalence_source_values.py

echo ""
echo "Step 4: Running drug exposure summary..."
python scripts/05_drug_exposure_summary.py

echo ""
echo "Step 5: Creating showcase markdown summary..."
python scripts/06_create_showcase_summary.py

echo ""
echo "Step 6: Running lightweight natural-language-to-SQL demo..."
python scripts/07_nl_to_sql_demo.py

echo ""
echo "============================================================"
echo "Demo complete."
echo "Outputs saved under: outputs/queries/"
echo "Main summary file: outputs/queries/ohdsi_showcase_summary.md"
echo "============================================================"
