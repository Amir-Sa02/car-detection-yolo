# -*- coding: utf-8 -*-
"""
Build the Run-3 subset of IADD — HONEST SPLIT BY VIDEO (leakage-free).
(Run-1 and Run-2 versions of this script live in git history.)

Key differences vs run-2:
  * SPLIT BY WHOLE VIDEO (Record folder), stratified by condition
    (_D day / _N night / _R rain / _A). Each video goes ENTIRELY to
    train, val, or test — no video appears in two splits, so there is
    NO frame leakage. (Professor approved re-splitting.)
  * A real, labelled TEST set (labels are KEPT for evaluation; we simply
    never train on those videos).
  * Rebalancing now also protects PERSON (class 0), which lagged in run-2.
  * Adds a CONTROLLED fraction of sparse (few-object) frames to the train
    set so the model learns what background looks like -> fewer false
    positives, without hurting recall.
  * MAX_SIDE 1280, trained later at imgsz 960.

Split fractions are by VIDEO: 70% train / 15% val / 15% test.
Output -> dataset/iadd_subset_v3/{images,labels}/{train,val,test} + data.yaml
Run:  python -u build_subset.py
"""
import os, glob, shutil, random
from collections import Counter, defaultdict
from PIL import Image

# ----------------------------------------------------------------------------
SRC   = r"D:\projects\car-detection-yolo\dataset\IADD"
OUT   = r"D:\projects\car-detection-yolo\dataset\iadd_subset_v3"
MAX_SIDE, JPEG_QUALITY = 1280, 88
SEED  = 42

LABELED_DIRS = ["train_part1", "train_part2", "train_part3", "val"]  # test/ has no labels
CLASS_NAMES  = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
COLAB_PATH   = "/content/iadd_subset_v3"

# split-by-video fractions (per condition, so day/night/rain all appear everywhere)
FRAC_TRAIN, FRAC_VAL = 0.70, 0.15   # test = remaining 0.15

# --- train rebalancing (tiered keep-rate) ---
VERY_RARE  = {2, 3, 5}   # motorcycle, bus, traffic_light -> keep ALL frames
PERSON     = 0
PERSON_STRIDE = 1        # frames with person (no very-rare): keep ALL (person was weak)
COMMON_STRIDE = 6        # frames with only car/truck: keep 1 of every 6
SPARSE_MAXOBJ = 2        # a frame is "sparse" if it has <= this many objects
SPARSE_TARGET = 0.12     # sparse frames should be ~12% of the final train set

# --- val/test: light, representative subsample (NOT rebalanced) ---
EVAL_STRIDE = 6          # keep 1 of every 6 frames per video

random.seed(SEED)


def record_dirs():
    """record_name -> list of its folders across all labeled split dirs."""
    m = defaultdict(list)
    for sd in LABELED_DIRS:
        base = os.path.join(SRC, sd)
        if not os.path.isdir(base):
            continue
        for d in sorted(os.listdir(base)):
            p = os.path.join(base, d)
            if os.path.isdir(p):
                m[d].append(p)
    return m


def frames_of(record, folders):
    """All (jpg, txt) pairs of a video, across its folders. Unique stems."""
    out, seen = [], set()
    for folder in folders:
        for jpg in sorted(glob.glob(os.path.join(folder, "*.jpg"))):
            stem = os.path.splitext(os.path.basename(jpg))[0]
            if stem in seen:
                continue
            txt = jpg[:-4] + ".txt"
            if os.path.exists(txt):
                out.append((jpg, txt, f"{record}__{stem}"))
                seen.add(stem)
    return out


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


def split_videos(records):
    """Stratified 70/15/15 split of VIDEOS by condition suffix."""
    by_cond = defaultdict(list)
    for r in records:
        by_cond[r.split("_")[-1]].append(r)
    train, val, test = [], [], []
    for cond, recs in by_cond.items():
        recs = sorted(recs)
        random.Random(SEED).shuffle(recs)
        n = len(recs)
        n_tr = max(1, round(n * FRAC_TRAIN))
        n_va = max(1, round(n * FRAC_VAL)) if n >= 3 else 0
        train += recs[:n_tr]
        val   += recs[n_tr:n_tr + n_va]
        test  += recs[n_tr + n_va:]
    return set(train), set(val), set(test)


