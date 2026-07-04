import os
import re
import glob
import time
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.stats import bootstrap


RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

REPO_ROOT = Path.cwd()
OUTPUT_DIR = REPO_ROOT / "results_reviewer_strengthening" / "fhir_omop_analytical_stability"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Change this only if your SQLite DBs are outside the repo.
SEARCH_ROOTS = [
    REPO_ROOT,
    Path("/content/drive/MyDrive/fhir_omop_colab"),
    Path("/content/drive/MyDrive"),
]

DB_EXTENSIONS = ["*.db", "*.sqlite", "*.sqlite3"]


def find_variant_databases():
    """
    Use the validated non-empty 25k SQLite databases.
    The results_combined_25k SQLite files are zero-byte placeholders and must not be used.
    """
    variant_map = {
        "V0": "/content/drive/MyDrive/fhir_omop_colab/results_25k/V0_clinical_core_25k.sqlite",
        "V1": "/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V1_missing_demographics_clinical_core_25k.sqlite",
        "V2": "/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V2_duplicate_encounter_ids_clinical_core_25k.sqlite",
        "V3": "/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V3_conflicting_codings_clinical_core_25k.sqlite",
        "V4": "/content/drive/MyDrive/fhir_omop_colab/results_V1_V4_25k/V4_missing_medications_clinical_core_25k.sqlite",
    }

    missing = [v for v, p in variant_map.items() if not Path(p).exists() or Path(p).stat().st_size == 0]
    if missing:
        raise FileNotFoundError(f"Missing or empty validated SQLite files for variants: {missing}")

    return variant_map


def table_exists(conn, table_name):
    q = """
    SELECT name FROM sqlite_master
    WHERE type='table' AND lower(name)=lower(?)
    """
    return pd.read_sql_query(q, conn, params=[table_name]).shape[0] > 0


def get_col(conn, table, col):
    if not table_exists(conn, table):
        return []
    try:
        df = pd.read_sql_query(f"SELECT {col} FROM {table}", conn)
        return df[col].fillna("__MISSING__").astype(str).tolist()
    except Exception:
        return []


def get_person_ids(conn, table):
    if not table_exists(conn, table):
        return set()
    try:
        df = pd.read_sql_query(f"SELECT DISTINCT person_id FROM {table}", conn)
        return set(df["person_id"].dropna().astype(int).tolist())
    except Exception:
        return set()


def get_count(conn, table):
    if not table_exists(conn, table):
        return 0
    return int(pd.read_sql_query(f"SELECT COUNT(*) AS n FROM {table}", conn)["n"].iloc[0])


def jaccard(a, b):
    a, b = set(a), set(b)
    if len(a | b) == 0:
        return 1.0
    return len(a & b) / len(a | b)


def distribution(values):
    s = pd.Series(values).fillna("__MISSING__").astype(str)
    counts = s.value_counts()
    return counts / counts.sum()


def aligned_probs(a_values, b_values):
    pa = distribution(a_values)
    pb = distribution(b_values)
    idx = sorted(set(pa.index) | set(pb.index))
    return pa.reindex(idx, fill_value=0).values, pb.reindex(idx, fill_value=0).values


def jsd(a_values, b_values):
    if len(a_values) == 0 or len(b_values) == 0:
        return np.nan
    p, q = aligned_probs(a_values, b_values)
    return float(jensenshannon(p, q, base=2) ** 2)


def shannon_entropy(values):
    if len(values) == 0:
        return np.nan
    p = distribution(values).values
    return float(-(p * np.log2(p)).sum())


def null_jsd_bootstrap(v0_values, n_iter=200):
    """
    Null/noise baseline: compare two bootstrap samples from V0.
    This estimates expected JSD due to sampling noise alone.
    """
    v0_values = np.array(v0_values, dtype=object)
    if len(v0_values) == 0:
        return {
            "null_mean": np.nan,
            "null_sd": np.nan,
            "null_p95": np.nan,
            "null_max": np.nan,
        }

    out = []
    n = len(v0_values)
    for _ in range(n_iter):
        a = np.random.choice(v0_values, size=n, replace=True)
        b = np.random.choice(v0_values, size=n, replace=True)
        out.append(jsd(a, b))

    out = np.array(out, dtype=float)
    return {
        "null_mean": float(np.nanmean(out)),
        "null_sd": float(np.nanstd(out)),
        "null_p95": float(np.nanpercentile(out, 95)),
        "null_max": float(np.nanmax(out)),
    }


def runtime_query(conn, query, repeats=10):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        pd.read_sql_query(query, conn)
        t1 = time.perf_counter()
        times.append(t1 - t0)

    arr = np.array(times)
    mean = float(arr.mean())
    sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    ci_low = float(mean - 1.96 * sd / np.sqrt(len(arr)))
    ci_high = float(mean + 1.96 * sd / np.sqrt(len(arr)))

    return mean, sd, ci_low, ci_high


