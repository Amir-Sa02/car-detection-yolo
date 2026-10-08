from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
from copy import deepcopy
import re, json, sys, shutil
from lxml import etree as E

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه معماری و پرسش‌های دفاع')
BACK=ROOT/'پشتیبان‌ها'/datetime.now().strftime('%Y%m%d_%H%M%S')
BACK.mkdir(parents=True,exist_ok=True)
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
NS={'w':W,'m':M}
def el(tag,**attrs):
    n=E.Element('{'+(M if tag.startswith('m:') else W)+'}'+tag.split(':')[1])
    for key,val in attrs.items(): n.set('{'+(M if tag.startswith('m:') else W)+'}'+key,str(val))
    return n
def ensure(parent,tag):
    q='{'+(M if tag.startswith('m:') else W)+'}'+tag.split(':')[1]
    found=parent.find(q)
    if found is None: found=el(tag); parent.insert(0,found)
    return found
def prop(parent,tag,value):
    q='{'+(M if tag.startswith('m:') else W)+'}'+tag.split(':')[1]
    for old in list(parent.findall(q)): parent.remove(old)
    parent.append(el(tag,val=value))
def run(t):
    r=el('m:r');rp=el('m:rPr');rp.append(el('m:sty',val='p'));r.append(rp)
    wp=el('w:rPr');fonts=el('w:rFonts',ascii='Times New Roman',hAnsi='Times New Roman',cs='Times New Roman',eastAsia='Times New Roman')
    wp.append(fonts);wp.append(el('w:sz',val='22'));wp.append(el('w:szCs',val='22'));wp.append(el('w:rtl',val='0'));wp.append(el('w:lang',val='en-US'));r.append(wp)
    tt=el('m:t');tt.set('{http://www.w3.org/XML/1998/namespace}space','preserve');tt.text=str(t);r.append(tt);return r
def nodes(v):
    if isinstance(v,str):return [run(v)]
    if isinstance(v,list):return [n for item in v for n in nodes(item)]
    return [v]
def container(tag,value):
    x=el(tag)
    for n in nodes(value):x.append(n)
    return x
def sub(a,b):
    x=el('m:sSub');x.append(container('m:e',a));x.append(container('m:sub',b));return x
def sup(a,b):
    x=el('m:sSup');x.append(container('m:e',a));x.append(container('m:sup',b));return x
def frac(a,b):
    x=el('m:f');x.append(container('m:num',a));x.append(container('m:den',b));return x
def rad(a):
    x=el('m:rad');rp=el('m:radPr');rp.append(el('m:degHide',val='1'));x.append(rp);x.append(el('m:deg'));x.append(container('m:e',a));return x
def delim(a,begin='(',end=')'):
    x=el('m:d');pr=el('m:dPr');pr.append(el('m:begChr',val=begin));pr.append(el('m:endChr',val=end));x.append(pr);x.append(container('m:e',a));return x
def sigma(a,low,high=None):
    x=el('m:nary');pr=el('m:naryPr');pr.append(el('m:chr',val='∑'));pr.append(el('m:limLoc',val='undOvr'));pr.append(el('m:grow',val='1'))
    if high is None:pr.append(el('m:supHide',val='1'))
    x.append(pr);x.append(container('m:sub',low));x.append(container('m:sup',high or ''));x.append(container('m:e',a));return x
def matrix(values):
    x=el('m:m')
    for row in values:
        rr=el('m:mr')
        for v in row:rr.append(container('m:e',str(v)))
        x.append(rr)
    return delim(x,'[',']')
def om(value):
    x=el('m:oMath')
    for n in nodes(value): x.append(n)
    return x
def df(a,b):return frac('∂'+a,'∂'+b)

