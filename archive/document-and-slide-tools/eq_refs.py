from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
for term in ['(۱\u200f-\u200f۶)','(۱\u200f-\u200f۷)','(۱\u200f-\u200f۸)','رابطه (۱\u200f-\u200f۶)','رابطه (۱\u200f-\u200f۷)','رابطه (۱\u200f-\u200f۸)']:
 hits=[]
 for p0 in root.xpath('//w:p',namespaces=NS):
  t=''.join(p0.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS))
  if term in t: hits.append(t[:400])
 print(term, len(hits)); [print(' ',x) for x in hits]
