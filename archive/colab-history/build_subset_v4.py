# -*- coding: utf-8 -*-
"""Build iadd_subset_v4.

Split by WHOLE VIDEO (no frame leakage), targeting ~70/15/15 by IMAGE count.
The three scarce classes (motorcycle, bus, traffic_light) are:
  - balanced ~70/15/15 across splits (so train keeps ~70% for learning), and
  - fully kept (every frame containing them is included).
Frames with only person/car/truck are subsampled to hit the per-split image target.
Stratified by condition suffix (_D day / _N night / _R rain / _A).
Output -> dataset/iadd_subset_v4/{images,labels}/{train,val,test} + data.yaml
"""
import os, glob, shutil, random
from collections import defaultdict, Counter
from PIL import Image

SRC = r"D:\projects\car-detection-yolo\dataset\IADD"
OUT = r"D:\projects\car-detection-yolo\dataset\iadd_subset_v4"
MAX_SIDE, JPEG_QUALITY = 1280, 88
SEED = 42
LABELED = ["train_part1", "train_part2", "train_part3", "val"]   # test/ has no labels
NAMES = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
COLAB_PATH = "/content/iadd_subset_v4"

KEEP_CLASSES = {2, 3, 5}        # motorcycle, bus, traffic_light -> keep ALL such frames
RARE_SCARCE = {2, 3, 5}         # balance these ~70/15/15 across splits
FRAC = {"train": 0.70, "val": 0.15, "test": 0.15}
TRAIN_TARGET = 26000
VAL_TARGET = round(TRAIN_TARGET * FRAC["val"] / FRAC["train"])
TARGET = {"train": TRAIN_TARGET, "val": VAL_TARGET, "test": VAL_TARGET}


def read_classes(txt):
    cls = []
    try:
        with open(txt) as f:
            for line in f:
                line = line.strip()
                if line:
                    cls.append(int(line.split()[0]))
    except FileNotFoundError:
        pass
    return cls


def record_dirs():
    m = defaultdict(list)
    for sd in LABELED:
        b = os.path.join(SRC, sd)
        if os.path.isdir(b):
            for d in sorted(os.listdir(b)):
                p = os.path.join(b, d)
                if os.path.isdir(p):
                    m[d].append(p)
    return m


def frames_of(record, folders):
    out, seen = [], set()
    for f in folders:
        for jpg in sorted(glob.glob(os.path.join(f, "*.jpg"))):
            stem = os.path.splitext(os.path.basename(jpg))[0]
            if stem in seen:
                continue
            txt = jpg[:-4] + ".txt"
            if os.path.exists(txt):
                out.append((jpg, txt, f"{record}__{stem}", tuple(read_classes(txt))))
                seen.add(stem)
    return out


def resize_save(src_jpg, dst_jpg):
    im = Image.open(src_jpg).convert("RGB")
    w, h = im.size
    scale = MAX_SIDE / max(w, h)
    if scale < 1.0:
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    im.save(dst_jpg, "JPEG", quality=JPEG_QUALITY)


def main():
    print("reading videos + labels ...", flush=True)
    rec_map = record_dirs()
    videos = {r: frames_of(r, folders) for r, folders in rec_map.items()}
    vsize = {r: len(v) for r, v in videos.items()}
    print(f"videos: {len(videos)}  total frames: {sum(vsize.values()):,}", flush=True)

    def rare_score(r):
        return sum(1 for _, _, _, cls in videos[r] for c in cls if c in RARE_SCARCE)

    by_cond = defaultdict(list)
    for r in videos:
        by_cond[r.split("_")[-1]].append(r)

    # assign whole videos: scarce-heavy first (balance rare), rest fill frames -> 70/15/15
    assign = {}
    for cond, recs in by_cond.items():
        rt = {s: FRAC[s] * sum(rare_score(r) for r in recs) for s in FRAC}
        ft = {s: FRAC[s] * sum(vsize[r] for r in recs) for s in FRAC}
        sr, sf = Counter(), Counter()
        for r in sorted(recs, key=lambda r: (-rare_score(r), -vsize[r])):
            if rare_score(r) > 0:
                s = max(FRAC, key=lambda s: rt[s] - sr[s])
            else:
                s = max(FRAC, key=lambda s: ft[s] - sf[s])
            assign[r] = s
            sr[s] += rare_score(r); sf[s] += vsize[r]

    tr = {r for r in videos if assign[r] == "train"}
    va = {r for r in videos if assign[r] == "val"}
    te = {r for r in videos if assign[r] == "test"}
    assert not (tr & va) and not (tr & te) and not (va & te)
    print(f"video split -> train {len(tr)} | val {len(va)} | test {len(te)}  (no overlap)", flush=True)

    def sample(split):
        frames = [fr for r in videos if assign[r] == split for fr in videos[r]]
        keep = [f for f in frames if set(f[3]) & KEEP_CLASSES]
        common = [f for f in frames if not (set(f[3]) & KEEP_CLASSES)]
        random.Random(SEED).shuffle(common)
        sel = keep + common[:max(0, TARGET[split] - len(keep))]
        random.Random(SEED).shuffle(sel)
        return sel

    sel = {s: sample(s) for s in ("train", "val", "test")}
    print("selected:", {s: len(sel[s]) for s in sel}, flush=True)

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for s in ("train", "val", "test"):
        os.makedirs(os.path.join(OUT, "images", s), exist_ok=True)
        os.makedirs(os.path.join(OUT, "labels", s), exist_ok=True)

    ctr = {s: Counter() for s in sel}
    for s in ("train", "val", "test"):
        idir, ldir = os.path.join(OUT, "images", s), os.path.join(OUT, "labels", s)
        for n, (jpg, txt, uniq, cls) in enumerate(sel[s], 1):
            resize_save(jpg, os.path.join(idir, uniq + ".jpg"))
            shutil.copy2(txt, os.path.join(ldir, uniq + ".txt"))
            for c in cls:
                ctr[s][c] += 1
            if n % 2000 == 0:
                print(f"  {s}: {n}/{len(sel[s])}", flush=True)
        print(f"  {s}: done ({len(sel[s])} images)", flush=True)

    with open(os.path.join(OUT, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("# IADD subset v4 (leakage-free split by video, 70/15/15 by image)\n")
        f.write(f"path: {COLAB_PATH}\n")
        f.write("train: images/train\nval: images/val\ntest: images/test\n\n")
        f.write("nc: 6\nnames:\n")
        for i, nm in enumerate(NAMES):
            f.write(f"  {i}: {nm}\n")

    print("\n" + "=" * 60)
    print("iadd_subset_v4 BUILT")
    print("=" * 60)
    for s in ("train", "val", "test"):
        print(f"{s:>5}: {len(sel[s]):>6,} images")
    print("\nclass instances per split:")
    print(f"  {'class':<15}{'train':>9}{'val':>8}{'test':>8}")
    for i, nm in enumerate(NAMES):
        print(f"  {nm:<15}{ctr['train'][i]:>9,}{ctr['val'][i]:>8,}{ctr['test'][i]:>8,}")
    print(f"\nOutput: {OUT}")
    print("Next, zip it (PowerShell):")
    print(f'  Compress-Archive -Path "{OUT}\\*" -DestinationPath "{OUT}.zip" -Force')


if __name__ == "__main__":
    main()
