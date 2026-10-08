from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
from copy import deepcopy
from pathlib import Path
import tempfile,os
P=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx')
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; M='http://schemas.openxmlformats.org/officeDocument/2006/math'; XML='http://www.w3.org/XML/1998/namespace'; NS={'w':W,'m':M}
def q(n,t): return f'{{{n}}}{t}'
def textof(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()
def fa(n): return str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
def rpr(kind):
 p=etree.Element(q(W,'rPr')); f=etree.SubElement(p,q(W,'rFonts'))
 if kind=='fa':
  f.set(q(W,'ascii'),'Times New Roman');f.set(q(W,'hAnsi'),'Times New Roman');f.set(q(W,'cs'),'B Zar');etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),'28');etree.SubElement(p,q(W,'rtl')); l=etree.SubElement(p,q(W,'lang'));l.set(q(W,'val'),'fa-IR');l.set(q(W,'bidi'),'fa-IR')
 else:
  f.set(q(W,'ascii'),'Times New Roman');f.set(q(W,'hAnsi'),'Times New Roman');f.set(q(W,'cs'),'Times New Roman');etree.SubElement(p,q(W,'sz')).set(q(W,'val'),'24');etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),'24');etree.SubElement(p,q(W,'lang')).set(q(W,'bidi'),'en-US')
 return p
def add_run(p,s,k='fa'):
 r=etree.SubElement(p,q(W,'r'));r.append(rpr(k));t=etree.SubElement(r,q(W,'t'));t.text=s
 if s.startswith(' ') or s.endswith(' '):t.set(q(XML,'space'),'preserve')
def mr(s):
 r=etree.Element(q(M,'r'));rp=etree.SubElement(r,q(W,'rPr'));f=etree.SubElement(rp,q(W,'rFonts'));f.set(q(W,'ascii'),'Cambria Math');f.set(q(W,'hAnsi'),'Cambria Math');etree.SubElement(rp,q(W,'sz')).set(q(W,'val'),'24');etree.SubElement(rp,q(W,'szCs')).set(q(W,'val'),'24');etree.SubElement(r,q(M,'t')).text=s;return r
def ssub(base,sub):
 s=etree.Element(q(M,'sSub'));sp=etree.SubElement(s,q(M,'sSubPr'));cp=etree.SubElement(sp,q(M,'ctrlPr'));rp=etree.SubElement(cp,q(W,'rPr'));f=etree.SubElement(rp,q(W,'rFonts'));f.set(q(W,'ascii'),'Cambria Math');f.set(q(W,'hAnsi'),'Cambria Math'); e=etree.SubElement(s,q(M,'e')); e.append(mr(base)); su=etree.SubElement(s,q(M,'sub'));su.append(mr(sub));return s
def add_math(p,kind):
 om=etree.SubElement(p,q(M,'oMath'))
 if kind=='APi05': om.extend([ssub('AP','i'),mr('(0.5)')])
 elif kind=='IoUj': om.append(ssub('IoU','j'))
 elif kind=='APiIoUj': om.extend([ssub('AP','i'),mr('('),ssub('IoU','j'),mr(')')])
def add_cite(p,n):
 add_run(p,' \u200f[');h=etree.SubElement(p,q(W,'hyperlink'));h.set(q(W,'anchor'),f'_ref_{n}');h.set(q(W,'history'),'1');r=etree.SubElement(h,q(W,'r'));r.append(rpr('fa'));etree.SubElement(r,q(W,'t')).text=fa(n);add_run(p,']\u200f:')
def rebuild(p,items,cite=None):
 pp=p.find(q(W,'pPr'));saved=deepcopy(pp)
 for c in list(p):p.remove(c)
 p.append(saved)
 for typ,s in items:
  if typ=='fa':add_run(p,s,'fa')
  elif typ=='en':add_run(p,s,'en')
  elif typ=='math':add_math(p,s)
 if cite:add_cite(p,cite)
with ZipFile(P) as z:files={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(files['word/document.xml']);body=root.find(q(W,'body'));ch=list(body)
idx=next(i for i,e in enumerate(ch) if etree.QName(e).localname=='p' and textof(e).startswith('۱\u200f-\u200f۴\u200f-\u200f۴-') and not e.xpath('./w:pPr/w:pStyle',namespaces=NS))
p_iou=ch[idx+5]; p_sum=ch[idx+10]
rebuild(p_iou,[('fa','در تشخیص اشیا، درست‌بودن یک پیش‌بینی افزون بر برچسب رده، به میزان هم‌پوشانی کادر پیش‌بینی‌شده با کادر واقعی وابسته است. این هم‌پوشانی با معیار '),('en','IoU'),('fa',' سنجیده می‌شود. در نماد '),('math','APi05'),('fa','، زیرنویس '),('en','i'),('fa',' رده مورد ارزیابی و عدد ۰٫۵ آستانه نسبت هم‌پوشانی است؛ بنابراین پیش‌بینی زمانی مثبت درست محسوب می‌شود که رده آن صحیح و مقدار '),('en','IoU'),('fa',' دست‌کم ۰٫۵ باشد. میانگین '),('math','APi05'),('fa',' روی '),('en','N'),('fa',' رده، معیار '),('en','mAP@0.5'),('fa',' را مطابق رابطه (۱\u200f-\u200f۶) به‌دست می‌دهد')],13)
rebuild(p_sum,[('fa','در رابطه (۱\u200f-\u200f۷)، '),('math','IoUj'),('fa',' آستانه شماره '),('en','j'),('fa',' است که از ۰٫۵ آغاز می‌شود و در هر گام ۰٫۰۵ افزایش می‌یابد؛ همچنین '),('math','APiIoUj'),('fa',' دقت متوسط رده '),('en','i'),('fa',' در همان آستانه را نشان می‌دهد. در نتیجه، عدد یا بازه پس از علامت '),('en','@'),('fa',' آستانه هم‌پوشانی را مشخص می‌کند و با آستانه اطمینان تفاوت دارد. معیار '),('en','mAP@0.5'),('fa',' عملکرد مدل را در آستانه ۰٫۵ می‌سنجد؛ '),('en','mAP@0.5:0.95'),('fa',' نیز با میانگین‌گیری در چند آستانه، کیفیت مکان‌یابی کادرها را سخت‌گیرانه‌تر ارزیابی می‌کند. در این پروژه هر دو معیار گزارش شده‌اند.')])
files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
fd,tmp=tempfile.mkstemp(suffix='.docx',dir=str(P.parent));os.close(fd)
with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
 for n,d in files.items():z.writestr(n,d)
os.replace(tmp,P)
