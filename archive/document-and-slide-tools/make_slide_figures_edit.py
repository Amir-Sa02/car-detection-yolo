# -*- coding: utf-8 -*-
"""Figures that exist only for the defence slides.

The thesis already owns every result plot; what it does not own is a single
picture of how the project moved from the first run to the last one, and why
the highest number on that chart is the one that was thrown away.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "00_قالب_و_آیین‌نامه")))
os.makedirs(OUT, exist_ok=True)

import matplotlib.pyplot as plt                                        # noqa: E402
from figstyle import fa, save, GREY                                    # noqa: E402

NAVY = "#19435B"
ROSE = "#9D485A"
MID = "#71808A"

# run, subset, input size, val mAP@0.5, whether the subset was still broken
# a value of None means the run produced no usable number; it is still drawn, so
# the jump from run5 to run7 is explained rather than left as a silent gap
RUNS = [("run-1", "v1", 640,  0.629, True),
        ("run2",  "v2", 960,  0.896, True),
        ("run3",  "v3", 960,  0.766, True),
        ("run4",  "v3", 1280, 0.802, True),
        ("run5",  "v4", 1280, 0.747, True),
        ("run6",  "v4", 960,  None,  True),
        ("run7",  "v5", 1280, 0.846, False),
        ("run8",  "v5", 1280, 0.849, False)]


def fig_runs():
    fig, ax = plt.subplots(figsize=(11.6, 5.6))
    xs = list(range(len(RUNS)))
    vals = [0 if r[3] is None else r[3] for r in RUNS]
    cols = [GREY if r[4] else (NAVY if r[0] == "run8" else MID) for r in RUNS]
    ax.bar(xs, vals, color=cols, width=0.62, zorder=3)

    for x, (name, sub, sz, v, broken) in zip(xs, RUNS):
        if v is None:
            # an outline where the bar would have been: the run happened, the
            # number never did
            ax.bar([x], [0.46], width=0.62, facecolor="none", edgecolor=GREY,
                   linewidth=1.6, linestyle=(0, (4, 3)), zorder=3)
            ax.text(x, 0.49, fa("بدون نتیجه"), ha="center", fontsize=12.5,
                    weight="bold", color=GREY, zorder=4)
            # no rotated subtitle here: the note under the chart carries the reason
            continue
        ax.text(x, v + 0.014, "%.3f" % v, ha="center", fontsize=12.5,
                weight="bold", color="#222", zorder=4)
        ax.text(x, 0.05, fa("زیرمجموعه %s" % sub) + "  ·  %d px" % sz,
                ha="center", fontsize=9, color="white", zorder=4, rotation=90,
                va="bottom")

    ax.text(1, 1.035, fa("داده نشت‌دار"), ha="center", fontsize=11.5, color=ROSE, weight="bold")
    ax.text(7, 1.035, fa("مدل نهایی"), ha="center", fontsize=11.5, color=NAVY, weight="bold")

    # band captions live under the tick labels, clear of the bars
    tr = ax.get_xaxis_transform()
    ax.text(2.5, -0.155, fa("زیرمجموعه‌های معیوب — عدد قابل استناد نیست"),
            ha="center", fontsize=12, color=GREY, weight="bold",
            transform=tr, clip_on=False)
    ax.text(6.5, -0.155, fa("زیرمجموعه سالم"), ha="center", fontsize=12,
            color=NAVY, weight="bold", transform=tr, clip_on=False)

    ax.set_xticks(xs)
    ax.set_xticklabels([r[0] for r in RUNS], fontsize=12.5)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(0, 1.14)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel(fa("mAP@0.5 روی اعتبارسنجی"), fontsize=12)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.subplots_adjust(bottom=0.20)
    save(fig, os.path.join(OUT, "slide_runs.png"))


if __name__ == "__main__":
    fig_runs()
    print("saved slide_runs.png")
