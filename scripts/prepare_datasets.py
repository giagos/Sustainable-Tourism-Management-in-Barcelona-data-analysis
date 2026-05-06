from __future__ import annotations

import csv
import gzip
import json
import shutil
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSPACE_ROOT / "Data"
MANIFEST_PATH = DATA_DIR / "catalog" / "dataset_manifest.csv"
PREPARED_DIR = DATA_DIR / "prepared"
REPORT_PATH = DATA_DIR / "catalog" / "preparation_report.csv"
SUMMARY_PATH = DATA_DIR / "catalog" / "preparation_summary.json"


def safe_members(zip_file: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members: list[zipfile.ZipInfo] = []
    for member in zip_file.infolist():
        if member.is_dir():
            continue
        parts = PurePosixPath(member.filename).parts
        if any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"Unsafe zip member path: {member.filename}")
        members.append(member)
    return members


def normalize_text_bytes(payload: bytes) -> tuple[bytes, bool]:
    try:
        text = payload.decode("utf-8-sig")
        encoding = "utf-8"
    except UnicodeDecodeError:
        return payload, False

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.count("\n") <= 1 and normalized.count("\\n") > 1:
        normalized = normalized.replace("\\r\\n", "\n").replace("\\n", "\n")
    if normalized == text:
        return payload, False
    return normalized.encode(encoding), True


def sniff_csv_dialect(sample: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.get_dialect("excel")


def validate_csv(path: Path) -> tuple[str, int]:
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        dialect = sniff_csv_dialect(sample)
        reader = csv.reader(handle, dialect)
        header = next(reader, None)
        if not header:
            raise ValueError("CSV file is empty")
        column_count = len(header)
        non_empty_rows = 0
        for row in reader:
            if row:
                non_empty_rows += 1
            if non_empty_rows >= 5:
                break
        if non_empty_rows == 0:
            raise ValueError("CSV file has a header but no data rows")
    return ("csv", column_count)


def validate_geojson(path: Path) -> tuple[str, int]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if payload.get("type") not in {"FeatureCollection", "Feature", "GeometryCollection"}:
        raise ValueError("GeoJSON root type is not valid")
    feature_count = len(payload.get("features", [])) if isinstance(payload.get("features"), list) else 0
    return ("geojson", feature_count)


def validate_json(path: Path) -> tuple[str, int]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        return ("json", len(payload))
    if isinstance(payload, list):
        return ("json", len(payload))
    return ("json", 1)


def validate_prepared_file(path: Path) -> tuple[str, int]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return validate_csv(path)
    if suffix == ".geojson":
        return validate_geojson(path)
    if suffix == ".json":
        return validate_json(path)
    return (suffix.lstrip("."), 0)


def copy_plain_file(source_path: Path, prepared_dataset_dir: Path) -> list[dict[str, str | int]]:
    prepared_path = prepared_dataset_dir / source_path.name
    prepared_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, prepared_path)
    file_type, detail = validate_prepared_file(prepared_path)
    return [
        {
            "prepared_relative_path": str(prepared_path.relative_to(WORKSPACE_ROOT)),
            "file_type": file_type,
            "detail": detail,
        }
    ]


def extract_gzip_file(source_path: Path, prepared_dataset_dir: Path) -> list[dict[str, str | int]]:
    prepared_path = prepared_dataset_dir / source_path.stem
    prepared_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(source_path, "rb") as source_handle:
        payload = source_handle.read()
    normalized_payload, _ = normalize_text_bytes(payload)
    with prepared_path.open("wb") as output_handle:
        output_handle.write(normalized_payload)
    file_type, detail = validate_prepared_file(prepared_path)
    return [
        {
            "prepared_relative_path": str(prepared_path.relative_to(WORKSPACE_ROOT)),
            "file_type": file_type,
            "detail": detail,
        }
    ]


def extract_zip_file(source_path: Path, prepared_dataset_dir: Path) -> list[dict[str, str | int]]:
    extracted_records: list[dict[str, str | int]] = []
    archive_key = source_path.name.split("__", 1)[0]
    archive_dir = prepared_dataset_dir / archive_key
    archive_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source_path) as archive:
        corrupt_member = archive.testzip()
        if corrupt_member is not None:
            raise ValueError(f"Corrupt zip member: {corrupt_member}")
        members = safe_members(archive)
        if not members:
            raise ValueError("Zip archive contains no files")
        for member in members:
            destination = archive_dir.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source_handle:
                payload = source_handle.read()
            normalized_payload, _ = normalize_text_bytes(payload)
            with destination.open("wb") as output_handle:
                output_handle.write(normalized_payload)
            file_type, detail = validate_prepared_file(destination)
            extracted_records.append(
                {
                    "prepared_relative_path": str(destination.relative_to(WORKSPACE_ROOT)),
                    "file_type": file_type,
                    "detail": detail,
                }
            )

    return extracted_records


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def prepare_dataset() -> tuple[list[dict[str, str | int]], dict[str, object]]:
    if PREPARED_DIR.exists():
        shutil.rmtree(PREPARED_DIR)
    PREPARED_DIR.mkdir(parents=True, exist_ok=True)

    report_rows: list[dict[str, str | int]] = []
    prepared_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()

    for row in load_manifest():
        source_path = WORKSPACE_ROOT / row["relative_path"]
        prepared_dataset_dir = PREPARED_DIR / row["source_group"] / row["dataset_id"]
        prepared_dataset_dir.mkdir(parents=True, exist_ok=True)

        base_row = {
            "source_group": row["source_group"],
            "dataset_id": row["dataset_id"],
            "resource_id": row["resource_id"],
            "raw_relative_path": row["relative_path"],
            "status": "ok",
            "file_type": "",
            "detail": 0,
            "prepared_relative_path": "",
            "message": "",
        }

        try:
            if not source_path.exists():
                raise FileNotFoundError(f"Missing raw file: {source_path}")

            suffix = source_path.suffix.lower()
            if suffix == ".gz":
                prepared_records = extract_gzip_file(source_path, prepared_dataset_dir)
            elif suffix == ".zip":
                prepared_records = extract_zip_file(source_path, prepared_dataset_dir)
            else:
                prepared_records = copy_plain_file(source_path, prepared_dataset_dir)

            prepared_counter[row["source_group"]] += len(prepared_records)
            status_counter["ok"] += 1
            for prepared_record in prepared_records:
                report_row = dict(base_row)
                report_row.update(prepared_record)
                report_rows.append(report_row)
        except Exception as exc:
            status_counter["error"] += 1
            error_row = dict(base_row)
            error_row["status"] = "error"
            error_row["message"] = str(exc)
            report_rows.append(error_row)

    summary = {
        "raw_files_in_manifest": len(load_manifest()),
        "prepared_files_written": len([row for row in report_rows if row["status"] == "ok"]),
        "status_counts": dict(status_counter),
        "prepared_files_by_source_group": dict(prepared_counter),
        "report_path": str(REPORT_PATH.relative_to(WORKSPACE_ROOT)),
    }
    return report_rows, summary


def write_outputs(report_rows: list[dict[str, str | int]], summary: dict[str, object]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_group",
        "dataset_id",
        "resource_id",
        "raw_relative_path",
        "status",
        "file_type",
        "detail",
        "prepared_relative_path",
        "message",
    ]
    with REPORT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)

    with SUMMARY_PATH.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    rows, summary = prepare_dataset()
    write_outputs(rows, summary)
    print(json.dumps(summary, indent=2))