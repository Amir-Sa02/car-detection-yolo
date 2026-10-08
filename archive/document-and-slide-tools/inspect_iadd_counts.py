from pathlib import Path
import re

root = Path(r"D:\projects\car-detection-yolo\dataset\iadd_subset_v5\images")
pat = re.compile(r"(Record\d+_[DNRA])")
for split in ("train", "val", "test"):
    files = [p for p in (root / split).iterdir()
             if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    videos = {m.group(1) for p in files if (m := pat.search(p.name))}
    print(split, len(files), len(videos))
