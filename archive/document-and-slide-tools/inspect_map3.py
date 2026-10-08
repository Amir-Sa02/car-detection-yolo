from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); ch=list(body)
def txt(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
for i in [228,232,235,238]:
 print('\n#####',i,txt(ch[i]))
 print(etree.tostring(ch[i],encoding='unicode',pretty_print=True))
print('\nBIB ENTRIES')
for i,e in enumerate(ch):
 t=txt(e)
 if t.startswith('[۱۳]') or t.startswith('[۱۴]') or t.startswith('[۲۱]'):
  print(i,repr(t[:500])); print(etree.tostring(e,encoding='unicode',pretty_print=True)[:5000])
