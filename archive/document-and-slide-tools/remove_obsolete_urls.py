from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
from pathlib import Path
import tempfile,os
P=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'); W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; M='http://schemas.openxmlformats.org/officeDocument/2006/math'; NS={'w':W,'m':M}
def text(e):return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
with ZipFile(P) as z:files={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(files['word/document.xml'])
urls={'https://arxiv.org/abs/2502.04161','https://arxiv.org/abs/2410.17725'}
removed=[]
for p in list(root.xpath('//w:body/w:p',namespaces=NS)):
 if text(p) in urls:
  removed.append(text(p));p.getparent().remove(p)
if set(removed)!=urls:raise RuntimeError(f'expected both obsolete URLs, removed={removed}')
files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
fd,tmp=tempfile.mkstemp(suffix='.docx',dir=str(P.parent));os.close(fd)
with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
 for n,d in files.items():z.writestr(n,d)
os.replace(tmp,P)
print(removed)
