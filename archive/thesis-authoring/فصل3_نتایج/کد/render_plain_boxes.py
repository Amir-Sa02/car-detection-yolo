# -*- coding: utf-8 -*-
"""Render the demo frames with coloured boxes and the confidence of each one.

Class identity is still carried by the colour legend under the figure, so the
only text on a frame is the confidence: the one thing a reader cannot infer from
the picture. It is drawn on a filled chip in the box colour so it stays legible
over any background, and sized from the frame height so it survives the
reduction to page width. Run once; results are cached in demo_pred_plain/.
"""
import os, glob
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FIG = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
OUT = os.path.join(FIG, "demo_pred_plain")
WEIGHTS = os.path.join(ROOT, "colab", "runs", "run8", "run8", "weights", "best.pt")
TEST = os.path.join(ROOT, "dataset", "iadd_subset_v5", "images", "test")
os.makedirs(OUT, exist_ok=True)

COLORS = {0: (230, 60, 60), 1: (0, 140, 255), 2: (60, 200, 60),
          3: (255, 170, 0), 4: (180, 90, 255), 5: (0, 205, 205)}

def _font(size):
    for name in ("arialbd.ttf", "tahomabd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


from ultralytics import YOLO

model = YOLO(WEIGHTS)

# the same frames the detailed comparison uses, so both figures agree
stems = []
for p in sorted(glob.glob(os.path.join(FIG, "demo_gt", "*.jpg"))):
    n = os.path.basename(p)
    stems.append((n.split("_", 1)[0], os.path.splitext(n.split("_gt_", 1)[1])[0]))

for cond, stem in stems:
    src = os.path.join(TEST, stem + ".jpg")
    if not os.path.exists(src):
        continue
    im = Image.open(src).convert("RGB")
    r = model.predict(src, imgsz=1280, conf=0.35, verbose=False)[0]
    d = ImageDraw.Draw(im)
    font = _font(max(20, im.height // 26))
    if r.boxes is not None:
        for b in r.boxes:
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            colour = COLORS[int(b.cls)]
            d.rectangle([x1, y1, x2, y2], outline=colour, width=4)
            txt = f"{round(float(b.conf) * 100)}%"
            tw, th = d.textbbox((0, 0), txt, font=font)[2:]
            pad = 3
            # the chip sits above the box, or just inside it when the box is at
            # the top edge of the frame
            ty = y1 - th - 2 * pad
            if ty < 0:
                ty = y1
            d.rectangle([x1, ty, x1 + tw + 2 * pad, ty + th + 2 * pad], fill=colour)
            d.text((x1 + pad, ty + pad), txt, fill=(255, 255, 255), font=font)
    im.save(os.path.join(OUT, f"{cond}_{stem}.jpg"), quality=92)
    print("drew", stem)

print("done ->", OUT)
