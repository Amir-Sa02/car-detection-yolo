import copy, sys, zipfile
from pathlib import Path
from lxml import etree
SRC=Path(sys.argv[1]); OUT=Path(sys.argv[2]); W="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"; XML="{http://www.w3.org/XML/1998/namespace}"
with zipfile.ZipFile(SRC) as z:
 infos=z.infolist(); blobs={i.filename:z.read(i.filename) for i in infos}
root=etree.fromstring(blobs['word/document.xml'])
for p in root.iter(W+'p'):
 text=''.join(p.itertext())
 if text.startswith('اصل دوم، به نحوه گزارش معیارها'):
  target=next((h for h in p.findall(W+'hyperlink') if h.get(W+'anchor')=='_ref_13'),None)
  if target is None: raise RuntimeError('target link missing')
  idx=p.index(target)
  inner=target.find(W+'r')
  def linked(n):
   h=copy.deepcopy(target);h.set(W+'anchor',f'_ref_{n}');h.find('.//'+W+'t').text=str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'));return h
  sep=copy.deepcopy(inner);sep.find(W+'t').text='، ';sep.find(W+'t').set(XML+'space','preserve')
  p.remove(target);p.insert(idx,linked(2));p.insert(idx+1,sep);p.insert(idx+2,linked(3))
  break
else: raise RuntimeError('paragraph missing')
blobs['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
with zipfile.ZipFile(OUT,'w') as z:
 for i in infos:z.writestr(i,blobs[i.filename])
