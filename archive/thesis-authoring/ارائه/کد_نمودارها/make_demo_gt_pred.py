# -*- coding: utf-8 -*-
"""Rebuild the demo images with clean annotations where EVERY box is labelled.

Outputs into 'thesis figures':
  demo_gt/          ground-truth boxes + class name
  demo_pred_clean/  predictions + class name and confidence
  demo_pairs/       side-by-side GT | Prediction
  demo_contact_sheet_pairs.jpg

Anti-clutter strategy (no label is ever dropped):
  - per-class colours, thin 2px boxes
  - font size scales down for small boxes
  - 8 candidate positions around/inside each box
  - if all are taken, the label is moved to nearby free space and joined to
    its box with a thin leader line
"""
import os, glob
from PIL import Image, ImageDraw, ImageFont

BASE = r"D:\projects\car-detection-yolo"
FIGS = os.path.join(BASE, r"colab\runs\run8\thesis figures")
GTDIR = os.path.join(FIGS, "demo_gt")
TEST_IMG = os.path.join(BASE, r"dataset\iadd_subset_v5\images\test")
TEST_LBL = os.path.join(BASE, r"dataset\iadd_subset_v5\labels\test")
WEIGHTS = os.path.join(BASE, r"colab\runs\run8\run8\weights\best.pt")

NAMES = {0: "person", 1: "car", 2: "motorcycle", 3: "bus", 4: "truck", 5: "traffic_light"}
COLORS = {0: (230, 60, 60), 1: (0, 140, 255), 2: (60, 200, 60),
          3: (255, 170, 0), 4: (180, 90, 255), 5: (0, 205, 205)}
LINE_W = 2
SMALL_BOX = 70          # boxes narrower than this get the small font


def _font(px):
    for path in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(path, px)
        except Exception:
            continue
    return ImageFont.load_default()


F_BIG, F_SMALL = _font(14), _font(10)


def text_wh(d, s, f):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    return r - l, b - t


def hit(a, b):
    return not (a[2] <= b[0] or a[0] >= b[2] or a[3] <= b[1] or a[1] >= b[3])


def free(rect, placed, W, H):
    if rect[0] < 0 or rect[1] < 0 or rect[2] > W or rect[3] > H:
        return False
    return not any(hit(rect, p) for p in placed)


def draw_boxes(img, boxes):
    """boxes: (cls, x1, y1, x2, y2, text). Every box gets its label."""
    d = ImageDraw.Draw(img)
    W, H = img.size
    placed = []
    # big boxes first so they claim the natural spots
    boxes = sorted(boxes, key=lambda b: (b[3] - b[1]) * (b[4] - b[2]), reverse=True)

    for cls, x1, y1, x2, y2, text in boxes:
        col = COLORS[cls]
        d.rectangle([x1, y1, x2, y2], outline=col, width=LINE_W)

        f = F_SMALL if (x2 - x1) < SMALL_BOX else F_BIG
        tw, th = text_wh(d, text, f)
        pad = 2
        bw, bh = tw + 2 * pad, th + 2 * pad

        cands = [
            (x1, y1 - bh - 1),            # above-left
            (x2 - bw, y1 - bh - 1),       # above-right
            (x1, y2 + 1),                 # below-left
            (x2 - bw, y2 + 1),            # below-right
            (x1 + LINE_W, y1 + LINE_W),   # inside top-left
            (x1 + LINE_W, y2 - bh - LINE_W),  # inside bottom-left
            (x2 + 2, y1),                 # right of box
            (x1 - bw - 2, y1),            # left of box
        ]
        rect = None
        for cx, cy in cands:
            r = (cx, cy, cx + bw, cy + bh)
            if free(r, placed, W, H):
                rect = r
                break

        leader = False
        if rect is None:                  # crowded: find nearby free space, use a leader line
            cx0, cy0 = x1, y1
            for radius in range(12, 170, 10):
                for dx, dy in ((0, -radius), (0, radius), (-radius, 0), (radius, 0),
                               (-radius, -radius), (radius, -radius),
                               (-radius, radius), (radius, radius)):
                    r = (cx0 + dx, cy0 + dy, cx0 + dx + bw, cy0 + dy + bh)
                    if free(r, placed, W, H):
                        rect = r
                        leader = True
                        break
                if rect:
                    break
        if rect is None:                  # last resort: clamp inside the frame
            rect = (min(max(x1, 0), W - bw), min(max(y1 - bh - 1, 0), H - bh))
            rect = (rect[0], rect[1], rect[0] + bw, rect[1] + bh)
            leader = True

        if leader:                        # thin line from label to the box corner
            lx = rect[0] + bw / 2
            ly = rect[1] + bh / 2
            tx = min(max(lx, x1), x2)
            ty = min(max(ly, y1), y2)
            d.line([lx, ly, tx, ty], fill=col, width=1)

        placed.append(rect)
        d.rectangle(rect, fill=col)
        lum = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
        d.text((rect[0] + pad, rect[1] + pad), text, font=f,
               fill=(0, 0, 0) if lum > 150 else (255, 255, 255))
    return img


