# -*- coding: utf-8 -*-
"""Figures for Chapter 2 (method, data and tools).

  fig_2_1.png  pipeline that turns the raw IADD into the final dataset
  fig_2_2.png  class distribution per split
  fig_2_3.png  object-size distribution per split
  fig_2_4.png  condition (day / night / rain / other) distribution per split

Figures 2-2 .. 2-4 read stats.json, which compute_v5_validity.py produces
directly from the built dataset, so no number here is typed by hand.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
STATS = os.path.join(OUT, "stats.json")
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "00_قالب_و_آیین‌نامه")))
os.makedirs(OUT, exist_ok=True)

import matplotlib.pyplot as plt                                            # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch             # noqa: E402
from figstyle import (fa, cls, save, legend, grid, CLASS_ORDER,
                      ylabel as _yl, xlabel as _xl,            # noqa: E402
                      SPLIT_COLOR, SPLIT_FA, NAVY, ORANGE, GREEN, RED, PURPLE,
                      TEAL, GREY)

SPLITS = ["train", "val", "test"]


def _grouped(ax, categories, series, ylabel, xlabel=None, fmt="{:.1f}",
             dy=0.6, label_fs=8.5, rot_y=False):
    """grouped bars, value printed on every bar so the chart can be read exactly"""
    n = len(series); w = 0.78 / n
    xs = range(len(categories))
    for i, (split, vals) in enumerate(series):
        off = (i - (n - 1) / 2) * w
        bars = ax.bar([x + off for x in xs], vals, w, color=SPLIT_COLOR[split],
                      label=fa(SPLIT_FA[split]), zorder=3)
        for b, v in zip(bars, vals):
            # dy=None means the axis is logarithmic, where a fixed offset is
            # wrong: scale the value instead so the gap looks the same everywhere
            y = v * 1.12 if dy is None else v + dy
            ax.text(b.get_x() + b.get_width() / 2, y, fmt.format(v),
                    ha="center", va="bottom", fontsize=label_fs, color="#1a1a1a")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([fa(c) for c in categories])
    _yl(ax, ylabel, rotate=rot_y)
    if xlabel:
        _xl(ax, xlabel)
    grid(ax)


# ------------------------------------------------------------------ figure 2-1
def fig_2_1():
    """Six steps on two rows, laid out as a snake: the top row runs left to
    right, drops down on the right-hand side, and the bottom row runs back right
    to left. A single row would be so wide that Word shrinks the picture and the
    text inside the blocks with it; the snake keeps the connector short instead
    of sweeping a long curve across the whole figure."""
    # Grey is what came in and green is what came out; the four steps between
    # them each answer a different fault in the raw data, so each carries its
    # own colour and no two blocks repeat one. Orange is left out of the set:
    # against white text it only reaches 2.7:1.
    # Each block also names the section that explains how that step was done,
    # so a reader can go straight from the diagram to the method.
    top = [("داده خام", GREY, "بخش ۲-۲-۱"),
           ("حذف ویدیوهای تکراری", RED, "بخش ۲-۲-۲-۲"),
           ("حذف ویدیوهای برچسب معیوب", PURPLE, "بخش ۲-۲-۲-۳")]
    # drawn left to right but read right to left, so the list is reversed
    bottom = [("داده نهایی", GREEN, "بخش ۲-۲-۴"),
              ("نمونه‌گیری با حفظ رده‌های نادر", TEAL, "بخش ۲-۲-۳"),
              ("تقسیم در سطح کل ویدیو", NAVY, "بخش‌های ۲-۲-۲-۱ و ۲-۲-۲-۴")]

    W, bw, bh, gap = 10.6, 3.15, 1.15, 0.55
    fig, ax = plt.subplots(figsize=(W, 3.5))
    ax.set_xlim(0, W); ax.set_ylim(0, 3.5); ax.axis("off")

    def draw(row, y):
        total = len(row) * bw + gap * (len(row) - 1)
        x = (W - total) / 2
        spans = []
        for label, col, where in row:
            ax.add_patch(FancyBboxPatch((x, y), bw, bh,
                                        boxstyle="round,pad=0.014,rounding_size=0.06",
                                        fc=col, ec="none", zorder=2))
            ax.text(x + bw / 2, y + bh * 0.60, fa(label), ha="center", va="center",
                    color="white", fontsize=10, weight="bold", zorder=3)
            ax.text(x + bw / 2, y + bh * 0.27, fa(where), ha="center", va="center",
                    color="white", fontsize=9, alpha=0.9, zorder=3)
            spans.append((x, x + bw)); x += bw + gap
        return spans

    def arr(p1, p2, rad=0.0):
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=20,
                                     lw=2.1, color=GREY, zorder=4, shrinkA=0,
                                     shrinkB=0, connectionstyle=f"arc3,rad={rad}"))

    y_top, y_bot = 2.10, 0.50
    st = draw(top, y_top)
    sb = draw(bottom, y_bot)                       # drawn left to right ...

    for (_, x2), (x1, _) in zip(st, st[1:]):       # top row: left to right
        arr((x2 + 0.05, y_top + bh / 2), (x1 - 0.05, y_top + bh / 2))
    for (x1, _), (_, x2) in zip(sb[1:], sb[:-1]):  # ... but read right to left
        arr((x1 - 0.05, y_bot + bh / 2), (x2 + 0.05, y_bot + bh / 2))

    # short drop on the right joins the two rows
    xr = st[-1][1] - bw / 2
    arr((xr, y_top - 0.05), (sb[-1][0] + bw / 2, y_bot + bh + 0.05))

    save(fig, os.path.join(OUT, "fig_2_1.png"))


# ------------------------------------------------------------------ figure 2-2
def fig_2_2(S):
    """One axis, all six classes. car dominates the scale, which is itself the
    point of the figure - the imbalance is the finding. Printing the value on
    every bar keeps the short bars exactly readable despite that scale."""
    share = {sp: [100 * S[sp]["cls"][str(c)] / S[sp]["instances"]
                  for c in range(6)] for sp in SPLITS}

    fig, ax = plt.subplots(figsize=(11.0, 5.0))
    _grouped(ax, CLASS_ORDER, [(sp, share[sp]) for sp in SPLITS],
             "درصد از نمونه‌های هر بخش", xlabel="رده شیء",
             fmt="{:.2f}", dy=None, label_fs=8.5, rot_y=True)
    ax.set_xticklabels([cls(c) for c in CLASS_ORDER])
    ax.set_yscale("log")                 # shares span two orders of magnitude
    ax.set_ylim(0.35, 170)
    ax.set_yticks([0.5, 1, 5, 10, 50, 100])
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    legend(ax, ncol=3, outside="below", y=-0.24)
    save(fig, os.path.join(OUT, "fig_2_2.png"))


# ------------------------------------------------------------------ figure 2-3
def fig_2_3(S):
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bins = ["کوچک\n(کمتر از ٪۱)", "متوسط\n(٪۱ تا ٪۶)", "بزرگ\n(بیش از ٪۶)"]
    series = []
    for sp in SPLITS:
        tot = sum(S[sp]["size"].values())
        series.append((sp, [100 * S[sp]["size"][str(k)] / tot for k in range(3)]))
    _grouped(ax, bins, series, "درصد از نمونه‌ها", xlabel="اندازه شیء", dy=1.2)
    ax.set_ylim(0, 84)
    legend(ax, ncol=3, outside="below", y=-0.26)
    save(fig, os.path.join(OUT, "fig_2_3.png"))


# ------------------------------------------------------------------ figure 2-4
def fig_2_4(S):
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    conds, names = ["D", "N", "R", "A"], ["روز آفتابی", "شب", "باران", "روز ابری"]
    series = [(sp, [100 * S[sp]["cond"].get(c, 0) / S[sp]["images"] for c in conds])
              for sp in SPLITS]
    _grouped(ax, names, series, "درصد از تصاویر هر بخش",
             xlabel="شرایط محیطی", dy=None, rot_y=True)
    ax.set_yscale("log")
    ax.set_ylim(0.35, 170)
    ax.set_yticks([0.5, 1, 5, 10, 50, 100])
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    legend(ax, ncol=3, outside="below", y=-0.22)
    save(fig, os.path.join(OUT, "fig_2_4.png"))


if __name__ == "__main__":
    S = json.load(open(STATS, encoding="utf-8"))
    fig_2_1(); fig_2_2(S); fig_2_3(S); fig_2_4(S)
    print("saved fig_2_1.png .. fig_2_4.png")
