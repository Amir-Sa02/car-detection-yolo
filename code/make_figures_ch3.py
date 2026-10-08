"""Generate the Chapter 3 figures from saved run outputs."""
import os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "outputs", "chapter3")
DATA_DIR = os.path.join(ROOT, "figure and table data")
RUN = os.path.join(ROOT, "runs", "run8", "run8")
LABELS = os.path.join(ROOT, "dataset", "iadd_subset_v5", "labels", "test")
os.makedirs(FIG, exist_ok=True)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from figstyle import (fa, cls, save, legend, grid, ylabel, xlabel,
                      SERIES, CLASS_FA, CLASS_ORDER,      # noqa: E402
                      NAVY, ORANGE, GREEN, GREY)


def _curves():
    return np.load(os.path.join(DATA_DIR, "eval_curves.npz"), allow_pickle=True)


def fig_3_1():
    df = pd.read_csv(os.path.join(RUN, "results.csv"))
    df.columns = [c.strip() for c in df.columns]
    x = df["epoch"]

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.4))

    panels = [
        (axes[0], "خطای مکان‌یابی کادر",
         [("train/box_loss", NAVY, "-", "آموزش"),
          ("val/box_loss", ORANGE, "--", "اعتبارسنجی")]),
        (axes[1], "خطای طبقه‌بندی",
         [("train/cls_loss", NAVY, "-", "آموزش"),
          ("val/cls_loss", ORANGE, "--", "اعتبارسنجی")]),
        # This panel shows mAP, not precision.
        (axes[2], "میانگین دقت متوسط روی اعتبارسنجی",
         [("metrics/mAP50(B)", GREEN, "-", None),
          ("metrics/mAP50-95(B)", NAVY, "--", None)]),
    ]
    latin = {"metrics/mAP50(B)": "mAP@0.5", "metrics/mAP50-95(B)": "mAP@0.5:0.95"}

    for ax, title, series in panels:
        for col, colour, ls, lbl in series:
            ax.plot(x, df[col], color=colour, lw=1.9, ls=ls,
                    label=fa(lbl) if lbl else latin[col])
        ax.set_title(fa(title), pad=30)
        ax.set_xlabel(fa("دوره آموزش"))
        grid(ax, axis="both")
        legend(ax, ncol=2, outside="above", fontsize=9.5)

    best = int(df["metrics/mAP50(B)"].idxmax())
    bx = df["epoch"].iloc[best]
    ax = axes[2]
    ax.axvline(bx, color=GREY, lw=1.1, ls=":")
    ax.annotate(fa("بهترین دوره"), xy=(bx, df["metrics/mAP50-95(B)"].iloc[best]),
                xytext=(bx - 3, 0.52), fontsize=9, color=GREY, ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.9, color=GREY))

    save(fig, os.path.join(FIG, "fig_3_1.png"))


def fig_3_2():
    runs = [("SGD", 0.846, 0.867), ("AdamW + cosine", 0.849, 0.874)]
    labels = [r[0] for r in runs]
    val = [r[1] for r in runs]; test = [r[2] for r in runs]
    xs = np.arange(len(runs)); w = 0.34

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    b1 = ax.bar(xs - w / 2, val, w, color=ORANGE, label=fa("اعتبارسنجی"), zorder=3)
    b2 = ax.bar(xs + w / 2, test, w, color=GREEN, label=fa("آزمون"), zorder=3)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.0015,
                    f"{b.get_height():.3f}", ha="center", va="bottom", fontsize=9.5)
    ax.set_xticks(xs); ax.set_xticklabels(labels)
    ax.set_ylim(0.80, 0.895)
    ylabel(ax, "mAP@0.5")
    xlabel(ax, "پیکربندی بهینه‌ساز")
    grid(ax)
    legend(ax, ncol=2, outside="below", y=-0.20)
    save(fig, os.path.join(FIG, "fig_3_2.png"))


def fig_3_3():
    df = pd.read_csv(os.path.join(DATA_DIR, "perclass_metrics.csv"))
    names = [cls(c) for c in df["class"]]
    xs = np.arange(len(df)); w = 0.36

    fig, ax = plt.subplots(figsize=(10.0, 4.8))
    b1 = ax.bar(xs - w / 2, df["mAP50"], w, color=GREEN, label="AP@0.5", zorder=3)
    b2 = ax.bar(xs + w / 2, df["F1"], w, color=NAVY, label=fa("امتیاز F1"), zorder=3)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.014,
                    f"{b.get_height():.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(xs); ax.set_xticklabels(names)
    ax.set_ylim(0, 1.12)
    ylabel(ax, "مقدار معیار")
    xlabel(ax, "رده شیء")
    grid(ax)
    legend(ax, ncol=2, outside="below", y=-0.22)
    save(fig, os.path.join(FIG, "fig_3_3.png"))


