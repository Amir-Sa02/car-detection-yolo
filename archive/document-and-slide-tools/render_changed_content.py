import fitz,os
pdf=r'C:\Users\amir2\Desktop\cat-claude\qa_reduced_refs_final\thesis.pdf';out=os.path.dirname(pdf);d=fitz.open(pdf)
for i,p in enumerate(d):
 t=p.get_text()
 if 'C2PSA' in t or ('Faster' in t and 'R-CNN' in t):
  print(i+1,repr(t[:120]));p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False).save(os.path.join(out,f'content-{i+1}.png'))
