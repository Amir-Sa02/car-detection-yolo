from zipfile import ZipFile
from lxml import etree
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")
path=Path(r"C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx")
ns={
 'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
 'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
}
with ZipFile(path) as z:
 root=etree.fromstring(z.read('word/document.xml'))
 body=root.find('w:body',ns)
 paras=body.xpath('./w:p',namespaces=ns)
 texts=[]
 for p in paras:
  t=''.join(p.xpath('.//w:t/text() | .//m:t/text()',namespaces=ns)).strip()
  texts.append(t)
 candidates=[i for i,t in enumerate(texts) if '۱‏-‏۴‏-‏۴' in t or ('دقت متوسط' in t and 'میانگین دقت متوسط' in t)]
 print('CANDIDATES',candidates)
 for ci in candidates:
  print('C',ci,texts[ci])
 start=221
 for i in range(start,min(len(paras),start+40)):
  p=paras[i]
  t=texts[i]
  if t:
   print(f'P{i}: {t}')
  maths=p.xpath('.//m:oMath | .//m:oMathPara',namespaces=ns)
  if maths:
   for j,math in enumerate(maths):
    mt=''.join(math.xpath('.//m:t/text()',namespaces=ns))
    print(f'  MATH{j}: {mt}')