FORMULAS=[
 ['r = ',delim(['min',delim([frac('1280','W'),' , ',frac('1280','H')])]),' = 1'],
 ['class = 1    x = 0.582292    y = 0.474537    w = 0.114583    h = 0.175'],
 [sub('z','o,i,j'),' = ',sigma([sub('W','o,c,u,v'),' × ',sub('X','c,2i+u−1,2j+v−1')],'c,u,v')],
 [sub('H','out'),' = ',delim(frac('H + 2p − k','s'),'⌊','⌋'),' + 1 = ',delim(frac('1280 + 2 − 3','2'),'⌊','⌋'),' + 1 = 640'],
 ['BN(z) = γ × ',frac('z − μ',rad([sup('σ','2'),' + ε'])),' + β'],
 ['SiLU(z) = z × sigmoid(z) = ',frac('z',['1 + exp',delim('−z')])],
 ['64 → (32, 32) → (32, 32, 32) → 96 → 128'],
 ['256 + 256 + 256 + 256 = 1024 → 512'],
 ['A = softmax',delim(frac([sup('Q','T'),'K'],rad(sub('d','k')))),'    O = V',sup('A','T')],
 ['raw channels = 4 × 16 + 6 = 70'],
 ['distance = ',sigma(['k × ',sub('softmax(logits)','k')],'k = 0','15')],
 [sub('x','1'),' = ',sub('a','x'),' − l × stride    ',sub('y','1'),' = ',sub('a','y'),' − t × stride'],
 [sub('x','2'),' = ',sub('a','x'),' + r × stride    ',sub('y','2'),' = ',sub('a','y'),' + b × stride'],
 ['alignment = ',sup('class_score','0.5'),' × ',sup('overlap_quality','6')],
 ['CIoU = IoU − ',frac(sup('ρ','2'),sup('c','2')),' − αv'],
 ['L = 7.5 × ',sub('L','box'),' + 0.5 × ',sub('L','cls'),' + 1.5 × ',sub('L','dfl')],
 ['BCE(p,y) = −y log(p) − (1−y) log(1−p)'],
 [df('L','w'),' = ',df('L','y'),' × ',df('y','z'),' × ',df('z','w')],
 [df('L',sub('W','o,c,u,v')) if False else frac('∂L',['∂',sub('W','o,c,u,v')]),' = ',sigma([frac('∂L',['∂',sub('z','o,i,j')]),' × ',sub('X','c,si+u−p,sj+v−p')],'i,j')],
 ['L = 0.5 × ',sup(delim('wx − t'),'2'),'    ',df('L','w'),' = (wx − t)x = −0.672'],
 [sub('w','new'),' = w − ηg = 0.2 − 0.01 × (−0.672) = 0.20672'],
 ['m(t) = ',sub('β','1'),' m(t−1) + (1−',sub('β','1'),') g(t)'],
 ['v(t) = ',sub('β','2'),' v(t−1) + (1−',sub('β','2'),') ',sup('g(t)','2')],
 ['m̂(t) = ',frac('m(t)',['1−',sup(sub('β','1'),'t')]),'    v̂(t) = ',frac('v(t)',['1−',sup(sub('β','2'),'t')])],
 ['w(t) = (1−η(t) λ) w(t−1) − η(t) ',frac('m̂(t)',[rad('v̂(t)'),' + ε'])],
 ['η(t) = ',sub('η','0'),' × ',delim(['lrf + (1−lrf) × ',frac(['1 + cos',delim(frac('πt','T'))],'2')],'[',']')],
]

def text(p):return ''.join(p.xpath('.//w:t/text() | .//m:t/text()',namespaces=NS))
def rtl_paragraph(p):
    pp=ensure(p,'w:pPr');prop(pp,'w:bidi','1')
    rp=ensure(pp,'w:rPr');prop(rp,'w:rtl','1')
    lang=ensure(rp,'w:lang');lang.set('{'+W+'}val','fa-IR');lang.set('{'+W+'}bidi','fa-IR')
    # Preserve centered table cells and equations, and make ordinary text explicitly right aligned.
    jc=pp.find('{'+W+'}jc')
    if jc is None:pp.append(el('w:jc',val='right'))
    elif jc.get('{'+W+'}val') in ('left','start'):jc.set('{'+W+'}val','right')
    fonts=ensure(rp,'w:rFonts')
    for key in ('ascii','hAnsi','cs','eastAsia'):fonts.set('{'+W+'}'+key,'B Zar')

def replace_ranges(p,ranges):
    # Match only a contiguous group of plain runs; hyperlinks and drawings retain their XML.
    count=0
    children=list(p); groups=[];current=[]
    for child in children:
        if child.tag=='{'+W+'}r' and child.find('{'+W+'}t') is not None and not child.xpath('.//w:drawing | .//w:fldChar',namespaces=NS):current.append(child)
        else:
            if current:groups.append(current);current=[]
    if current:groups.append(current)
    for group in groups:
        full=''.join(''.join(r.xpath('./w:t/text()',namespaces=NS)) for r in group)
        matches=[]
        for a,b,content in ranges(full):
            if not any(a<bb and b>aa for aa,bb,_ in matches):matches.append((a,b,content))
        if not matches:continue
        matches.sort();offsets=[];pos=0
        for r in group:
            s=''.join(r.xpath('./w:t/text()',namespaces=NS));offsets.append((pos,pos+len(s),r,s));pos+=len(s)
        def segment(a,b):
            out=[]
            for start,end,old,s in offsets:
                if start>=b or end<=a:continue
                rr=deepcopy(old);tt=rr.find('{'+W+'}t');tt.text=s[max(0,a-start):min(len(s),b-start)];tt.set('{http://www.w3.org/XML/1998/namespace}space','preserve');out.append(rr)
            return out
        result=[];pos=0
        for a,b,content in matches:
            result+=segment(pos,a);result.append(om(deepcopy(content)));pos=b;count+=1
        result+=segment(pos,len(full));idx=p.index(group[0])
        for old in group:p.remove(old)
        for n in result:p.insert(idx,n);idx+=1
    return count

