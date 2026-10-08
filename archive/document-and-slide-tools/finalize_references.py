import copy,re,sys,zipfile
from pathlib import Path
from lxml import etree
SRC,OUT=map(Path,sys.argv[1:3])
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
XML='{http://www.w3.org/XML/1998/namespace}'
FA=str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹')
TOASC=str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩','01234567890123456789')
CITE=re.compile(r'\[\s*([۰-۹٠-٩0-9]+(?:\s*[,،؛;]\s*[۰-۹٠-٩0-9]+)*)\s*\]')
NUM=re.compile(r'[۰-۹٠-٩0-9]+')
BIB=[
(1,'Khosravian, A., Amirkhani, A., Masih-Tehrani, M., and Yazdanijoo, A., ','Multi-domain autonomous driving dataset: Towards enhancing the generalization of the convolutional neural networks in new environments',', IET Image Processing, vol. 17, no. 4, 2023, pp. 1253-1266.','https://github.com/ahv1373/IADD'),
(2,'Zou, Z., Chen, K., Shi, Z., Guo, Y., and Ye, J., ','Object Detection in 20 Years: A Survey',', Proceedings of the IEEE, vol. 111, no. 3, 2023, pp. 257-276.',None),
(3,'Ren, S., He, K., Girshick, R., and Sun, J., ','Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks',', Advances in Neural Information Processing Systems (NeurIPS), 2015, pp. 91-99.',None),
(4,'Redmon, J., Divvala, S., Girshick, R., and Farhadi, A., ','You Only Look Once: Unified, Real-Time Object Detection',', Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 779-788.',None),
(5,'Sundaresan Geetha, A., ','YOLOv4: A Breakthrough in Real-Time Object Detection',', arXiv preprint arXiv:2502.04161, 2025.','https://arxiv.org/abs/2502.04161'),
(6,'Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y., and Berg, A. C., ','SSD: Single Shot MultiBox Detector',', Proceedings of the European Conference on Computer Vision (ECCV), 2016, pp. 21-37.',None),
(7,'Khanam, R., and Hussain, M., ','YOLOv11: An Overview of the Key Architectural Enhancements',', arXiv preprint arXiv:2410.17725, 2024.','https://arxiv.org/abs/2410.17725'),
(8,'Sapkota, R., Flores-Calero, M., Qureshi, R., Badgujar, C., Nepal, U., Poulose, A., Zeno, P., Vaddevolu, U. B. P., Khan, S., Shoman, M., Yan, H., and Karkee, M., ','YOLO advances to its genesis: a decadal and comprehensive review of the You Only Look Once (YOLO) series',', Artificial Intelligence Review, vol. 58, no. 9, 2025, article 274.',None),
(9,'Ultralytics, ','Ultralytics YOLO Documentation',', Ultralytics Docs, 2024.','https://docs.ultralytics.com/models/yolo11/'),
(10,'Zhang, H., Cisse, M., Dauphin, Y. N., and Lopez-Paz, D., ','mixup: Beyond Empirical Risk Minimization',', Proceedings of the International Conference on Learning Representations (ICLR), 2018.',None),
(11,'Chaman, M., El Maliki, A., El Yanboiy, H., Dahou, H., Laamari, H., and Hadjoudja, A., ','A Real-Time Vehicle Detection System for ADAS in Autonomous Vehicles Using YOLOv11 Deep Neural Network on Embedded Edge Platforms',', Engineering, Technology and Applied Science Research, vol. 15, no. 5, 2025, pp. 28077-28082.',None),
(12,'Chaman, M., El Maliki, A., El Yanboiy, H., Dahou, H., Laamari, H., and Hadjoudja, A., ','Comparative Analysis of Deep Neural Networks YOLOv11 and YOLOv12 for Real-Time Vehicle Detection in Autonomous Vehicles',', International Journal of Transport Development and Integration, vol. 9, no. 1, 2025, pp. 39-48.',None),
(13,'Lin, T.-Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., Dollar, P., and Zitnick, C. L., ','Microsoft COCO: Common Objects in Context',', Proceedings of the European Conference on Computer Vision (ECCV), 2014, pp. 740-755.',None),
(14,'Kaufman, S., Rosset, S., Perlich, C., and Stitelman, O., ','Leakage in Data Mining: Formulation, Detection, and Avoidance',', ACM Transactions on Knowledge Discovery from Data, vol. 6, no. 4, 2012, article 15.',None),
(15,'Oksuz, K., Cam, B. C., Kalkan, S., and Akbas, E., ','Imbalance Problems in Object Detection: A Review',', IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 43, no. 10, 2021, pp. 3388-3415.',None),
(16,'Song, H., Kim, M., Park, D., Shin, Y., and Lee, J.-G., ','Learning From Noisy Labels With Deep Neural Networks: A Survey',', IEEE Transactions on Neural Networks and Learning Systems, vol. 34, no. 11, 2023, pp. 8135-8153.',None),
(17,'Monga, V., and Evans, B. L., ','Perceptual Image Hashing Via Feature Points: Performance Evaluation and Tradeoffs',', IEEE Transactions on Image Processing, vol. 15, no. 11, 2006, pp. 3452-3465.',None),
(18,'Loshchilov, I., and Hutter, F., ','Decoupled Weight Decay Regularization',', Proceedings of the International Conference on Learning Representations (ICLR), 2019.',None),
(19,'Loshchilov, I., and Hutter, F., ','SGDR: Stochastic Gradient Descent with Warm Restarts',', Proceedings of the International Conference on Learning Representations (ICLR), 2017.',None),
(20,'Goodfellow, I., Bengio, Y., and Courville, A., ','Deep Learning',', MIT Press, 2016, pp. 108-119.',None),
(21,'Lin, T.-Y., Goyal, P., Girshick, R., He, K., and Dollar, P., ','Focal Loss for Dense Object Detection',', Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017, pp. 2980-2988.',None)]
def ptext(p):return ''.join(t.text or '' for t in p.iter(W+'t'))
def space(t):
 v=t.text or ''
 if v.startswith(' ') or v.endswith(' '):t.set(XML+'space','preserve')
 else:t.attrib.pop(XML+'space',None)
