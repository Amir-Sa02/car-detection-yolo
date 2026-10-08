# Archive verification record

Packaging date: 2026-10-08. Source directories: the author's original project, Desktop working tools, Desktop repository and final hand-in/study files.

## Checks performed

- Parsed every active Python source and all Python code cells of the final run8 notebook; shell/magic installation lines were excluded from Python parsing.
- Executed the single-image demo using the exported model and included original label.
- Regenerated the three quantitative chapter-2 figures and six chapter-3 outputs from archived inputs. Inspected a regenerated class-share chart and normalized matrix visually.
- Restored three historical V5 images from original raw data using the exact manifest. All three matched original label hashes, dimensions and JPEG SHA-256 values.
- Executed the portable evaluator on four included example images, including separate low-confidence curve export and 0.406 operating-point evaluation. This is a functionality check, **not a new full-test-set performance report**.
- Scanned package text for common credential-token patterns and checked for files exceeding GitHub's 100MB individual-file limit.
- Confirmed every saved model state tensor equals the selected original checkpoint's half-precision tensor; all 499 state entries matched.
- Verified ZIP entry CRCs for the pre-change repository backup, full training-checkpoint archive and private reference-paper archive.
- Checked all 632 copy-provenance records: none are missing. The final thesis and presentation are byte-identical to their selected source files; active code adaptations are separate from preserved original snapshots.
- Retrieved the public Drive folder page without authentication; it lists `iadd_subset_v5.zip`. Full dataset ZIP download/content integrity remains unchecked.

Local execution used Python 3.13.3, CPU PyTorch 2.11.0 and the installed Ultralytics 8.4.42. The historical training checkpoint records Ultralytics 8.4.120; requirements preserve that training version. Local smoke results are not substituted into historical figures or metrics. Fused inference summaries report fewer parameters than the unfused checkpoint because normalization layers are fused into convolution layers.

Exact dataset counts, condition/class/size counters, image/label hashes and record disjointness are recorded in `dataset manifests/v5-stats-verified.json`, `v5-images.csv` and `v5-records.json`. The final integrity manifest identifies the packaged file bytes.

No new model training, full held-out test reevaluation, scientific source audit or document-content rewriting was performed as part of this archiving task. The repository preserves historical source material and explains its limitations.

Final full-data check: 37,142 manifest rows, 275,813 annotation instances and 160 disjoint represented records. Fresh class, size and condition counters match archived chart statistics exactly. Every label backup entry passed ZIP CRC verification.
