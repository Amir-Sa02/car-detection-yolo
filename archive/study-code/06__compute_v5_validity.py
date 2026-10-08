"""Compute iadd_subset_v5 distribution stats + charts to document its validity."""
import os, glob, json
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DS = r"D:\projects\car-detection-yolo\dataset\iadd_subset_v5"
OUT = r"D:\projects\car-detection-yolo\docs\dataset_validity"
os.makedirs(OUT, exist_ok=True)
NAMES = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
SMALL, LARGE = 0.01, 0.06
SPLITS = ["train", "val", "test"]
COL = {"train": "#1f4e79", "val": "#2eb669", "test": "#e08a00"}

# Analyze the distribution of images in a given split
def analyze(split):
    imgs = glob.glob(f"{DS}/images/{split}/*.jpg")
    cls = Counter(); size = Counter(); cond = Counter(); inst = 0; vids = set()
    for p in imgs:
        stem = os.path.basename(p)[:-4]
        rec = stem.split("__")[0]
        vids.add(rec)
        cond[rec.split("_")[-1]] += 1
        t = f"{DS}/labels/{split}/{stem}.txt"
        if os.path.exists(t):
            for line in open(t):
                q = line.split()
                if len(q) == 5:
                    inst += 1
                    cls[int(q[0])] += 1
                    a = float(q[3]) * float(q[4])
                    if a < SMALL:
                        size[0] += 1
                    elif a >= LARGE:
                        size[2] += 1
                    else:
                        size[1] += 1
    return {"images": len(imgs), "videos": len(vids), "instances": inst,
            "cls": {i: cls.get(i, 0) for i in range(6)},
            "size": {k: size.get(k, 0) for k in range(3)},
            "cond": dict(cond)}


S = {sp: analyze(sp) for sp in SPLITS}
json.dump(S, open(f"{OUT}/stats.json", "w"), indent=2)

# ---- chart 1: class distribution (share of each split's instances) ----
fig, ax = plt.subplots(figsize=(8, 4))
x = range(6); w = 0.26
for i, sp in enumerate(SPLITS):
    tot = S[sp]["instances"]
    vals = [100 * S[sp]["cls"][c] / tot for c in range(6)]
    ax.bar([xx + (i-1)*w for xx in x], vals, w, label=sp, color=COL[sp])
ax.set_xticks(list(x)); ax.set_xticklabels(NAMES, rotation=20)
ax.set_ylabel("% of split instances"); ax.set_title("Class distribution per split")
ax.legend(); plt.tight_layout(); plt.savefig(f"{OUT}/class_dist.png", dpi=140); plt.close()

# ---- chart 2: object-size distribution ----
fig, ax = plt.subplots(figsize=(6, 4))
bins = ["small\n(<1%)", "medium\n(1-6%)", "large\n(>6%)"]; x = range(3)
for i, sp in enumerate(SPLITS):
    tot = sum(S[sp]["size"].values())
    vals = [100 * S[sp]["size"][k] / tot for k in range(3)]
    ax.bar([xx + (i-1)*w for xx in x], vals, w, label=sp, color=COL[sp])
ax.set_xticks(list(x)); ax.set_xticklabels(bins)
ax.set_ylabel("% of instances"); ax.set_title("Object-size distribution per split")
ax.legend(); plt.tight_layout(); plt.savefig(f"{OUT}/size_dist.png", dpi=140); plt.close()

# ---- chart 3: condition distribution ----
fig, ax = plt.subplots(figsize=(6, 4))
conds = ["D", "N", "R", "A"]; x = range(4)
for i, sp in enumerate(SPLITS):
    tot = S[sp]["images"]
    vals = [100 * S[sp]["cond"].get(c, 0) / tot for c in conds]
    ax.bar([xx + (i-1)*w for xx in x], vals, w, label=sp, color=COL[sp])
ax.set_xticks(list(x)); ax.set_xticklabels(["day", "night", "rain", "other"])
ax.set_ylabel("% of images"); ax.set_title("Condition distribution per split")
ax.legend(); plt.tight_layout(); plt.savefig(f"{OUT}/cond_dist.png", dpi=140); plt.close()

print("=== iadd_subset_v5 stats ===")
for sp in SPLITS:
    d = S[sp]
    sz = sum(d["size"].values())
    print(f"{sp}: videos={d['videos']} images={d['images']} inst={d['instances']} "
          f"inst/img={d['instances']/d['images']:.1f}  "
          f"size S/M/L={[round(100*d['size'][k]/sz) for k in range(3)]}%")
print("charts + stats.json ->", OUT)
