from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,re,sys
from pypdf import PdfReader
sys.stdout.reconfigure(encoding='utf-8')
p=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع\۰۱_آموزش_گام‌به‌گام_معماری_YOLOv11s.docx')
n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(p) as z:x=E.fromstring(z.read('word/document.xml'))
plain_runs=x.xpath('//w:r[w:t]',namespaces=n)
latin_fonts=set();persian_fonts=set();latin_sizes=set();persian_sizes=set()
for r in plain_runs:
 rtl=r.xpath('string(w:rPr/w:rtl/@w:val)',namespaces=n)
 font=r.xpath('string(w:rPr/w:rFonts/@w:cs)',namespaces=n)
 size=r.xpath('string(w:rPr/w:szCs/@w:val)',namespaces=n)
 if rtl=='0':latin_fonts.add(font);latin_sizes.add(size)
 else:persian_fonts.add(font);persian_sizes.add(size)
assert latin_fonts=={'Times New Roman'},latin_fonts
assert persian_fonts=={'B Zar'},persian_fonts
assert latin_sizes <= {'22','24','28'},latin_sizes
assert persian_sizes <= {'24','26','30','34'},persian_sizes
assert not re.search('[\u064b-\u0652\u0670]',''.join(x.xpath('//w:t/text()',namespaces=n)))
assert len(PdfReader('architecture_conceptual_qa/architecture.pdf').pages)==11
report={'pages':11,'native_equations':len(x.xpath('//m:oMath',namespaces=n)),'latin_fonts':sorted(latin_fonts),'latin_halfpoint_sizes':sorted(latin_sizes),'persian_fonts':sorted(persian_fonts),'persian_halfpoint_sizes':sorted(persian_sizes),'diacritics':0}
Path('architecture_conceptual_qa/font_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

