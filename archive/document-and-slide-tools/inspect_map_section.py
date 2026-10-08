from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); children=list(body)
def textof(ch): return ''.join(ch.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
idx=next(i for i,ch in enumerate(children) if 'دقت متوسط و میانگین دقت متوسط' in textof(ch) and etree.QName(ch).localname=='p')
print('heading child',idx)
for i in range(idx,idx+18):
 ch=children[i]; txt=textof(ch)
 print('\n###',i,etree.QName(ch).localname,repr(txt[:500]))
 print(etree.tostring(ch,encoding='unicode',pretty_print=True)[:8000])
