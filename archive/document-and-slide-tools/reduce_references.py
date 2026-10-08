from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from copy import deepcopy
from pathlib import Path
import os,tempfile,re

DOC=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx')
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; M='http://schemas.openxmlformats.org/officeDocument/2006/math'; XML='http://www.w3.org/XML/1998/namespace'; NS={'w':W,'m':M}
def q(ns,t): return f'{{{ns}}}{t}'
def textof(e): return ''.join(e.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS)).strip()
def fa(n): return str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))

def rpr_fa():
 p=etree.Element(q(W,'rPr')); f=etree.SubElement(p,q(W,'rFonts')); f.set(q(W,'ascii'),'Times New Roman'); f.set(q(W,'hAnsi'),'Times New Roman'); f.set(q(W,'cs'),'B Zar'); etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),'28'); etree.SubElement(p,q(W,'rtl')); l=etree.SubElement(p,q(W,'lang')); l.set(q(W,'val'),'fa-IR'); l.set(q(W,'bidi'),'fa-IR'); return p
def rpr_en():
 p=etree.Element(q(W,'rPr')); f=etree.SubElement(p,q(W,'rFonts')); f.set(q(W,'ascii'),'Times New Roman'); f.set(q(W,'hAnsi'),'Times New Roman'); f.set(q(W,'cs'),'Times New Roman'); etree.SubElement(p,q(W,'sz')).set(q(W,'val'),'24'); etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),'24'); etree.SubElement(p,q(W,'lang')).set(q(W,'bidi'),'en-US'); return p
def add_run(p,s,kind='fa'):
 r=etree.SubElement(p,q(W,'r')); r.append(rpr_fa() if kind=='fa' else rpr_en()); t=etree.SubElement(r,q(W,'t')); t.text=s
 if s.startswith(' ') or s.endswith(' '): t.set(q(XML,'space'),'preserve')
def add_hyper_num(p,n):
 h=etree.SubElement(p,q(W,'hyperlink')); h.set(q(W,'anchor'),f'_ref_{n}'); h.set(q(W,'history'),'1'); r=etree.SubElement(h,q(W,'r')); r.append(rpr_fa()); etree.SubElement(r,q(W,'t')).text=fa(n)
def add_citations(p,nums,colon=False):
 add_run(p,' [')
 for j,n in enumerate(nums):
  if j:add_run(p,'، ')
  add_hyper_num(p,n)
 add_run(p,']'+(':' if colon else ''))
def rebuild_small_object(p):
 ppr=p.find(q(W,'pPr')); saved=deepcopy(ppr)
 for c in list(p):p.remove(c)
 p.append(saved)
 add_run(p,'یافتن اشیای کوچک، یکی از دشوارترین جنبه‌های مسئله تشخیص اشیا به‌شمار می‌رود')
 add_citations(p,[3])
 add_run(p,'. اشیای کوچک پیکسل‌های کمتری را اشغال می‌کنند و در نتیجه، ویژگی‌های بصری کمتری برای استخراج در اختیار شبکه قرار می‌دهند؛ افزون بر این، در لایه‌های عمیق‌تر شبکه، وضوح مکانی نگاشت ویژگی کاهش می‌یابد. بنابراین، احتمال از دست رفتن کامل اطلاعات آن‌ها وجود دارد. در صحنه‌های ترافیکی، اشخاص دور، چراغ‌های راهنمایی و خودروهای انتهای صف، نمونه‌های متداول این دسته‌اند. دو راهکار متداول برای مقابله با این چالش، افزایش تفکیک‌پذیری ورودی و به‌کارگیری سازوکارهای چندمقیاسی و توجه است. بلوک ')
 add_run(p,'C2PSA','en'); add_run(p,' در معماری '); add_run(p,'YOLOv11','en'); add_run(p,' با تقویت توجه مکانی، به پالایش ویژگی‌های ناحیه‌ای کمک می‌کند'); add_citations(p,[9,10]); add_run(p,'.')