def rpr(r):
 x=r.find(W+'rPr')
 if x is None:x=etree.Element(W+'rPr');r.insert(0,x)
 return x
def font(r,face,size,lang,rtl=False,italic=False,style=None):
 x=rpr(r)
 for q in ('rFonts','sz','szCs','lang','rtl','i','iCs','rStyle'):
  for e in list(x.findall(W+q)):x.remove(e)
 if style:
  e=etree.SubElement(x,W+'rStyle');e.set(W+'val',style)
 f=etree.SubElement(x,W+'rFonts')
 for a in ('ascii','hAnsi','cs'):f.set(W+a,face)
 for q in ('sz','szCs'):
  e=etree.SubElement(x,W+q);e.set(W+'val',str(size*2))
 e=etree.SubElement(x,W+'lang');e.set(W+'val',lang);e.set(W+'bidi','fa-IR' if rtl else lang)
 if rtl:etree.SubElement(x,W+'rtl')
 if italic:etree.SubElement(x,W+'i');etree.SubElement(x,W+'iCs')
def run(txt,face='Times New Roman',size=12,lang='en-US',rtl=False,italic=False,style=None):
 r=etree.Element(W+'r');font(r,face,size,lang,rtl,italic,style);t=etree.SubElement(r,W+'t');t.text=txt;space(t);return r
def setrt(r,val):
 t=r.find(W+'t');t.text=val;space(t)
def replace(p,old,new):
 ts=list(p.iter(W+'t'));vs=[t.text or '' for t in ts];full=''.join(vs);a=full.find(old)
 if a<0:raise RuntimeError('not found: '+old)
 b=a+len(old);starts=[];k=0
 for v in vs:starts.append(k);k+=len(v)
 si=max(i for i,s in enumerate(starts) if s<=a);ei=max(i for i,s in enumerate(starts) if s<b)
 so=a-starts[si];eo=b-starts[ei]
 if si==ei:ts[si].text=vs[si][:so]+new+vs[si][eo:];space(ts[si])
 else:
  ts[si].text=vs[si][:so]+new;space(ts[si])
  for j in range(si+1,ei):ts[j].text=''
  ts[ei].text=vs[ei][eo:];space(ts[ei])
def appendcite(p,c):
 for t in reversed(list(p.iter(W+'t'))):
  v=t.text or ''
  if not v:continue
  s=v.rstrip();tail=v[len(s):]
  t.text=(s[:-1]+' '+c+'.'+tail) if s.endswith('.') else (s+' '+c+tail);space(t);return
