"""Rendering GT labels on frames of the worst-scoring videos (per pervideo_run5.csv)
so they can be visually judged as broken-labels vs just-hard"""
import os, glob
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

CSV    = r"D:\projects\car-detection-yolo\pervideo_run5.csv"
DS     = r"D:\projects\car-detection-yolo\dataset\iadd_subset_v4"
OUT    = r"D:\projects\car-detection-yolo\docs\dataset\dataset_label_evidence"
NAMES  = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]
COL    = [(255,60,60), (60,200,60), (70,130,255), (255,160,0), (180,70,220), (0,200,200)]
THRESH = 0.63     # review every video below this mAP50
NFRAMES = 10       # sample frames per video
THUMB  = 760      # thumbnail width (space-saving)

os.makedirs(OUT, exist_ok=True)
try:
    F  = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
    FC = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
except Exception:
    F = FC = ImageFont.load_default()


def read_labels(txt):
    out = []
    if os.path.exists(txt):
        for line in open(txt):
            q = line.split()
            if len(q) == 5:
                out.append((int(q[0]), *map(float, q[1:])))
    return out

# Generating class bounding box, class name and caption
def render(stem, split, caption):
    ip = f"{DS}/images/{split}/{stem}.jpg"
    if not os.path.exists(ip):
        return None
    im = Image.open(ip).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    for c, cx, cy, w, h in read_labels(f"{DS}/labels/{split}/{stem}.txt"):
        x1, y1, x2, y2 = (cx-w/2)*W, (cy-h/2)*H, (cx+w/2)*W, (cy+h/2)*H
        d.rectangle([x1, y1, x2, y2], outline=COL[c], width=3)
        d.text((x1+2, max(0, y1-16)), NAMES[c], fill=COL[c], font=F)
    d.rectangle([0, 0, W, 30], fill=(0, 0, 0))
    d.text((6, 4), caption, fill=(255, 255, 255), font=FC)
    im.thumbnail((THUMB, THUMB))
    return im


df = pd.read_csv(CSV)
sus = df[df.mAP50 < THRESH].sort_values("mAP50")
print(f"suspicious videos (mAP50 < {THRESH}): {len(sus)}")

rows = []
for _, r in sus.iterrows():
    vid, split = r.video, r.split
    paths = sorted(glob.glob(f"{DS}/images/{split}/{vid}__*.jpg"))
    if not paths:
        continue
    if len(paths) >= NFRAMES:
        idx = [int(i * (len(paths)-1) / (NFRAMES-1)) for i in range(NFRAMES)]
    else:
        idx = list(range(len(paths)))
    vdir = os.path.join(OUT, f"{split}_{vid}_mAP{r.mAP50:.3f}")
    os.makedirs(vdir, exist_ok=True)
    cap = f"{vid} | {r.cond} | mAP50={r.mAP50:.3f} | inst={int(r.instances)}"
    saved = 0
    for j in idx:
        stem = os.path.basename(paths[j])[:-4]
        im = render(stem, split, cap)
        if im:
            im.save(os.path.join(vdir, f"{stem}.jpg"), quality=80)
            saved += 1
    rows.append({"split": split, "video": vid, "cond": r.cond, "images": int(r.images),
                 "instances": int(r.instances), "mAP50": r.mAP50,
                 "frames_saved": saved, "verdict": "REVIEW"})
    print(f"  {split:5} {vid:<15} mAP50={r.mAP50:.3f}  -> {saved} frames")

summ = pd.DataFrame(rows)
summ.to_csv(os.path.join(OUT, "SUMMARY.csv"), index=False)
print("\nsaved evidence to", OUT)
print("summary ->", os.path.join(OUT, "SUMMARY.csv"))
