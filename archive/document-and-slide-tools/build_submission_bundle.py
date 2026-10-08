from __future__ import annotations

import csv
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment

P = Path(r'D:\projects\car-detection-yolo')
S = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی')
O = S / 'مدارک تکمیلی و منابع شکل‌ها'
CODE = O / 'کدهای قابل بررسی'
DATA = O / 'داده‌های نمودار و جدول'
DRAW = O / 'شکل‌های قابل ویرایش'
EVID = O / 'شواهد بازبینی'
for d in (CODE, DATA, DRAW, EVID): d.mkdir(parents=True, exist_ok=True)

def cp(src: Path, dst: Path):
    if not src.exists():
        print('MISSING', src)
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True

def write(path, content):
    path.write_text(content.strip()+'\n', encoding='utf-8')

# Preserve actual project scripts. The v5 builder is evidence, not a script to run:
# its normal main can replace the output dataset.
code_files = {
 'build_subset_v4.py': P/'colab/build_subset_v4.py',
 'build_subset_v5.py': P/'colab/build_subset_v5.py',
 'IADD_YOLOv11_Colab_pervideo.ipynb': P/'colab/IADD_YOLOv11_Colab_pervideo.ipynb',
 'make_label_evidence.py': P/'docs/make_label_evidence.py',
 'compute_v5_validity.py': P/'docs/compute_v5_validity.py',
 'make_figures_ch1.py': P/'thesis/فصل1_پیشینه/کد/make_figures_ch1.py',
 'make_figures_ch2.py': P/'thesis/فصل2_روش_و_داده/کد/make_figures_ch2.py',
 'make_figures_ch3.py': P/'thesis/فصل3_نتایج/کد/make_figures_ch3.py',
 'export_eval_curves.py': P/'thesis/فصل3_نتایج/کد/export_eval_curves.py',
 'make_demo_gt_pred.py': P/'thesis/فصل3_نتایج/کد/make_demo_gt_pred.py',
 'render_plain_gt.py': P/'thesis/فصل3_نتایج/کد/render_plain_gt.py',
 'render_plain_boxes.py': P/'thesis/فصل3_نتایج/کد/render_plain_boxes.py',
 'figstyle.py': P/'thesis/00_قالب_و_آیین‌نامه/figstyle.py',
}
for name, src in code_files.items(): cp(src, CODE/name)

for name, src in {
 'stats.json': P/'thesis/فصل2_روش_و_داده/شکل‌ها/stats.json',
 'perclass_metrics.csv': P/'thesis/فصل3_نتایج/شکل‌ها/perclass_metrics.csv',
 'eval_curves.npz': P/'thesis/فصل3_نتایج/شکل‌ها/eval_curves.npz',
 'pervideo_review_summary.csv': P/'docs/dataset_label_evidence/SUMMARY.csv',
 'BROKEN_VIDEOS.md': P/'docs/dataset_label_evidence/BROKEN_VIDEOS.md',
}.items(): cp(src, DATA/name)

for name in ('fig_1_1.png','fig_1_3.png'):
 cp(P/'thesis/فصل1_پیشینه/شکل‌ها'/name, DRAW/name)
for name in ('fig_2_1.png','fig_2_2.png','fig_2_3.png','fig_2_4.png'):
 cp(P/'thesis/فصل2_روش_و_داده/شکل‌ها'/name, DRAW/name)
for name in ('fig_3_1.png','fig_3_2.png','fig_3_3.png','fig_3_4.png','fig_3_5.png','fig_3_6.png','fig_3_7.png'):
 cp(P/'thesis/فصل3_نتایج/شکل‌ها'/name, DRAW/name)

for vid, srcdir in [
 ('Record426_D', P/'docs/dataset_label_evidence/val_Record426_D_mAP0.007'),
 ('Record046_D', P/'docs/dataset_label_evidence/train_Record046_D_mAP0.451')
]:
 for f in sorted(srcdir.glob('*.jpg')): cp(f, EVID/vid/f.name)