def main():
    variant_dbs = find_variant_databases()

    if not variant_dbs:
        raise FileNotFoundError(
            "No V0-V4 SQLite databases found. Put the OMOP .db/.sqlite files in the repo "
            "or under /content/drive/MyDrive/fhir_omop_colab, then rerun."
        )

    print("Detected variant databases:")
    for v, p in variant_dbs.items():
        print(v, "->", p)

    if "V0" not in variant_dbs:
        raise FileNotFoundError("V0 baseline database not found. Cannot compare variants.")

    # ---------- Cohort and prevalence analysis ----------
    cohort_rows = []
    prevalence_rows = []
    table_count_rows = []

    conns = {v: sqlite3.connect(p) for v, p in variant_dbs.items()}

    v0_conn = conns["V0"]
    v0_condition_persons = get_person_ids(v0_conn, "condition_occurrence")
    v0_drug_persons = get_person_ids(v0_conn, "drug_exposure")
    v0_both = v0_condition_persons & v0_drug_persons
    v0_all_persons = get_person_ids(v0_conn, "person")

    base_cohorts = {
        "any_condition": v0_condition_persons,
        "any_drug": v0_drug_persons,
        "condition_and_drug": v0_both,
    }

    for v, conn in conns.items():
        persons = get_person_ids(conn, "person")
        condition_persons = get_person_ids(conn, "condition_occurrence")
        drug_persons = get_person_ids(conn, "drug_exposure")
        both = condition_persons & drug_persons

        cohorts = {
            "any_condition": condition_persons,
            "any_drug": drug_persons,
            "condition_and_drug": both,
        }

        for cohort_name, ids in cohorts.items():
            base_ids = base_cohorts[cohort_name]
            cohort_rows.append({
                "variant": v,
                "cohort": cohort_name,
                "v0_count": len(base_ids),
                "variant_count": len(ids),
                "overlap": len(base_ids & ids),
                "union": len(base_ids | ids),
                "lost_from_v0": len(base_ids - ids),
                "gained_vs_v0": len(ids - base_ids),
                "jaccard_vs_v0": jaccard(base_ids, ids),
            })

        n_persons = max(len(persons), 1)
        prevalence_rows.append({
            "variant": v,
            "persons": len(persons),
            "condition_persons": len(condition_persons),
            "drug_persons": len(drug_persons),
            "condition_prevalence": len(condition_persons) / n_persons,
            "drug_exposure_prevalence": len(drug_persons) / n_persons,
            "condition_and_drug_prevalence": len(both) / n_persons,
        })

        for table in [
            "person", "visit_occurrence", "condition_occurrence",
            "drug_exposure", "measurement", "observation",
            "procedure_occurrence"
        ]:
            table_count_rows.append({
                "variant": v,
                "table": table,
                "row_count": get_count(conn, table),
            })

    cohort_df = pd.DataFrame(cohort_rows)
    prevalence_df = pd.DataFrame(prevalence_rows)
    table_count_df = pd.DataFrame(table_count_rows)

    # Add prevalence changes vs V0
    v0_prev = prevalence_df[prevalence_df["variant"] == "V0"].iloc[0]
    for col in ["condition_prevalence", "drug_exposure_prevalence", "condition_and_drug_prevalence"]:
        prevalence_df[col + "_change_vs_v0"] = prevalence_df[col] - float(v0_prev[col])
        prevalence_df[col + "_pct_change_vs_v0"] = (
            prevalence_df[col + "_change_vs_v0"] / max(float(v0_prev[col]), 1e-12)
        ) * 100

    cohort_df.to_csv(OUTPUT_DIR / "cohort_jaccard_downstream_shift.csv", index=False)
    prevalence_df.to_csv(OUTPUT_DIR / "downstream_exposure_prevalence_shift.csv", index=False)
    table_count_df.to_csv(OUTPUT_DIR / "omop_table_row_counts_by_variant.csv", index=False)

    # ---------- JSD, entropy, and null baseline ----------
    metric_specs = [
        ("gender_concept_id", "person", "gender_concept_id"),
        ("condition_source_value", "condition_occurrence", "condition_source_value"),
        ("drug_source_value", "drug_exposure", "drug_source_value"),
    ]

    drift_rows = []
    for metric_name, table, col in metric_specs:
        v0_values = get_col(v0_conn, table, col)
        null_stats = null_jsd_bootstrap(v0_values, n_iter=200)

        for v, conn in conns.items():
            values = get_col(conn, table, col)
            observed = jsd(v0_values, values)
            ent_v0 = shannon_entropy(v0_values)
            ent_v = shannon_entropy(values)

            drift_rows.append({
                "variant": v,
                "metric": metric_name,
                "table": table,
                "column": col,
                "v0_unique": len(set(v0_values)),
                "variant_unique": len(set(values)),
                "unique_change": len(set(values)) - len(set(v0_values)),
                "jsd_vs_v0": observed,
                "v0_entropy_bits": ent_v0,
                "variant_entropy_bits": ent_v,
                "entropy_change_bits": ent_v - ent_v0 if pd.notna(ent_v0) and pd.notna(ent_v) else np.nan,
                "null_jsd_mean": null_stats["null_mean"],
                "null_jsd_sd": null_stats["null_sd"],
                "null_jsd_p95": null_stats["null_p95"],
                "observed_exceeds_null_p95": observed > null_stats["null_p95"] if pd.notna(observed) else False,
            })

    drift_df = pd.DataFrame(drift_rows)
    drift_df.to_csv(OUTPUT_DIR / "distributional_drift_with_null_baseline.csv", index=False)

    # ---------- Runtime confidence intervals ----------
    runtime_queries = {
        "total_persons": "SELECT COUNT(*) AS n FROM person",
        "persons_with_conditions": "SELECT COUNT(DISTINCT person_id) AS n FROM condition_occurrence",
        "persons_with_drugs": "SELECT COUNT(DISTINCT person_id) AS n FROM drug_exposure",
        "condition_source_summary": """
            SELECT condition_source_value, COUNT(*) AS n
            FROM condition_occurrence
            GROUP BY condition_source_value
            ORDER BY n DESC
            LIMIT 20
        """,
        "condition_drug_overlap": """
            SELECT COUNT(DISTINCT c.person_id) AS n
            FROM condition_occurrence c
            INNER JOIN drug_exposure d
              ON c.person_id = d.person_id
        """,
    }

    runtime_rows = []
    for v, conn in conns.items():
        for qname, q in runtime_queries.items():
            try:
                mean, sd, ci_low, ci_high = runtime_query(conn, q, repeats=10)
                runtime_rows.append({
                    "variant": v,
                    "query": qname,
                    "mean_runtime_sec": mean,
                    "sd_runtime_sec": sd,
                    "ci95_low_sec": ci_low,
                    "ci95_high_sec": ci_high,
                    "repeats": 10,
                })
            except Exception as e:
                runtime_rows.append({
                    "variant": v,
                    "query": qname,
                    "mean_runtime_sec": np.nan,
                    "sd_runtime_sec": np.nan,
                    "ci95_low_sec": np.nan,
                    "ci95_high_sec": np.nan,
                    "repeats": 10,
                    "error": str(e),
                })

    runtime_df = pd.DataFrame(runtime_rows)
    runtime_df.to_csv(OUTPUT_DIR / "runtime_confidence_intervals.csv", index=False)

    # ---------- Summary text for manuscript ----------
    summary_path = OUTPUT_DIR / "README_analysis_summary.md"

    v4_drug = cohort_df[(cohort_df["variant"] == "V4") & (cohort_df["cohort"] == "any_drug")]
    if not v4_drug.empty:
        v4_drug = v4_drug.iloc[0].to_dict()

    v3_cond = drift_df[(drift_df["variant"] == "V3") & (drift_df["metric"] == "condition_source_value")]
    if not v3_cond.empty:
        v3_cond = v3_cond.iloc[0].to_dict()

    with open(summary_path, "w") as f:
        f.write("# FHIR-to-OMOP Analytical Stability Strengthening Analysis\n\n")
        f.write("This folder contains additional reviewer-strengthening analyses for the FHIRy-pyOMOP manuscript.\n\n")
        f.write("## Generated outputs\n\n")
        f.write("- `cohort_jaccard_downstream_shift.csv`\n")
        f.write("- `downstream_exposure_prevalence_shift.csv`\n")
        f.write("- `omop_table_row_counts_by_variant.csv`\n")
        f.write("- `distributional_drift_with_null_baseline.csv`\n")
        f.write("- `runtime_confidence_intervals.csv`\n\n")

        f.write("## Key interpretation\n\n")
        if v4_drug:
            f.write(
                f"- V4 drug-exposed cohort Jaccard vs V0: "
                f"{v4_drug.get('jaccard_vs_v0', np.nan):.3f}; "
                f"lost from V0: {int(v4_drug.get('lost_from_v0', 0))}; "
                f"gained vs V0: {int(v4_drug.get('gained_vs_v0', 0))}.\n"
            )
        if v3_cond:
            f.write(
                f"- V3 condition source-value JSD vs V0: "
                f"{v3_cond.get('jsd_vs_v0', np.nan):.4f}; "
                f"null JSD 95th percentile: {v3_cond.get('null_jsd_p95', np.nan):.4f}; "
                f"observed exceeds null p95: {v3_cond.get('observed_exceeds_null_p95', False)}.\n"
            )

        f.write("\nThese analyses help connect engineering-level perturbation metrics to downstream analytical consequences.\n")

    for conn in conns.values():
        conn.close()

    print("\nAnalysis complete.")
    print("Outputs written to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