def left(p):
 pp=p.find(W+'pPr')
 if pp is None:pp=etree.Element(W+'pPr');p.insert(0,pp)
 for e in list(pp.findall(W+'jc'))+list(pp.findall(W+'bidi')):pp.remove(e)
 e=etree.SubElement(pp,W+'jc');e.set(W+'val','left')
def splitlink(r,ints):
 par=r.getparent();ix=par.index(r);orig=r.find(W+'t').text or '';cur=0;pieces=[]
 for a,b,n in sorted(ints):
  if a>cur:q=copy.deepcopy(r);setrt(q,orig[cur:a]);pieces.append(q)
  q=copy.deepcopy(r);setrt(q,orig[a:b]);h=etree.Element(W+'hyperlink');h.set(W+'anchor',f'_ref_{n}');h.set(W+'history','1');h.append(q);pieces.append(h);cur=b
 if cur<len(orig):q=copy.deepcopy(r);setrt(q,orig[cur:]);pieces.append(q)
 par.remove(r)
 for q in pieces:par.insert(ix,q);ix+=1
with zipfile.ZipFile(SRC) as z:infos=z.infolist();blobs={i.filename:z.read(i.filename) for i in infos}
root=etree.fromstring(blobs['word/document.xml']);fr=etree.fromstring(blobs['word/footnotes.xml']);body=root.find('.//'+W+'body')
# shift existing high references, then unwrap all reference links
for h in list(root.iter(W+'hyperlink')):
 m=re.fullmatch(r'_ref_(\d+)',h.get(W+'anchor') or '')
 if not m:continue
 old=int(m.group(1));new=old+2 if old>=16 else old;h.set(W+'anchor',f'_ref_{new}')
 if new!=old:
  for t in h.iter(W+'t'):
   if t.text:t.text=str(new).translate(FA)
for h in list(root.iter(W+'hyperlink')):
 if not re.fullmatch(r'_ref_\d+',h.get(W+'anchor') or ''):continue
 par=h.getparent();ix=par.index(h)
 for c in list(h):par.insert(ix,c);ix+=1
 par.remove(h)
ps=body.findall(W+'p');head=next(p for p in ps if ptext(p).strip() in {'مراجع و منابع','منابع و مراجع'});hi=ps.index(head)
def find(s):
 m=[p for p in ps[:hi] if s in ptext(p)]
 if len(m)!=1:raise RuntimeError(f'{s}: {len(m)}')
 return m[0]
replace(find('خودروهای خودران و سامانه‌های کمک‌راننده پیشرفته'),'به تصادف بینجامد','به تصادف بینجامد [۱]')
p=find('اهمیت این موضوع دو وجه دارد');replace(p,'با جان انسان‌ها سروکار دارد.','با جان انسان‌ها سروکار دارد [۱].');replace(p,'بی‌آنکه مدل واقعاً بهتر شده باشد.','بی‌آنکه مدل واقعاً بهتر شده باشد [۱۴].')
appendcite(find('به‌روزترین نسخه پایدار'),'[۹]')
appendcite(find('وزن‌های از پیش آموزش‌دیده روی مجموعه‌داده'),'[۹]')
replace(find('رویکردهای نیمه‌نظارتی'),'خود کاملاً بی‌خطا نیست.','خود کاملاً بی‌خطا نیست [۱۶].')
appendcite(find('برای شناسایی این موارد از روش درهم‌سازی ادراکی'),'[۱۷]')
appendcite(find('افزایش داده، مجموعه‌ای از تبدیل‌های تصادفی'),'[۹]')
appendcite(find('کادرهای هر دو تصویر در کنار یکدیگر نگه داشته می‌شوند'),'[۹]')
appendcite(find('هر دو تبدیل نمونه‌هایی می‌سازند'),'[۵، ۱۰]')
appendcite(find('از امتیاز 1F استفاده می‌شود'),'[۸]')
replace(find('افزایش داده مجموعه‌ای از تبدیل‌های تصادفی'),'و کمتر دچار بیش‌برازش گردد.','و کمتر دچار بیش‌برازش گردد [۹].')
appendcite(find('سازوکار توقف زودهنگام برای تعیین نقطه پایان'),'[۹]')
appendcite(find('نبود آن، سلامت فرایند آموزش را تأیید می‌کند'),'[۲۰]')
replace(find('در بازه‌ای قرار دارد که برای مجموعه‌های هم‌تراز'),'این تفاوت که حدود دو و نیم درصد است، ناشی از تفاوت طبیعی دشواری میان دو مجموعه ویدیوی متفاوت است و در بازه‌ای قرار دارد که برای مجموعه‌های هم‌تراز، متعارف به‌شمار می‌رود.','این تفاوت حدود دو و نیم درصد است.')
replace(find('وزن‌های از پیش آموزش‌دیده نیز شناخت خوبی'),' افزون بر این، وزن‌های از پیش آموزش‌دیده نیز شناخت خوبی از این رده داشتند.','')
# rebuild bibliography
children=list(body);hp=children.index(head);old=next(p for p in children[hp+1:] if re.match(r'^\[[۰-۹0-9]+\]',ptext(p).strip()));tpl=copy.deepcopy(old.find(W+'pPr'))
for c in list(body)[hp+1:]:
 if c.tag!=W+'sectPr':body.remove(c)
