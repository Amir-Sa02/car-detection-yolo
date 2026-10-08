"""Check filenames only; dataset files are never changed."""
from pathlib import Path
from collections import defaultdict
import csv

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset/IADD"
OUTPUT = ROOT / "outputs/filename_audit"


def audit(dataset):
    files_by_name = defaultdict(list)
    mismatches = []
    checked = 0

    for file in sorted(dataset.glob("*/Record*/*")):
        if not file.is_file():
            continue
        if file.suffix.lower() not in (".jpg", ".jpeg", ".png", ".txt"):
            continue

        checked += 1
        record = file.parent.name
        files_by_name[file.name.lower()].append(file)

        if not file.name.lower().startswith(record.lower() + "_"):
            prefix = "_".join(file.stem.split("_")[:2])
            mismatches.append([record, prefix, file.name, str(file)])

    shared = []
    for files in files_by_name.values():
        records = set()
        paths = []
        for file in files:
            records.add(file.parent.name)
            paths.append(file.parent.relative_to(dataset).as_posix())

        if len(records) > 1:
            shared.append([files[0].name, "; ".join(sorted(records)), "; ".join(paths)])

    return checked, shared, mismatches


def save_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=DATASET)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    DATASET, OUTPUT = args.dataset, args.output
    if not DATASET.is_dir():
        raise FileNotFoundError(DATASET)
    checked, shared, mismatches = audit(DATASET)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_csv(OUTPUT / "shared_filenames.csv", ["filename", "records", "folders"], shared)
    save_csv(OUTPUT / "record_name_mismatches.csv",
             ["folder_record", "filename_record", "filename", "path"], mismatches)
    print("Checked files:", checked)
    print("Shared names across different records:", len(shared))
    print("Names not matching their record folder:", len(mismatches))
    print("Reports:", OUTPUT)
