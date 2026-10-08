# -*- coding: utf-8 -*-
"""Build iadd_subset_v5 - honest rebuild of v4.

Changes vs v4:
  * EXCLUDE confirmed-broken-label videos (Record426_D, Record046_D).
  * EXCLUDE one copy of each duplicate-video pair so no near-duplicate can straddle
    splits (drop Record407_D, Record416_R, Record043_D; their twins stay).
  * Fresh fixed-seed shuffle without using model scores for video assignment.
Everything else (whole-video split, 70/15/15 by image, rare-class balance,
condition stratification, 1280 px) is identical to the tested v4 build.

Pass --dry-run to compute and print statistics without copying images.
"""
import os, glob, shutil, random
from collections import defaultdict, Counter
from PIL import Image

from pathlib import Path
from argparse import ArgumentParser

ROOT = Path(__file__).resolve().parents[1]
parser = ArgumentParser(description="Rebuild the IADD V5 subset (whole-video split).")
parser.add_argument("--source", default=str(ROOT / "dataset/IADD"))
parser.add_argument("--output", default=str(ROOT / "dataset/iadd_subset_v5"))
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--yaml-path", help="Override the dataset path written to data.yaml")
args = parser.parse_args()
SRC = args.source
OUT = args.output
if Path(SRC).resolve().is_relative_to(Path(OUT).resolve()):
    raise SystemExit("Output cannot be the source folder or one of its ancestors.")
if not Path(SRC).is_dir():
    raise SystemExit("IADD source folder is missing: " + SRC)
if Path(OUT).exists() and any(Path(OUT).iterdir()) and not args.dry_run and not args.overwrite:
    raise SystemExit("Output is not empty. Choose a new folder or explicitly use --overwrite.")
MAX_SIDE, JPEG_QUALITY = 1280, 88
SEED = 80                         # fixed seed recorded for the V5 split
DRY_RUN = args.dry_run                   # True = stats only, no image copying
LABELED = ["train_part1", "train_part2", "train_part3", "val"]
NAMES = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
COLAB_PATH = args.yaml_path or str(Path(OUT).resolve())

# broken labels (verified) + one copy of each duplicate-video pair
EXCLUDE = {"Record426_D", "Record046_D", "Record407_D", "Record416_R", "Record043_D"}

KEEP_CLASSES = {2, 3, 5}
RARE_SCARCE = {2, 3, 5}
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
    videos = {r: frames_of(r, folders) for r, folders in rec_map.items() if r not in EXCLUDE}
    vsize = {r: len(v) for r, v in videos.items()}
    print(f"videos: {len(videos)} (excluded {len(EXCLUDE)})  total frames: {sum(vsize.values()):,}", flush=True)

    def rare_score(r):
        return sum(1 for _, _, _, cls in videos[r] for c in cls if c in RARE_SCARCE)

    by_cond = defaultdict(list)
    for r in videos:
        by_cond[r.split("_")[-1]].append(r)

    assign = {}
    for cond, recs in by_cond.items():
        rt = {s: FRAC[s] * sum(rare_score(r) for r in recs) for s in FRAC}
        ft = {s: FRAC[s] * sum(vsize[r] for r in recs) for s in FRAC}
        sr, sf = Counter(), Counter()
        # blind reshuffle: shuffle within condition before the deficit-greedy assignment
        recs = sorted(recs)
        random.Random(SEED).shuffle(recs)
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

    # ---- stats (condition mix + crowd are the difficulty proxies) ----
    print("\n" + "=" * 64)
    print("PLAN" if DRY_RUN else "iadd_subset_v5 BUILT")
    print("=" * 64)
    tot = sum(len(sel[s]) for s in sel)
    print(f"videos per split: train {len(tr)} | val {len(va)} | test {len(te)}")
    for s in ("train", "val", "test"):
        imgs = sel[s]
        inst = sum(len(c[3]) for c in imgs)
        cond = Counter(c[2].split("__")[0].split("_")[-1] for c in imgs)
        condpct = {k: f"{100*v/len(imgs):.0f}%" for k, v in sorted(cond.items())}
        print(f"  {s:<5} {len(imgs):>6,} imgs ({100*len(imgs)/tot:>4.1f}%)  inst/img={inst/len(imgs):.1f}  cond={condpct}")
    print("\nclass instances per split:")
    print(f"  {'class':<15}{'train':>9}{'val':>8}{'test':>8}{'val%':>7}{'test%':>7}")
    ctr = {s: Counter(c for im in sel[s] for c in im[3]) for s in sel}
    for i, nm in enumerate(NAMES):
        t, v, e = ctr['train'][i], ctr['val'][i], ctr['test'][i]
        tot_i = t + v + e
        print(f"  {nm:<15}{t:>9,}{v:>8,}{e:>8,}{100*v/tot_i:>6.1f}%{100*e/tot_i:>6.1f}%")

    if DRY_RUN:
        print("\n(DRY_RUN: no images written. Set DRY_RUN=False to build.)")
        return

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for s in ("train", "val", "test"):
        os.makedirs(os.path.join(OUT, "images", s), exist_ok=True)
        os.makedirs(os.path.join(OUT, "labels", s), exist_ok=True)
    for s in ("train", "val", "test"):
        idir, ldir = os.path.join(OUT, "images", s), os.path.join(OUT, "labels", s)
        for n, (jpg, txt, uniq, cls) in enumerate(sel[s], 1):
            resize_save(jpg, os.path.join(idir, uniq + ".jpg"))
            shutil.copy2(txt, os.path.join(ldir, uniq + ".txt"))
            if n % 2000 == 0:
                print(f"  {s}: {n}/{len(sel[s])}", flush=True)
        print(f"  {s}: done ({len(sel[s])} images)", flush=True)
    with open(os.path.join(OUT, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("# IADD subset v5 (leakage-free, broken+duplicate videos removed, blind reshuffle)\n")
        f.write(f"path: {COLAB_PATH}\n")
        f.write("train: images/train\nval: images/val\ntest: images/test\n\nnc: 6\nnames:\n")
        for i, nm in enumerate(NAMES):
            f.write(f"  {i}: {nm}\n")
    print(f"\nOutput: {OUT}")
    print(f'  Compress-Archive -Path "{OUT}\\*" -DestinationPath "{OUT}.zip" -Force')


if __name__ == "__main__":
    main()