def fig_3_4():
    d = _curves()
    recall, prec = d["pr_recall"], d["pr_precision"]
    names = [str(n) for n in d["names"]]; ap = d["ap50"]

    fig, ax = plt.subplots(figsize=(9.4, 9.0))
    # Keep the legend ordered by AP.
    for i in sorted(range(len(names)), key=lambda k: -ap[k]):
        ax.plot(recall, prec[i], lw=2.2, color=SERIES[i % len(SERIES)],
                solid_capstyle="round",
                label=f"{ap[i]:.3f}  {cls(names[i])}")
    ax.plot(recall, prec.mean(0), lw=3.8, color="#10305c", zorder=5, ls=(0, (4.2, 2.4)),
            label=f"{float(d['map50']):.3f}  {fa('میانگین همه رده‌ها')}")

    xlabel(ax, "فراخوانی", fontsize=16)
    ylabel(ax, "دقت", rotate=True, fontsize=16)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.001)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.tick_params(labelsize=11)
    ax.set_aspect("equal", adjustable="box")
    grid(ax, axis="both", alpha=0.9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    legend(ax, loc="lower left", ncol=1, fontsize=11.5, frameon=True,
           framealpha=0.95, edgecolor="#c8c8c8", fancybox=False,
           borderpad=0.7, labelspacing=0.5, handlelength=3.2)
    save(fig, os.path.join(FIG, "fig_3_4.png"), pad=0.12)


# Matrix saved by the final test evaluation at the selected confidence threshold.
CONFUSION_RUN8 = np.array([          # predicted rows, true columns
    [ 1863,     1,    5,    0,    0,    1,  379],
    [    1, 27391,    0,    2,   49,    0, 3113],
    [    3,     0,  456,    0,    0,    0,   94],
    [    0,     0,    0,  201,    7,    0,   32],
    [    0,    27,    0,   30,  971,    0,  204],
    [    1,     0,    0,    0,    0,  955,  257],
    [  546,  1784,   58,   90,  179,  373,    0],
], dtype=float)


def _confusion(shade, text, cbar_label, vmax, out):
    """Draw one view of the final confusion matrix."""
    d = _curves()
    m = CONFUSION_RUN8.copy()
    assert (m.sum(0)[:-1] == d["confusion"].astype(float).sum(0)[:-1]).all(),         "class column totals must match the exported run: same split, same labels"
    names = [str(n) for n in d["names"]]
    labels = [cls(n) for n in names] + [fa("پس‌زمینه")]

    sh = shade(m)
    fig, ax = plt.subplots(figsize=(8.0, 6.6))
    im = ax.imshow(sh, cmap="Blues", vmin=0, vmax=vmax)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            label = text(m[i, j], sh[i, j])
            if label is None:
                continue
            ax.text(j, i, label, ha="center", va="center", fontsize=9.5,
                    color="white" if sh[i, j] > 0.55 * vmax else "#1a1a1a")
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
    xlabel(ax, "رده واقعی", pad=10)
    ax.set_ylabel(fa("رده پیش‌بینی‌شده"), fontsize=10.5, color="#1a1a1a",
                  rotation=90, va="bottom", labelpad=12)
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.10)
    cb.set_label(fa(cbar_label), fontsize=10, labelpad=12)
    save(fig, os.path.join(FIG, out))


def fig_3_5():
    """Normalized confusion matrix."""
    def shade(m):
        col = m.sum(0, keepdims=True)
        return np.divide(m, col, out=np.zeros_like(m), where=col > 0)

    _confusion(shade, lambda raw, s: None if s < 0.005 else f"{s:.2f}",
               "نسبت از رده واقعی", 1.0, "fig_3_5.png")


def fig_3_5_counts():
    """Confusion matrix as raw counts."""
    _confusion(lambda m: m, lambda raw, s: None if raw < 1 else f"{int(raw)}",
               "شمار نمونه", float(CONFUSION_RUN8.max()), "fig_3_5_counts.png")


TITLES = {"D": "روز آفتابی", "N": "شب", "R": "باران", "A": "روز ابری"}


