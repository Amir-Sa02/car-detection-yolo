from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from copy import deepcopy
from pathlib import Path
import os, tempfile

SRC=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\پایان‌نامه.docx')
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
XML='http://www.w3.org/XML/1998/namespace'
NS={'w':W,'m':M}
def q(ns,tag): return f'{{{ns}}}{tag}'
def fa(n): return str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
def textof(e): return ''.join(e.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS)).strip()

def rpr_fa(size=28):
    p=etree.Element(q(W,'rPr'))
    f=etree.SubElement(p,q(W,'rFonts')); f.set(q(W,'ascii'),'Times New Roman'); f.set(q(W,'hAnsi'),'Times New Roman'); f.set(q(W,'cs'),'B Zar')
    etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),str(size))
    etree.SubElement(p,q(W,'rtl'))
    l=etree.SubElement(p,q(W,'lang')); l.set(q(W,'val'),'fa-IR'); l.set(q(W,'bidi'),'fa-IR')
    return p

def rpr_en(size=24, italic=False):
    p=etree.Element(q(W,'rPr'))
    f=etree.SubElement(p,q(W,'rFonts')); f.set(q(W,'ascii'),'Times New Roman'); f.set(q(W,'hAnsi'),'Times New Roman'); f.set(q(W,'cs'),'Times New Roman')
    if italic: etree.SubElement(p,q(W,'i')); etree.SubElement(p,q(W,'iCs'))
    etree.SubElement(p,q(W,'sz')).set(q(W,'val'),str(size)); etree.SubElement(p,q(W,'szCs')).set(q(W,'val'),str(size))
    etree.SubElement(p,q(W,'lang')).set(q(W,'bidi'),'en-US')
    return p

def add_run(p,text,kind='fa',italic=False):
    r=etree.SubElement(p,q(W,'r')); r.append(rpr_fa() if kind=='fa' else rpr_en(24,italic))
    t=etree.SubElement(r,q(W,'t'))
    if text.startswith(' ') or text.endswith(' '): t.set(q(XML,'space'),'preserve')
    t.text=text
    return r

def add_footnote(p,fid):
    r=etree.SubElement(p,q(W,'r')); rp=rpr_fa(); st=etree.SubElement(rp,q(W,'rStyle')); st.set(q(W,'val'),'FootnoteReference'); r.append(rp)
    etree.SubElement(r,q(W,'footnoteReference')).set(q(W,'id'),str(fid))

def add_citation(p,num):
    add_run(p,' \u200f[','fa')
    h=etree.SubElement(p,q(W,'hyperlink')); h.set(q(W,'anchor'),f'_ref_{num}'); h.set(q(W,'history'),'1')
    r=etree.SubElement(h,q(W,'r')); r.append(rpr_fa()); etree.SubElement(r,q(W,'t')).text=fa(num)
    add_run(p,']\u200f:','fa')

def rebuild_para(p,items,citation=None):
    ppr=p.find(q(W,'pPr')); saved=deepcopy(ppr) if ppr is not None else None
    for c in list(p): p.remove(c)
    if saved is not None: p.append(saved)
    for item in items:
        typ=item[0]
        if typ=='fa': add_run(p,item[1],'fa')
        elif typ=='en': add_run(p,item[1],'en')
        elif typ=='fn': add_footnote(p,item[1])
    if citation is not None: add_citation(p,citation)

def m_r(text):
    r=etree.Element(q(M,'r'))
    rp=etree.SubElement(r,q(W,'rPr')); f=etree.SubElement(rp,q(W,'rFonts')); f.set(q(W,'ascii'),'Cambria Math'); f.set(q(W,'hAnsi'),'Cambria Math')
    etree.SubElement(r,q(M,'t')).text=text
    return r

def m_frac(num_children,den_children):
    f=etree.Element(q(M,'f')); fp=etree.SubElement(f,q(M,'fPr')); cp=etree.SubElement(fp,q(M,'ctrlPr')); rp=etree.SubElement(cp,q(W,'rPr')); rf=etree.SubElement(rp,q(W,'rFonts')); rf.set(q(W,'ascii'),'Cambria Math'); rf.set(q(W,'hAnsi'),'Cambria Math')
    num=etree.SubElement(f,q(M,'num')); den=etree.SubElement(f,q(M,'den'))
    for x in num_children: num.append(x)
    for x in den_children: den.append(x)
    return f

