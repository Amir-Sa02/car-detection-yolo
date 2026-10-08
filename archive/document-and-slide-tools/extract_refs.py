from docx import Document
import sys
sys.stdout.reconfigure(encoding="utf-8")
p=r"D:\projects\car-detection-yolo\thesis\ارائه\مطالعات قبل از ارائه\اسناد اصلی\پایان‌نامه_نهایی.docx"
d=Document(p)
for para in d.paragraphs:
    t=" ".join(para.text.split())
    if t.startswith("[13]") or t.startswith("[14]") or t.startswith("[۱۳]") or t.startswith("[۱۴]"):
        print(t)
