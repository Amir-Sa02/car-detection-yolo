from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); children=list(body)
def txt(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
for n in range(1,22):
 hits=[]
 for h in root.xpath(f'//w:hyperlink[@w:anchor="_ref_{n}"]',namespaces=NS):
  top=h
  while top.getparent() is not body: top=top.getparent()
  i=children.index(top)
  if i<470: hits.append((i,txt(top)[:220],txt(h)))
 print(n, hits[:8])
