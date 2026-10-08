"""Count original IADD files and draw Chapter-2-style charts. No files are changed."""
import os
import glob
import json
import csv
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figstyle import fa, save, legend, grid, CLASS_FA, CLASS_ORDER, SPLIT_COLOR, SPLIT_FA
from figstyle import ylabel, xlabel

DS = r"D:\projects\car-detection-yolo\dataset\IADD"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iadd_validity")
FOLDERS = {
    "train": ["train_part1", "train_part2", "train_part3"],
    "val": ["val"],
    "test": ["test"]
}
SPLITS = ["train", "val", "test"]
SMALL, LARGE = 0.01, 0.06


def analyze(split):
    imgs = []
    for folder in FOLDERS[split]:
        imgs.extend(glob.glob(os.path.join(DS, folder, "Record*", "*.jpg")))

    vids = set()
    classes = Counter()
    size = Counter()
    cond = Counter()
    instances = 0
    labeled = 0
    missing = 0
    invalid = 0
    empty = 0

    for image in imgs:
        record = os.path.basename(os.path.dirname(image))
        vids.add(record)
        cond[record.split("_")[-1]] += 1
        label = os.path.splitext(image)[0] + ".txt"
        if not os.path.exists(label):
            missing += 1
            continue

        labeled += 1
        valid_objects = 0
        with open(label, encoding="utf-8-sig") as f:
            for line in f:
                q = line.split()
                if not q:
                    continue
                if len(q) != 5:
                    invalid += 1
                    continue
                try:
                    class_id = int(q[0])
                    cx, cy, width, height = map(float, q[1:])
                    if class_id not in range(6) or not (0 <= cx <= 1 and 0 <= cy <= 1 and 0 < width <= 1 and 0 < height <= 1):
                        invalid += 1
                        continue
                except ValueError:
                    invalid += 1
                    continue

                instances += 1
                valid_objects += 1
                classes[class_id] += 1
                area = width * height
                if area < SMALL:
                    size[0] += 1
                elif area >= LARGE:
                    size[2] += 1
                else:
                    size[1] += 1
        if valid_objects == 0:
            empty += 1

    class_counts = {}
    for c in range(6):
        class_counts[c] = classes.get(c, 0)
    size_counts = {}
    for k in range(3):
        size_counts[k] = size.get(k, 0)

    return {"images": len(imgs), "videos": len(vids), "instances": instances,
            "cls": class_counts, "size": size_counts, "cond": dict(cond),
            "labeled_images": labeled, "missing_labels": missing,
            "empty_or_no_valid_objects": empty, "invalid_lines": invalid,
            "records": sorted(vids)}


def grouped(categories, series, ytext, xtext, filename, log=False):
    fig, ax = plt.subplots(figsize=(11, 5))
    w = 0.78 / len(series)
    xs = range(len(categories))
    positive = []
    for i, (split, vals) in enumerate(series):
        positions = []
        for x in xs:
            positions.append(x + (i - (len(series) - 1) / 2) * w)
        bars = ax.bar(positions, vals, w, color=SPLIT_COLOR[split],
                      label=fa(SPLIT_FA[split]), zorder=3)
        for b, v in zip(bars, vals):
            if v > 0:
                positive.append(v)
            if log and v == 0:
                continue
            y = v * 1.12 if log else v + 1.2
            ax.text(b.get_x() + b.get_width() / 2, y, f"{v:.2f}",
                    ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([fa(c) for c in categories])
    ylabel(ax, ytext, rotate=True)
    xlabel(ax, xtext)
    grid(ax)
    if log:
        ax.set_yscale("log")
        lower = min(0.35, min(positive) / 2)
        ax.set_ylim(lower, 170)
        ticks = [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100]
        ax.set_yticks([v for v in ticks if v >= lower])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    else:
        ax.set_ylim(0, max(positive) + 12)
    legend(ax, ncol=len(series), outside="below", y=-0.24)
    save(fig, os.path.join(OUT, filename))


def main():
    os.makedirs(OUT, exist_ok=True)
    S = {}
    for split in SPLITS:
        print("Reading", split, "...", flush=True)
        S[split] = analyze(split)
        print(split, S[split]["images"], "images;", S[split]["instances"], "objects", flush=True)

    with open(os.path.join(OUT, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(S, f, indent=2)

    labeled_splits = []
    for split in SPLITS:
        if S[split]["instances"] > 0:
            labeled_splits.append(split)

    series = []
    for split in labeled_splits:
        vals = []
        for c in range(6):
            vals.append(100 * S[split]["cls"][c] / S[split]["instances"])
        series.append((split, vals))
    if series:
        grouped([CLASS_FA[c] for c in CLASS_ORDER], series, "درصد از نمونه‌های برچسب‌خورده هر بخش",
                "رده شیء", "class_dist.png", log=True)

    series = []
    for split in labeled_splits:
        vals = []
        for k in range(3):
            vals.append(100 * S[split]["size"][k] / S[split]["instances"])
        series.append((split, vals))
    if series:
        grouped(["کوچک\n(کمتر از ۱٪)", "متوسط\n(۱٪ تا کمتر از ۶٪)", "بزرگ\n(۶٪ و بیشتر)"],
                series, "درصد از نمونه‌های برچسب‌خورده", "اندازه شیء", "size_dist.png")

    series = []
    for split in SPLITS:
        if S[split]["images"] == 0:
            continue
        vals = []
        for c in ["D", "N", "R", "A"]:
            vals.append(100 * S[split]["cond"].get(c, 0) / S[split]["images"])
        series.append((split, vals))
    grouped(["روز", "شب", "باران", "ابری"], series,
            "درصد از تصاویر هر بخش", "شرایط محیطی", "cond_dist.png", log=True)

    counts = Counter()
    all_records = set()
    total_images = 0
    for split in SPLITS:
        counts.update(S[split]["cond"])
        all_records.update(S[split]["records"])
        total_images += S[split]["images"]

    with open(os.path.join(OUT, "summary.csv"), "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["split", "videos", "images", "labeled_images", "missing_labels",
                         "instances", "instances_per_labeled_image", "invalid_lines"])
        for split in SPLITS:
            d = S[split]
            average = round(d["instances"] / d["labeled_images"], 2) if d["labeled_images"] else ""
            writer.writerow([split, d["videos"], d["images"], d["labeled_images"],
                             d["missing_labels"], d["instances"], average, d["invalid_lines"]])

    with open(os.path.join(OUT, "conditions.csv"), "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["condition", "train", "val", "test", "total", "percent_of_all_images"])
        for c in ["D", "N", "R", "A"]:
            writer.writerow([c, S["train"]["cond"].get(c, 0), S["val"]["cond"].get(c, 0),
                             S["test"]["cond"].get(c, 0), counts[c], round(100 * counts[c] / total_images, 2)])

    print("Unique record folder names:", len(all_records))
    print("Total images:", total_images)
    print("Saved in:", OUT)


if __name__ == "__main__":
    main()
