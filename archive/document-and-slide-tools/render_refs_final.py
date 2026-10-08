import fitz,os
pdf=r'C:\Users\amir2\Desktop\cat-claude\qa_reduced_refs_final\thesis.pdf';out=os.path.dirname(pdf);d=fitz.open(pdf);print('pages',len(d))
for i,p in enumerate(d):
 t=p.get_text()
 if 'Object Detection in 20 Years' in t or 'Decoupled Weight Decay' in t:
  path=os.path.join(out,f'page-{i+1}.png');p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False).save(path);print(path)