# A simple, editable Draw.io recreation of authored diagrams; never called an
# original design file because the originals were generated as raster by Python.
def drawio(path, label, nodes, edges):
    root=ET.Element('mxfile', {'host':'app.diagrams.net', 'modified':'2026-09-23T00:00:00.000Z', 'agent':'Codex', 'version':'24.7.17'})
    diagram=ET.SubElement(root,'diagram',{'id':'main','name':label})
    model=ET.SubElement(diagram,'mxGraphModel',{'dx':'1200','dy':'800','grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':'1169','pageHeight':'827','math':'0','shadow':'0'})
    r=ET.SubElement(model,'root'); ET.SubElement(r,'mxCell',{'id':'0'}); ET.SubElement(r,'mxCell',{'id':'1','parent':'0'})
    for n in nodes:
        ident,txt,x,y,w,h,color=n
        c=ET.SubElement(r,'mxCell',{'id':ident,'value':txt,'style':f'rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor={color};fontColor=#ffffff;fontSize=18;fontFamily=B Zar;align=center;verticalAlign=middle;','vertex':'1','parent':'1'})
        ET.SubElement(c,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'})
    for i,(a,b) in enumerate(edges):
        c=ET.SubElement(r,'mxCell',{'id':f'e{i}','style':'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeColor=#596579;strokeWidth=2;','edge':'1','parent':'1','source':a,'target':b})
        ET.SubElement(c,'mxGeometry',{'relative':'1','as':'geometry'})
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)

drawio(DRAW/'شکل_۲-۱_بازسازی_قابل_ویرایش.drawio','مراحل ساخت زیرمجموعه',[
 ('a','دادهٔ خام<br>بخش ۲-۲-۱',835,80,260,100,'#667080'),
 ('b','حذف ویدیوهای تکراری<br>بخش ۲-۲-۲-۲',495,80,260,100,'#b03836'),
 ('c','حذف برچسب‌های معیوب<br>بخش ۲-۲-۲-۳',155,80,260,100,'#704090'),
 ('d','تقسیم در سطح ویدیو<br>بخش ۲-۲-۲-۱',155,300,260,100,'#183d69'),
 ('e','نمونه‌گیری با حفظ رده‌های نادر<br>بخش ۲-۲-۳',495,300,260,100,'#0e7f87'),
 ('f','دادهٔ نهایی<br>بخش ۲-۲-۴',835,300,260,100,'#23804b')],
 [('a','b'),('b','c'),('c','d'),('d','e'),('e','f')])

drawio(DRAW/'شکل_۱-۱_بازسازی_قابل_ویرایش.drawio','روش‌های آشکارسازی',[
 ('a','ورودی',890,80,180,75,'#667080'),('b','استخراج ویژگی',660,80,180,75,'#183d69'),
 ('c','پیشنهاد ناحیه',430,80,180,75,'#d17e21'),('d','رده‌بندی و کادر',200,80,180,75,'#0e7f87'),('e','خروجی',0,80,150,75,'#23804b'),
 ('f','ورودی',890,290,180,75,'#667080'),('g','استخراج ویژگی',610,290,220,75,'#183d69'),
 ('h','پیش‌بینی هم‌زمان کادر و رده',230,290,320,75,'#0e7f87'),('i','خروجی',0,290,150,75,'#23804b')],
 [('a','b'),('b','c'),('c','d'),('d','e'),('f','g'),('g','h'),('h','i')])

# Figure 1-3 is geometric (IoU). The exact plotted values remain in the
# Python source; this editable diagram preserves the three visual cases.
def iou_drawio():
    root=ET.Element('mxfile',{'host':'app.diagrams.net','version':'24.7.17'})
    dia=ET.SubElement(root,'diagram',{'id':'iou','name':'نسبت هم‌پوشانی'})
    model=ET.SubElement(dia,'mxGraphModel',{'page':'1','pageWidth':'1169','pageHeight':'827'})
    r=ET.SubElement(model,'root'); ET.SubElement(r,'mxCell',{'id':'0'}); ET.SubElement(r,'mxCell',{'id':'1','parent':'0'})
    shifts=[(0,165,'ضعیف'),(380,90,'مرزی'),(760,30,'خوب')]
    for i,(x,dx,label) in enumerate(shifts):
        for suffix, xx, stroke, dash in [('gt',x+50,'#23804b','0'),('pred',x+50+dx,'#d17e21','1')]:
            c=ET.SubElement(r,'mxCell',{'id':f'{i}_{suffix}','value':'','style':f'rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor={stroke};strokeWidth=3;dashed={dash};','vertex':'1','parent':'1'})
            ET.SubElement(c,'mxGeometry',{'x':str(xx),'y':'180','width':'150','height':'150','as':'geometry'})
        c=ET.SubElement(r,'mxCell',{'id':f't{i}','value':label,'style':'text;html=1;align=center;verticalAlign=middle;fontSize=22;fontFamily=B Zar;','vertex':'1','parent':'1'})
        ET.SubElement(c,'mxGeometry',{'x':str(x+25),'y':'365','width':'310','height':'50','as':'geometry'})
    ET.ElementTree(root).write(DRAW/'شکل_۱-۳_بازسازی_قابل_ویرایش.drawio',encoding='utf-8',xml_declaration=True)
