
"""
Comparator benchmark for FHIR flattening workflows.

Purpose
-------
This script addresses a common reviewer question:
"How does the proposed deterministic FHIRy-style flattening workflow compare with a simpler baseline?"

The comparator used here is intentionally narrow and reproducible:
1. fhiry_style_flatten:
   - deterministic recursive flattening
   - list handling by retaining the first scalar/simple element where possible
   - designed to mimic the lightweight analytics-first behavior described in the manuscript

2. generic_json_flatten:
   - generic recursive JSON flattening
   - expands list indexes into column names
   - represents a simple non-FHIR-specific flattening baseline

This is not a claim of superiority over mature external frameworks such as fhircrackr,
FHIR-PYrate, or FHIRpack. It is a transparent, local comparator benchmark that reports
coverage, shape, missingness, and wall-clock runtime on the same input files.

Input
-----
A folder containing FHIR NDJSON files, usually exported by Synthea or another FHIR Bulk
Data workflow.

Example
-------
python analysis/reviewer_gap_strengthening/comparator_benchmark/run_comparator_benchmark.py \
  --input_dir data/synthea_fhir \
  --output_dir results_reviewer_gap_strengthening/comparator_benchmark
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def load_ndjson_file(path: Path) -> List[Dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def discover_ndjson(input_dir: Path) -> List[Path]:
    patterns = ["*.ndjson", "*.jsonl"]
    files = []
    for pattern in patterns:
        files.extend(sorted(input_dir.rglob(pattern)))
    return files


def first_simple_value(value: Any) -> Any:
    """
    Convert nested/list values into a deterministic analytics-friendly scalar.

    This intentionally favors simplicity and reproducibility.
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        if not value:
            return None
        return first_simple_value(value[0])

    if isinstance(value, dict):
        # Prefer common FHIR coding/reference/display/text fields when available.
        preferred = [
            "reference",
            "display",
            "text",
            "code",
            "system",
            "value",
            "id",
            "url",
        ]
        for key in preferred:
            if key in value:
                simple = first_simple_value(value[key])
                if simple is not None:
                    return simple

        # Fallback: first deterministic key.
        for key in sorted(value.keys()):
            simple = first_simple_value(value[key])
            if simple is not None:
                return simple

    return str(value)


def fhiry_style_flatten(obj: Dict[str, Any], parent: str = "") -> Dict[str, Any]:
    """
    Deterministic FHIRy-style flattening:
    - nested dictionary keys become path-like columns
    - lists are simplified by taking the first analytically usable value
    - output remains compact
    """
    out = {}

    for key in sorted(obj.keys()):
        value = obj[key]
        new_key = f"{parent}.{key}" if parent else key

        if isinstance(value, dict):
            out.update(fhiry_style_flatten(value, new_key))
        elif isinstance(value, list):
            out[new_key] = first_simple_value(value)
        else:
            out[new_key] = value

    return out


def generic_json_flatten(obj: Any, parent: str = "") -> Dict[str, Any]:
    """
    Generic JSON flattening:
    - nested dictionary keys become path-like columns
    - list indexes are retained as explicit columns
    - output may become wider and less analytics-friendly
    """
    out = {}

    if isinstance(obj, dict):
        for key in sorted(obj.keys()):
            value = obj[key]
            new_key = f"{parent}.{key}" if parent else key
            out.update(generic_json_flatten(value, new_key))

    elif isinstance(obj, list):
        if not obj:
            out[parent] = None
        else:
            for idx, value in enumerate(obj):
                new_key = f"{parent}.{idx}"
                out.update(generic_json_flatten(value, new_key))

    else:
        out[parent] = obj

    return out


def summarize_dataframe(df: pd.DataFrame, workflow: str, resource_type: str, runtime_sec: float) -> Dict[str, Any]:
    if df.empty:
        return {
            "workflow": workflow,
            "resource_type": resource_type,
            "rows": 0,
            "columns": 0,
            "runtime_sec": runtime_sec,
            "cells": 0,
            "non_null_cells": 0,
            "missing_cells": 0,
            "missing_fraction": None,
        }

    cells = int(df.shape[0] * df.shape[1])
    non_null_cells = int(df.notna().sum().sum())
    missing_cells = int(cells - non_null_cells)
    missing_fraction = float(missing_cells / cells) if cells else None

    return {
        "workflow": workflow,
        "resource_type": resource_type,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "runtime_sec": float(runtime_sec),
        "cells": cells,
        "non_null_cells": non_null_cells,
        "missing_cells": missing_cells,
        "missing_fraction": missing_fraction,
    }


def run_benchmark(input_dir: Path, output_dir: Path, max_records_per_file: int = 0) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    files = discover_ndjson(input_dir)
    if not files:
        raise FileNotFoundError(f"No NDJSON/JSONL files found under: {input_dir}")

    summaries = []
    file_level_rows = []

    for path in files:
        records = load_ndjson_file(path)
        if max_records_per_file and max_records_per_file > 0:
            records = records[:max_records_per_file]

        if not records:
            continue

        resource_type = records[0].get("resourceType", path.stem)

        for workflow, flatten_func in [
            ("fhiry_style_flatten", fhiry_style_flatten),
            ("generic_json_flatten", generic_json_flatten),
        ]:
            start = time.perf_counter()
            flattened = [flatten_func(record) for record in records]
            df = pd.DataFrame(flattened)
            runtime_sec = time.perf_counter() - start

            summary = summarize_dataframe(df, workflow, resource_type, runtime_sec)
            summary["source_file"] = str(path)
            summaries.append(summary)

            file_level_rows.append({
                "source_file": str(path),
                "resource_type": resource_type,
                "workflow": workflow,
                "input_records": len(records),
                "output_rows": int(df.shape[0]),
                "output_columns": int(df.shape[1]),
                "runtime_sec": float(runtime_sec),
            })

            safe_resource = resource_type.replace("/", "_")
            out_csv = output_dir / f"{safe_resource}_{workflow}_preview.csv"
            df.head(100).to_csv(out_csv, index=False)

    summary_df = pd.DataFrame(summaries)
    file_level_df = pd.DataFrame(file_level_rows)

    summary_path = output_dir / "comparator_benchmark_summary.csv"
    file_level_path = output_dir / "comparator_benchmark_file_level.csv"

    summary_df.to_csv(summary_path, index=False)
    file_level_df.to_csv(file_level_path, index=False)

    print("Comparator benchmark complete.")
    print(f"Wrote: {summary_path}")
    print(f"Wrote: {file_level_path}")
    print()
    print(summary_df)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Folder containing FHIR NDJSON/JSONL files")
    parser.add_argument("--output_dir", required=True, help="Folder where benchmark outputs should be written")
    parser.add_argument(
        "--max_records_per_file",
        type=int,
        default=0,
        help="Optional cap per NDJSON file. Use 0 for all records.",
    )
    args = parser.parse_args()

    run_benchmark(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        max_records_per_file=args.max_records_per_file,
    )


if __name__ == "__main__":
    main()
