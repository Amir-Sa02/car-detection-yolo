from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
from pathlib import Path
import tempfile,os
P=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx'); W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; M='http://schemas.openxmlformats.org/officeDocument/2006/math'; NS={'w':W,'m':M}
def q(n,t):return f'{{{n}}}{t}'
def text(e):return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
with ZipFile(P) as z:files={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(files['word/document.xml'])
p=next(x for x in root.xpath('//w:p',namespaces=NS) if text(x).startswith('بسیاری از پژوهش‌ها YOLOv11'))
links=p.xpath('./w:hyperlink[@w:anchor="_ref_8"]',namespaces=NS)
if len(links)!=2:raise RuntimeError(f'expected 2 ref8 links, got {len(links)}')
second=links[1]; prev=second.getprevious()
if prev is None or '،' not in text(prev):raise RuntimeError('separator before duplicate citation not found')
p.remove(prev);p.remove(second)
files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
fd,tmp=tempfile.mkstemp(suffix='.docx',dir=str(P.parent));os.close(fd)
with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
 for n,d in files.items():z.writestr(n,d)
os.replace(tmp,P)
print(text(p))
