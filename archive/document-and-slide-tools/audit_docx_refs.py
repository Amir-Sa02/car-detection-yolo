from zipfile import ZipFile
from lxml import etree
import re, json, collections

DOCX = r"C:\Users\amir2\Desktop\cat-claude\thesis_refs_audit.docx"
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS={'w':W,'r':R}
fa_to_en=str.maketrans('۰۱۲۳۴۵۶۷۸۹','0123456789')
pat=re.compile(r'\[([۰-۹0-9]+(?:\s*[،,]\s*[۰-۹0-9]+)*)\]')

def txt(el):
    return ''.join(el.xpath('.//w:t/text()',namespaces=NS))

with ZipFile(DOCX) as z:
    root=etree.fromstring(z.read('word/document.xml'))
    relroot=etree.fromstring(z.read('word/_rels/document.xml.rels'))
    rels={e.get('Id'):e.get('Target') for e in relroot}
    ps=root.xpath('//w:body//w:p',namespaces=NS)
    bib_i=next(i for i,p in enumerate(ps) if txt(p).strip()=='مراجع و منابع')
    body=ps[:bib_i]
    bmarks={e.get('{%s}name'%W): e.get('{%s}id'%W) for e in root.xpath('//w:bookmarkStart',namespaces=NS)}
    uses=[]
    first=[]
    for i,p in enumerate(body):
        t=txt(p)
        for m in pat.finditer(t):
            nums=[int(x.translate(fa_to_en)) for x in re.findall(r'[۰-۹0-9]+',m.group(1))]
            for n in nums:
                uses.append((n,i,t))
                if n not in first: first.append(n)
    counts=collections.Counter(n for n,_,_ in uses)
    # For each visible citation, capture hyperlink anchors covering citation text.
    citation_links=[]
    for i,p in enumerate(body):
        t=txt(p)
        if not pat.search(t): continue
        links=[]
        for h in p.xpath('.//w:hyperlink',namespaces=NS):
            ht=txt(h)
            anchor=h.get('{%s}anchor'%W)
            rid=h.get('{%s}id'%R)
            if pat.search(ht): links.append((ht,anchor,rels.get(rid)))
        citation_links.append((i,t,links))
    print('BIB_INDEX',bib_i)
    print('FIRST_ORDER',first)
    print('BODY_COUNTS',dict(sorted(counts.items())))
    print('UNUSED',[n for n in range(1,22) if counts[n]==0])
    print('BOOKMARKS',[x for x in sorted(bmarks) if 'Ref' in x or 'ref' in x])
    broken=[]
    notlinked=[]
    for i,t,links in citation_links:
        if not links:
            notlinked.append((i,t))
        for ht,anchor,target in links:
            if anchor and anchor not in bmarks: broken.append((i,ht,anchor))
    print('CITATION_PARAGRAPHS',len(citation_links))
    print('NOT_LINKED',len(notlinked))
    for x in notlinked: print('NL',x)
    print('BROKEN_LINKS',broken)
