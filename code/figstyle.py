# -*- coding: utf-8 -*-
"""Shared drawing style for every figure in the thesis.

Keeping this in one place is what makes the figures look like one set rather
than a collection: same font, same palette, same tick and grid weights, same
legend behaviour, same export settings.

Two Persian-specific problems are solved here once:
  * letters must be joined and reordered before matplotlib draws them -> fa()
  * a Persian legend reads right-to-left, so the colour swatch belongs on the
    RIGHT of its label and the labels must be right-aligned -> legend()
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper
from bidi.algorithm import get_display

# ------------------------------------------------------------------ palette
NAVY = "#1f4e79"     # primary
ORANGE = "#e08a00"   # secondary
GREEN = "#2e7d32"    # positive / test split
RED = "#c0392b"      # removal / worst case
PURPLE = "#7b4fa8"
TEAL = "#00838f"
GREY = "#5a5a5a"
LIGHT = "#9e9e9e"

SERIES = [NAVY, ORANGE, GREEN, RED, PURPLE, TEAL]

SPLIT_COLOR = {"train": NAVY, "val": ORANGE, "test": GREEN}
SPLIT_FA = {"train": "آموزش", "val": "اعتبارسنجی", "test": "آزمون"}
CLASS_FA = {"person": "شخص", "car": "خودروی سبک", "motorcycle": "موتورسیکلت",
            "bus": "اتوبوس", "truck": "خودروی باری", "traffic_light": "چراغ راهنمایی"}
CLASS_ORDER = ["person", "car", "motorcycle", "bus", "truck", "traffic_light"]

# ------------------------------------------------------------------ typography
_FONT_CANDIDATES = (r"C:\Windows\Fonts\tahoma.ttf",
                    r"C:\Windows\Fonts\ARIALUNI.TTF",
                    r"C:\Windows\Fonts\arial.ttf")

for _c in _FONT_CANDIDATES:
    if os.path.exists(_c):
        font_manager.fontManager.addfont(_c)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=_c).get_name()
        break

plt.rcParams.update({
    "axes.edgecolor": "#8a8a8a",
    "axes.labelcolor": "#1a1a1a",
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.linewidth": 0.9,
    "xtick.color": "#4a4a4a",
    "ytick.color": "#4a4a4a",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.color": "#b4b4b4",
    "grid.linewidth": 0.8,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def fa(s):
    """join and reorder Persian text so matplotlib renders it correctly"""
    return get_display(arabic_reshaper.reshape(str(s)))


def cls(name):
    return fa(CLASS_FA[name])


def pct(v, digits=1):
    """Persian writes the percent sign before the number: ٪۷۰, not ۷۰٪"""
    txt = f"{v:.{digits}f}".rstrip("0").rstrip(".") if digits else f"{v:.0f}"
    return "٪" + txt


# ------------------------------------------------------------------ helpers
def grid(ax, axis="y", alpha=0.7):
    ax.grid(axis=axis, alpha=alpha, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    return ax


def legend(ax, loc="best", ncol=1, outside=None, fontsize=10,
           handlelength=1.8, **kw):
    """Persian-aware legend: swatch on the right of the label, labels right-aligned.

    `outside` may be 'above' or 'right' to lift the legend clear of the data,
    which is the safe choice when curves cross the corners of the axes.

    `handlelength` is worth raising when a series is dashed: the default swatch
    is too short to fit a whole dash period, so a dashed line reads as solid."""
    if outside == "above":
        kw.update(loc="lower center", bbox_to_anchor=(0.5, 1.02))
    elif outside == "below":
        kw.update(loc="upper center", bbox_to_anchor=(0.5, kw.pop("y", -0.16)))
    elif outside == "right":
        kw.update(loc="center left", bbox_to_anchor=(1.02, 0.5))
    else:
        kw.update(loc=loc)
    lg = ax.legend(ncol=ncol, fontsize=fontsize, frameon=kw.pop("frameon", False),
                   markerfirst=False,          # swatch after the text: RTL reading
                   handlelength=handlelength, handletextpad=0.6,
                   borderaxespad=0.4, **kw)
    for t in lg.get_texts():
        t.set_horizontalalignment("right")
    return lg


def bar_labels(ax, bars, fmt="{:.2f}", dy=0.012, fontsize=9):
    """value on top of every bar - a chart the examiner can read without guessing"""
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + dy, fmt.format(h),
                ha="center", va="bottom", fontsize=fontsize, color="#1a1a1a")


def save(fig, path, pad=0.25):
    fig.savefig(path, dpi=220, bbox_inches="tight", pad_inches=pad,
                facecolor="white")
    plt.close(fig)


def ylabel(ax, text, pad=14, rotate=False, fontsize=10.5):
    """Persian rotated 90 degrees is hard to read, so a SHORT vertical-axis label
    sits horizontally above the axis, centred on the axis line itself.

    A long label cannot be placed that way: half of it hangs to the left of the
    axes, the saved bounding box grows on that side only, and the plot then sits
    off-centre inside its frame in Word. Long labels therefore pass rotate=True
    and run along the axis, the usual scientific convention."""
    ax.set_ylabel("")
    if rotate:
        ax.set_ylabel(fa(text), rotation=90, va="bottom", labelpad=pad,
                      fontsize=fontsize, color="#1a1a1a")
        return
    ax.annotate(fa(text), xy=(0, 1), xycoords="axes fraction",
                xytext=(0, pad), textcoords="offset points",
                ha="center", va="bottom", fontsize=fontsize, color="#1a1a1a")


def xlabel(ax, text, pad=8, fontsize=None):
    """fontsize matters on the physically large panels: they are scaled down a
    lot on the page, so a label sized for a small figure ends up unreadable."""
    ax.set_xlabel(fa(text), labelpad=pad,
                  **({} if fontsize is None else {"fontsize": fontsize}))
