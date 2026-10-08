# -*- coding: utf-8 -*-
"""Run the evaluation locally once and export the RAW curve data.

Ultralytics only writes English PNGs, so we capture the underlying arrays
(precision-recall curve and confusion matrix) into a .npz file. The Persian
versions of those figures are then drawn from this file by make_figures_ch3.py,
which keeps every label in the thesis language.

This runs on CPU and takes a while; it only has to be done once.
"""
import os, numpy as np, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
WEIGHTS = os.path.join(ROOT, "colab", "runs", "run8", "run8", "weights", "best.pt")
DS = os.path.join(ROOT, "dataset", "iadd_subset_v5")
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها", "eval_curves.npz"))

# the shipped yaml points at the Colab path; write a local copy
local_yaml = os.path.join(HERE, "_data_local.yaml")
cfg = yaml.safe_load(open(os.path.join(DS, "data.yaml"), encoding="utf-8"))
cfg["path"] = DS
yaml.safe_dump(cfg, open(local_yaml, "w", encoding="utf-8"), allow_unicode=True)

from ultralytics import YOLO

model = YOLO(WEIGHTS)
res = model.val(data=local_yaml, split="test", imgsz=1280, batch=1,
                device="cpu", plots=True, verbose=True)   # plots=True is what
                # populates confusion_matrix.matrix; the English PNGs it also
                # writes are ignored - the thesis uses the Persian redraw

store = {"names": np.array([model.names[i] for i in sorted(model.names)])}

# curves_results holds four curves as (x, y, x_label, y_label):
#   Recall/Precision (the PR curve), and three Confidence/* curves.
# Matching on the y label alone also catches Precision-vs-Confidence, so both
# labels are checked. Every curve is stored, keyed by its axis pair.
for x, y, xl, yl in res.curves_results:
    key = f"{xl}_{yl}".lower()
    store[f"x_{key}"] = np.asarray(x)
    store[f"y_{key}"] = np.asarray(y)           # shape: (classes, points)

assert "x_recall_precision" in store, "PR curve missing from curves_results"
store["pr_recall"] = store["x_recall_precision"]
store["pr_precision"] = store["y_recall_precision"]

store["ap50"] = np.asarray(res.box.ap50)
store["map50"] = np.float64(res.box.map50)

cm = res.confusion_matrix.matrix                # (nc+1, nc+1), includes background
store["confusion"] = np.asarray(cm)

np.savez(OUT, **store)
print("saved eval_curves.npz | mAP50 =", float(res.box.map50))