def m_ssub(base_children,sub_text):
    s=etree.Element(q(M,'sSub')); sp=etree.SubElement(s,q(M,'sSubPr')); cp=etree.SubElement(sp,q(M,'ctrlPr')); rp=etree.SubElement(cp,q(W,'rPr')); rf=etree.SubElement(rp,q(W,'rFonts')); rf.set(q(W,'ascii'),'Cambria Math'); rf.set(q(W,'hAnsi'),'Cambria Math')
    e=etree.SubElement(s,q(M,'e')); sub=etree.SubElement(s,q(M,'sub'))
    for x in base_children: e.append(x)
    sub.append(m_r(sub_text)); return s

def m_nary(sub_text,sup_text,e_children):
    n=etree.Element(q(M,'nary')); np=etree.SubElement(n,q(M,'naryPr')); etree.SubElement(np,q(M,'chr')).set(q(M,'val'),'∑'); etree.SubElement(np,q(M,'limLoc')).set(q(M,'val'),'undOvr')
    cp=etree.SubElement(np,q(M,'ctrlPr')); rp=etree.SubElement(cp,q(W,'rPr')); rf=etree.SubElement(rp,q(W,'rFonts')); rf.set(q(W,'ascii'),'Cambria Math'); rf.set(q(W,'hAnsi'),'Cambria Math')
    sub=etree.SubElement(n,q(M,'sub')); sub.append(m_r(sub_text)); sup=etree.SubElement(n,q(M,'sup')); sup.append(m_r(sup_text)); e=etree.SubElement(n,q(M,'e'))
    for x in e_children: e.append(x)
    return n

def m_delim(children):
    d=etree.Element(q(M,'d')); dp=etree.SubElement(d,q(M,'dPr')); etree.SubElement(dp,q(M,'begChr')).set(q(M,'val'),'('); etree.SubElement(dp,q(M,'endChr')).set(q(M,'val'),')')
    e=etree.SubElement(d,q(M,'e'))
    for x in children: e.append(x)
    return d

def replace_math(table, children):
    om=table.find('.//m:oMath',NS)
    for c in list(om): om.remove(c)
    for c in children: om.append(c)

def set_label(table,label):
    # first table cell contains the equation number
    t=table.find('./w:tr/w:tc[1]//w:t',NS); t.text=label

def clone_ref_para(template,num,bookmark_id,authors,title,journal_tail):
    p=deepcopy(template); ppr=p.find(q(W,'pPr')); saved=deepcopy(ppr)
    for c in list(p): p.remove(c)
    p.append(saved)
    bs=etree.SubElement(p,q(W,'bookmarkStart')); bs.set(q(W,'id'),str(bookmark_id)); bs.set(q(W,'name'),f'_ref_{num}')
    add_run(p,' ','fa'); add_run(p,f'[{fa(num)}] ','fa'); add_run(p,' ','fa')
    add_run(p,authors,'en'); add_run(p,title,'en',italic=True); add_run(p,journal_tail,'en')
    be=etree.SubElement(p,q(W,'bookmarkEnd')); be.set(q(W,'id'),str(bookmark_id))
    return p

with ZipFile(SRC,'r') as zin:
    files={n:zin.read(n) for n in zin.namelist()}
root=etree.fromstring(files['word/document.xml']); body=root.find(q(W,'body'))
children=list(body)
# Locate the body section, excluding the TOC occurrence.
head=next(e for e in children if etree.QName(e).localname=='p' and textof(e).startswith('۱\u200f-\u200f۴\u200f-\u200f۴-') and not e.xpath('./w:pPr/w:pStyle[@w:val="TOC3"]',namespaces=NS))
idx=children.index(head)
sec=children[idx:idx+14]
p_intro=sec[1]; tbl_ap=sec[2]; p_after_ap=sec[4]; p_iou=sec[5]; tbl_extra=sec[6]; blank_extra=sec[7]; p_map50=sec[8]; tbl_map50=sec[9]; p_before_95=sec[11]; tbl_map95=sec[12]; p_summary=sec[13]

