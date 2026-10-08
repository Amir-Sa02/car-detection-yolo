# Project memory

## Workflow

1. Obtain original IADD training parts and validation data with YOLO annotations; exclude the original unlabeled test portion.
2. Inspect earlier subsets and evaluate videos with a historical run5 model. Screening is separate from final V5 training.
3. Exclude problematic annotation records `Record426_D` and `Record046_D`, plus one side of three duplicate/alias pairs.
4. Assign whole records to splits within each condition. Prioritize rare-class instance deficits; use frame-count deficits for records without those classes.
5. Retain frames containing selected scarce classes and fill remaining capacity randomly from common-class frames. Downscale only images whose longest side exceeds 1280; preserve aspect ratio and normalized labels.
6. Fine-tune YOLO11s. Compare main and finishing candidates by validation mAP@0.5, then report held-out test results.
7. Select confidence from validation F1 and create matrices and qualitative examples.

## Record exclusions

| Excluded alias | Retained counterpart |
|---|---|
| `Record407_D` | `Record409_D` |
| `Record416_R` | `Record438_R` |
| `Record043_D` | `Record042_D` |

Original local filenames were edited during later inspection, so the current raw tree is not a pristine upstream snapshot. The 416/438 pair can contain equivalent images without identical prefixes. Filename equality flags candidates, not every visual duplicate. Fixed-pair audits support inspection of suspected pairs; they are not an exhaustive discovery algorithm. Use archived per-video reports, annotation evidence and actual image comparisons together. A low metric alone does not prove incorrect labels; do not invent an unrecorded exclusion threshold.

The final dataset contains 160 represented records. Available source folders, eligible records, excluded aliases and represented selected records are different populations. Do not infer the final count simply by subtracting exclusions from an article's headline total. The exact manifest is authoritative for final membership.

## Builder logic

`record_dirs()` groups record folders across source parts. `frames_of()` collects image/label pairs. Records are grouped by condition suffix. Target fractions are 70/15/15. `rare_score()` counts selected scarce-class annotation instances. A whole record goes to the split with the largest remaining rare-instance deficit; records without those classes use remaining frame deficit.

The sampler keeps images containing `KEEP_CLASSES` and fills the remaining budget from shuffled common images. It is not a time-contiguous frame sampling rule. The fixed seed is 80. The algorithm does not use final test performance to allocate videos and does not directly optimize object-size balance. Size distributions are measured afterward. Video disjointness alone does not detect duplicate aliases; those need explicit exclusions.

## Definitions

- Instance: one YOLO label row, not one unique tracked object.
- Condition: image inherits its record suffix, not a newly predicted weather category.
- Size: normalized box area `width * height`; small below 0.01, medium from 0.01 to below 0.06, large at least 0.06. These are project thresholds, not COCO pixel bins.
- Person: may include people inside vehicles. A pedestrian-only detector requires a revised label policy and corresponding training annotations.
- Matrix background: unmatched detections or unmatched ground truths, not a seventh trained class.

## Environmental counts

| Condition | Train | Validation | Test | Total | All-image share |
|---|---:|---:|---:|---:|---:|
| Day (`D`) | 21,416 | 4,656 | 3,995 | 30,067 | 81.0% |
| Night (`N`) | 1,977 | 454 | 854 | 3,285 | 8.8% |
| Rain (`R`) | 2,302 | 432 | 542 | 3,276 | 8.8% |
| Cloudy (`A`) | 305 | 29 | 180 | 514 | 1.4% |

All-image percentages use 37,142 as denominator. Per-split plot percentages use that split's image count.

When returning: read this file and `EXPERIMENTS.md`, then the active run8 notebook. Use the final thesis for detailed wording and final presentation for the defense narrative. Saved counters and annotation scans verify tables; older explanations are not independent scientific evidence.
