
"""
FHIR NDJSON profiling scaffold for public or governance-approved deidentified data.

Purpose
-------
This script addresses the reviewer-facing generalizability concern that the submitted
evaluation used synthetic FHIR data only.

Important
---------
This script does NOT include or claim use of real patient data. It provides a reproducible
profiling workflow that can be run on:

1. publicly available FHIR example resources,
2. deidentified FHIR Bulk NDJSON exports approved for research use, or
3. institutional deidentified FHIR extracts when governance permits.

No real patient data should be committed to the repository.

Outputs
-------
- resource_profile_summary.csv
- field_presence_summary.csv
- reference_integrity_summary.csv

These outputs help characterize source-data complexity before FHIR-to-OMOP transformation.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set

import pandas as pd


def discover_ndjson(input_dir: Path) -> List[Path]:
    files = []
    files.extend(sorted(input_dir.rglob("*.ndjson")))
    files.extend(sorted(input_dir.rglob("*.jsonl")))
    return files


def load_ndjson(path: Path, max_records: int = 0) -> List[Dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
            if max_records and len(records) >= max_records:
                break
    return records


def flatten_keys(obj: Any, prefix: str = "") -> Set[str]:
    keys = set()

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            keys.add(new_key)
            keys.update(flatten_keys(v, new_key))

    elif isinstance(obj, list):
        for item in obj:
            keys.update(flatten_keys(item, prefix))

    return keys


def get_references(obj: Any) -> List[str]:
    refs = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "reference" and isinstance(v, str):
                refs.append(v)
            else:
                refs.extend(get_references(v))

    elif isinstance(obj, list):
        for item in obj:
            refs.extend(get_references(item))

    return refs


def profile_fhir(input_dir: Path, output_dir: Path, max_records_per_file: int = 0) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    files = discover_ndjson(input_dir)
    if not files:
        raise FileNotFoundError(f"No NDJSON/JSONL files found under: {input_dir}")

    resource_rows = []
    field_rows = []
    reference_rows = []

    all_resource_ids = set()

    loaded_by_file = []

    for path in files:
        records = load_ndjson(path, max_records=max_records_per_file)
        if not records:
            continue

        loaded_by_file.append((path, records))

        for record in records:
            resource_type = record.get("resourceType", "UNKNOWN")
            resource_id = record.get("id")

            if resource_type and resource_id:
                all_resource_ids.add(f"{resource_type}/{resource_id}")

    for path, records in loaded_by_file:
        resource_type = records[0].get("resourceType", path.stem)

        all_keys = set()
        reference_count = 0
        unresolved_reference_count = 0
        missing_id_count = 0

        field_presence_counter = {}

        for record in records:
            if not record.get("id"):
                missing_id_count += 1

            keys = flatten_keys(record)
            all_keys.update(keys)

            for key in keys:
                field_presence_counter[key] = field_presence_counter.get(key, 0) + 1

            refs = get_references(record)
            reference_count += len(refs)

            for ref in refs:
                # Ignore contained, absolute, and urn references in this simple scaffold.
                if ref.startswith("#") or ref.startswith("urn:") or ref.startswith("http"):
                    continue
                if ref not in all_resource_ids:
                    unresolved_reference_count += 1

        resource_rows.append({
            "source_file": str(path),
            "resource_type": resource_type,
            "records": len(records),
            "unique_flattened_fields": len(all_keys),
            "missing_id_count": missing_id_count,
            "reference_count": reference_count,
            "unresolved_reference_count": unresolved_reference_count,
        })

        for field, present_count in sorted(field_presence_counter.items()):
            field_rows.append({
                "source_file": str(path),
                "resource_type": resource_type,
                "field": field,
                "present_count": present_count,
                "records": len(records),
                "presence_fraction": present_count / len(records) if records else None,
            })

        reference_rows.append({
            "source_file": str(path),
            "resource_type": resource_type,
            "reference_count": reference_count,
            "unresolved_reference_count": unresolved_reference_count,
            "unresolved_reference_fraction": (
                unresolved_reference_count / reference_count if reference_count else 0.0
            ),
        })

    resource_df = pd.DataFrame(resource_rows)
    field_df = pd.DataFrame(field_rows)
    reference_df = pd.DataFrame(reference_rows)

    resource_path = output_dir / "resource_profile_summary.csv"
    field_path = output_dir / "field_presence_summary.csv"
    reference_path = output_dir / "reference_integrity_summary.csv"

    resource_df.to_csv(resource_path, index=False)
    field_df.to_csv(field_path, index=False)
    reference_df.to_csv(reference_path, index=False)

    print("FHIR profiling complete.")
    print(f"Wrote: {resource_path}")
    print(f"Wrote: {field_path}")
    print(f"Wrote: {reference_path}")
    print()
    print(resource_df)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Folder containing public/deidentified FHIR NDJSON files")
    parser.add_argument("--output_dir", required=True, help="Folder for profiling outputs")
    parser.add_argument(
        "--max_records_per_file",
        type=int,
        default=0,
        help="Optional cap per file. Use 0 for all records.",
    )
    args = parser.parse_args()

    profile_fhir(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        max_records_per_file=args.max_records_per_file,
    )


if __name__ == "__main__":
    main()
