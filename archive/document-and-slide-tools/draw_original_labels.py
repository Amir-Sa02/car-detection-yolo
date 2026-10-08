"""Draw the dataset's original YOLO labels on frames of one V4 video.

Read-only on V4. Example:
  python draw_original_labels.py --video Record426_D --limit 4
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NAMES=('person','car','motorcycle','bus','truck','traffic_light')
COLORS=('#e63946','#277da1','#43aa8b','#f8961e','#7b2cbf','#00a6a6')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset',type=Path,default=Path(r'D:\projects\car-detection-yolo\dataset\iadd_subset_v4'))
    ap.add_argument('--video',required=True)
    ap.add_argument('--limit',type=int,default=4)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent.parent/'شواهد بازبینی'/'بازرسم برچسب‌ها')
    a=ap.parse_args()
    paths=[]
    for split in ('train','val','test'):
        paths.extend((a.dataset/'images'/split).glob(a.video+'__*.jpg'))
    paths=sorted(paths)
    if not paths: raise SystemExit(f'No frames for {a.video}; check --dataset')
    chosen=[paths[round(i*(len(paths)-1)/(min(a.limit,len(paths))-1))] for i in range(min(a.limit,len(paths)))] if len(paths)>1 and a.limit>1 else paths[:1]
    a.out.mkdir(parents=True,exist_ok=True)
    try: font=ImageFont.truetype('arial.ttf',16)
    except OSError: font=ImageFont.load_default()
    for p in chosen:
        split=p.parent.name; label=a.dataset/'labels'/split/(p.stem+'.txt')
        with Image.open(p) as source: image=source.convert('RGB')
        W,H=image.size; draw=ImageDraw.Draw(image)
        if label.exists():
            for line in label.read_text(encoding='utf-8').splitlines():
                q=line.split()
                if len(q)!=5: continue
                c=int(q[0]); cx,cy,w,h=map(float,q[1:])
                xy=((cx-w/2)*W,(cy-h/2)*H,(cx+w/2)*W,(cy+h/2)*H)
                draw.rectangle(xy,outline=COLORS[c],width=3)
                draw.text((xy[0],max(0,xy[1]-19)),NAMES[c],fill=COLORS[c],font=font)
        out=a.out/(p.stem+'_original_labels.jpg')
        image.save(out,quality=90)
        print(out)
    print('Boxes come from the original label files; no model inference is used.')

if __name__=='__main__': main()
