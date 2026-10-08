# Actual experiment record

## Main run8

Original checkpoint metadata records Ultralytics 8.4.120, a six-class YOLO11s model, **9,430,114 learned parameters**, input size 1280 and batch 12. Parameters are scalar weights/biases, not neurons.

The main notebook uses AdamW, initial learning rate 0.001, cosine scheduling, up to 150 epochs and patience 10, with mixup 0.1, `hsv_v=0.4` and `degrees=5`. Consult `models/run8-metadata.json` and saved run arguments for all actual settings.

The complete main CSV contains 62 epochs. The original best checkpoint has zero-based epoch 50 (epoch 51), saved validation mAP@0.5 0.84904 and mAP@0.5:0.95 0.68725. This checkpoint supplies the public inference model. `results_checkpoint.csv` is partial checkpoint-carried history, not the full experiment CSV.

## Finishing stage

The original ten-epoch finishing call specifies **SGD**, `lr0=0.001`, `lrf=0.01`, `warmup_epochs=0`, `mosaic=0`, `mixup=0`, `hsv_v=0.4`, `degrees=5`; it does not explicitly enable cosine scheduling. Do not describe it as AdamW at 0.0001 based on a later edited defense notebook. That edited copy is preserved separately.

`runs/run8/run8_ft/results_reconstructed.csv` combines the recorded history fragments into epochs 1–10. Original fragments remain in the archive. The finishing candidate did not replace the main model in final selection.

## Selection and early stopping

Library checkpoint selection/patience and the later main-versus-finishing selection are distinct. The retained checkpoint reports fitness 0.68725, equal to mAP@0.5:0.95. A manually calculated weighted fitness in a diagnostic cell does not prove it drove version-specific library early stopping.

The evaluation cell selects the candidate by **validation mAP@0.5**. Test scores are printed, but not used by its `max(...)` expression. The run7/run8 comparison changed multiple training settings; it is not an isolated optimizer-only causal experiment.

## Evaluation confidence

The validation F1 curve labels aggregate F1 near 0.80 at confidence 0.406. The historical cell averages per-class F1 values, finds the maximum and rounds its confidence to three decimals. Initial 0.25 is a fallback if the curve is not found.

AP needs a range of confidence thresholds. The portable evaluator first uses low-confidence evaluation (`conf=0.001`) for metrics/curves, then separately generates matrices at 0.406. Restricted high-confidence AP should not be substituted for original full-curve AP. Mean per-class F1 also differs from F1 computed from mean precision and mean recall.

## Batch iterations and checkpoints

Approximately `ceil(26000/12) = 2167` batches per epoch and 134,354 across 62 main epochs. This is not necessarily the optimizer update count: gradient accumulation and warmup affect that. The finishing stage is separate.

The public inference checkpoint lacks original optimizer state. Full historical checkpoints were backed up privately. Their historical Colab paths are provenance, not directories required for inference.

## Historical notebooks

Earlier builders and Colab notebooks are under `archive/colab-history/`; recorded experiment directories are under `archive/experiment-results/`. A notebook filename (including run9/run10) does not by itself establish that a completed experiment happened. Use actual saved results/checkpoints as evidence, and use run8 as the final reported run.
