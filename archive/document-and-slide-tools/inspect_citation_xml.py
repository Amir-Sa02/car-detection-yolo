from zipfile import ZipFile
from lxml import etree
DOCX=r"C:\Users\amir2\Desktop\cat-claude\thesis_refs_audit.docx"
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}
def txt(e): return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
with ZipFile(DOCX) as z:
 r=etree.fromstring(z.read('word/document.xml'))
 for p in r.xpath('//w:body//w:p',namespaces=NS):
  if '[۱]' in txt(p) and 'خودروهای خودران' in txt(p):
   print(etree.tostring(p,encoding='unicode',pretty_print=True)); break
