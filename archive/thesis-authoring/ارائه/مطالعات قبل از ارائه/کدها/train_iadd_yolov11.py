# -*- coding: utf-8 -*-
"""Train, fine-tune and evaluate YOLOv11 on the cleaned IADD subset.

This is the whole training pipeline of the project in one file. It reproduces
run 8, the final model reported in the thesis:

    stage "train"     150 epochs max with early stopping, AdamW + cosine LR
    stage "finetune"  10 low-LR SGD epochs from the best weight, augmentation off
    stage "evaluate"  every candidate weight is scored on val and test; the
                      winner is chosen on val only, test is reported once

The dataset itself is built by colab/build_subset_v5.py; this script expects the
resulting folder with a data.yaml inside.

Usage:
    python train_iadd_yolov11.py --data iadd_subset_v5/data.yaml --stage all
    python train_iadd_yolov11.py --stage train --resume      # continue a run
"""
import argparse
import csv
import json
import os
from dataclasses import asdict, dataclass

from ultralytics import YOLO


@dataclass
class Config:
    """Training settings of the final run. Every value here appears in the
    thesis (table 2-5) and in the args.yaml that Ultralytics writes."""
    data: str = "iadd_subset_v5/data.yaml"
    project: str = "runs"            # where Ultralytics writes weights and logs
    name: str = "run8"
    model: str = "yolo11s.pt"        # COCO-pretrained, scale s (9.46 M params)
    imgsz: int = 1280                # longer side of the input, letterboxed
    batch: int = 12                  # the most that fits a free 15 GB GPU at 1280
    epochs: int = 150
    patience: int = 10               # early stopping on the val fitness
    optimizer: str = "AdamW"
    lr0: float = 0.001
    cos_lr: bool = True
    weight_decay: float = 0.0005
    warmup_epochs: int = 3
    mixup: float = 0.1               # kept low: labels are semi-automatic
    hsv_v: float = 0.4               # brightness jitter for night and overcast
    degrees: float = 5.0             # small rotation for camera shake
    seed: int = 0
    # fine-tune stage
    ft_epochs: int = 10
    ft_lr0: float = 0.001

    @property
    def run_dir(self):
        return os.path.join(self.project, self.name)

    @property
    def ft_dir(self):
        return os.path.join(self.project, self.name + "_ft")


def train(cfg, resume=False):
    """Main training run. Resuming picks up last.pt of the same run."""
    last = os.path.join(cfg.run_dir, "weights", "last.pt")
    if resume and os.path.exists(last):
        YOLO(last).train(resume=True)
        return
    YOLO(cfg.model).train(
        data=cfg.data, project=cfg.project, name=cfg.name, exist_ok=True,
        epochs=cfg.epochs, patience=cfg.patience, imgsz=cfg.imgsz, batch=cfg.batch,
        optimizer=cfg.optimizer, lr0=cfg.lr0, cos_lr=cfg.cos_lr,
        weight_decay=cfg.weight_decay, warmup_epochs=cfg.warmup_epochs,
        mixup=cfg.mixup, hsv_v=cfg.hsv_v, degrees=cfg.degrees, seed=cfg.seed,
    )


def finetune(cfg):
    """Short low-LR pass from the best main weight, with mosaic and mixup off so
    the model settles on the real image distribution."""
    best = os.path.join(cfg.run_dir, "weights", "best.pt")
    YOLO(best).train(
        data=cfg.data, project=cfg.project, name=cfg.name + "_ft", exist_ok=True,
        epochs=cfg.ft_epochs, imgsz=cfg.imgsz, batch=cfg.batch,
        optimizer="SGD", lr0=cfg.ft_lr0, lrf=0.01, warmup_epochs=0,
        mosaic=0.0, mixup=0.0, hsv_v=cfg.hsv_v, degrees=cfg.degrees, seed=cfg.seed,
    )


def evaluate(cfg):
    """Score every candidate weight on val and test.

    The winner is the candidate with the higher val mAP@0.5; test is only
    reported, never used to choose. Results go to <run_dir>/evaluation.csv and
    evaluation.json; the thesis tables (3-1 to 3-3) hold the same numbers."""
    candidates = [("main", os.path.join(cfg.run_dir, "weights", "best.pt"))]
    ft = os.path.join(cfg.ft_dir, "weights", "best.pt")
    if os.path.exists(ft):
        candidates.append(("finetune", ft))

    rows = []
    for tag, weight in candidates:
        model = YOLO(weight)
        for split in ("val", "test"):
            r = model.val(data=cfg.data, split=split, imgsz=cfg.imgsz,
                          batch=cfg.batch, plots=False, verbose=False)
            rows.append({"candidate": tag, "split": split,
                         "mAP50": round(float(r.box.map50), 4),
                         "mAP50_95": round(float(r.box.map), 4),
                         "precision": round(float(r.box.mp), 4),
                         "recall": round(float(r.box.mr), 4),
                         "per_class_mAP50": [round(float(x), 4) for x in r.box.ap50]})

    val_scores = {row["candidate"]: row["mAP50"] for row in rows if row["split"] == "val"}
    winner = max(val_scores, key=val_scores.get)

    os.makedirs(cfg.run_dir, exist_ok=True)
    with open(os.path.join(cfg.run_dir, "evaluation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["candidate", "split", "mAP50", "mAP50_95",
                                          "precision", "recall"])
        w.writeheader()
        for row in rows:
            w.writerow({k: row[k] for k in w.fieldnames})
    with open(os.path.join(cfg.run_dir, "evaluation.json"), "w") as f:
        json.dump({"config": asdict(cfg), "results": rows, "winner": winner}, f, indent=2)

    print("winner (chosen on val):", winner)
    for row in rows:
        print("%-9s %-5s mAP50=%.3f mAP50-95=%.3f" % (row["candidate"], row["split"],
                                                    row["mAP50"], row["mAP50_95"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=Config.data, help="path to data.yaml")
    ap.add_argument("--project", default=Config.project)
    ap.add_argument("--name", default=Config.name)
    ap.add_argument("--stage", choices=["train", "finetune", "evaluate", "all"],
                    default="all")
    ap.add_argument("--resume", action="store_true", help="continue the main run")
    args = ap.parse_args()

    cfg = Config(data=args.data, project=args.project, name=args.name)
    if args.stage in ("train", "all"):
        train(cfg, resume=args.resume)
    if args.stage in ("finetune", "all"):
        finetune(cfg)
    if args.stage in ("evaluate", "all"):
        evaluate(cfg)


if __name__ == "__main__":
    main()
