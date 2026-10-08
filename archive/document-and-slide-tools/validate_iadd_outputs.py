from pathlib import Path
import re, zipfile
from lxml import etree
import fitz

out_dir = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه مقاله IADD')
pdf = out_dir / 'مقاله_IADD_هایلایت_مطالعه_دفاع.pdf'
docx = out_dir / 'راهنمای_فارسی_مطالعه_مقاله_IADD.docx'
src = next(Path(r'D:\projects\car-detection-yolo\thesis\مراجع').glob('IET Image Processing*Multi*domain autonomous driving dataset*.pdf'))

s=fitz.open(src); o=fitz.open(pdf)
print('pdf_pages', s.page_count, o.page_count)
print('text_equal', ''.join(p.get_text() for p in s) == ''.join(p.get_text() for p in o))
subj={}
for p in o:
    for a in p.annots() or []:
        info=a.info
        subject=info.get('subject') or a.type[1]
        subj[subject]=subj.get(subject,0)+1
print('annotation_subjects', subj)
s.close(); o.close()

with zipfile.ZipFile(docx) as z:
    xml_parts=[n for n in z.namelist() if n.startswith('word/') and n.endswith('.xml')]
    text=''
    for n in xml_parts:
        data=z.read(n)
        try:
            root=etree.fromstring(data)
        except Exception:
            continue
        text += ''.join(root.xpath('//w:t/text()', namespaces={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}))
    marks=re.findall(r'[\u064B-\u065F\u0670\u06D6-\u06ED]',text)
    print('docx_diacritic_marks',len(marks))
    print('docx_chars',len(text))
    print('docx_parts',len(z.namelist()))
print('outputs', [(p.name,p.stat().st_size) for p in out_dir.iterdir()])
