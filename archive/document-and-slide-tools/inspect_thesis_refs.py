from pathlib import Path
from zipfile import ZipFile
from lxml import etree

p=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx')
with ZipFile(p) as z:
 r=etree.fromstring(z.read('word/document.xml'))
 ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 ps=r.xpath('.//w:body//w:p',namespaces=ns)
 print('all paragraphs',len(ps))
 for i,par in enumerate(ps[-120:],len(ps)-120):
  t=''.join(par.xpath('.//w:t/text()',namespaces=ns))
  if t.strip(): print(i,repr(t[:800]))
 print('\nMETRICS')
 for i,par in enumerate(ps):
  t=''.join(par.xpath('.//w:t/text()',namespaces=ns))
  if ('نسبت هم‌پوشانی' in t or 'دقت متوسط' in t or 'فراخوانی' in t) and i<400:
   print(i,repr(t[:650]))
 print('\nMAP SECTION')
 for i in range(273,293):
  t=''.join(ps[i].xpath('.//w:t/text()',namespaces=ns))
  if t.strip(): print(i,repr(t[:900]))