ids=[int(x) for x in root.xpath('//w:bookmarkStart/@w:id',namespaces={'w':W[1:-1]}) if str(x).isdigit()];bid=max(ids,default=0)+1
sect=body.find(W+'sectPr');ix=body.index(sect) if sect is not None else len(body)
for n,a,t,z,u in BIB:
 p=etree.Element(W+'p')
 if tpl is not None:p.append(copy.deepcopy(tpl))
 left(p);bs=etree.Element(W+'bookmarkStart');bs.set(W+'id',str(bid));bs.set(W+'name',f'_ref_{n}');be=etree.Element(W+'bookmarkEnd');be.set(W+'id',str(bid));bid+=1
 p.append(bs);p.append(run('['+str(n).translate(FA)+'] ','B Zar',12,'fa-IR',True));p.append(run(a));p.append(run(t,italic=True));p.append(run(z));p.append(be);body.insert(ix,p);ix+=1
 if u:
  p=etree.Element(W+'p')
  if tpl is not None:p.append(copy.deepcopy(tpl))
  left(p);p.append(run(u));body.insert(ix,p);ix+=1
# hyperlink citations
ps=body.findall(W+'p');head=next(p for p in ps if ptext(p).strip() in {'مراجع و منابع','منابع و مراجع'});hi=ps.index(head);links=0
for p in ps[:hi]:
 st=p.find('./'+W+'pPr/'+W+'pStyle')
 if st is not None and (st.get(W+'val') or '').lower().startswith('toc'):continue
 ts=list(p.iter(W+'t'));starts=[];k=0
 for t in ts:starts.append(k);k+=len(t.text or '')
 full=''.join(t.text or '' for t in ts);by={}
 for cm in CITE.finditer(full):
  for nm in NUM.finditer(cm.group(0)):
   a=cm.start()+nm.start();b=cm.start()+nm.end();n=int(nm.group(0).translate(TOASC))
   if n not in range(1,22):raise RuntimeError(f'bad ref {n}')
   for s,t in zip(starts,ts):
    v=t.text or ''
    if s<=a and b<=s+len(v):
     r=t.getparent()
     if r.tag!=W+'r' or len(r.findall(W+'t'))!=1:raise RuntimeError('unsupported citation')
     by.setdefault(r,[]).append((a-s,b-s,n));links+=1;break
   else:raise RuntimeError('citation crosses runs')
 for r,ints in list(by.items()):splitlink(r,ints)
# normalize footnotes
for fn in fr.findall(W+'footnote'):
 fid=fn.get(W+'id')
 if not fid or int(fid)<=0:continue
 rs=[r for r in fn.iter(W+'r') if any((t.text or '') for t in r.findall(W+'t'))]
 if not rs:continue
 d=''.join(t.text or '' for t in rs[0].findall(W+'t'))
 if not re.fullmatch(r'[۰-۹]+',d):raise RuntimeError(f'bad footnote {fid}: {d}')
 font(rs[0],'B Zar',10,'fa-IR',True,style='FootnoteReference')
 for r in rs[1:]:font(r,'Times New Roman',10,'en-US')
for x in root.iter(W+'footnoteReference'):
 r=x.getparent()
 if r is not None and r.tag==W+'r':font(r,'B Zar',14,'fa-IR',True,style='FootnoteReference')
blobs['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
blobs['word/footnotes.xml']=etree.tostring(fr,xml_declaration=True,encoding='UTF-8',standalone='yes')
with zipfile.ZipFile(OUT,'w') as z:
 for i in infos:z.writestr(i,blobs[i.filename])
print('links',links,'refs',len(BIB))
