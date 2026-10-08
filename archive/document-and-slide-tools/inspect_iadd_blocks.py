from pathlib import Path
import fitz

p=Path(r"D:\projects\car-detection-yolo\thesis\مراجع\IET Image Processing - 2022 - Khosravian - Multi‐domain autonomous driving dataset  Towards enhancing the generalization of.pdf")
d=fitz.open(p)
for n in [1,2,5,6,7,8,9,11,12,13]:
    print("\n===== PAGE",n,"=====")
    for b in d[n-1].get_text("blocks"):
        x0,y0,x1,y1,text,*_=b
        text=" ".join(text.split())
        if text:
            print(f"{x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f} :: {text[:180]}")
