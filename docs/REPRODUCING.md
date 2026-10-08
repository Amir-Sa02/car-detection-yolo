# Reproduction guide

Run from the repository root. New generated files go in ignored `outputs/`. Do not execute historical document repair scripts on final files.

## Offline demo and charts

```bash
python -m pip install -r requirements.txt
python code/demo_boxes.py
python code/make_figures_ch2.py
python code/make_figures_ch3.py
```

The demo needs only an included image/label and model; it draws GT and prediction images separately. Ground truth has no confidence scores. Four included examples illustrate conditions, not unbiased aggregate performance. Chart commands use archived data, without running inference or training.

## Exact V5 restoration

Download the complete author's V5 archive from the Drive folder linked in README, or extract the original labeled IADD parts and run:

```bash
python code/restore_v5_from_manifest.py --source "D:/data/IADD" --output "D:/data/v5_check" --limit 3
python code/restore_v5_from_manifest.py --source "D:/data/IADD" --output "D:/data/restored_v5"
```

Output must be absent or empty. The manifest records filenames, split, source record, dimensions and image/label SHA-256. The tool matches labels by hash and handles certain corrected filename prefixes. It stops on missing matches. Pillow/libjpeg differences may change JPEG bytes; a restoration report records exact matches. A manifest cannot reconstruct missing pixels or missing labels by itself.

To rerun the heuristic rather than restore historical membership:

```bash
python code/build_subset_v5.py --source "D:/data/IADD" --output "D:/data/new_v5" --dry-run
python code/build_subset_v5.py --source "D:/data/IADD" --output "D:/data/new_v5"
```

Existing nonempty output is rejected unless `--overwrite` is explicitly passed. Use a new destination. Source naming/version changes can affect selection despite an unchanged seed.

## Recount and evaluate

```bash
python code/compute_v5_validity.py --dataset "D:/data/restored_v5" --output outputs/dataset_validity
python code/evaluate.py --dataset "D:/data/restored_v5/data.yaml" --split test --device cpu --batch 1
```

The validity script counts images, record names, annotation rows, class IDs, normalized-area size groups and condition suffixes. Objects/image is instances divided by images. Size keys 0/1/2 are size groups, not classes.

The chapter-2 plotter reads **archived** `figure and table data/stats.json`, not the new scan automatically. Compare JSON files first. The chapter-3 plotter reads archived evaluation data and captured historical comparison/matrix values; it does not automatically use new evaluator outputs. New evaluation writes metrics and operating-point matrices separately under `outputs/evaluation/`.

## Training and inspections

Use `IADD_YOLOv11_Colab_run8.ipynb` for actual final training; update its Drive/data paths. Retraining requires compute and is unnecessary for inference.

- `audit_duplicate_filenames.py --dataset ...`: shared names and prefix inconsistencies, two distinct CSV checks.
- `audit_duplicate_pairs.py --help`: supporting checks of suspected pairs, not exhaustive duplicate discovery.
- `IADD_YOLOv11_Colab_pervideo.ipynb`: historical V4/run5 diagnostics, creates temporary linked datasets and evaluates each record.
- `make_label_evidence.py`, `render_plain_gt.py`, `render_plain_boxes.py`: preserved earlier renderers with historical local paths; prefer portable `demo_boxes.py` for new single-image evidence.
- `archive/`: historical code/output snapshots. One-off authoring tools may modify documents or contain obsolete paths; preservation is not a claim they are current runnable entry points.
