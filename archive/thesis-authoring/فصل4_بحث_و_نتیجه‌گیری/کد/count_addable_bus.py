# -*- coding: utf-8 -*-
"""Evidence for the claim in 4-3-2: the bus class cannot be strengthened from
inside this dataset.

For every video that ended up in the v5 train split, this counts the bus
instances in ALL of its raw IADD frames and compares that with the bus
instances in the frames the sampling step actually kept. If the two are equal,
no bus instance was left on the table and the only way to add bus data is an
external source.

Result on 2026-08-25: 43,014 raw frames -> 1,022 bus instances, of which all
1,022 are already in the 26,000 kept frames. Addable = 0.

Run from D:\projects\car-detection-yolo. Takes a few minutes.
"""
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.join("dataset", "IADD")
V5  = os.path.join("dataset", "iadd_subset_v5")
used = {os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(V5, "images", "train", "*.jpg"))}
train_vids = {u.split("__", 1)[0] for u in used}
used_stems = {u.split("__", 1)[1] for u in used}
print("train videos", len(train_vids), "frames used", len(used), flush=True)
tot_bus = used_bus = tot_fr = used_fr = 0
for part in os.listdir(SRC):
    pdir = os.path.join(SRC, part)
    if not os.path.isdir(pdir):
        continue
    for rec in os.listdir(pdir):
        if rec not in train_vids:
            continue
        for lbl in glob.glob(os.path.join(pdir, rec, "**", "*.txt"), recursive=True):
            stem = os.path.splitext(os.path.basename(lbl))[0]
            try:
                n = sum(1 for ln in open(lbl) if ln.split()[:1] == ["3"])
            except Exception:
                continue
            tot_bus += n; tot_fr += 1
            if stem in used_stems:
                used_bus += n; used_fr += 1
print("raw frames of those videos:", tot_fr, "bus:", tot_bus)
print("already used in v5 train  :", used_fr, "bus:", used_bus)
print("ADDABLE bus instances     :", tot_bus - used_bus)
