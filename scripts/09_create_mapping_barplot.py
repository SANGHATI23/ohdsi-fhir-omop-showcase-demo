import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path("outputs/figures")
out_dir.mkdir(parents=True, exist_ok=True)

tables = [
    "Condition\nOccurrence",
    "Drug\nExposure",
    "Measurement",
    "Observation",
    "Visit\nOccurrence"
]

mapped_percent = [100.00, 78.12, 99.99, 99.99, 0.00]

fig, ax = plt.subplots(figsize=(8.5, 5.2))

bars = ax.bar(tables, mapped_percent)

ax.set_ylabel("Mapped records (%)", fontsize=11)
ax.set_xlabel("OMOP clinical table", fontsize=11)
ax.set_title(
    "Athena Vocabulary Mapping Completeness Across OMOP Clinical Tables",
    fontsize=13,
    fontweight="bold"
)

ax.set_ylim(0, 110)

for bar, value in zip(bars, mapped_percent):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.2f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

caption = (
    "Figure 1. Percentage of imported OMOP records mapped to non-zero concept identifiers "
    "after loading OHDSI Athena Standardized Vocabulary files and applying pyOMOP concept mappings. "
    "Visit occurrence mapping remained incomplete in this lightweight demonstration configuration."
)

fig.text(
    0.5,
    -0.03,
    caption,
    ha="center",
    va="top",
    fontsize=9,
    wrap=True
)

plt.tight_layout()

png_path = out_dir / "figure1_athena_vocabulary_mapping_barplot.png"
pdf_path = out_dir / "figure1_athena_vocabulary_mapping_barplot.pdf"

plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")

print(f"Created: {png_path}")
print(f"Created: {pdf_path}")
