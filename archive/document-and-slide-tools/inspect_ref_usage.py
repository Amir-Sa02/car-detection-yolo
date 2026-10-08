from zipfile import ZipFile
from lxml import etree
import sys,re
sys.stdout.reconfigure(encoding='utf-8')
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(p) as z:
 root=etree.fromstring(z.read('word/document.xml'))
 paras=root.xpath('.//w:body//w:p',namespaces=ns)
 for target in ('_ref_12','_ref_13','_ref_14'):
  print('\nTARGET',target)
  for i,p in enumerate(paras):
   for h in p.xpath('.//w:hyperlink[@w:anchor=$a]',namespaces=ns,a=target):
    tx=''.join(p.xpath('.//w:t/text()',namespaces=ns)).strip()
    ht=''.join(h.xpath('.//w:t/text()',namespaces=ns)).strip()
    print(i,'H=',repr(ht),'P=',tx)
