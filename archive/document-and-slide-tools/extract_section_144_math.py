from zipfile import ZipFile
from lxml import etree
import sys
sys.stdout.reconfigure(encoding='utf-8')
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z:
 root=etree.fromstring(z.read('word/document.xml'))
 pars=root.xpath('.//w:body//w:p',namespaces=ns)
 rows=[]
 for i,par in enumerate(pars):
  plain=''.join(par.xpath('.//w:t/text()',namespaces=ns)).strip()
  math=''.join(par.xpath('.//m:t/text()',namespaces=ns)).strip()
  rows.append((i,plain,math))
 starts=[i for i,a,b in rows if a.strip()=='۱‏-‏۴‏-‏۴- دقت متوسط و میانگین دقت متوسط']
 print('starts',starts)
 s=starts[-1]
 for i,a,b in rows[s:s+25]:
  if a or b: print(i,'TEXT=',a,'MATH=',b)