# Intro and AP definition: preserve both existing footnotes.
rebuild_para(p_intro,[
 ('fa','معیار اصلی و استاندارد برای ارزیابی آشکارسازهای اشیا، میانگین دقت متوسط'),('fn',35),
 ('fa',' است. برای محاسبه این معیار، ابتدا منحنی دقت برحسب فراخوانی برای هر رده رسم می‌شود. مساحت زیر این منحنی، دقت متوسط'),('fn',36),
 ('fa',' آن رده را مطابق رابطه (۱\u200f-\u200f۵) نشان می‌دهد')],citation=13)
# Keep equation 1-5 unchanged; polish its variable definition.
rebuild_para(p_after_ap,[('fa','در این رابطه، '),('en','P(r)'),('fa',' مقدار دقت در سطح فراخوانی '),('en','r'),('fa',' برای رده مورد ارزیابی است.')])
# Replace the unsupported standalone AP_c@0.5 equation with prose that leads directly to mAP@0.5.
rebuild_para(p_iou,[
 ('fa','در تشخیص اشیا، درست‌بودن یک پیش‌بینی افزون بر برچسب رده، به میزان هم‌پوشانی کادر پیش‌بینی‌شده با کادر واقعی وابسته است. این هم‌پوشانی با معیار '),('en','IoU'),
 ('fa',' سنجیده می‌شود. در نماد '),('en','AP_i(0.5)'),('fa','، زیرنویس '),('en','i'),
 ('fa',' رده مورد ارزیابی و عدد ۰٫۵ آستانه نسبت هم‌پوشانی است؛ بنابراین پیش‌بینی زمانی مثبت درست محسوب می‌شود که رده آن صحیح و مقدار '),('en','IoU'),
 ('fa',' دست‌کم ۰٫۵ باشد. میانگین '),('en','AP_i(0.5)'),('fa',' روی '),('en','N'),('fa',' رده، معیار '),('en','mAP@0.5'),
 ('fa',' را مطابق رابطه (۱\u200f-\u200f۶) به‌دست می‌دهد')],citation=13)
# Delete the equation not present in the paper, its spacer, and the now-redundant following paragraph.
body.remove(tbl_extra); body.remove(blank_extra); body.remove(p_map50)
# Renumber and align mAP@0.5 with article Eq. 16.
set_label(tbl_map50,'(۱\u200f-\u200f۶)')
for mt in tbl_map50.xpath('.//m:t',namespaces=NS):
    if mt.text=='c=1': mt.text='i=1'
    elif mt.text=='c': mt.text='i'
    elif mt.text=='@0.5': mt.text='(0.5)'
# mAP@0.5:0.95 lead-in.
rebuild_para(p_before_95,[
 ('fa','معیار سخت‌گیرانه‌تر '),('en','mAP@0.5:0.95'),
 ('fa',' است. این معیار از میانگین دقت متوسط در ده آستانه هم‌پوشانی ۰٫۵۰ تا ۰٫۹۵ با گام ۰٫۰۵ به‌دست می‌آید و مطابق رابطه (۱\u200f-\u200f۷) محاسبه می‌شود')],citation=13)
set_label(tbl_map95,'(۱\u200f-\u200f۷)')
# Article-aligned double average: classes × ten IoU thresholds, while retaining thesis colon notation.
api=[m_ssub([m_r('AP')],'i'),m_r('('),m_ssub([m_r('IoU')],'j'),m_r(')')]
inner=[m_frac([m_r('1')],[m_r('10')]),m_nary('j=1','10',api)]
outer=m_nary('i=1','N',[m_delim(inner)])
replace_math(tbl_map95,[m_r('mAP@0.5:0.95='),m_frac([m_r('1')],[m_r('N')]),outer])
rebuild_para(p_summary,[
 ('fa','در رابطه (۱\u200f-\u200f۷)، '),('en','IoU_j'),('fa',' آستانه شماره '),('en','j'),
 ('fa',' است که از ۰٫۵ آغاز می‌شود و در هر گام ۰٫۰۵ افزایش می‌یابد؛ همچنین '),('en','AP_i(IoU_j)'),
 ('fa',' دقت متوسط رده '),('en','i'),('fa',' در همان آستانه را نشان می‌دهد. در نتیجه، عدد یا بازه پس از علامت '),('en','@'),
 ('fa',' آستانه هم‌پوشانی را مشخص می‌کند و با آستانه اطمینان تفاوت دارد. معیار '),('en','mAP@0.5'),
 ('fa',' عملکرد مدل را در آستانه ۰٫۵ می‌سنجد؛ '),('en','mAP@0.5:0.95'),
 ('fa',' نیز با میانگین‌گیری در چند آستانه، کیفیت مکان‌یابی کادرها را سخت‌گیرانه‌تر ارزیابی می‌کند. در این پروژه هر دو معیار گزارش شده‌اند.')])

