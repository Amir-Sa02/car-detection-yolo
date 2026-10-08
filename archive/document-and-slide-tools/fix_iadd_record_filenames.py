from pathlib import Path
from datetime import datetime
from zipfile import ZipFile, ZIP_STORED
from collections import Counter
import hashlib
import json

root = Path(r'D:\projects\car-detection-yolo\dataset\IADD').resolve()
corrections = [
    ('train_part2/Record407_D', 'Record409_D', 'Record407_D'),
    ('train_part3/Record042_D', 'Record043_D', 'Record042_D'),
]
plan = []
for relative, old, new in corrections:
    folder = (root / relative).resolve()
    assert folder.is_relative_to(root)
    for source in sorted(folder.iterdir()):
        if not source.is_file() or source.suffix.lower() not in ('.jpg', '.txt'):
            continue
        if not source.name.startswith(old + '_'):
            continue
        destination = source.with_name(new + source.name[len(old):])
        assert destination.resolve().is_relative_to(folder)
        assert not destination.exists(), f'Destination already exists: {destination}'
        if source.suffix.lower() == '.jpg':
            assert source.with_suffix('.txt').exists()
        plan.append((source, destination))
assert len(plan) == 1416
assert len({destination for _, destination in plan}) == len(plan)

backup = Path(r'D:\projects\car-detection-yolo\docs\dataset_validity\filename_backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
mapping = []
with ZipFile(backup / 'original_files.zip', 'w', compression=ZIP_STORED) as archive:
    for source, destination in plan:
        data = source.read_bytes()
        archive.writestr(source.relative_to(root).as_posix(), data)
        mapping.append({'old': str(source), 'new': str(destination),
                        'sha256': hashlib.sha256(data).hexdigest()})
(backup / 'rename_map.json').write_text(json.dumps(mapping, indent=2), encoding='utf-8')

completed = []
try:
    for source, destination in plan:
        assert not destination.exists()
        source.rename(destination)
        completed.append((source, destination))
    for item in mapping:
        assert not Path(item['old']).exists()
        assert hashlib.sha256(Path(item['new']).read_bytes()).hexdigest() == item['sha256']
    for relative, _, record in corrections:
        folder = root / relative
        files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in ('.jpg', '.txt')]
        assert all(f.name.startswith(record + '_') for f in files)
        for f in files:
            if f.suffix.lower() == '.jpg':
                assert f.with_suffix('.txt').exists()
except Exception:
    for source, destination in reversed(completed):
        destination.rename(source)
    raise

counts = Counter(str(source.parent.relative_to(root)) for source, _ in plan)
print(json.dumps({'renamed_files': len(plan), 'counts': dict(counts), 'backup': str(backup),
                  'content_hashes_unchanged': True, 'image_label_pairs_verified': True}))
