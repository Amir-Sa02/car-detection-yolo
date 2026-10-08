from pathlib import Path
import fitz


REF_DIR = Path(r"D:\projects\car-detection-yolo\thesis\مراجع")
OUT_DIR = Path(r"C:\Users\amir2\Desktop\نسخه ارسالی\مطالعه مقاله IADD")
OUT_DIR.mkdir(parents=True, exist_ok=True)

matches = list(REF_DIR.glob("IET Image Processing*Multi*domain autonomous driving dataset*.pdf"))
if not matches:
    raise FileNotFoundError("IADD paper was not found")
SRC = matches[0]
OUT = OUT_DIR / "مقاله_IADD_هایلایت_مطالعه_دفاع.pdf"

COLORS = {
    "used": (1.0, 0.82, 0.05),       # yellow: directly used in thesis/slides
    "extra": (0.25, 0.78, 0.38),     # green: useful extra knowledge
    "caution": (1.0, 0.43, 0.08),    # orange: interpret carefully
}

# page number is one-based. Coordinates were obtained from the original PDF text blocks.
REGIONS = [
    (1, (46, 108, 523, 172), "used", "عنوان مقاله و موضوع اصلی: مجموعه داده چنددامنه برای بهبود تعمیم مدل ها"),
    (1, (46, 197, 549, 209), "used", "نویسندگان مقاله"),
    (1, (46, 230, 187, 253), "used", "وابستگی سازمانی نویسندگان: دانشگاه علم و صنعت ایران"),
    (1, (205, 234, 550, 435), "used", "چکیده: هدف IADD، بیش از 97 هزار تصویر، شش رده، شرایط گوناگون و ارزیابی تعمیم"),
    (1, (307, 473, 550, 662), "extra", "اهمیت تعمیم در سامانه های رانندگی خودکار و مسئله تغییر دامنه"),

    (2, (46, 48, 546, 221), "used", "جدول مقایسه IADD با مجموعه داده های دیگر؛ اندازه، شهرها، شرایط و تفکیک پذیری"),
    (2, (46, 445, 288, 726), "used", "شهرهای گردآوری، شش رده اصلی و تنوع مسیرهای IADD"),
    (2, (307, 262, 550, 439), "used", "استخراج فریم های کلیدی و وجود داده های بدون برچسب"),
    (2, (307, 453, 550, 606), "extra", "مشارکت های اصلی مقاله و هدف ارزیابی تعمیم میان دامنه ها"),

    (5, (46, 383, 288, 429), "extra", "ساختار بخش معرفی مجموعه داده"),
    (5, (46, 478, 288, 727), "used", "فرایند گردآوری داده در شهرها، مسیرها و شرایط محیطی گوناگون"),
    (5, (307, 48, 550, 500), "used", "تفکیک پذیری ها، نرخ فریم، استخراج با نرخ نیم فریم بر ثانیه، تصاویر تار و حسگرهای جانبی"),
    (5, (307, 525, 550, 727), "used", "آغاز توضیح فرایند برچسب گذاری نیمه خودکار"),

    (6, (46, 323, 288, 489), "used", "سی هزار تصویر دستی، آموزش YoloR، برچسب گذاری خودکار، بازبینی کارشناسان و قالب YOLO"),
    (6, (46, 513, 288, 728), "extra", "تفکیک عناصر صریح و ضمنی در داده های رانندگی"),
    (6, (307, 48, 550, 142), "extra", "ادامه عناصر ضمنی مانند رفتار پرخطر راننده و عابر"),
    (6, (307, 166, 550, 333), "caution", "آمار رسمی 97,528 داده برچسب دار، 171 ویدیو و نسبت رسمی 78/7.2/14.8؛ با نسخه دانلودی پروژه یکسان فرض نشود"),

    (7, (46, 622, 288, 728), "extra", "قیود انتخاب مدل ها و محدودیت منابع محاسباتی"),
    (7, (307, 670, 550, 728), "extra", "معماری های انتخاب شده برای آزمایش مقاله"),

    (8, (46, 202, 288, 335), "extra", "جدول تنظیمات مدل های آزمایش شده در مقاله"),
    (8, (46, 371, 288, 728), "extra", "پیش آموزش روی COCO، یادگیری انتقالی، عدم توازن رده ها و تنظیمات آموزش"),
    (8, (307, 48, 533, 159), "extra", "جدول تعداد پارامتر و هزینه محاسباتی مدل ها"),
    (8, (307, 598, 550, 728), "used", "تعریف AP به عنوان مساحت زیر منحنی دقت-فراخوانی و mAP به عنوان میانگین رده ها"),

    (9, (46, 48, 281, 141), "caution", "نتایج سناریوی دوم؛ mAP مدل YOLOv4 برابر 86.6 است، اما آستانه IoU در این قسمت مشخص نشده"),
    (9, (46, 177, 288, 371), "extra", "سناریوهای آزمایش و مقایسه میان دامنه ها"),
    (9, (307, 545, 550, 728), "caution", "ادعای جداسازی دامنه های آموزش و آزمون در سناریوی دوم؛ الگوریتم تقسیم ویدیویی قابل بازتولید ارائه نشده"),

    (11, (46, 383, 288, 537), "extra", "تحلیل عملکرد رده های کم نمونه با توجه به شکل واضح و تنوع دامنه"),
    (11, (46, 565, 273, 714), "extra", "نتایج آزمایش های تکمیلی مقاله"),
    (11, (307, 383, 550, 716), "extra", "بحث تکمیلی درباره تعمیم و تفاوت دامنه ها"),

    (12, (46, 335, 288, 716), "extra", "آزمایش تعمیم به داده شبیه سازی شده CARLA"),
    (12, (307, 335, 550, 717), "extra", "ترکیب داده CARLA و شرایط روز، شب و باران"),

    (13, (46, 48, 288, 261), "extra", "ادامه نتایج تعمیم میان IADD، KITTI و CARLA"),
    (13, (46, 286, 288, 727), "used", "جمع بندی مقاله و اثر تنوع دامنه IADD بر تعمیم"),
    (13, (307, 48, 550, 154), "extra", "پیشنهادهای آینده: شهرها و شرایط بیشتر، مه و حسگرهای دیگر"),
    (13, (307, 375, 550, 421), "used", "دسترسی به داده و مخزن GitHub"),
]