def header(img, label):
    W = img.size[0]
    strip = Image.new("RGB", (W, 26), (30, 30, 30))
    d = ImageDraw.Draw(strip)
    tw, th = text_wh(d, label, F_BIG)
    d.text(((W - tw) // 2, (26 - th) // 2 - 2), label, font=F_BIG, fill=(255, 255, 255))
    out = Image.new("RGB", (W, img.size[1] + 26), (30, 30, 30))
    out.paste(strip, (0, 0)); out.paste(img, (0, 26))
    return out


def main():
    # the 16 selected frames, recovered from the existing demo_gt filenames
    stems = []
    for p in sorted(glob.glob(os.path.join(GTDIR, "*.jpg"))):
        n = os.path.basename(p)                       # {cond}_gt_{stem}.jpg
        cond = n.split("_", 1)[0]
        stem = os.path.splitext(n.split("_gt_", 1)[1])[0]
        stems.append((cond, stem))
    print(f"{len(stems)} frames")

    for sub in ("demo_gt", "demo_pred_clean", "demo_pairs"):
        os.makedirs(os.path.join(FIGS, sub), exist_ok=True)

    from ultralytics import YOLO
    model = YOLO(WEIGHTS)

    pairs = []
    for cond, stem in stems:
        src = os.path.join(TEST_IMG, stem + ".jpg")
        if not os.path.exists(src):
            print("MISSING:", stem); continue

        gt_img = Image.open(src).convert("RGB")
        W, H = gt_img.size
        gt_boxes = []
        lbl = os.path.join(TEST_LBL, stem + ".txt")
        if os.path.exists(lbl):
            for line in open(lbl):
                q = line.split()
                if len(q) == 5:
                    c = int(q[0]); xc, yc, bw, bh = map(float, q[1:])
                    gt_boxes.append((c, (xc - bw / 2) * W, (yc - bh / 2) * H,
                                     (xc + bw / 2) * W, (yc + bh / 2) * H, NAMES[c]))
        gt_img = draw_boxes(gt_img, gt_boxes)
        gt_img.save(os.path.join(FIGS, "demo_gt", f"{cond}_gt_{stem}.jpg"), quality=92)

        pr_img = Image.open(src).convert("RGB")
        r = model.predict(src, imgsz=1280, conf=0.35, verbose=False)[0]
        pr_boxes = []
        if r.boxes is not None:
            for b in r.boxes:
                c = int(b.cls); x1, y1, x2, y2 = b.xyxy[0].tolist()
                pr_boxes.append((c, x1, y1, x2, y2, f"{NAMES[c]} {float(b.conf):.0%}"))
        pr_img = draw_boxes(pr_img, pr_boxes)
        pr_img.save(os.path.join(FIGS, "demo_pred_clean", f"{cond}_pred_{stem}.jpg"), quality=92)

        g = header(gt_img.copy(), "Ground Truth")
        p = header(pr_img.copy(), "Prediction")
        pair = Image.new("RGB", (g.size[0] * 2 + 6, g.size[1]), (255, 255, 255))
        pair.paste(g, (0, 0)); pair.paste(p, (g.size[0] + 6, 0))
        out = os.path.join(FIGS, "demo_pairs", f"{cond}_pair_{stem}.jpg")
        pair.save(out, quality=90); pairs.append(out)
        print(f"done: {stem}  (gt {len(gt_boxes)} / pred {len(pr_boxes)})")

    if pairs:
        pw, ph = 960, 296
        cols = 2; rows = (len(pairs) + cols - 1) // cols
        sheet = Image.new("RGB", (pw * cols + 12, (ph + 6) * rows), (255, 255, 255))
        for k, pp in enumerate(pairs):
            sheet.paste(Image.open(pp).resize((pw, ph)),
                        ((k % cols) * (pw + 12), (k // cols) * (ph + 6)))
        sheet.save(os.path.join(FIGS, "demo_contact_sheet_pairs.jpg"), quality=88)

    old = os.path.join(FIGS, "demo_contact_sheet.jpg")     # stale car-heavy sheet
    if os.path.exists(old):
        os.remove(old); print("removed stale demo_contact_sheet.jpg")
    print("ALL DONE ->", FIGS)


if __name__ == "__main__":
    main()
