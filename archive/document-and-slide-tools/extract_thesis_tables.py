from docx import Document
p=r"D:\projects\car-detection-yolo\thesis\ارائه\مطالعات قبل از ارائه\اسناد اصلی\پایان‌نامه_نهایی.docx"
d=Document(p)
for i,t in enumerate(d.tables):
    rows=[[c.text.replace('\n',' / ').strip() for c in r.cells] for r in t.rows]
    blob=' | '.join(' | '.join(r) for r in rows)
    if any(k in blob for k in ['۰٫۸۷۴','AdamW','۲۶٬۰۰۰','۲۰۴٬۰۰۹','YOLOv11s','۱۲۸۰']):
        print('\nTABLE',i)
        for r in rows: print(' || '.join(r))
