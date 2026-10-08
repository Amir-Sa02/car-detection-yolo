from pathlib import Path
from datetime import datetime
from zipfile import ZipFile, ZIP_STORED
import hashlib
import json

root=Path(r'D:\projects\car-detection-yolo\dataset\IADD').resolve()
plan=[]
folder=root/'train_part2'/'Record407_D'
for f in sorted(folder.iterdir()):
    if f.is_file() and f.suffix.lower() in ('.jpg','.txt') and f.name.startswith('Record407_D_'):
        target=f.with_name(f.name.replace('Record407_D','Record409_D',1))
        plan.append((f,target))
assert len(plan)==1258

folder=root/'train_part3'/'Record042_D'
reference=root/'train_part3'/'Record043_D'
matched=[]
for image in sorted(folder.glob('Record042_D_*.jpg')):
    ref=reference/image.name.replace('Record042_D','Record043_D',1)
    if ref.exists():
        assert hashlib.sha256(image.read_bytes()).digest()==hashlib.sha256(ref.read_bytes()).digest()
        label=image.with_suffix('.txt')
        ref_label=ref.with_suffix('.txt')
        assert label.is_file() and ref_label.is_file()
        assert label.read_bytes()==ref_label.read_bytes()
        matched.append(image)
        for source in (image,label):
            target=source.with_name(source.name.replace('Record042_D','Record043_D',1))
            plan.append((source,target))
assert len(matched)==79 and len(plan)==1416
for source,target in plan:
    assert source.resolve().is_relative_to(root)
    assert target.resolve().is_relative_to(root)
    assert source.parent==target.parent
    assert not target.exists()

backup=Path(r'D:\projects\car-detection-yolo\docs\dataset_validity\filename_backups')/('before_restoration_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
backup.mkdir(parents=True)
mapping=[]
with ZipFile(backup/'files_before_restoration.zip','w',compression=ZIP_STORED) as archive:
    for source,target in plan:
        data=source.read_bytes()
        archive.writestr(source.relative_to(root).as_posix(),data)
        mapping.append({'before':str(source),'restored':str(target),'sha256':hashlib.sha256(data).hexdigest()})
(backup/'restore_map.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
completed=[]
try:
    for source,target in plan:
        assert not target.exists()
        source.rename(target)
        completed.append((source,target))
    for item in mapping:
        assert not Path(item['before']).exists()
        assert hashlib.sha256(Path(item['restored']).read_bytes()).hexdigest()==item['sha256']
except Exception:
    for source,target in reversed(completed):
        target.rename(source)
    raise
print(json.dumps({'restored_files':len(completed),'restored_images_in_042':len(matched),'backup':str(backup),'content_verified':True}))