def select_train(frames):
    """Tiered rebalancing + controlled sparse frames."""
    kept, leftover_sparse = [], []
    p_seen = c_seen = 0
    for jpg, txt, uniq in frames:
        cls = read_classes(txt)
        n = len(cls)
        s = set(cls)
        if s & VERY_RARE:
            kept.append((jpg, txt, uniq))
        elif PERSON in s:
            if p_seen % PERSON_STRIDE == 0:
                kept.append((jpg, txt, uniq))
            elif n <= SPARSE_MAXOBJ:
                leftover_sparse.append((jpg, txt, uniq))
            p_seen += 1
        else:  # common (car/truck only)
            if c_seen % COMMON_STRIDE == 0:
                kept.append((jpg, txt, uniq))
            elif n <= SPARSE_MAXOBJ:
                leftover_sparse.append((jpg, txt, uniq))
            c_seen += 1
    # add sparse frames up to ~SPARSE_TARGET of the final set
    random.Random(SEED).shuffle(leftover_sparse)
    n_sparse = int(SPARSE_TARGET / (1 - SPARSE_TARGET) * len(kept))
    kept += leftover_sparse[:n_sparse]
    random.Random(SEED).shuffle(kept)
    return kept, min(n_sparse, len(leftover_sparse))


def select_eval(frames):
    return frames[::EVAL_STRIDE]


def resize_save(src_jpg, dst_jpg):
    im = Image.open(src_jpg).convert("RGB")
    w, h = im.size
    scale = MAX_SIDE / max(w, h)
    if scale < 1.0:
        im = im.resize((max(1, round(w*scale)), max(1, round(h*scale))), Image.LANCZOS)
    im.save(dst_jpg, "JPEG", quality=JPEG_QUALITY)


def build(pairs, split, counter):
    idir = os.path.join(OUT, "images", split)
    ldir = os.path.join(OUT, "labels", split)
    for n, (jpg, txt, uniq) in enumerate(pairs, 1):
        resize_save(jpg, os.path.join(idir, uniq + ".jpg"))
        shutil.copy2(txt, os.path.join(ldir, uniq + ".txt"))
        for c in read_classes(txt):
            counter[c] += 1
        if n % 1000 == 0:
            print(f"   {split}: {n}/{len(pairs)}", flush=True)
    print(f"   {split}: done ({len(pairs)} images)", flush=True)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for s in ["train", "val", "test"]:
        os.makedirs(os.path.join(OUT, "images", s), exist_ok=True)
        os.makedirs(os.path.join(OUT, "labels", s), exist_ok=True)

    rec_map = record_dirs()
    records = list(rec_map.keys())
    print(f"videos (records): {len(records)}", flush=True)

    tr_vid, va_vid, te_vid = split_videos(records)
    print(f"video split -> train {len(tr_vid)} | val {len(va_vid)} | test {len(te_vid)}")
    # sanity: no overlap
    assert not (tr_vid & va_vid) and not (tr_vid & te_vid) and not (va_vid & te_vid)
    print("leakage check: no video shared across splits  OK", flush=True)

    print("gathering frames per split...", flush=True)
    tr_frames = [f for r in tr_vid for f in frames_of(r, rec_map[r])]
    va_frames = [f for r in va_vid for f in frames_of(r, rec_map[r])]
    te_frames = [f for r in te_vid for f in frames_of(r, rec_map[r])]
    print(f"  available frames -> train {len(tr_frames)} | val {len(va_frames)} | test {len(te_frames)}")

    tr_sel, n_sparse = select_train(tr_frames)
    va_sel = select_eval(va_frames)
    te_sel = select_eval(te_frames)
    print(f"  selected -> train {len(tr_sel)} (incl ~{n_sparse} sparse) | "
          f"val {len(va_sel)} | test {len(te_sel)}", flush=True)

    ctr = {s: Counter() for s in ("train", "val", "test")}
    print("building TRAIN...", flush=True); build(tr_sel, "train", ctr["train"])
    print("building VAL...",   flush=True); build(va_sel, "val",   ctr["val"])
    print("building TEST...",  flush=True); build(te_sel, "test",  ctr["test"])

    with open(os.path.join(OUT, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("# IADD Run-3 subset (leakage-free split by video)\n")
        f.write(f"path: {COLAB_PATH}\n")
        f.write("train: images/train\nval: images/val\ntest: images/test\n\n")
        f.write("nc: 6\nnames:\n")
        for i, nm in enumerate(CLASS_NAMES):
            f.write(f"  {i}: {nm}\n")

    print("\n" + "=" * 64)
    print("RUN-3 SUBSET BUILT (leakage-free, split by video)")
    print("=" * 64)
    for s in ("train", "val", "test"):
        n = len(glob.glob(os.path.join(OUT, "images", s, "*.jpg")))
        print(f"{s:>5}: {n:>6,} images")
    print("\nclass instances per split:")
    print(f"  {'class':<15}{'train':>9}{'val':>8}{'test':>8}")
    for i, nm in enumerate(CLASS_NAMES):
        print(f"  {nm:<15}{ctr['train'].get(i,0):>9,}{ctr['val'].get(i,0):>8,}"
              f"{ctr['test'].get(i,0):>8,}")
    print(f"\nOutput: {OUT}")
    print("Next, zip it (PowerShell):")
    print(f'  Compress-Archive -Path "{OUT}\\*" -DestinationPath "{OUT}.zip" -Force')


if __name__ == "__main__":
    main()
