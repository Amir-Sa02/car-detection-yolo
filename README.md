# IADD road-user detection with YOLO11s

Undergraduate final project by Mohammad Amir Sadeghzadeh. This repository preserves the code, final documents, experiment outputs, inference model and decisions needed to revisit the project after removing the original working directories.

The work covers two stages: creating a video-separated subset from labeled IADD data, then fine-tuning a pretrained YOLO11s detector. Labels: `person`, `car`, `motorcycle`, `bus`, `truck`, `traffic_light`. This is object detection, including localization. Cargo vehicles include pickups; `person` is not restricted to pedestrians outside vehicles.

## Final dataset

| Split | Videos | Images | Annotation instances | Image share |
|---|---:|---:|---:|---:|
| Train | 79 | 26,000 | 204,009 | 70% |
| Validation | 39 | 5,571 | 36,810 | 15% |
| Test | 42 | 5,571 | 34,994 | 15% |
| Total | 160 | 37,142 | 275,813 | 100% |

Shares refer to images, not videos. An instance means one annotation row, including repeated appearances of an object in different frames.

The final main `run8` checkpoint achieved approximately **mAP@0.5 = 0.874**, **mAP@0.5:0.95 = 0.707**, mean precision 0.803 and mean recall 0.818 on the test split. These are archived historical results. The final operating confidence was **0.406**, selected from validation F1; AP curves were evaluated separately over a range of confidence thresholds.

## Start here

- [Persian quick review](docs/QUICK_REVIEW_FA.md): a short reminder for returning to the project.
- [Project memory](docs/PROJECT_MEMORY.md): decisions, exclusions, definitions and caveats.
- [Reproduction guide](docs/REPRODUCING.md): code entry points and commands.
- [Experiment record](docs/EXPERIMENTS.md): actual optimizer settings, checkpoints and evaluation.
- [Figure sources](docs/FIGURES.md): table/chart inputs and editable diagrams.
- [Archive and cleanup](docs/ARCHIVE_AND_CLEANUP.md): what to preserve before deleting local data.

## Quick demonstration

```bash
python -m pip install -r requirements.txt
python code/demo_boxes.py
python code/make_figures_ch2.py
python code/make_figures_ch3.py
```

The demo uses an included image/label and the final model. It writes separate ground-truth and prediction images. Chart commands use archived numerical inputs, without retraining or reevaluating. New outputs go in ignored `outputs/`.

The recorded training library was **Ultralytics 8.4.120**. `models/run8_best.pt` is an inference checkpoint with **9,430,114 model parameters**. It does not include the original optimizer state and cannot resume the historical session.

## Repository map

| Location | Contents |
|---|---|
| `code/` | Dataset construction, analysis, evaluation, charts, evidence and demo tools |
| `models/` | Final inference model and original checkpoint metadata |
| `dataset manifests/` | Exact V5 image/split list, hashes, record assignments and counted statistics |
| `figure and table data/` | Saved statistics, evaluation arrays, per-class metrics and original-IADD summaries |
| `runs/run8/` | Main/finishing settings, training records and evaluation plots |
| `record review/` | Earlier per-video screening results |
| `figures/` | Final figures, editable reconstructed diagrams and qualitative source tiles |
| `presentation and thesis/` | Final Word thesis, PowerPoint and existing PDF exports |
| `docs/study-guides/` | Persian study documents and speaking notes |
| `archive/` | Earlier notebooks, experiment outputs, authoring tools and defense-edited code |

The active final training notebook is `code/IADD_YOLOv11_Colab_run8.ipynb`. The `pervideo` notebook is an earlier V4/run5 diagnostic. Historical scripts may contain old absolute paths or one-off document repairs; they are not current entry points.

## Dataset access

- [IADD project and multipart downloads](https://github.com/ahv1373/IADD)
- [Original IADD article](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.12710)
- [Author-provided Drive folder](https://drive.google.com/drive/folders/1uC7HJFWZ-ysFRPSJ_Fdu5yY4Ul3Erd9-?usp=sharing)

Full dataset images are not stored in Git. The author-provided Drive folder was reachable without signing in during archiving and its page listed `iadd_subset_v5.zip`. The archive itself was not downloaded or integrity-checked. Confirm its complete image/label contents before deleting the local dataset.

We used the publicly labeled original training and validation portions. The downloaded original test portion lacked labels and was excluded. Our new test split comes from previously labeled source videos, without a complete new relabeling campaign.

Exact-manifest restoration is preferable to rerunning the heuristic against a changed source tree. Dataset, article and library rights remain with their owners; this repository does not grant a new license to redistribute third-party data or papers.
