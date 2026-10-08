import copy,re,sys,zipfile
from pathlib import Path
from lxml import etree
SRC,OUT=map(Path,sys.argv[1:3])
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
FA=str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹')
MAP={1:1,14:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12,12:13,13:14,15:15,16:16,17:17,18:18,19:19,20:20,21:21}
ORDER=[1,14,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21]
def txt(x):return ''.join(t.text or '' for t in x.iter(W+'t'))
with zipfile.ZipFile(SRC) as z:infos=z.infolist();blobs={i.filename:z.read(i.filename) for i in infos}
r=etree.fromstring(blobs['word/document.xml']);body=r.find('.//'+W+'body')
# remap linked citations
for h in r.iter(W+'hyperlink'):
 m=re.fullmatch(r'_ref_(\d+)',h.get(W+'anchor') or '')
 if not m:continue
 old=int(m.group(1));new=MAP[old];h.set(W+'anchor',f'_ref_{new}')
 for t in h.iter(W+'t'):
  if t.text:t.text=str(new).translate(FA)
# collect bibliography entry groups
ps=body.findall(W+'p');head=next(p for p in ps if txt(p).strip() in {'مراجع و منابع','منابع و مراجع'})
children=list(body);hp=children.index(head);groups={};current=None
for c in children[hp+1:]:
 if c.tag==W+'sectPr':continue
 b=c.find('.//'+W+'bookmarkStart')
 name=b.get(W+'name') if b is not None else ''
 m=re.fullmatch(r'_ref_(\d+)',name or '')
 if m:
  current=int(m.group(1));groups[current]=[c]
 elif current is not None and txt(c).strip().startswith('http'):
  groups[current].append(c)
 if c.getparent() is body:body.remove(c)
if set(groups)!=set(ORDER):raise RuntimeError((sorted(groups),ORDER))
sect=body.find(W+'sectPr');ix=body.index(sect) if sect is not None else len(body)
for old in ORDER:
 new=MAP[old]
 for c in groups[old]:
  b=c.find('.//'+W+'bookmarkStart')
  if b is not None:b.set(W+'name',f'_ref_{new}')
  if c is groups[old][0]:
   ts=list(c.iter(W+'t'));full=''.join(t.text or '' for t in ts);m=re.match(r'^\[[۰-۹]+\]',full)
   if not m:raise RuntimeError(full[:40])
   want='['+str(new).translate(FA)+']'
   remain=len(m.group(0));pos=0
   for t in ts:
    v=t.text or ''
    if pos<remain:
     take=min(len(v),remain-pos)
     if pos==0:t.text=want+v[take:]
     else:t.text=v[take:]
     pos+=take
  body.insert(ix,c);ix+=1
blobs['word/document.xml']=etree.tostring(r,xml_declaration=True,encoding='UTF-8',standalone='yes')
with zipfile.ZipFile(OUT,'w') as z:
 for i in infos:z.writestr(i,blobs[i.filename])
print('reordered')