iou_drawio()

# The editable source for IoU is the original Python, which draws exact geometry.

stats=json.loads((DATA/'stats.json').read_text(encoding='utf-8'))
splits=('train','val','test')
names=('شخص','خودروی سبک','موتورسیکلت','اتوبوس','خودروی باری','چراغ راهنمایی')
wb=Workbook(); ws=wb.active; ws.title='جدول ۲-۱'
ws.append(['بخش','ویدیو','تصویر','نمونهٔ برچسب‌خورده','نمونه در تصویر'])
for s,fa in zip(splits,('آموزش','اعتبارسنجی','آزمون')):
 d=stats[s]; i=ws.max_row+1
 ws.append([fa,d['videos'],d['images'],d['instances'],f'=D{i}/C{i}'])
ws=wb.create_sheet('جدول ۲-۲'); ws.append(['رده','آموزش','اعتبارسنجی','آزمون'])
for c,name in enumerate(names): ws.append([name]+[stats[s]['cls'][str(c)] for s in splits])
ws.append(['مجموع']+[stats[s]['instances'] for s in splits])
ws=wb.create_sheet('شکل ۲-۲'); ws.append(['رده','آموزش ٪','اعتبارسنجی ٪','آزمون ٪'])
for c,name in enumerate(names): ws.append([name]+[round(100*stats[s]['cls'][str(c)]/stats[s]['instances'],4) for s in splits])
chart=BarChart(); chart.title='سهم رده‌ها از نمونه‌های هر بخش'; chart.type='col'; chart.grouping='clustered'; chart.y_axis.title='درصد'
chart.add_data(Reference(ws,min_col=2,max_col=4,min_row=1,max_row=7),titles_from_data=True); chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=7)); ws.add_chart(chart,'F2')
ws=wb.create_sheet('جدول ۲-۳'); ws.append(['اندازهٔ شیء','آموزش ٪','اعتبارسنجی ٪','آزمون ٪'])
for k,name in enumerate(('کوچک: سطح کادر < ۱٪','متوسط: ۱٪ تا < ۶٪','بزرگ: ≥ ۶٪')):
 ws.append([name]+[round(100*stats[s]['size'][str(k)]/stats[s]['instances'],4) for s in splits])
ws=wb.create_sheet('شکل ۲-۳'); ws.append(['اندازه','آموزش ٪','اعتبارسنجی ٪','آزمون ٪'])
for k,name in enumerate(('کوچک','متوسط','بزرگ')):
 ws.append([name]+[round(100*stats[s]['size'][str(k)]/stats[s]['instances'],4) for s in splits])
chart=BarChart(); chart.title='اندازهٔ اشیا در سه بخش'; chart.type='col'; chart.grouping='clustered'; chart.add_data(Reference(ws,min_col=2,max_col=4,min_row=1,max_row=4),titles_from_data=True); chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=4)); ws.add_chart(chart,'F2')
ws=wb.create_sheet('جدول ۲-۴'); ws.append(['شرایط','آموزش ٪','اعتبارسنجی ٪','آزمون ٪'])
for code,name in zip('DNRA',('روز','شب','باران','روز ابری')):
 ws.append([name]+[round(100*stats[s]['cond'].get(code,0)/stats[s]['images'],1) for s in splits])
