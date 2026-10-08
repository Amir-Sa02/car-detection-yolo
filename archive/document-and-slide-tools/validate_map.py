from zipfile import ZipFile
from lxml import etree
from collections import Counter
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z:
 root=etree.fromstring(z.read('word/document.xml'))
 body=root.find('w:body',NS); ch=list(body)
def text(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
idx=next(i for i,e in enumerate(ch) if etree.QName(e).localname=='p' and text(e).startswith('۱\u200f-\u200f۴\u200f-\u200f۴-') and not e.xpath('./w:pPr/w:pStyle',namespaces=NS))
print('SECTION')
for e in ch[idx:idx+12]: print(etree.QName(e).localname, text(e))
print('\nREFS')
for e in ch:
 names=e.xpath('.//w:bookmarkStart/@w:name',namespaces=NS)
 if names and names[0].startswith('_ref_'):
  n=int(names[0].split('_')[-1])
  if 12<=n<=22: print(n,text(e)[:230])
print('\nLINK CHECK')
bookmarks=set(root.xpath('//w:bookmarkStart/@w:name',namespaces=NS))
links=root.xpath('//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS)
print('links',len(links),'broken',[(h.get('{%s}anchor'%NS['w']),text(h)) for h in links if h.get('{%s}anchor'%NS['w']) not in bookmarks])
for n in range(1,23):
 print(n,sum(1 for h in links if h.get('{%s}anchor'%NS['w'])==f'_ref_{n}'))
