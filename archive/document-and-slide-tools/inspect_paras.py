from zipfile import ZipFile
from lxml import etree
p=r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z: root=etree.fromstring(z.read('word/document.xml'))
body=root.find('w:body',NS); ch=list(body)
for i in [227,230,231,234,237,239,434,451]:
 print('\n###',i)
 print(etree.tostring(ch[i],encoding='unicode',pretty_print=True))
