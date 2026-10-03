"""iadd_subset_v5

Changes vs v4:
  * EXCLUDE confirmed-broken-label videos (Record426_D, Record046_D).
  * EXCLUDE one copy of each duplicate-video pair (drop Record407_D, Record416_R, Record043_D; their twins stay).
  * Fresh blind reshuffle (new SEED) so the val/test partition is redrawn without any reference to model scores
Everything else (whole-video split, 70/15/15 by image, rare-class balance,
condition stratification, 1280 px) is identical to the tested v4 build.

Set DRY_RUN=True to only compute + print the split stats (no image copying).
"""
import os, glob, shutil, random
from collections import defaultdict, Counter
from PIL import Image

SRC = r"D:\projects\car-detection-yolo\dataset\IADD"
OUT = r"D:\projects\car-detection-yolo\dataset\iadd_subset_v5"
MAX_SIDE, JPEG_QUALITY = 1280, 88
SEED = 80                         # best val/test balance on object-size + class + weather
DRY_RUN = False                   # True = stats only, no image copying
LABELED = ["train_part1", "train_part2", "train_part3", "val"]
NAMES = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
COLAB_PATH = "/content/iadd_subset_v5"

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
    return out  # list of (jpg, txt, stem, cls) for all frames in the record


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
    # Frames info per each video (record). Each frame: (jpg, txt, stem, cls)
    videos = {r: frames_of(r, folders) for r, folders in rec_map.items() if r not in EXCLUDE}
    # Count of frames per video
    vsize = {r: len(v) for r, v in videos.items()}
    print(f"videos: {len(videos)} (excluded {len(EXCLUDE)})  total frames: {sum(vsize.values()):,}", flush=True)

    def rare_score(r):
        count = 0
        for frame in videos[r]:
            classes = frame[3]
            for c in classes:
                if c in RARE_SCARCE:
                    count += 1
        return count

    by_cond = defaultdict(list)
    for r in videos:
        by_cond[r.split("_")[-1]].append(r)

    assign = {}
    for cond, recs in by_cond.items():
        total_rare = 0
        total_frames = 0
        for r in recs:
            total_rare += rare_score(r)
            total_frames += vsize[r]
        rt = {}  # target rare counts per split
        ft = {} # target frame counts per split
        for s in FRAC:
            rt[s] = FRAC[s] * total_rare
            ft[s] = FRAC[s] * total_frames
        sr = Counter()  # rare counts per split
        sf = Counter()  # frame counts per split

        # Process videos with more rare instances first, then assign each to the split with the largest deficit.
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


    # Defining which images to keep in the final dataset 
    def sample(split):
        frames = []
        for r in videos:
            if assign[r] == split:
                for frame in videos[r]:
                    frames.append(frame)
        keep = []
        common = []
        for frame in frames:
            has_rare_class = False
            for class_id in frame[3]:
                if class_id in KEEP_CLASSES:
                    has_rare_class = True
                    break
            # If the frame has a rare class, keep it; otherwise, add it to the common list
            if has_rare_class:
                keep.append(frame)
            else:
                common.append(frame)
        random.Random(SEED).shuffle(common)
        needed = TARGET[split] - len(keep)
        if needed < 0:
            needed = 0
        selected = keep + common[:needed]
        random.Random(SEED).shuffle(selected)
        return selected

    sel = {s: sample(s) for s in ("train", "val", "test")}

    for split in ("train", "val", "test"):
        instances = 0
        for frame in sel[split]:
            instances += len(frame[3])
        print(split, "images:", len(sel[split]), "instances:", instances)

    if DRY_RUN:
        print("DRY_RUN: no files written.")
        return

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    for split in ("train", "val", "test"):
        image_dir = os.path.join(OUT, "images", split)
        label_dir = os.path.join(OUT, "labels", split)
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)

        for frame in sel[split]:
            jpg = frame[0]
            txt = frame[1]
            name = frame[2]
            resize_save(jpg, os.path.join(image_dir, name + ".jpg"))
            shutil.copy2(txt, os.path.join(label_dir, name + ".txt"))

        print(split, "saved", flush=True)

    yaml_path = os.path.join(OUT, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("path: " + COLAB_PATH + "\n")
        f.write("train: images/train\n")
        f.write("val: images/val\n")
        f.write("test: images/test\n")
        f.write("\nnc: 6\n")
        f.write("names:\n")
        for class_id, name in enumerate(NAMES):
            f.write("  " + str(class_id) + ": " + name + "\n")

    print("Output:", OUT)


if __name__ == "__main__":
    main()