def quads_in_rect(page, box):
    area = fitz.Rect(box)
    by_line = {}
    for w in page.get_text("words"):
        r = fitz.Rect(w[:4])
        if area.contains(r.tl) or area.contains(r.br) or area.intersects(r):
            key = (w[5], w[6])
            by_line.setdefault(key, []).append(r)
    quads = []
    for key in sorted(by_line):
        rects = by_line[key]
        merged = fitz.Rect(rects[0])
        for r in rects[1:]:
            merged |= r
        # Small inset keeps highlights from touching neighboring columns.
        merged.x0 += 0.4
        merged.x1 -= 0.4
        quads.append(fitz.Quad(merged.tl, merged.tr, merged.bl, merged.br))
    return quads


doc = fitz.open(SRC)
created = 0
for page_no, box, category, note in REGIONS:
    page = doc[page_no - 1]
    quads = quads_in_rect(page, box)
    if not quads:
        raise RuntimeError(f"No text found for page {page_no}, box {box}")
    annot = page.add_highlight_annot(quads)
    annot.set_colors(stroke=COLORS[category])
    annot.set_opacity(0.34)
    annot.set_info(
        title="IADD study guide",
        subject={"used": "Used in thesis/presentation", "extra": "Important extra", "caution": "Read with caution"}[category],
        content=note,
    )
    annot.update()
    created += 1

# A compact sticky-note legend keeps the article page layout unchanged.
legend = doc[0].add_text_annot(
    fitz.Point(557, 95),
    "Highlight legend:\nYellow: used in thesis/presentation\nGreen: important extra knowledge\nOrange: caution or project/article mismatch\nPersian explanations are in the companion Word file.",
)
legend.set_info(title="راهنمای رنگ ها", subject="IADD study highlights")
legend.update()

doc.save(OUT, garbage=4, deflate=True, clean=True)
doc.close()

check = fitz.open(OUT)
annots = sum(1 for p in check for _ in (p.annots() or []))
print(f"source_name={SRC.name.encode('unicode_escape').decode()}")
print(f"output_name={OUT.name.encode('unicode_escape').decode()}")
print(f"pages={check.page_count}")
print(f"region_annotations={created}")
print(f"all_annotations={annots}")
check.close()
