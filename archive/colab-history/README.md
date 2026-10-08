# Traffic Object Detection with YOLOv11 (IADD)

Small-scale training of a **YOLOv11** traffic-object detector on the
**IADD — Iran Autonomous Driving Dataset**, run on Google Colab.

## Classes (6)

`0 person · 1 car · 2 motorcycle · 3 bus · 4 truck · 5 traffic_light`

## Repository layout

```
IADD_YOLOv11_Colab.ipynb   the Colab training notebook (resume-safe)
build_subset.py            builds a small, rebalanced subset of IADD (runs locally)
runs/
  run-1/                   run 1 results (plots, metrics, args)
  run2/                    run 2 results (plots, metrics, args)
```

> The dataset, Python virtual environment, and model weights (`*.pt`) are **not**
> tracked here — only the code and results. The IADD dataset is available at
> https://github.com/ahv1373/IADD.

## How to run (Google Colab)

1. `python build_subset.py` — builds the subset zip locally.
2. Upload the zip to Google Drive.
3. Open `IADD_YOLOv11_Colab.ipynb` in Colab, set runtime to a **GPU**, run all cells.
   Checkpoints are written to Drive every epoch, so a disconnect is not fatal —
   re-run and training resumes automatically.

## Results

| Run | Model | Images | Epochs | mAP@0.5 | mAP@0.5:0.95 | Notes |
|-----|-------|--------|--------|---------|--------------|-------|
| run-1 | YOLOv11n | ~5,000 | 40 | 0.63 | 0.45 | Baseline. Car strong (AP 0.92); rare classes weak (~0.5); many small objects missed. |
| run2  | YOLOv11s | ~13,000 | 43* | 0.89 | 0.73 | Rebalanced data + 960px + larger model. Rare classes jumped to ~0.9; bus↔truck confusion 45% → 2%. |

\* Stopped early by the free-Colab time limit while still improving (target was 150).

### Per-class AP@0.5 (run 1 → run 2)

| person | car | motorcycle | bus | truck | traffic_light |
|--------|-----|------------|-----|-------|---------------|
| 0.59 → 0.86 | 0.92 → 0.96 | 0.49 → 0.90 | 0.52 → 0.90 | 0.78 → 0.85 | 0.48 → 0.88 |

> **Note on evaluation:** IADD's official test labels were not released, so these
> metrics are on the validation set. The dataset's train/val splits also share
> videos (different frames of the same drives), so the numbers are optimistic. A
> leakage-free split by whole video is planned for the next run.
