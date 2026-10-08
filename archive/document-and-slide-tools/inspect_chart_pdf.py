from pathlib import Path
from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageDraw
import sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path('chart_guide_qa')
reader=PdfReader(root/'chart_guide.pdf')
for i,page in enumerate(reader.pages):
 text=page.extract_text() or ''
 print(i+1,len(text),text[:135].replace('\n',' | '))
imgs=convert_from_path(root/'chart_guide.pdf',dpi=90,poppler_path=r'C:\Users\amir2\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
for i,im in enumerate(imgs):im.save(root/f'page_{i+1:02d}.png')
for j in range(0,len(imgs),9):
 thumb=Image.new('RGB',(3*360,3*540),'#dddddd');draw=ImageDraw.Draw(thumb)
 for i,im in enumerate(imgs[j:j+9]):
  scaled=ImageOps.contain(im,(346,508));x=(i%3)*360+7;y=(i//3)*540+25
  thumb.paste(scaled,(x,y));draw.text((x,y-20),str(j+i+1),fill='black')
 thumb.save(root/f'contact_{j//9+1}.png')
