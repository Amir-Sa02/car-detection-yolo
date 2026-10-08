from zipfile import ZipFile
from lxml import etree
from collections import Counter
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z:
 assert z.testzip() is None
 root=etree.fromstring(z.read('word/document.xml'))
 body=root.find('w:body',NS); children=list(body)
def text(e):return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
# bookmark uniqueness and link validity
names=root.xpath('//w:bookmarkStart/@w:name',namespaces=NS); dup=[k for k,v in Counter(names).items() if v>1]
anchors=root.xpath('//w:hyperlink/@w:anchor',namespaces=NS); broken=[a for a in anchors if a.startswith('_ref_') and a not in set(names)]
# first appearance order
first=[]
for e in children:
 if e.xpath('.//w:bookmarkStart[starts-with(@w:name,"_ref_")]',namespaces=NS): continue
 for h in e.xpath('.//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS):
  n=int(h.get('{%s}anchor'%NS['w']).split('_')[-1])
  if n not in first:first.append(n)
section='\n'.join(text(e) for e in children if 225<=children.index(e)<=240)
print('zip=ok dup_bookmarks=',dup,'broken_refs=',broken)
print('first_order=',first)
print('eq_labels=',[text(t) for t in children if etree.QName(t).localname=='tbl' and text(t).startswith('(۱')][:20])
print('has_1_8=', '(۱\u200f-\u200f۸)' in section, 'footnotes35_36=', len(root.xpath('//w:footnoteReference[@w:id="35" or @w:id="36"]',namespaces=NS)))
print('file_size=',__import__('os').path.getsize(p))
