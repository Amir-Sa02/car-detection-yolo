# Archive and cleanup

The repository contains active code, historical notebooks/outputs, final documents, chart inputs, editable reconstructed diagrams, qualitative tiles, study documents, inference weights and exact V5 membership. Word/PowerPoint contents were copied without rewriting.

`archive-sources.json` records source paths and hashes **at copy time**. Active code was subsequently adapted, so this is provenance, not final integrity. `archive-integrity.json` records final packaged hashes, excluding itself, Git internals, outputs and caches.

## Private backups

In the author's Desktop `project-archive-backups/2026-10-08/` directory:

- `desktop_repository_before.zip`: repository before changes, excluding Git internals.
- `training-checkpoints-private.zip`: original full training checkpoints.
- `v5-labels-private.zip`: all final labels and the original data configuration.
- `reference-papers-private.zip`: available nonempty article PDFs, including highlighted versions, with an index.

These private ZIPs are **not published to GitHub**. Keep another copy outside the computer before removing originals. Inference weights cannot replace optimizer-containing checkpoints. Third-party paper PDFs are not newly republished; keep personal copies for offline reading.

`completed-repository.zip` is a verified portable copy of the finished package, without Git internals or runtime outputs. It is also stored in the private backup directory. `.gitattributes` disables automatic line-ending conversion so archived file hashes remain meaningful across checkouts.

## Before removing source folders

1. Verify the completed GitHub commit and final model file.
2. Confirm the author's [Drive dataset backup](https://drive.google.com/drive/folders/1uC7HJFWZ-ysFRPSJ_Fdu5yY4Ul3Erd9-?usp=sharing) downloads successfully and contains all 37,142 V5 images, corresponding labels and configuration. The URL alone is not a verified backup.
3. Move private checkpoint/label ZIPs to external storage or Drive and verify they open.
4. Keep offline article PDFs and any raw images separately needed. Exact manifests still require source pixels/labels or the actual V5 archive.
5. Then remove obsolete subsets, environments, caches and redundant local projects if no longer needed.

No original dataset directory is deleted by this packaging operation. Full raw data, environments and package caches are not duplicated into Git. Historical authoring tools preserve context but should not be executed indiscriminately.

Reevaluation can differ slightly across software/hardware. Raw filename edits after V5 construction make exact-manifest restoration preferable. Archive preservation does not assert that every older explanation or one-off script was correct.
