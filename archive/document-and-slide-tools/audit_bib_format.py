import zipfile,re,collections
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
z=zipfile.ZipFile(r'D:\projects\car-detection-yolo\thesis\پایان‌نامه_نهایی.docx')
r=etree.fromstring(z.read('word/document.xml'))
started=False
for p in r.iter(W+'p'):
 t=''.join(p.itertext()).strip()
 if t in ('مراجع و منابع','منابع و مراجع'): started=True;continue
 if not started or not t: continue
 if not re.match(r'^\[[۰-۹0-9]+\]',t) and not t.startswith('http'): continue
 vals=[]
 for run in p.iter(W+'r'):
  txt=''.join(run.itertext());
  if not txt:continue
  rp=run.find(W+'rPr');f=rp.find(W+'rFonts') if rp is not None else None;sz=rp.find(W+'sz') if rp is not None else None;cs=rp.find(W+'szCs') if rp is not None else None;i=rp.find(W+'i') if rp is not None else None
  vals.append((txt,f.get(W+'ascii') if f is not None else None,f.get(W+'cs') if f is not None else None,sz.get(W+'val') if sz is not None else None,cs.get(W+'val') if cs is not None else None,i is not None))
 print(t[:85]);print(vals)
