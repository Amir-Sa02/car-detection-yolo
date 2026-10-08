# Figures and tables: inputs and tools

| Material | Input | Generator/source |
|---|---|---|
| Dataset volume / table 2-1 | Images, record prefixes, label-row counts | `compute_v5_validity.py`, exact manifest |
| Class counts / table 2-2 | Class ID in every annotation row | Validity class counters |
| Class shares / figure 2-2 | Class count / instances in each split | `make_figures_ch2.py`, logarithmic axis |
| Size table/chart 2-3 | Normalized annotation width × height | Validity counters and chapter-2 plotter |
| Conditions table/chart 2-4 | Image record suffix | Validity counters and chapter-2 plotter |
| Training curves / figure 3-1 | Main `runs/run8/run8/results.csv` | `make_figures_ch3.py` |
| Strategy comparison / figure 3-2 | Captured run7/run8 summary numbers | Values embedded in chapter-3 function |
| Per-class table 3-2 / figure 3-3 | Saved per-class evaluation CSV | Chapter-3 plotter; evaluation, not label counting |
| F1 and evaluation curves | `figure and table data/eval_curves.npz` | Curve export and chapter-3 plotter |
| Final matrices | Captured count matrix embedded in plotter | Chapter-3 plotter; `evaluate.py` produces new matrices |
| GT/prediction figures 3-6/3-7 | Individual image/label/model-output tiles | `figures/qualitative-source/`, final figures; new single-image `demo_boxes.py` |
| Workflow diagrams | Project methodology | `figures/editable/*.drawio` |
| Original-IADD summaries | Previously scanned local source copy | `figure and table data/original-iadd/` |

Use the final thesis to confirm figure numbering. Draw.io files are editable **reconstructions**, not proof of which software originally produced the first image. Third-party architecture attribution remains in the thesis.

Matrix rows are predicted, columns true. Last row: missed ground truths (FN). Last column: unmatched predictions (FP). Background-background is not a meaningful TN count in this object detector. Normalization is by column; rounded/hidden small values affect visible sums. Car/background 0.76 means 76% of unmatched predictions were cars, not 76% of all background pixels or images.

Preserve historical figures when running new evaluations. Record the new checkpoint, library version, dataset manifest and confidence. Qualitative examples illustrate behavior without proving aggregate performance. Local source counts and article headline counts are separate evidence and should not be conflated.
