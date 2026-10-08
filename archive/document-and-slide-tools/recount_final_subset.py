"""Recount V5 tables from YOLO label files. Read-only on the dataset.

Usage: python recount_final_subset.py --dataset D:\\projects\\car-detection-yolo\\dataset\\iadd_subset_v5
The output is a JSON file beside this script unless --output is supplied.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

def recount(root: Path) -> dict:
    result = {}
    for split in ('train', 'val', 'test'):
        images = sorted((root/'images'/split).glob('*.jpg'))
        videos = set()
        cls, size, cond = Counter(), Counter(), Counter()
        instances = 0
        for img in images:
            video = img.stem.split('__')[0]
            videos.add(video)
            cond[video.rsplit('_',1)[-1]] += 1
            label = root/'labels'/split/(img.stem+'.txt')
            if not label.exists(): continue
            for line in label.read_text(encoding='utf-8').splitlines():
                parts = line.split()
                if len(parts) != 5: continue
                category = int(parts[0]); area = float(parts[3])*float(parts[4])
                cls[category] += 1
                size[0 if area < .01 else 1 if area < .06 else 2] += 1
                instances += 1
        result[split] = {
            'images':len(images),'videos':len(videos),'instances':instances,
            'instances_per_image': round(instances/len(images),4),
            'cls':{str(i):cls[i] for i in range(6)},
            'size':{str(i):size[i] for i in range(3)},
            'cond':dict(sorted(cond.items()))
        }
    return result

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset',type=Path,default=Path(r'D:\projects\car-detection-yolo\dataset\iadd_subset_v5'))
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('recount_v5.json'))
    a=ap.parse_args()
    stats=recount(a.dataset)
    a.output.write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    for split,item in stats.items():
        print(split, 'videos=',item['videos'],'images=',item['images'],
              'boxes=',item['instances'],'boxes/image=',item['instances_per_image'])
    print('saved',a.output)
