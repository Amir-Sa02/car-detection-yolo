# -*- coding: utf-8 -*-
"""Confusion matrix at the operating point the thesis actually describes.

Section 2-6 says the confidence threshold is the one that maximises the F1 score
on the validation split, and that the same threshold is then applied to the test
split. The run's own F1-confidence curve on validation peaks at 0.406, so that is
the threshold used here. export_eval_curves.py left the threshold at the library
default, which is why its matrix counted every marginal detection.

Only the confusion matrix is written; the curves in eval_curves.npz are
threshold-free and stay as they are.
"""
import os
import numpy as np
import yaml

CONF_OP = 0.406            # argmax of the all-class F1 curve on the validation split

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
WEIGHTS = os.path.join(ROOT, "colab", "runs", "run8", "run8", "weights", "best.pt")
DS = os.path.join(ROOT, "dataset", "iadd_subset_v5")
OUT = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها", "confusion_at_op.npz"))

local_yaml = os.path.join(HERE, "_data_local.yaml")
if not os.path.exists(local_yaml):
    cfg = yaml.safe_load(open(os.path.join(DS, "data.yaml"), encoding="utf-8"))
    cfg["path"] = DS
    yaml.safe_dump(cfg, open(local_yaml, "w", encoding="utf-8"), allow_unicode=True)

from ultralytics import YOLO

model = YOLO(WEIGHTS)
res = model.val(data=local_yaml, split="test", imgsz=1280, batch=1,
                device="cpu", conf=CONF_OP, plots=True, verbose=True)

cm = np.asarray(res.confusion_matrix.matrix)
np.savez(OUT, confusion=cm, conf=np.float64(CONF_OP),
         names=np.array([model.names[i] for i in sorted(model.names)]))
print("threshold", CONF_OP)
print("matrix\n", cm.astype(int))
print("saved", OUT)