# Reference ordering: new paper is 13; existing 14-20 stay; old 13 moves to 21; old 21 becomes 22.
children=list(body)
def ref_para(n):
    return next(p for p in children if p.xpath(f'.//w:bookmarkStart[@w:name="_ref_{n}"]',namespaces=NS))
old13=ref_para(13); old21=ref_para(21)
# Move old 13 after reference 20 and rename it to 21.
for bs in old13.xpath('.//w:bookmarkStart',namespaces=NS): bs.set(q(W,'name'),'_ref_21')
for t in old13.xpath('.//w:t',namespaces=NS):
    if t.text and '[۱۳]' in t.text: t.text=t.text.replace('[۱۳]','[۲۱]')
# Rename old 21 to 22.
for bs in old21.xpath('.//w:bookmarkStart',namespaces=NS): bs.set(q(W,'name'),'_ref_22')
for t in old21.xpath('.//w:t',namespaces=NS):
    if t.text and '[۲۱]' in t.text: t.text=t.text.replace('[۲۱]','[۲۲]')
# In-text links: old Chaman citation outside metric section -> 21; old Focal Loss -> 22.
for h in root.xpath('//w:hyperlink[@w:anchor="_ref_13"]',namespaces=NS):
    # section citations stay at 13; only citations after the references discussion paragraph move.
    anc=h
    while anc.getparent() is not body: anc=anc.getparent()
    if body.index(anc)>400:
        h.set(q(W,'anchor'),'_ref_21')
        for t in h.xpath('.//w:t',namespaces=NS):
            if t.text=='۱۳': t.text='۲۱'
for h in root.xpath('//w:hyperlink[@w:anchor="_ref_21"]',namespaces=NS):
    anc=h
    while anc.getparent() is not body: anc=anc.getparent()
    # Ignore the just-renumbered old Chaman citation; move only the original Focal Loss citation.
    if 'خطای کانونی' in textof(anc):
        h.set(q(W,'anchor'),'_ref_22')
        for t in h.xpath('.//w:t',namespaces=NS):
            if t.text=='۲۱': t.text='۲۲'
# Insert new reference 13 before reference 14.
children=list(body); ref14=next(p for p in children if p.xpath('.//w:bookmarkStart[@w:name="_ref_14"]',namespaces=NS))
max_id=max(int(x) for x in root.xpath('//w:bookmarkStart/@w:id',namespaces=NS) if str(x).isdigit())
new13=clone_ref_para(old13,13,max_id+1,
    'Lin, J., Wang, P., Ruan, Y., and Sun, Y., ',
    'YOLO11-WLBS: an efficient model for pavement defect detection',
    ', Scientific Reports, vol. 16, article 5284, 2026.')
body.insert(body.index(ref14),new13)
# Physically move old 13/new 21 after reference 20.
children=list(body); ref20=next(p for p in children if p.xpath('.//w:bookmarkStart[@w:name="_ref_20"]',namespaces=NS))
body.remove(old13); body.insert(body.index(ref20)+1,old13)

# Save through a new zip, then replace atomically.
files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
fd,tmp=tempfile.mkstemp(suffix='.docx',dir=str(SRC.parent)); os.close(fd)
with ZipFile(tmp,'w',ZIP_DEFLATED) as zout:
    for name,data in files.items(): zout.writestr(name,data)
os.replace(tmp,SRC)
print(SRC)
