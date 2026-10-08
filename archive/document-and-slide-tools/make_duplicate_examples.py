import csv
from pathlib import Path
from PIL import Image, ImageDraw

base=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\مدارک تکمیلی و منابع شکل‌ها')
ds=Path(r'D:\projects\car-detection-yolo\dataset\iadd_subset_v4\images')
out=base/'شواهد بازبینی'/'جفت‌ویدیوهای_مشکوک.jpg'
rows=list(csv.DictReader((base/'داده‌های نمودار و جدول'/'duplicate_pair_audit.csv').open(encoding='utf-8-sig')))
canvas=Image.new('RGB',(1200,3*390),'white')
d=ImageDraw.Draw(canvas)
for i,row in enumerate(rows):
    for j,col in enumerate(('example_a','example_b')):
        matches=list(ds.glob('*'+'/'+row[col]))
        if not matches: continue
        with Image.open(matches[0]) as im:
            im=im.convert('RGB'); im.thumbnail((580,330))
            x=10+j*600; y=i*390+35
            canvas.paste(im,(x,y))
            d.text((x,i*390+8),row[col],fill='black')
    d.text((10,i*390+365),f"dHash distance={row['best_distance']} | {row['video_a']} vs {row['video_b']}",fill='black')
canvas.save(out,quality=92)
print(out)
