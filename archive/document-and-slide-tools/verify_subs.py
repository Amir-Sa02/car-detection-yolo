import fitz,re
files={
'survey':r'D:\projects\car-detection-yolo\thesis\مراجع\Object Detection in 20 Years A Survey.pdf',
'review':r'D:\projects\car-detection-yolo\thesis\مراجع\Sapkota 2025 - YOLO Decadal Comprehensive Review.pdf',
'new13':r'C:\Users\amir2\Desktop\s41598-026-35743-8.pdf'}
for key,path in files.items():
 text=re.sub(r'\s+',' ','\n'.join(p.get_text() for p in fitz.open(path)))
 print('\n##',key)
 for pat in ['focal loss','YOLOv1','first YOLO','mosaic data augmentation','C2PSA','spatial attention','precision and recall','trade-off','average precision','IoU threshold']:
  ms=list(re.finditer(re.escape(pat),text,re.I))
  print(pat,len(ms))
  if ms:
   m=ms[0]; print(text[max(0,m.start()-180):m.end()+300])