ws=wb.create_sheet('شکل ۲-۴'); ws.append(['شرایط','آموزش ٪','اعتبارسنجی ٪','آزمون ٪'])
for code,name in zip('DNRA',('روز','شب','باران','ابری')): ws.append([name]+[round(100*stats[s]['cond'].get(code,0)/stats[s]['images'],4) for s in splits])
chart=BarChart(); chart.title='شرایط محیطی در سه بخش'; chart.type='col'; chart.grouping='clustered'; chart.add_data(Reference(ws,min_col=2,max_col=4,min_row=1,max_row=5),titles_from_data=True); chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=5)); ws.add_chart(chart,'F2')
ws=wb.create_sheet('توضیح'); ws.append(['منبع', 'توضیح'])
ws.append(['stats.json','خروجی compute_v5_validity.py از فایل‌های images و labels زیرمجموعهٔ V5'])
ws.append(['نمونه در تصویر','تعداد کادرها تقسیم بر تعداد تصویر؛ مقادیرِ نمایشی به یک رقم اعشار گرد می‌شوند.'])
ws.append(['اندازه','مساحت نسبی کادر = عرض نرمال‌شده × ارتفاع نرمال‌شده'])
ws.append(['شرایط','حرف آخر نام ویدیو D/N/R/A؛ شمار تصویر، نه شمار ویدیو'])
ws=wb.create_sheet('شکل ۳-۲'); ws.append(['راهبرد','اعتبارسنجی mAP@0.5','آزمون mAP@0.5'])
ws.append(['SGD',0.846,0.867]); ws.append(['AdamW و زمان‌بند کسینوسی',0.849,0.874])
chart=BarChart(); chart.title='مقایسه دو راهبرد'; chart.type='col'; chart.grouping='clustered'; chart.add_data(Reference(ws,min_col=2,max_col=3,min_row=1,max_row=3),titles_from_data=True); chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=3)); ws.add_chart(chart,'E2')
ws=wb.create_sheet('جدول ۳-۲ و شکل ۳-۳'); ws.append(['رده','دقت','فراخوانی','F1','AP@0.5','AP@0.5:0.95'])
with (DATA/'perclass_metrics.csv').open(encoding='utf-8-sig',newline='') as f:
 for row in csv.DictReader(f):
  ws.append([names[('person','car','motorcycle','bus','truck','traffic_light').index(row['class'])]]+
            [float(row[k]) for k in ('P','R','F1','mAP50','mAP50-95')])
chart=BarChart(); chart.title='معیارهای هر رده'; chart.type='col'; chart.grouping='clustered'; chart.add_data(Reference(ws,min_col=4,max_col=5,min_row=1,max_row=7),titles_from_data=True); chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=7)); ws.add_chart(chart,'H2')
for ws in wb:
 ws.sheet_view.rightToLeft=True
 ws.freeze_panes='B2'
 for cell in ws[1]: cell.fill=PatternFill('solid',fgColor='183D69'); cell.font=Font(name='B Zar',bold=True,color='FFFFFF',size=12)
 for col in ws.columns:
  letter=col[0].column_letter; ws.column_dimensions[letter].width=min(60,max(17,max(len(str(c.value or '')) for c in col)+3))
 for row in ws.iter_rows(min_row=2):
  for cell in row: cell.font=Font(name='B Zar',size=12); cell.alignment=Alignment(horizontal='center')
wb.save(DATA/'اعداد_فصل_۲_و_نمودارهای_قابل_ویرایش.xlsx')

