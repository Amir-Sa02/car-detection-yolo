import fitz,os
pdf=r'C:\Users\amir2\Desktop\cat-claude\qa_reduced_refs_20260922\thesis.pdf'; out=os.path.dirname(pdf);d=fitz.open(pdf);print('PDF_PAGES',len(d))
need=['فستر آر','اشیای کوچک، یکی از دشوارترین','بسیاری از پژوهش','Object Detection in 20 Years','Decoupled Weight Decay']
found=[]
for i,p in enumerate(d):
 t=p.get_text()
 if any(x in t for x in need):
  found.append(i+1); pix=p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False);pix.save(os.path.join(out,f'page-{i+1}.png'))
print('RENDERED',found)
