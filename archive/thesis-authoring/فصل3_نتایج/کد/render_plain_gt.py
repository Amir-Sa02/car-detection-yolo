# -*- coding: utf-8 -*-
"""Render the demo frames with the ground-truth boxes only - no text.

The comparison figures put ground truth beside the prediction, so both sides
must be drawn identically: same colours, same line width, no baked-in text.
demo_pred_plain/ already holds the prediction side; this produces the matching
ground-truth side from the label files, so no model is needed. Run once.
"""
import os, glob
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FIG = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
OUT = os.path.join(FIG, "demo_gt_plain")
TEST_IMG = os.path.join(ROOT, "dataset", "iadd_subset_v5", "images", "test")
TEST_LBL = os.path.join(ROOT, "dataset", "iadd_subset_v5", "labels", "test")
os.makedirs(OUT, exist_ok=True)

COLORS = {0: (230, 60, 60), 1: (0, 140, 255), 2: (60, 200, 60),
          3: (255, 170, 0), 4: (180, 90, 255), 5: (0, 205, 205)}

# the same frames the prediction side uses, so the two grids line up
stems = []
for p in sorted(glob.glob(os.path.join(FIG, "demo_gt", "*.jpg"))):
    n = os.path.basename(p)
    stems.append((n.split("_", 1)[0], os.path.splitext(n.split("_gt_", 1)[1])[0]))

for cond, stem in stems:
    src = os.path.join(TEST_IMG, stem + ".jpg")
    lbl = os.path.join(TEST_LBL, stem + ".txt")
    if not (os.path.exists(src) and os.path.exists(lbl)):
        continue
    im = Image.open(src).convert("RGB")
    d = ImageDraw.Draw(im)
    n = 0
    for line in open(lbl):
        q = line.split()
        if len(q) != 5:
            continue
        c, xc, yc, bw, bh = int(q[0]), *map(float, q[1:])
        x1, y1 = (xc - bw / 2) * im.width, (yc - bh / 2) * im.height
        x2, y2 = (xc + bw / 2) * im.width, (yc + bh / 2) * im.height
        d.rectangle([x1, y1, x2, y2], outline=COLORS[c], width=4)
        n += 1
    im.save(os.path.join(OUT, f"{cond}_{stem}.jpg"), quality=92)
    print("drew", n, "boxes ->", stem)

print("done ->", OUT)
