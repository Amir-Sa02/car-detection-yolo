import fitz, os
pdf=r'C:\Users\amir2\Desktop\cat-claude\qa_map_20260922_1220\thesis.pdf'
out=r'C:\Users\amir2\Desktop\cat-claude\qa_map_20260922_1220'
d=fitz.open(pdf)
for i,p in enumerate(d):
    t=p.get_text()
    if 'دقت متوسط و میانگین دقت متوسط' in t or 'mAP@0.5:0.95' in t:
        print('page',i+1,repr(t[:500]))
        pix=p.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False)
        path=os.path.join(out,f'page-{i+1}.png'); pix.save(path); print(path)
