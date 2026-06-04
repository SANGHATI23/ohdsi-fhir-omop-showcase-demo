import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

out_dir = Path("outputs/figures")
out_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 7)
ax.axis("off")

def box(x, y, w, h, text, fontsize=10):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        linewidth=1.5,
        edgecolor="black",
        facecolor="white"
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True
    )

def arrow(x1, y1, x2, y2):
    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="->",
        mutation_scale=15,
        linewidth=1.4,
        color="black"
    )
    ax.add_patch(arr)

# Title
ax.text(
    5.5,
    6.55,
    "Figure 1. Lightweight FHIR Bulk-to-OMOP Software Demonstration Workflow",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold"
)

# Main workflow boxes
box(0.4, 4.8, 1.7, 0.9, "Synthea\nSynthetic Patients\nn = 25", fontsize=9)
box(2.55, 4.8, 1.7, 0.9, "FHIR Bulk\nNDJSON\nResources", fontsize=9)
box(4.7, 4.8, 1.7, 0.9, "pyOMOP\nFHIR Import", fontsize=9)
box(6.85, 4.8, 1.7, 0.9, "SQLite\nOMOP CDM\nDatabase", fontsize=9)
box(9.0, 4.8, 1.7, 0.9, "OMOP\nAnalytics\nOutputs", fontsize=9)

arrow(2.1, 5.25, 2.55, 5.25)
arrow(4.25, 5.25, 4.7, 5.25)
arrow(6.4, 5.25, 6.85, 5.25)
arrow(8.55, 5.25, 9.0, 5.25)

# Vocabulary box
box(4.7, 3.25, 3.85, 0.85, "OHDSI Athena Standardized Vocabulary\nconcept, vocabulary, concept_relationship,\nconcept_ancestor, concept_synonym, drug_strength", fontsize=8)
arrow(6.6, 4.8, 6.6, 4.1)

# Clinical table counts
ax.text(
    0.5,
    2.75,
    "Imported OMOP Clinical Tables",
    ha="left",
    va="center",
    fontsize=11,
    fontweight="bold"
)

clinical_text = (
    "person: 27 records\n"
    "visit_occurrence: 1,386 records\n"
    "condition_occurrence: 983 records\n"
    "drug_exposure: 1,275 records\n"
    "observation: 14,168 records\n"
    "measurement: 14,150 records"
)
box(0.5, 1.05, 4.6, 1.45, clinical_text, fontsize=9)

# Mapping results
ax.text(
    5.75,
    2.75,
    "Vocabulary Mapping Completeness",
    ha="left",
    va="center",
    fontsize=11,
    fontweight="bold"
)

mapping_text = (
    "condition_occurrence: 100.00% mapped\n"
    "drug_exposure: 78.12% mapped\n"
    "measurement: 99.99% mapped\n"
    "observation: 99.99% mapped\n"
    "visit_occurrence: 0.00% mapped"
)
box(5.75, 1.05, 4.75, 1.45, mapping_text, fontsize=9)

# Caption
caption = (
    "The demonstration uses fully synthetic FHIR Bulk NDJSON data, imports it into a local SQLite OMOP CDM "
    "database using pyOMOP, applies OHDSI Athena vocabulary mappings, and generates basic standard concept "
    "analytics for interactive software demonstration."
)
ax.text(
    0.5,
    0.45,
    caption,
    ha="left",
    va="center",
    fontsize=9,
    wrap=True
)

plt.tight_layout()

png_path = out_dir / "figure1_fhir_bulk_to_omop_workflow.png"
pdf_path = out_dir / "figure1_fhir_bulk_to_omop_workflow.pdf"

plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")

print(f"Created: {png_path}")
print(f"Created: {pdf_path}")
