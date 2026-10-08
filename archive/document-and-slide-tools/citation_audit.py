from zipfile import ZipFile
from lxml import etree
from collections import defaultdict
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); children=list(body)
def txt(e): return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
# references
refs={}
for e in children:
 names=e.xpath('.//w:bookmarkStart/@w:name',namespaces=NS)
 for name in names:
  if name.startswith('_ref_'):
   refs[int(name.split('_')[-1])]=txt(e)
# citations by top-level body item, one count per hyperlink
uses=defaultdict(list)
for i,e in enumerate(children):
 if any(n.startswith('_ref_') for n in e.xpath('.//w:bookmarkStart/@w:name',namespaces=NS)): continue
 for h in e.xpath('.//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS):
  n=int(h.get('{%s}anchor'%NS['w']).split('_')[-1]); uses[n].append((i,txt(e)))
for n in sorted(refs):
 print('\n'+'='*100)
 print(f'REF {n} HYPERLINKS {len(uses[n])}')
 print(refs[n])
 seen=[]
 for i,t in uses[n]:
  key=(i,t)
  if key not in seen: seen.append(key)
 for i,t in seen: print(f'  CHILD {i}: {t}')
