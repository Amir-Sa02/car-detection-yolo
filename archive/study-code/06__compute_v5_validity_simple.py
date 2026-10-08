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
    class_counts = {}
    for i in range(6):
        class_counts[i] = cls.get(i, 0)  # {0: number of person instances, 1: number of car instances, ...}

    size_counts = {}
    for k in range(3):
        size_counts[k] = size.get(k, 0)  # {0: number of small instances, 1: number of medium instances, 2: number of large instances}

    result = {
        "images": len(imgs),
        "videos": len(vids),
        "instances": inst,
        "cls": class_counts,
        "size": size_counts,
        "cond": dict(cond)
    }
    return result


S = {sp: analyze(sp) for sp in SPLITS}
json.dump(S, open(f"{OUT}/stats.json", "w"), indent=2)

# chart 1: class distribution
#  Plot each class's share of all object instances within each split.
# Place train, val, and test bars side by side, then save the chart as class_dist.png.
fig, ax = plt.subplots(figsize=(8, 4))
x = range(6)
w = 0.26
for i, sp in enumerate(SPLITS):
    tot = S[sp]["instances"]
    vals = []
    # For each class, compute its percentage of the total instances in the split.
    for c in range(6):  
        count = S[sp]["cls"][c]
        percent = 100 * count / tot
        vals.append(percent)
    # Compute the positions for the bars of each split
    positions = []
    for xx in x:
        position = xx + (i - 1) * w
        positions.append(position)
    ax.bar(positions, vals, w, label=sp, color=COL[sp])
ax.set_xticks(list(x))
ax.set_xticklabels(NAMES, rotation=20)
ax.set_yscale("log")
ax.set_ylabel("% of split instances")
ax.set_title("Class distribution per split")
ax.legend(); plt.tight_layout(); plt.savefig(f"{OUT}/class_dist.png", dpi=140); plt.close()

# chart 2: object-size distribution
# Plot each size group's share of all object instances within each split.
# Place the split bars side by side and save the chart as size_dist.png.
fig, ax = plt.subplots(figsize=(6, 4))
bins = ["small\n(<1%)", "medium\n(1% to <6%)", "large\n(>=6%)"]
x = range(3)
w = 0.26

for i, sp in enumerate(SPLITS):
    tot = 0
    for count in S[sp]["size"].values():
        tot += count

    vals = []
    for k in range(3):
        count = S[sp]["size"][k]
        percent = 100 * count / tot
        vals.append(percent)

    positions = []
    for xx in x:
        position = xx + (i - 1) * w
        positions.append(position)

    ax.bar(positions, vals, w, label=sp, color=COL[sp])

ax.set_xticks(list(x))
ax.set_xticklabels(bins)
ax.set_ylabel("% of instances")
ax.set_title("Object-size distribution per split")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/size_dist.png", dpi=140)
plt.close()

# chart 3: condition distribution
# Plot each condition's share of all images within each split.
# Place the split bars side by side and save the chart as cond_dist.png.
fig, ax = plt.subplots(figsize=(6, 4))
conds = ["D", "N", "R", "A"]
condition_names = ["day", "night", "rain", "cloudy"]
x = range(4)
w = 0.26

for i, sp in enumerate(SPLITS):
    tot = S[sp]["images"]

    vals = []
    for c in conds:
        count = S[sp]["cond"].get(c, 0)
        percent = 100 * count / tot
        vals.append(percent)

    positions = []
    for xx in x:
        position = xx + (i - 1) * w
        positions.append(position)

    ax.bar(positions, vals, w, label=sp, color=COL[sp])

ax.set_xticks(list(x))
ax.set_xticklabels(condition_names)
ax.set_ylabel("% of images")
ax.set_title("Condition distribution per split")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/cond_dist.png", dpi=140)
plt.close()


# Print summary statistics for each split
for sp in SPLITS:
    d = S[sp]
    total_objects = 0
    for count in d["size"].values():
        total_objects += count
    size_percentages = []
    for k in range(3):
        percent = 100 * d["size"][k] / total_objects
        size_percentages.append(round(percent))
    objects_per_image = d["instances"] / d["images"]
    print("Split:", sp)
    print("Videos:", d["videos"])
    print("Images:", d["images"])
    print("Instances:", d["instances"])
    print("Instances per image:", round(objects_per_image, 1))
    print("Size S/M/L (%):", size_percentages)
    print()
print("Charts and stats.json saved in:", OUT)
