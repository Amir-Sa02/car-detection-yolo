from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); children=list(body)
def txt(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
for p0 in root.xpath('//w:p',namespaces=NS):
 t=txt(p0)
 if 'دقت متوسط و میانگین دقت متوسط' in t:
  top=p0
  while top.getparent() is not body: top=top.getparent()
  print('occ',children.index(top), etree.QName(top).localname, t[:100], 'style',p0.xpath('./w:pPr/w:pStyle/@w:val',namespaces=NS))
# find body section by exact starting and print 25 body elems
idxs=[]
for i,ch in enumerate(children):
 if 'دقت متوسط و میانگین دقت متوسط' in txt(ch): idxs.append(i)
print('idxs',idxs)
idx=idxs[-1]
for i in range(idx,idx+20): print(i,etree.QName(children[i]).localname,repr(txt(children[i])[:500]))
