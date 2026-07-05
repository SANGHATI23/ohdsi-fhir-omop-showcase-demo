
#!/usr/bin/env python3
"""
Profile public/deidentified FHIR NDJSON files.

This script is designed for the MIMIC-IV Clinical Database Demo on FHIR
or similar public/deidentified FHIR Bulk NDJSON exports.

It writes aggregate CSV outputs only. It does not commit or redistribute
raw patient-level FHIR resources.
"""

import argparse
import gzip
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd


def iter_ndjson_gz(path: Path) -> Iterable[Dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def flatten_json(obj: Any, prefix: str = "") -> Dict[str, Any]:
    out = {}

    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.update(flatten_json(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f"{prefix}[{i}]"
            out.update(flatten_json(v, key))
    else:
        out[prefix] = obj

    return out


def compact_flatten_fhir(resource: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compact deterministic FHIR flattening approximation.

    This intentionally keeps first coding/category/identifier values,
    similar to an analytics-oriented compact flattening strategy.
    """
    row = {
        "resourceType": resource.get("resourceType"),
        "id": resource.get("id"),
    }

    # subject/patient reference
    for key in ["subject", "patient", "encounter", "medicationReference"]:
        value = resource.get(key)
        if isinstance(value, dict):
            row[f"{key}.reference"] = value.get("reference")
            row[f"{key}.display"] = value.get("display")

    # common dates
    for key in [
        "birthDate",
        "effectiveDateTime",
        "issued",
        "recordedDate",
        "onsetDateTime",
        "authoredOn",
        "performedDateTime",
    ]:
        if key in resource:
            row[key] = resource.get(key)

    # periods
    for key in ["period", "effectivePeriod", "performedPeriod"]:
        value = resource.get(key)
        if isinstance(value, dict):
            row[f"{key}.start"] = value.get("start")
            row[f"{key}.end"] = value.get("end")

    # code first coding
    code = resource.get("code")
    if isinstance(code, dict):
        row["code.text"] = code.get("text")
        codings = code.get("coding")
        if isinstance(codings, list) and codings:
            first = codings[0]
            row["code.coding.system"] = first.get("system")
            row["code.coding.code"] = first.get("code")
            row["code.coding.display"] = first.get("display")

    # medication code
    med_code = resource.get("medicationCodeableConcept")
    if isinstance(med_code, dict):
        row["medicationCodeableConcept.text"] = med_code.get("text")
        codings = med_code.get("coding")
        if isinstance(codings, list) and codings:
            first = codings[0]
            row["medicationCodeableConcept.coding.system"] = first.get("system")
            row["medicationCodeableConcept.coding.code"] = first.get("code")
            row["medicationCodeableConcept.coding.display"] = first.get("display")

    # status/class/gender
    for key in ["status", "gender"]:
        if key in resource:
            row[key] = resource.get(key)

    class_value = resource.get("class")
    if isinstance(class_value, dict):
        row["class.system"] = class_value.get("system")
        row["class.code"] = class_value.get("code")
        row["class.display"] = class_value.get("display")

    return row


def find_references(obj: Any) -> List[str]:
    refs = []

    if isinstance(obj, dict):
        if "reference" in obj and isinstance(obj["reference"], str):
            refs.append(obj["reference"])
        for v in obj.values():
            refs.extend(find_references(v))
    elif isinstance(obj, list):
        for v in obj:
            refs.extend(find_references(v))

    return refs


def normalize_ref(ref: str) -> str:
    # Convert "Patient/123" to ("Patient", "123") style key string.
    ref = ref.strip()
    ref = ref.split("?")[0]
    ref = ref.split("#")[0]

    if "/" in ref:
        parts = ref.split("/")
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"

    return ref


def shannon_entropy(values: List[str]) -> Tuple[int, float, float]:
    cleaned = ["<MISSING>" if v is None or str(v).strip() == "" else str(v) for v in values]
    total = len(cleaned)
    counts = Counter(cleaned)

    entropy = 0.0
    for c in counts.values():
        p = c / total if total else 0
        if p > 0:
            entropy -= p * math.log2(p)

    normalized = entropy / math.log2(len(counts)) if len(counts) > 1 else 0.0
    return len(counts), entropy, normalized


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.ndjson.gz"))
    if not files:
        raise FileNotFoundError(f"No .ndjson.gz files found in {input_dir}")

    resource_counts = []
    field_presence_rows = []
    reference_rows = []
    flatten_benchmark_rows = []
    entropy_rows = []

    all_resource_ids = set()
    resources_by_file = {}

    print(f"Reading {len(files)} FHIR NDJSON files...")

    for path in files:
        resources = list(iter_ndjson_gz(path))
        resources_by_file[path.name] = resources

        rtypes = Counter([r.get("resourceType", "UNKNOWN") for r in resources])
        for rtype, count in rtypes.items():
            resource_counts.append({
                "file": path.name,
                "resource_type": rtype,
                "record_count": count,
            })

        for r in resources:
            rtype = r.get("resourceType")
            rid = r.get("id")
            if rtype and rid:
                all_resource_ids.add(f"{rtype}/{rid}")

    for fname, resources in resources_by_file.items():
        print(f"Profiling {fname}: {len(resources)} records")

        # field presence
        field_counts = Counter()
        missing_id_count = 0

        # references
        total_refs = 0
        unresolved_refs = 0
        ref_type_counts = Counter()
        unresolved_type_counts = Counter()

        # flattening benchmark
        start = time.perf_counter()
        generic_rows = [flatten_json(r) for r in resources]
        generic_runtime = time.perf_counter() - start

        start = time.perf_counter()
        compact_rows = [compact_flatten_fhir(r) for r in resources]
        compact_runtime = time.perf_counter() - start

        generic_fields = sorted(set().union(*[set(r.keys()) for r in generic_rows])) if generic_rows else []
        compact_fields = sorted(set().union(*[set(r.keys()) for r in compact_rows])) if compact_rows else []

        flatten_benchmark_rows.append({
            "file": fname,
            "records": len(resources),
            "generic_json_columns": len(generic_fields),
            "compact_fhir_columns": len(compact_fields),
            "generic_json_runtime_seconds": generic_runtime,
            "compact_fhir_runtime_seconds": compact_runtime,
            "column_reduction": len(generic_fields) - len(compact_fields),
        })

        code_values = []
        med_values = []
        status_values = []

        for r in resources:
            rid = r.get("id")
            if not rid:
                missing_id_count += 1

            flat = flatten_json(r)
            for field, value in flat.items():
                if value is not None and str(value).strip() != "":
                    field_counts[field] += 1

            refs = find_references(r)
            total_refs += len(refs)

            for ref in refs:
                norm = normalize_ref(ref)
                ref_type = norm.split("/")[0] if "/" in norm else "UNKNOWN"
                ref_type_counts[ref_type] += 1
                if norm not in all_resource_ids:
                    unresolved_refs += 1
                    unresolved_type_counts[ref_type] += 1

            # source-value style entropy
            code = r.get("code")
            if isinstance(code, dict):
                codings = code.get("coding")
                if isinstance(codings, list) and codings:
                    c = codings[0]
                    code_values.append(f"{c.get('system')}|{c.get('code')}")
                elif code.get("text"):
                    code_values.append(code.get("text"))

            med_code = r.get("medicationCodeableConcept")
            if isinstance(med_code, dict):
                codings = med_code.get("coding")
                if isinstance(codings, list) and codings:
                    c = codings[0]
                    med_values.append(f"{c.get('system')}|{c.get('code')}")
                elif med_code.get("text"):
                    med_values.append(med_code.get("text"))

            if "status" in r:
                status_values.append(r.get("status"))

        total_records = len(resources)
        for field, non_null_count in field_counts.items():
            field_presence_rows.append({
                "file": fname,
                "field_path": field,
                "non_null_count": non_null_count,
                "record_count": total_records,
                "presence_fraction": non_null_count / total_records if total_records else 0,
            })

        reference_rows.append({
            "file": fname,
            "record_count": total_records,
            "missing_id_count": missing_id_count,
            "total_references": total_refs,
            "unresolved_references": unresolved_refs,
            "unresolved_reference_fraction": unresolved_refs / total_refs if total_refs else 0,
            "reference_type_counts": json.dumps(dict(ref_type_counts), sort_keys=True),
            "unresolved_reference_type_counts": json.dumps(dict(unresolved_type_counts), sort_keys=True),
        })

        for label, values in [
            ("code_first_coding", code_values),
            ("medication_first_coding", med_values),
            ("status", status_values),
        ]:
            if values:
                unique_count, entropy, normalized_entropy = shannon_entropy(values)
                entropy_rows.append({
                    "file": fname,
                    "source_field_group": label,
                    "total_values": len(values),
                    "unique_values": unique_count,
                    "shannon_entropy_bits": entropy,
                    "normalized_entropy": normalized_entropy,
                    "most_common_value": Counter(values).most_common(1)[0][0],
                    "most_common_count": Counter(values).most_common(1)[0][1],
                })

    resource_counts_df = pd.DataFrame(resource_counts)
    field_presence_df = pd.DataFrame(field_presence_rows)
    reference_df = pd.DataFrame(reference_rows)
    flatten_df = pd.DataFrame(flatten_benchmark_rows)
    entropy_df = pd.DataFrame(entropy_rows)

    overall_reference = pd.DataFrame([{
        "files_processed": len(files),
        "total_records": int(resource_counts_df["record_count"].sum()) if not resource_counts_df.empty else 0,
        "total_references": int(reference_df["total_references"].sum()) if not reference_df.empty else 0,
        "unresolved_references": int(reference_df["unresolved_references"].sum()) if not reference_df.empty else 0,
        "unresolved_reference_fraction": (
            reference_df["unresolved_references"].sum() / reference_df["total_references"].sum()
            if not reference_df.empty and reference_df["total_references"].sum() else 0
        ),
    }])

    resource_counts_df.to_csv(output_dir / "mimic_demo_resource_counts.csv", index=False)
    field_presence_df.to_csv(output_dir / "mimic_demo_field_presence.csv", index=False)
    reference_df.to_csv(output_dir / "mimic_demo_reference_integrity_summary.csv", index=False)
    overall_reference.to_csv(output_dir / "mimic_demo_reference_integrity_overall.csv", index=False)
    flatten_df.to_csv(output_dir / "mimic_demo_compact_vs_generic_flattening_benchmark.csv", index=False)
    entropy_df.to_csv(output_dir / "mimic_demo_source_value_entropy.csv", index=False)

    print("\nWrote outputs to:", output_dir)
    for p in sorted(output_dir.glob("*.csv")):
        print(p.name)


if __name__ == "__main__":
    main()
