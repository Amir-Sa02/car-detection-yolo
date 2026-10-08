# -*- coding: utf-8 -*-
"""Figures for Chapter 1 (literature review and theory).

  fig_1_1.png  two-stage versus one-stage detector pipelines
  fig_1_2.png  YOLOv11 architecture: backbone / neck / head
  fig_1_3.png  IoU concept at three degrees of overlap

Drawing style (font, palette, Persian shaping) comes from figstyle so every
figure in the thesis matches.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "00_قالب_و_آیین‌نامه")))
os.makedirs(OUT, exist_ok=True)

import matplotlib.pyplot as plt                                          # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402
from figstyle import (fa, save, legend, NAVY, ORANGE, GREEN, RED,         # noqa: E402
                      PURPLE, TEAL, GREY)

BOX_FS = 10          # text inside a block
ARROW_LW = 2.2       # arrows must read clearly at print size
ARROW_MS = 22


def block(ax, x, y, w, h, text, fc, fs=BOX_FS):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.04",
                                fc=fc, ec="none", zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            color="white", fontsize=fs, weight="bold", zorder=3)
    return x, y, w, h


def arrow(ax, p1, p2, color=GREY):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>",
                                 mutation_scale=ARROW_MS, lw=ARROW_LW,
                                 color=color, zorder=4,
                                 shrinkA=0, shrinkB=0))


def flow(ax, steps, y, h, width, gap=0.72, color_arrow=GREY):
    """lay the blocks left to right, centred inside `width`, with a gap wide
    enough that the arrow between two blocks is clearly visible"""
    total = sum(w for _, _, w in steps) + gap * (len(steps) - 1)
    x = (width - total) / 2
    spans = []
    for text, fc, w in steps:
        block(ax, x, y, w, h, text, fc)
        spans.append((x, x + w)); x += w + gap
    for (_, x2), (x1, _) in zip(spans, spans[1:]):
        arrow(ax, (x2 + 0.05, y + h / 2), (x1 - 0.05, y + h / 2), color_arrow)
    return spans


# ------------------------------------------------------------------ figure 1-1
def fig_1_1():
    W = 12.8
    fig, ax = plt.subplots(figsize=(W, 4.9))
    ax.set_xlim(0, W); ax.set_ylim(0, 4.9); ax.axis("off")

    # --- (a) two-stage -------------------------------------------------
    ax.text(W / 2, 4.52, fa("الف) روش دومرحله‌ای"), ha="center", fontsize=13,
            weight="bold", color=NAVY)
    spans_a = flow(ax, [(fa("تصویر ورودی"), GREY, 1.80),
                        (fa("استخراج ویژگی"), NAVY, 1.95),
                        (fa("پیشنهاد ناحیه"), ORANGE, 1.95),
                        (fa("طبقه‌بندی و" + chr(10) + "بازگردانی کادر"), TEAL, 2.10),
                        (fa("خروجی"), GREEN, 1.40)],
                   y=3.28, h=0.92, width=W)

    # brace under the two stages, each spanning exactly its own blocks
    for (i, j), label, col in (((1, 2), "مرحله اول", ORANGE),
                               ((3, 3), "مرحله دوم", TEAL)):
        x1, x2 = spans_a[i][0], spans_a[j][1]
        ax.plot([x1, x2], [3.12, 3.12], color=col, lw=1.2)
        ax.text((x1 + x2) / 2, 2.86, fa(label), ha="center", fontsize=10, color=col)

    # --- (b) one-stage -------------------------------------------------
    ax.text(W / 2, 2.22, fa("ب) روش یک‌مرحله‌ای"), ha="center", fontsize=13,
            weight="bold", color=GREEN)
    spans_b = flow(ax, [(fa("تصویر ورودی"), GREY, 1.80),
                        (fa("استخراج ویژگی"), NAVY, 2.35),
                        (fa("پیش‌بینی هم‌زمان کادر و رده"), TEAL, 3.95),
                        (fa("خروجی"), GREEN, 1.40)],
                   y=0.98, h=0.92, width=W)
    x1, x2 = spans_b[1][0], spans_b[2][1]
    ax.plot([x1, x2], [0.82, 0.82], color=TEAL, lw=1.2)
    ax.text((x1 + x2) / 2, 0.56, fa("یک گذر رو به جلو"), ha="center",
            fontsize=10, color=TEAL)

    save(fig, os.path.join(OUT, "fig_1_1.png"))


# ------------------------------------------------------------------ figure 1-2
def fig_1_2():
    """YOLOv11 architecture, taken unchanged from reference [13].

    Sapkota et al. (2025) is open access under CC BY 4.0, so the diagram may be
    reproduced with attribution. Only two things are removed: the English title
    banner, which the Persian caption replaces, and the right-hand panel listing
    tasks this thesis does not use (segmentation, pose, OBB, classification).
    Nothing inside the diagram itself is altered.
    """
    import fitz
    from PIL import Image

    src = os.path.normpath(os.path.join(
        HERE, "..", "..", "مراجع",
        "Sapkota 2025 - YOLO Decadal Comprehensive Review.pdf"))
    doc = fitz.open(src)
    raw = doc.extract_image(475)["image"]          # single raster on page 19
    im = Image.open(io.BytesIO(raw)).convert("RGB")

    im.paste((255, 255, 255), (500, 0, 896, 33))   # the "YOLO11 Architecture" banner
    im = im.crop((0, 0, 1134, im.size[1]))         # stop just past the Head box
    im.save(os.path.join(OUT, "fig_1_2.png"))


def fig_1_3():
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))

    def panel(ax, dx, caption, col):
        ax.set_xlim(0, 10); ax.set_ylim(0, 8.6); ax.axis("off"); ax.set_aspect("equal")
        gt = Rectangle((2.0, 2.2), 4.0, 4.0, fill=False, ec=GREEN, lw=2.6, zorder=3)
        pr = Rectangle((2.0 + dx, 2.2), 4.0, 4.0, fill=False, ec=ORANGE, lw=2.6,
                       ls=(0, (5, 3)), zorder=3)
        ax.add_patch(gt); ax.add_patch(pr)
        x1, x2 = max(2.0, 2.0 + dx), min(6.0, 6.0 + dx)
        inter = max(0.0, x2 - x1) * 4.0
        if x2 > x1:
            ax.add_patch(Rectangle((x1, 2.2), x2 - x1, 4.0, fc=NAVY, alpha=0.22,
                                   ec="none", zorder=2))
        iou = inter / (2 * 16.0 - inter)
        ax.text(5.0, 7.55, f"IoU = {iou:.2f}", ha="center", fontsize=14,
                weight="bold", color=col)
        ax.text(5.0, 0.85, fa(caption), ha="center", fontsize=11, color=col)

    panel(axes[0], 3.2, "انطباق ضعیف — رد می‌شود", RED)
    panel(axes[1], 1.6, "انطباق مرزی", ORANGE)
    panel(axes[2], 0.5, "انطباق خوب — پذیرفته می‌شود", GREEN)

    axes[1].plot([], [], color=GREEN, lw=2.6, label=fa("کادر واقعی"))
    axes[1].plot([], [], color=ORANGE, lw=2.6, ls=(0, (5, 3)),
                 label=fa("کادر پیش‌بینی‌شده"))
    axes[1].add_patch(Rectangle((0, 0), 0, 0, fc=NAVY, alpha=0.22,
                                label=fa("ناحیه اشتراک")))
    legend(axes[1], ncol=3, fontsize=11,
           loc="upper center", bbox_to_anchor=(0.5, -0.02))

    save(fig, os.path.join(OUT, "fig_1_3.png"))


if __name__ == "__main__":
    fig_1_1(); fig_1_2(); fig_1_3()
    print("saved fig_1_1.png, fig_1_2.png, fig_1_3.png")
