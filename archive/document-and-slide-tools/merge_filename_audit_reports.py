from pathlib import Path
from datetime import datetime
import ast,shutil,runpy,csv

p=Path(r'C:\Users\amir2\Desktop\car-detection-yolo\code\audit_duplicate_filenames.py')
raw=p.read_bytes()
new='''"""Report filename problems without changing dataset files."""
from pathlib import Path
from collections import defaultdict
import csv

DATASET = Path(r"D:\\projects\\car-detection-yolo\\dataset\\IADD")
OUTPUT = Path(__file__).parent / "filename_audit"


def audit(dataset):
    files_by_name = defaultdict(list)
    checked = 0
    for file in sorted(dataset.glob("*/Record*/*")):
        if file.is_file() and file.suffix.lower() in (".jpg", ".jpeg", ".png", ".txt"):
            files_by_name[file.name.lower()].append(file)
            checked += 1

    rows = []
    for files in files_by_name.values():
        records = set()
        for file in files:
            records.add(file.parent.name)
        shared_name = len(records) > 1

        for file in files:
            record = file.parent.name
            wrong_name = not file.name.lower().startswith(record.lower() + "_")
            if shared_name or wrong_name:
                if shared_name and wrong_name:
                    problem = "نام تکراری و نام رکورد اشتباه"
                elif shared_name:
                    problem = "نام تکراری بین رکوردها"
                else:
                    problem = "نام رکورد اشتباه"
                folder = file.parent.relative_to(dataset).as_posix()
                others = "; ".join(sorted(records - {record}))
                rows.append([problem, file.name, folder, others])
    return checked, rows


if __name__ == "__main__":
    if not DATASET.is_dir():
        raise FileNotFoundError(DATASET)
    checked, rows = audit(DATASET)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "filename_problems.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["مشکل", "نام فایل", "پوشه", "رکوردهای دیگر با همین نام فایل"])
        writer.writerows(rows)
    print("Checked files:", checked)
    print("Files with filename problems:", len(rows))
    print("Report:", OUTPUT / "filename_problems.csv")
'''
ast.parse(new)
env={'__name__':'verification','__file__':str(p)}
exec(new,env)
fixture=Path(r'C:\Users\amir2\Desktop\cat-claude')/('merged_audit_fixture_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
examples=[('train_part2','Record407_D','Record409_D_0'),('train_part2','Record409_D','Record409_D_0'),
          ('val','Record409_D','Record409_D_1'),('train_part2','Record409_D','Record409_D_1'),
          ('val','Record010_N','Record099_N_0')]
for split,record,name in examples:
    folder=fixture/split/record;folder.mkdir(parents=True,exist_ok=True)
    for ext in ('.jpg','.txt'):(folder/(name+ext)).write_text('test')
checked,rows=env['audit'](fixture)
assert checked==10 and len(rows)==6
assert sum(r[0]=='نام تکراری و نام رکورد اشتباه' for r in rows)==2
assert sum(r[0]=='نام تکراری بین رکوردها' for r in rows)==2
assert sum(r[0]=='نام رکورد اشتباه' for r in rows)==2
backup=p.parent/'backups'/datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
shutil.copy2(p,backup/p.name)
report_dir=p.parent/'filename_audit'
for f in report_dir.glob('*.csv'):shutil.copy2(f,backup/f.name)
nl='\r\n' if b'\r\n' in raw else '\n'
p.write_bytes(new.replace('\n',nl).encode('utf-8'))
# The previous two reports remain backed up; archive them after successful generation.
(backup/'previous_reports.txt').write_text(str(report_dir),encoding='utf-8')
print('Code changed to one report; both issue types and same-record split exclusion verified; code and reports backed up.')
print(str(backup).encode('ascii','backslashreplace').decode())
