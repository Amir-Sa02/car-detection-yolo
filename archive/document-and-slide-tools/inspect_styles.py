import zipfile
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
r=etree.fromstring(zipfile.ZipFile(r'D:\projects\car-detection-yolo\thesis\پایان‌نامه_نهایی.docx').read('word/styles.xml'))
for sid in ['FootnoteText','FootnoteReference','Normal']:
    s=next((x for x in r.findall(W+'style') if x.get(W+'styleId')==sid),None)
    print(sid, etree.tostring(s,encoding='unicode') if s is not None else 'missing')