TO_ASCII=str.maketrans('۰۱۲۳۴۵۶۷۸۹٫٬','0123456789.,')
def spans(s):
    # Tensor dimensions and numeric arithmetic are mathematical expressions, not RTL prose.
    patterns=[r'[0-9۰-۹]+(?:\s*×\s*[0-9۰-۹]+){1,4}(?:\s*=\s*[0-9۰-۹٬,]+)?',r'[0-9۰-۹]+\s*\+\s*[0-9۰-۹]+\s*=\s*[0-9۰-۹]+']
    for pat in patterns:
        for m in re.finditer(pat,s):yield m.start(),m.end(),m.group().translate(TO_ASCII)
    specs={
      'dk=32':[sub('d','k'),' = 32'],
      'ceil(26000/12)=2167':[delim(frac('26000','12'),'⌈','⌉'),' = 2167'],
      'round(64/12)=5':['round',delim(frac('64','12')),' = 5'],
      'η0=0.001':[sub('η','0'),' = 0.001'],
      'lrf=0.01':['lrf = 0.01'],
      'T=150':['T = 150'],
      'y=1':['y = 1'],
      'sigmoid(z)−y':['sigmoid(z) − y'],
      'w=0.2':['w = 0.2'],
      'x=0.8':['x = 0.8'],
      't=1':['t = 1'],
      'y=wx=0.16':['y = wx = 0.16'],
      'y=wx':['y = wx'],
      '(y−t)x':[delim('y−t'),'x'],
      '(wx−t)x':[delim('wx−t'),'x'],
      'y−t':['y−t'],
      'z×sigmoid(z)':['z × sigmoid(z)'],
      'TP/(TP+FP)':frac('TP','TP+FP'),
      'TP/(TP+FN)':frac('TP','TP+FN'),
      '2PR/(P+R)':frac('2PR','P+R'),
      '۰٫۱×mAP@0.5+۰٫۹×mAP@0.5:0.95':['0.1 × mAP@0.5 + 0.9 × mAP@0.5:0.95'],
      '[۱،۲،۰؛ ۰،۱،۳؛ ۲،۰،۱]':matrix([[1,2,0],[0,1,3],[2,0,1]]),
      '[۱،۰،۱؛ ۰،۱،۰؛ ۱،۰،۱]':matrix([[1,0,1],[0,1,0],[1,0,1]]),
    }
    for literal,content in specs.items():
        for match in re.finditer(re.escape(literal),s):yield match.start(),match.end(),content

reports=[]
for path in sorted(ROOT.glob('*.docx')):
    shutil.copy2(path,BACK/path.name)
    with ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(parts['word/document.xml']);old_math=root.xpath('//m:oMath',namespaces=NS)
    if old_math:
        if len(old_math)!=len(FORMULAS):raise RuntimeError('Unexpected equation count; original file preserved')
        for old,content in zip(old_math,FORMULAS):old.getparent().replace(old,om(deepcopy(content)))
    added=0
    for par in root.xpath('//w:p',namespaces=NS):
        rtl_paragraph(par);added+=replace_ranges(par,spans)
    # Section direction and paragraph defaults are also explicitly RTL in Word.
    for sp in root.xpath('//w:sectPr',namespaces=NS):prop(sp,'w:bidi','1')
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    for name in list(parts):
        if name=='word/styles.xml':
            styles=E.fromstring(parts[name])
            for st in styles.xpath('//w:style[@w:type="paragraph"] | //w:docDefaults/w:pPrDefault',namespaces=NS):
                pp=ensure(st,'w:pPr');prop(pp,'w:bidi','1');rp=ensure(pp,'w:rPr');prop(rp,'w:rtl','1')
            parts[name]=E.tostring(styles,xml_declaration=True,encoding='UTF-8',standalone=True)
        elif re.fullmatch(r'word/(?:footer|header)\d+\.xml',name):
            story=E.fromstring(parts[name])
            for par in story.xpath('//w:p',namespaces=NS):rtl_paragraph(par)
            parts[name]=E.tostring(story,xml_declaration=True,encoding='UTF-8',standalone=True)
    temp=path.with_suffix('.fixed.docx')
    with ZipFile(temp,'w',ZIP_DEFLATED) as z:
        for n,data in parts.items():z.writestr(n,data)
    temp.replace(path)
    reports.append({'file':str(path),'backup':str(BACK/path.name),'equations_rebuilt':len(old_math),'inline_equations_added':added,'paragraphs':len(root.xpath('//w:p',namespaces=NS))})
print(json.dumps(reports,ensure_ascii=False,indent=2))
