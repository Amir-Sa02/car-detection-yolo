from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import sys
sys.stdout.reconfigure(encoding='utf-8')
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS={'w':W,'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
ORDER='pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange'.split()
RO='rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath rPrChange'.split()
def prop(p,tag,value=None):
 for old in list(p.findall('{'+W+'}'+tag)):p.remove(old)
 x=E.SubElement(p,'{'+W+'}'+tag)
 if value is not None:x.set('{'+W+'}val',value)
 return x
def canonical(p,order):
 for x in sorted(list(p),key=lambda x:order.index(E.QName(x).localname) if E.QName(x).localname in order else len(order)):
  p.remove(x);p.append(x)
root=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع')
for path in root.glob('*.docx'):
 with ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
 for name,data in list(parts.items()):
  if name=='word/document.xml' or name=='word/styles.xml' or (name.startswith('word/header') or name.startswith('word/footer')) and name.endswith('.xml'):
   x=E.fromstring(data)
   if name=='word/styles.xml':
    for st in x.xpath('//w:style[@w:type="paragraph"]',namespaces=NS):
     pp=st.find('{'+W+'}pPr')
     if pp is None:pp=E.SubElement(st,'{'+W+'}pPr')
     for rp in list(pp.findall('{'+W+'}rPr')):pp.remove(rp)
     prop(pp,'bidi');canonical(pp,ORDER)
    for pp in x.xpath('//w:pPrDefault/w:pPr',namespaces=NS):
     for rp in list(pp.findall('{'+W+'}rPr')):pp.remove(rp)
     prop(pp,'bidi');canonical(pp,ORDER)
   else:
    for p in x.xpath('//w:p',namespaces=NS):
     pp=p.find('{'+W+'}pPr')
     if pp is None:pp=E.Element('{'+W+'}pPr');p.insert(0,pp)
     prop(pp,'bidi')
     center=bool(pp.xpath('./w:jc[@w:val="center"]',namespaces=NS))
     mathonly=bool(p.xpath('./m:oMath',namespaces=NS)) and not bool(p.xpath('./w:r/w:t',namespaces=NS))
     # Word maps this logical start alignment to physical right with bidi enabled.
     prop(pp,'jc','center' if center or mathonly or name.startswith('word/footer') else 'left')
     rp=pp.find('{'+W+'}rPr')
     if rp is None:rp=E.SubElement(pp,'{'+W+'}rPr')
     prop(rp,'rtl');canonical(rp,RO);canonical(pp,ORDER)
   for rp in x.xpath('//w:rPr',namespaces=NS):canonical(rp,RO)
   parts[name]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
 temp=path.with_suffix('.canonical.docx')
 with ZipFile(temp,'w',ZIP_DEFLATED) as z:
  for n,d in parts.items():z.writestr(n,d)
 temp.replace(path)
 print(path.name,'RTL and schema order fixed')
