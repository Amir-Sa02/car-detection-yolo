"""Figures for Chapter 2 (method, data and tools).

  fig_2_2.png  class distribution per split
  fig_2_3.png  object-size distribution per split
  fig_2_4.png  condition (day / night / rain / other) distribution per split

Figures 2-2 .. 2-4 read stats.json, which compute_v5_validity.py produces
directly from the built dataset.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
STATS = os.path.join(OUT, "stats.json")
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "00_قالب_و_آیین‌نامه")))
os.makedirs(OUT, exist_ok=True)

import matplotlib.pyplot as plt
from figstyle import (fa, cls, save, legend, grid, CLASS_ORDER, ylabel as _yl, xlabel as _xl, SPLIT_COLOR, SPLIT_FA)
SPLITS = ["train", "val", "test"]

# draws grouped bar chart with labels above each bar
def _grouped(ax, categories, series, ylabel, xlabel=None, fmt="{:.1f}", dy=0.6, label_fs=8.5, rot_y=False):
    n = len(series)
    w = 0.78 / n
    xs = range(len(categories))  # x-coordinates of the bars
    for i, (split, vals) in enumerate(series):
        off = (i - (n - 1) / 2) * w  # offset for the bars of this split
        bars = ax.bar([x + off for x in xs], vals, w, color=SPLIT_COLOR[split], label=fa(SPLIT_FA[split]), zorder=3)
        for b, v in zip(bars, vals):
            y = v * 1.12 if dy is None else v + dy  # vertical position for the label
            ax.text(b.get_x() + b.get_width() / 2, y, fmt.format(v), ha="center", va="bottom", fontsize=label_fs, color="#1a1a1a")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([fa(c) for c in categories])
    _yl(ax, ylabel, rotate=rot_y)
    if xlabel:
        _xl(ax, xlabel)
    grid(ax)


# figure 2-2
def fig_2_2(S):
    share = {}
    for sp in SPLITS:
        percentages = []
        total = S[sp]["instances"]
        for c in range(6):
            count = S[sp]["cls"][str(c)]
            percent = 100 * count / total
            percentages.append(percent)
        share[sp] = percentages

    series = []
    for sp in SPLITS:
        series.append((sp, share[sp]))
    fig, ax = plt.subplots(figsize=(11.0, 5.0))

    _grouped(
        ax,
        CLASS_ORDER,
        series,
        "درصد از نمونه‌های هر بخش",
        xlabel="رده شیء",
        fmt="{:.2f}",  # format string for the percentage labels above each bar
        dy=None,       # vertical offset for the percentage labels above each bar (for logarithmic scale)
        label_fs=8.5,  # font size for the percentage labels above each bar
        rot_y=True     # rotate the y-axis label to be vertical
    )

    class_names = []
    for c in CLASS_ORDER:
        class_names.append(cls(c))
    ax.set_xticklabels(class_names)
    ax.set_yscale("log")
    ax.set_ylim(0.35, 170)
    ax.set_yticks([0.5, 1, 5, 10, 50, 100])

    # Format the y-axis tick labels to remove trailing zeros and decimal points
    def format_tick(value, position):
        return f"{value:g}"

    formatter = plt.FuncFormatter(format_tick)
    ax.get_yaxis().set_major_formatter(formatter)
    legend(ax, ncol=3, outside="below", y=-0.24)
    output_path = os.path.join(OUT, "fig_2_2.png")
    save(fig, output_path)


# figure 2-3
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


# figure 2-4
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
    fig_2_2(S)
    fig_2_3(S)
    fig_2_4(S)
    print("saved fig_2_2.png .. fig_2_4.png")