# Test frames used in the qualitative figures.
DEMO_POOL = {
    "D": ["Record006_D__Record006_D_75",
          "Record114_D__Record114_D_126",
          "Record024_D__Record024_D_Record024_D_046513",
          "Record427_D__Record427_D_26"],
    "N": ["Record020_N__Record020_N_Record020_N_042442",
          "Record031_N__Record031_N_Record031_N_054948",
          "Record100_N__Record100_N_77",
          "Record020_N__Record020_N_Record020_N_042527"],
    "R": ["Record438_R__Record438_R_889",
          "Record204_R__Record204_R_147",
          "Record438_R__Record438_R_144",
          "Record438_R__Record438_R_325"],
    "A": ["Record105_A__Record105_A_18",
          "Record105_A__Record105_A_64",
          "Record105_A__Record105_A_60",
          "Record415_A__Record415_A_863"],
}


def _demo_frames(cond, k=2):
    """Select busy frames from different videos."""
    cand = []
    for stem in DEMO_POOL[cond]:
        lbl = os.path.join(LABELS, stem + ".txt")
        n = sum(1 for _ in open(lbl)) if os.path.exists(lbl) else 0
        cand.append((n, stem.split("__", 1)[0], stem))
    cand.sort(key=lambda t: -t[0])
    out, seen = [], set()
    for n, video, stem in cand:
        if video in seen:
            continue
        seen.add(video); out.append(stem)
        if len(out) == k:
            break
    return out


def _compare(conds, out_name):
    """Place ground truth and model output side by side."""
    from matplotlib.patches import Patch

    rows = [(c, stem) for c in conds for stem in _demo_frames(c)]
    if len(rows) < len(conds) * 2:
        return

    TW = 5.0
    TH = TW * 9 / 16
    GUT, BAND = 0.045, 0.20
    LBL, HEAD, LEG = 0.46, 0.34, 0.46

    off = [r * (TH + GUT) + (r // 2) * BAND for r in range(len(rows))]
    W = 2 * TW + GUT + LBL
    H = HEAD + off[-1] + TH + LEG
    fig = plt.figure(figsize=(W, H))

    cols = [("demo_pred_plain", 0.0, "خروجی مدل"),
            ("demo_gt_plain", TW + GUT, "برچسب واقعی")]
    for folder, x, head in cols:
        for r, (cond, stem) in enumerate(rows):
            y = H - HEAD - off[r] - TH
            ax = fig.add_axes([x / W, y / H, TW / W, TH / H])
            ax.imshow(Image.open(os.path.join(FIG, folder, f"{cond}_{stem}.jpg")))
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_visible(False)
        fig.text((x + TW / 2) / W, (H - HEAD * 0.62) / H, fa(head),
                 ha="center", va="center", fontsize=11.5, weight="bold")

    for i, cond in enumerate(conds):
        top = H - HEAD - off[2 * i]
        bot = H - HEAD - off[2 * i + 1] - TH
        fig.text((2 * TW + GUT + LBL / 2) / W, (bot + top) / 2 / H,
                 fa(TITLES[cond]), ha="center", va="center", fontsize=11.5,
                 rotation=90)

    box_colors = {"person": "#e63c3c", "car": "#008cff", "motorcycle": "#3cc83c",
                  "bus": "#ffaa00", "truck": "#b45aff", "traffic_light": "#00cdcd"}
    handles = [Patch(facecolor=box_colors[c], label=cls(c)) for c in CLASS_ORDER]
    lg = fig.legend(handles=handles, loc="center", ncol=6, frameon=False,
                    markerfirst=False, fontsize=10,
                    bbox_to_anchor=(0.5, LEG / 2 / H),
                    handlelength=1.5, handletextpad=0.5, columnspacing=1.4)
    for t in lg.get_texts():
        t.set_horizontalalignment("right")

    fig.savefig(os.path.join(FIG, out_name), dpi=200, facecolor="white")
    plt.close(fig)


def fig_3_6():
    _compare(("D", "N"), "fig_3_6.png")


def fig_3_7():
    _compare(("R", "A"), "fig_3_7.png")


if __name__ == "__main__":
    fig_3_1(); fig_3_2(); fig_3_3(); fig_3_4(); fig_3_5(); fig_3_5_counts()
    print("Qualitative figures are preserved in figures/; call their functions only after restoring the required source images.")
    print("Saved quantitative figures 3_1 through 3_5, plus the count matrix.")
