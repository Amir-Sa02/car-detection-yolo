"""Read-only visual audit of the three suspected duplicate-video pairs in V4.

This is a reproducible *supporting check*, not the original discovery log.
Requires Pillow. It writes only a CSV beside this script, never edits the dataset.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from statistics import median
from PIL import Image

PAIRS = [
    ('Record407_D', 'Record409_D'),
    ('Record416_R', 'Record438_R'),
    ('Record043_D', 'Record042_D'),
]

def frames(dataset: Path, video: str) -> list[Path]:
    result = []
    for split in ('train', 'val', 'test'):
        result.extend((dataset / 'images' / split).glob(video + '__*.jpg'))
    return sorted(result)

def sample(items: list[Path], limit: int = 32) -> list[Path]:
    if len(items) <= limit:
        return items
    return [items[round(i * (len(items)-1) / (limit-1))] for i in range(limit)]

def dhash(path: Path) -> int:
    with Image.open(path) as image:
        small = image.convert('L').resize((9, 8), Image.Resampling.LANCZOS)
        pix = list(small.get_flattened_data())
    value = 0
    for y in range(8):
        for x in range(8):
            value = (value << 1) | int(pix[y*9+x] > pix[y*9+x+1])
    return value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path(r'D:\projects\car-detection-yolo\dataset\iadd_subset_v4'))
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('duplicate_pair_audit.csv'))
    args = parser.parse_args()
    rows = []
    for a, b in PAIRS:
        aa, bb = sample(frames(args.dataset, a)), sample(frames(args.dataset, b))
        if not aa or not bb:
            print(f'{a} / {b}: missing frames; check --dataset')
            continue
        ah, bh = [(p, dhash(p)) for p in aa], [(p, dhash(p)) for p in bb]
        distances = [min((h ^ j).bit_count() for _, j in bh) for _, h in ah]
        best_i = min(range(len(ah)), key=lambda i: distances[i])
        best_j = min(range(len(bh)), key=lambda j: (ah[best_i][1] ^ bh[j][1]).bit_count())
        row = {'video_a':a,'video_b':b,'frames_a':len(frames(args.dataset,a)),
               'frames_b':len(frames(args.dataset,b)),'sampled_a':len(ah),'sampled_b':len(bh),
               'median_nearest_dhash_distance':median(distances),
               'best_distance':distances[best_i],
               'example_a':ah[best_i][0].name,'example_b':bh[best_j][0].name}
        rows.append(row)
        print(row)
    if rows:
        with args.output.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
        print('saved:',args.output)
    print('dHash is a screening signal. Inspect the matched frames and temporal sequence before calling a pair duplicated.')

if __name__ == '__main__': main()