write(O/'راهنمای_مطالعه_و_منشأ_شواهد.md', r'''
# راهنمای بستهٔ تکمیلی پروژه

این پوشه مکمل فایل‌های موجود در `نسخه ارسالی` است. پایان‌نامه، پاورپوینت، نتایج ران ۸ و کد آموزش را دوباره کپی نکرده‌ایم. فایل‌های `make_figures_*` و دفترچهٔ `IADD_YOLOv11_Colab_pervideo.ipynb` همان منابع موجود در پروژه‌اند. فایل‌های `.drawio` **بازسازی قابل ویرایش** از شکل‌های ساخته‌شده با پایتون‌اند؛ فایل اصلی تاریخی نرم‌افزار رسم نیستند.

## مسیر مطالعهٔ ۱۰ تا ۱۲ روزه

۱. روز ۱: جدول‌های ۲-۱ و ۲-۲ را در فایل اکسل باز کنید. «نمونه» یک کادر شیء است، نه یک تصویر؛ نمونه در تصویر = مجموع کادرها ÷ شمار تصاویر. با فایل `stats.json` مقایسه کنید.

۲. روز ۲: جدول‌های ۲-۳ و ۲-۴، شکل‌های ۲-۲ تا ۲-۴ و `compute_v5_validity.py` را ببینید. اندازه از حاصل‌ضرب عرض و ارتفاع نرمال‌شدهٔ هر کادر در فایل برچسب حساب می‌شود. شرایط محیطی از حرف آخر شناسهٔ ویدیو می‌آید؛ نیازی به طبقه‌بندی چشمی هزاران تصویر نیست. ساخت نمودارها در اکسل هم ممکن است؛ دادهٔ خام و نمودار قابل ویرایش همراه این بسته است.

۳. روزهای ۳ و ۴: `build_subset_v4.py` و `build_subset_v5.py` را کنار هم بخوانید. فرق اصلی: پنج ویدیوی کنارگذاشته‌شده، بذر تازه و تقسیم مجدد در سطح ویدیو. مقدار `DRY_RUN=False` در فایل V5 را بدون تغییر اجرا نکنید: خروجی V5 را از نو می‌سازد. فقط کد را مطالعه کنید. بخش‌های `record_dirs`، `allocate`، `sample` و بررسی اشتراک را دنبال کنید.

۴. روز ۵: دفترچهٔ `IADD_YOLOv11_Colab_pervideo.ipynb` و `pervideo_review_summary.csv` را بخوانید. این دفترچه مدل ران ۵ را بر هر ویدیو جداگانه ارزیابی و mAP@0.5 را ثبت کرده است. آستانهٔ ۰٫۶۳ صرفاً **آستانهٔ انتخاب برای بازبینی** بود. ۱۳ ویدیو زیر آن قرار گرفتند؛ پس از دیدن کادرهای برچسب، فقط ۴۲۶ و ۴۶ به‌عنوان معیوب تأیید شدند. ۱۱ ویدیوی دشوار حفظ شدند.

۵. روز ۶: `make_label_evidence.py` و تصاویر پوشهٔ «شواهد بازبینی» را نگاه کنید. هر سطر برچسب YOLO شامل `class cx cy w h` با مختصات نرمال‌شده است. کد با ضرب در عرض/ارتفاع تصویر، کادر را روی عکس می‌کشد. برای پاسخ در جلسه می‌توان گفت: «امتیاز هر ویدیو غربال اولیه بود؛ سپس برچسب مرجع را روی چند فریم رسم و خطاهای واقعی را چشمی تأیید کردیم.» دربارهٔ اینکه چه کسی نخستین‌بار کد را نوشته، ادعای نادرست نکنید؛ خودتان کد را اجرا و خروجی را وارسی کنید.

۶. روز ۷: `audit_duplicate_pairs.py` را بخوانید و اجرا کنید. سه جفت بررسی‌شده عبارت‌اند از ۴۰۷/۴۰۹، ۴۱۶/۴۳۸، ۰۴۳/۰۴۲. کد با dHash فاصلهٔ دیداری فریم‌ها را می‌سنجد. این بررسی نشانگر شباهت است؛ تشخیص نهایی تکراری بودن با نگاه به نمونه‌های متناظر و دنبالهٔ ویدیو انجام می‌شود. در V5 یک عضو از هر جفت کنار گذاشته شد.

۷. روز ۸: شکل ۱-۱ و ۲-۱ را در draw.io باز کنید. شکل ۱-۳ با `make_figures_ch1.py` و مستطیل‌های دقیق رسم شده؛ شکل ۱-۲ از مقاله استخراج شده و شکل تألیفی پروژه نیست. کد `make_figures_ch2.py` منبع تصویری شکل‌های ۲-۱ تا ۲-۴ است.

۸. روزهای ۹ و ۱۰: `make_figures_ch3.py` را بخوانید. شکل ۳-۱ از `results.csv` ران ۸؛ شکل ۳-۲ از چهار مقدار **صریحاً داخل کد**؛ شکل ۳-۳ و جدول ۳-۲ از `perclass_metrics.csv`؛ شکل ۳-۴ از `eval_curves.npz`؛ شکل ۳-۵ از آرایهٔ ماتریس ثبت‌شده در کد؛ شکل‌های ۳-۶ و ۳-۷ از برچسب‌های آزمون و خروجی `best.pt` ساخته شده‌اند. برای داده‌های خام نمودارها به فولدر نتایجِ موجود در بستهٔ اصلی رجوع کنید. کد ساخت تصاویر کیفی `make_demo_gt_pred.py` است.

۹. روزهای ۱۱ و ۱۲: با اسلایدها تمرین کنید. هر عدد را به یکی از `stats.json`، `perclass_metrics.csv`، `results.csv`، یا گزارش ارزیابی ویدیو وصل کنید. اگر منشأ عددی فقط در یک شکل رستری است، آن را دادهٔ خام قابل محاسبه معرفی نکنید.

## نکتهٔ مهم دربارهٔ اسلاید ۱۴

در نسخهٔ فعلی ارائه نوشته شده «هم‌پوشانی ۰٫۰۰۷» و «هم‌پوشانی ۰٫۴۵۱». این عنوان **اشتباه است**: عددها `mAP@0.5` هر ویدیو در ران ۵ هستند، نه IoU یک کادر. در اسلاید باید به «mAP@0.5 ویدیو» تغییر یابد. این بسته خود ارائه را تغییر نمی‌دهد. `pervideo_run5.csv` کامل در فایل‌های محلی پیدا نشد؛ `SUMMARY.csv` شامل ۱۳ مورد بازبینی‌شده است و دفترچهٔ محاسبهٔ اصل اعداد موجود است. این تفاوت را پنهان نکنید.

## فهرست منشأ شکل‌ها

| مورد | داده / منبع | فایل بازتولید |
|---|---|---|
| جدول ۲-۱ و ۲-۲ | برچسب‌های V5 | `compute_v5_validity.py`، `stats.json` و اکسل این پوشه |
| شکل ۲-۲، ۲-۳، ۲-۴ | شمار رده، اندازهٔ کادر، پسوند شناسه | `make_figures_ch2.py` و اکسل |
| جدول ۲-۳، ۲-۴ | `stats.json` | اکسل |
| شکل ۳-۱ | ران ۸ `results.csv` | `make_figures_ch3.py` |
| شکل ۳-۲ | چهار مقدار ارزیابی ران ۷ و ۸ | `make_figures_ch3.py`، تابع `fig_3_2` |
| جدول ۳-۲ و شکل ۳-۳ | `perclass_metrics.csv` | `make_figures_ch3.py`، تابع `fig_3_3` |
| شکل ۳-۴، ۳-۵ | خروجی ارزیابی ران ۸ | `export_eval_curves.py`، `make_figures_ch3.py` |
| شکل ۳-۶، ۳-۷ | عکس، برچسب YOLO، `best.pt` | `make_demo_gt_pred.py`، `make_figures_ch3.py` |
| شکل ۱-۱، ۱-۳، ۲-۱ | نمودار مفهومی/فرایندی | فایل‌های پایتون؛ برای ۱-۱ و ۲-۱ نسخهٔ بازسازی‌شدهٔ draw.io |
| شکل ۱-۲ | مقالهٔ Sapkota و همکاران | `make_figures_ch1.py`؛ منبع تألیفی نیست |

**محدودیت:** بعضی کدهای قدیمی مسیرهای مطلق سیستم اولیه را دارند و برای اجرای مجدد باید مسیر ورودی/خروجی در نسخهٔ کپی اصلاح شود؛ داده‌های فصل ۲ در اکسل بدون اجرای مجدد کل دیتاست قابل بررسی‌اند. دفترچهٔ per-video به وزن ران ۵ و V4 نیاز دارد و اجرای آن پردازشی است، نه یک دستور سریع روز دفاع.
''')

# Simple manifest: hashes allow the receiver to check integrity without copying
# the full dataset into the hand-in folder.
with (O/'فهرست_فایل‌ها_sha256.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f); w.writerow(['path','bytes','sha256'])
 for file in sorted(O.rglob('*')):
  if file.is_file() and file.name!='فهرست_فایل‌ها_sha256.csv':
   w.writerow([str(file.relative_to(O)),file.stat().st_size,hashlib.sha256(file.read_bytes()).hexdigest()])
print('BUILT',O)
