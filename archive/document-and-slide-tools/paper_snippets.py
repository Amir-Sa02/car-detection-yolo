import fitz,re,os
files={
'survey':r'D:\projects\car-detection-yolo\thesis\مراجع\Object Detection in 20 Years A Survey.pdf',
'review':r'D:\projects\car-detection-yolo\thesis\مراجع\Sapkota 2025 - YOLO Decadal Comprehensive Review.pdf',
'y11overview':r'D:\projects\car-detection-yolo\thesis\مراجع\YOLOV11 AN OVERVIEW OF THE KEY ARCHITECTURAL.pdf',
'y4':r'D:\projects\car-detection-yolo\thesis\مراجع\YOLOV4 A BREAKTHROUGH IN REAL-TIME OBJECT.pdf',
'chaman12':r'D:\projects\car-detection-yolo\thesis\مراجع\Chaman 2025 - Real-Time Vehicle Detection ADAS YOLOv11 (ETASR).pdf',
'chaman21':r'D:\projects\car-detection-yolo\thesis\مراجع\Chaman 2025 - Comparative YOLOv11 vs YOLOv12 (IJTDI).pdf',
'new13':r'C:\Users\amir2\Desktop\s41598-026-35743-8.pdf',
}
patterns=['Faster R-CNN','region proposal','SSD','Single Shot MultiBox','YOLOv4','Mosaic','mosaic','anchor-free','anchor free','C2PSA','small object','Precision','Recall','confidence threshold','vehicle detection','autonomous vehicle']
for key,path in files.items():
 d=fitz.open(path); pages=[p.get_text('text') for p in d]; full='\n'.join(pages); norm=re.sub(r'\s+',' ',full)
 print('\n'+'#'*110+'\n',key,os.path.basename(path),'pages',len(d),'chars',len(full))
 for pat in patterns:
  m=re.search(re.escape(pat),norm,re.I)
  if m:
   a=max(0,m.start()-260);b=min(len(norm),m.end()+420)
   print(f'[{pat}]',norm[a:b])
