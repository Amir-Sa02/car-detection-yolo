from pathlib import Path
from datetime import datetime
import runpy
import shutil
import ast

target=Path(r'C:\Users\amir2\Desktop\car-detection-yolo\code\audit_duplicate_filenames.py')
original=target.read_bytes()
old=runpy.run_path(str(target),run_name='verification')
new='''"""Check filenames only; dataset files are never changed."""
from pathlib import Path
from collections import defaultdict
import csv

DATASET = Path(r"D:\\projects\\car-detection-yolo\\dataset\\IADD")
OUTPUT = Path(__file__).parent / "filename_audit"


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
            paths.append(str(file))

        if len(records) > 1:
            shared.append([files[0].name, "; ".join(sorted(records)), "; ".join(paths)])

    return checked, shared, mismatches


def save_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    if not DATASET.is_dir():
        raise FileNotFoundError(DATASET)
    checked, shared, mismatches = audit(DATASET)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_csv(OUTPUT / "shared_filenames.csv", ["filename", "records", "paths"], shared)
    save_csv(OUTPUT / "record_name_mismatches.csv",
             ["folder_record", "filename_record", "filename", "path"], mismatches)
    print("Checked files:", checked)
    print("Shared names across different records:", len(shared))
    print("Names not matching their record folder:", len(mismatches))
    print("Reports:", OUTPUT)
'''
ast.parse(new)
namespace={'__file__':str(target),'__name__':'verification'}
exec(new,namespace)
fixture=Path(r'C:\Users\amir2\Desktop\cat-claude')/('short_filename_fixture_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
examples=[('train_part2','Record407_D','Record409_D_0'),('train_part2','Record409_D','Record409_D_0'),
          ('val','Record409_D','Record409_D_1'),('train_part2','Record409_D','Record409_D_1'),
          ('train_part3','Record042_D','Record043_D_068700'),('train_part3','Record043_D','Record043_D_068700')]
for split,record,name in examples:
    folder=fixture/split/record
    folder.mkdir(parents=True,exist_ok=True)
    for ext in ('.jpg','.txt'):
        (folder/(name+ext)).write_text('test')
a,old_shared,old_mismatch=old['audit'](fixture)
b,new_shared,new_mismatch=namespace['audit'](fixture)
assert a==b
assert sorted(tuple(r.values()) for r in old_shared)==sorted(tuple(r) for r in new_shared)
assert sorted(tuple(r.values()) for r in old_mismatch)==sorted(tuple(r) for r in new_mismatch)
backup=target.parent/'backups'/datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
shutil.copy2(target,backup/target.name)
nl='\r\n' if b'\r\n' in original else '\n'
target.write_bytes(new.replace('\n',nl).encode())
print('Shortened from',len(original.splitlines()),'to',len(new.splitlines()),'lines; both checks verified. Backup saved.')