def set_link(h,n):
 h.set(q(W,'anchor'),f'_ref_{n}')
 ts=h.xpath('.//w:t',namespaces=NS)
 if ts:
  # Citation hyperlinks contain only the number.
  ts[0].text=fa(n)
  for t in ts[1:]: t.text=''

with ZipFile(DOC) as z: files={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(files['word/document.xml']); body=root.find(q(W,'body')); children=list(body)
# Tighten the one statement whose old arXiv source overstated the link to small-object detection.
p_small=next(p for p in root.xpath('//w:p',namespaces=NS) if textof(p).startswith('یافتن اشیای کوچک، یکی از دشوارترین'))
rebuild_small_object(p_small)

# Redirect every citation from a removed source to an existing source that explicitly covers the claim.
for h in list(root.xpath('//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS)):
 old=int(h.get(q(W,'anchor')).split('_')[-1])
 top=h
 while top.getparent() is not body: top=top.getparent()
 context=textof(top)
 if old==4:
  set_link(h,13 if ('اصل دوم' in context or 'آستانه‌های ۰٫۵ تا ۰٫۹۵' in context) else 3)
 elif old==6: set_link(h,9)
 elif old==7: set_link(h,3)
 elif old==8: set_link(h,9)
 elif old==21: set_link(h,12)
 elif old==22: set_link(h,3)

# Remove the six bibliography entries.
removed={4,6,7,8,21,22}
for n in removed:
 nodes=root.xpath(f'//w:bookmarkStart[@w:name="_ref_{n}"]',namespaces=NS)
 if len(nodes)!=1: raise RuntimeError(f'Expected one bibliography bookmark for ref {n}, got {len(nodes)}')
 p=nodes[0]
 while etree.QName(p).localname!='p': p=p.getparent()
 p.getparent().remove(p)

# Remaining sources, in the order in which their first valid citation now appears.
old_order=[1,2,3,5,9,10,11,12,13,14,15,16,17,18,19,20]
new_for_old={old:i+1 for i,old in enumerate(old_order)}
# Rename bibliography bookmarks through temporary names to avoid collisions.
for old in old_order:
 for bs in root.xpath(f'//w:bookmarkStart[@w:name="_ref_{old}"]',namespaces=NS): bs.set(q(W,'name'),f'_ref_tmp_{old}')
# Renumber all in-text hyperlinks (they currently point only to retained old references).
for h in root.xpath('//w:hyperlink[starts-with(@w:anchor,"_ref_")]',namespaces=NS):
 anchor=h.get(q(W,'anchor'))
 if anchor.startswith('_ref_tmp_'): continue
 old=int(anchor.split('_')[-1])
 if old not in new_for_old: raise RuntimeError(f'Unresolved citation still points to removed ref {old}: {textof(h)}')
 set_link(h,new_for_old[old])
# Rename bibliography bookmarks and visible labels.
for old,new in new_for_old.items():
 nodes=root.xpath(f'//w:bookmarkStart[@w:name="_ref_tmp_{old}"]',namespaces=NS)
 if len(nodes)!=1: raise RuntimeError(f'Missing retained bibliography ref {old}')
 bs=nodes[0]; bs.set(q(W,'name'),f'_ref_{new}')
 p=bs
 while etree.QName(p).localname!='p': p=p.getparent()
 # Replace only the bracketed bibliography label.
 done=False
 for t in p.xpath('.//w:t',namespaces=NS):
  if t.text and re.search(r'\[[۰-۹]+\]',t.text):
   t.text=re.sub(r'\[[۰-۹]+\]',f'[{fa(new)}]',t.text,count=1); done=True; break
 if not done: raise RuntimeError(f'No visible label in retained ref {old}')

files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
fd,tmp=tempfile.mkstemp(suffix='.docx',dir=str(DOC.parent)); os.close(fd)
with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
 for n,d in files.items(): z.writestr(n,d)
os.replace(tmp,DOC)
print(DOC)
print(new_for_old)
