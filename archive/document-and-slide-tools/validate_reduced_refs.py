from zipfile import ZipFile
from lxml import etree
from collections import Counter,defaultdict
import re,os
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z:
 bad=z.testzip(); root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); children=list(body)
def txt(e):return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
bookmarks=root.xpath('//w:bookmarkStart/@w:name',namespaces=NS); refnames=sorted((int(x.split('_')[-1]) for x in bookmarks if re.fullmatch(r'_ref_\d+',x)))
links=root.xpath('//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS); bset=set(bookmarks); broken=[]; uses=defaultdict(list); first=[]
for h in links:
 a=h.get('{%s}anchor'%NS['w']);
 if a not in bset: broken.append(a)
 n=int(a.split('_')[-1]); uses[n].append(txt(h))
 top=h
 while top.getparent() is not body:top=top.getparent()
 if not top.xpath('.//w:bookmarkStart[starts-with(@w:name,"_ref_")]',namespaces=NS) and n not in first:first.append(n)
print('zip_bad',bad,'refs',refnames,'broken',broken,'first',first)
print('dup bookmarks',[k for k,v in Counter(bookmarks).items() if v>1])
print('usecounts',{n:len(uses[n]) for n in refnames})
print('\nBIB')
for e in children:
 ns=e.xpath('.//w:bookmarkStart/@w:name',namespaces=NS)
 if ns and re.fullmatch(r'_ref_\d+',ns[0]):print(ns[0],txt(e))
print('\nREPLACEMENT CONTEXTS')
for needle in ['فستر آر-سی','نمونه شاخص دیگر این خانواده','موزاییک است که','یافتن اشیای کوچک','بسیاری از پژوهش‌ها YOLOv11','خطای کانونی','اصل دوم، به نحوه گزارش']:
 for e in children:
  if needle in txt(e):print('\n',txt(e))
print('size',os.path.getsize(p))
