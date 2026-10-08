import zipfile
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
z=zipfile.ZipFile(r'D:\projects\car-detection-yolo\thesis\پایان‌نامه_نهایی.docx')
fr=etree.fromstring(z.read('word/footnotes.xml'))
for fn in fr.findall(W+'footnote'):
    if fn.get(W+'id')=='1': print(etree.tostring(fn,encoding='unicode'))
dr=etree.fromstring(z.read('word/document.xml'))
xs=dr.findall('.//'+W+'sectPr/'+W+'footnotePr')
print('sect footnotePr',len(xs))
for x in xs: print(etree.tostring(x,encoding='unicode'))
