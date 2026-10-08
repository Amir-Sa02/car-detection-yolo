# -*- coding: utf-8 -*-
"""نسخه هایلایت‌شده مقاله‌ها را می‌سازد.

هر جمله‌ای از مقاله که در پایان‌نامه به آن استناد شده، به‌صورت **کامل** زرد
می‌شود - نه چند کلمه از وسط جمله. روی هر هایلایت که کلیک کنی، یادداشتش می‌گوید
کدام بند پایان‌نامه و دقیقاً کدام جملهٔ فارسی روی آن بنا شده است.

فایل‌های اصلی دست‌نخورده می‌مانند؛ خروجی در پوشه «هایلایت‌شده» ساخته می‌شود.

روش: هر ادعا با یک «لنگر» کوتاه و یکتا پیدا می‌شود، بعد از روی مختصات واژه‌ها
تا نقطهٔ پیش و نقطهٔ پس از آن گسترش می‌یابد تا جملهٔ کامل به دست آید، و همه
سطرهای آن جمله هایلایت می‌شوند.
"""
import io
import os
import re
import sys

import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "هایلایت‌شده")
os.makedirs(OUT, exist_ok=True)

IADD = ("IET Image Processing - 2022 - Khosravian - Multi‐domain autonomous "
        "driving dataset  Towards enhancing the generalization of.pdf")

# شماره هر فایل برابر شماره همان مرجع در بخش «مراجع و منابع» پایان‌نامه است
REF_NO = {
    "Chaman 2025 - Real-Time Vehicle Detection ADAS YOLOv11 (ETASR).pdf": 1,
    "Chaman 2025 - Comparative YOLOv11 vs YOLOv12 (IJTDI).pdf": 2,
    "YOLOV11 AN OVERVIEW OF THE KEY ARCHITECTURAL.pdf": 3,
    "IET Image Processing - 2022 - Khosravian - Multi‐domain autonomous driving dataset  Towards enhancing the generalization of.pdf": 4,
    "Liang 2025 - Vehicle-Road Cooperative Driving improved YOLO11 (Sci Reports).pdf": 5,
    "Microsoft COCO Common Objects in Context.pdf": 6,
    "Lin 2017 - Focal Loss for Dense Object Detection.pdf": 7,
    "Liu 2016 - SSD Single Shot MultiBox Detector.pdf": 8,
    "Loshchilov 2019 - Decoupled Weight Decay Regularization (AdamW).pdf": 9,
    "Loshchilov 2017 - SGDR Warm Restarts (Cosine Schedule).pdf": 10,
    "You Only Look Once Unified, Real-Time Object Detection.pdf": 11,
    "Ren 2015 - Faster R-CNN.pdf": 12,
    "Sapkota 2025 - YOLO Decadal Comprehensive Review.pdf": 13,
    "YOLOV4 A BREAKTHROUGH IN REAL-TIME OBJECT.pdf": 14,
    "mixup BEYOND EMPIRICAL RISK MINIMIZATION.pdf": 15,
    "Object Detection in 20 Years A Survey.pdf": 16,
}


def numbered(fname):
    """نام خروجی با پیشوند شماره مرجع تا ترتیب پوشه با بخش مراجع یکی شود."""
    return "%02d - %s" % (REF_NO[fname], fname)


# فایل -> [(لنگر جست‌وجو، بند پایان‌نامه، جملهٔ فارسیِ متکی بر آن)]
JOBS = {
    IADD: [
        ("the IADD contains 97,528 labelled data", "بند ۱-۵-۲ (ص ۲۶) و جدول ۱-۱ (ص ۲۷)",
         "«این مجموعه شامل ۹۷٬۵۲۸ تصویر برچسب‌گذاری‌شده است که از ۱۷۱ ویدیوی "
         "ضبط‌شده در شهرهای مختلف ایران استخراج شده‌اند.»"),
        ("Of these images, 78% are used for training", "جدول ۱-۱ (ص ۲۷)",
         "سطر «تقسیم آموزش / اعتبارسنجی / آزمون» با مقدار ٪۷۸ / ٪۷٫۲ / ٪۱۴٫۸"),
        ("First, a small portion of the dataset containing", "بند ۱-۵-۲ (ص ۲۶)",
         "«نخست حدود ۳۰٬۰۰۰ تصویر به‌صورت دستی برچسب‌گذاری شده و برای آموزش یک "
         "مدل یادگیری عمیق به‌کار رفته‌اند.»"),
        ("The keyframes have been extracted with a sampling rate", "بند ۱-۵-۲ (ص ۲۶)",
         "«تصاویر این مجموعه با نرخ نمونه‌برداری نیم فریم بر ثانیه از ویدیوها "
         "استخراج شده است.»"),
        ("the images in the IADD have been presented with the resolutions",
         "جدول ۱-۱ (ص ۲۷)",
         "سطر «تفکیک‌پذیری تصاویر» با مقدار ۶۴۰×۴۸۰ تا ۳۸۴۰×۲۱۶۰"),
        ("the images have been acquired from the cities of Tehran", "جدول ۱-۱ (ص ۲۷)",
         "سطر «شمار شهرهای گردآوری» با مقدار ۸"),
        ("Contrary to the datasets of KITTI", "بند ۱-۵-۲ (ص ۲۶)",
         "«استفاده از چندین دوربین با تفکیک‌پذیری‌های متفاوت به‌منظور کاهش "
         "وابستگی مدل به یک دوربین خاص.»"),
        ("A semi-supervised approach has also been employed",
         "بند ۱-۵-۲ (ص ۲۶)، ۲-۲-۲-۳ (ص ۳۴) و ۴-۳-۳ (ص ۶۴)",
         "«به‌دلیل هزینه و زمان‌بر بودن برچسب‌گذاری دستی، از یک رویکرد "
         "نیمه‌نظارتی استفاده شده است.» — پایهٔ کل بحث نوفهٔ برچسب."),
    ],
    "YOLOV11 AN OVERVIEW OF THE KEY ARCHITECTURAL.pdf": [
        ("It employs two smaller convolutions instead of one large convolution",
         "بند ۱-۳-۴ (ص ۲۱)",
         "«این بلوک به‌جای یک پیچش بزرگ از دو پیچش کوچک‌تر استفاده می‌کند و در "
         "نتیجه بار محاسباتی را کاهش و سرعت استخراج ویژگی را افزایش می‌دهد.»"),
        ("YOLO11 retains the Spatial Pyramid Pooling", "بند ۱-۳-۴ (ص ۲۱)",
         "«بلوک SPPF که ادغام هرمی مکانی سریع را انجام می‌دهد… از نسخه‌های "
         "پیشین حفظ شده است.»"),
        ("This attention mechanism enables the model to concentrate",
         "بند ۱-۳-۴ (ص ۲۱) و ۱-۶-۳ (ص ۲۹)",
         "«طبق گزارش مرجع [۳]، به‌طور خاص دقت تشخیص اشیای کوچک و اشیایی که تا "
         "حدی پوشیده شده‌اند را بهبود می‌بخشد.»"),
        ("versatility across different model sizes", "بند ۱-۳-۴ (ص ۲۱)",
         "«این معماری در پنج اندازه مختلف عرضه می‌شود.»"),
    ],
    "Liang 2025 - Vehicle-Road Cooperative Driving improved YOLO11 (Sci Reports).pdf": [
        ("DAIR-V2X-I dataset", "جدول ۴-۱ (ص ۶۳)",
         "ستون مجموعه‌داده: «DAIR-V2X-I (عمومی)» — نشان می‌دهد ارزیابی روی دادهٔ "
         "عمومی انجام شده، نه دادهٔ اختصاصی."),
    ],
    "Chaman 2025 - Real-Time Vehicle Detection ADAS YOLOv11 (ETASR).pdf": [
        ("A custom dataset of 38,500", "جدول ۴-۱ (ص ۶۳)",
         "ستون مجموعه‌داده: «اختصاصی و عمومی» — بخش اختصاصی."),
        ("Additional samples", "جدول ۴-۱ (ص ۶۳)",
         "ستون مجموعه‌داده: «اختصاصی و عمومی» — بخش عمومی."),
    ],
    "Chaman 2025 - Comparative YOLOv11 vs YOLOv12 (IJTDI).pdf": [
        ("^Each image underwent manual annotation using Roboflow, with bounding boxes", "جدول ۴-۱ (ص ۶۳)",
         "ستون مجموعه‌داده: «اختصاصی»."),
    ],
    "Microsoft COCO Common Objects in Context.pdf": [
        ("We present a new dataset with the goal", "بند ۱-۵-۱ (ص ۲۶)",
         "«مجموعه‌داده COCO به‌عنوان مرجع استاندارد شناخته می‌شود که شامل بیش "
         "از سیصد هزار تصویر در هشتاد رده شیء است.»"),
    ],
    "Object Detection in 20 Years A Survey.pdf": [
        ("There are two groups of detectors in the deep learning era",
         "بند ۱-۳ (ص ۱۸)",
         "«روش‌های مبتنی بر یادگیری عمیق… امروزه به دو خانواده اصلی تقسیم "
         "می‌شوند.»"),
        ("the challenges in object detection include but are not limited to", "بند ۱-۶-۳ (ص ۲۹)",
         "«تشخیص اشیای کوچک، یکی از دشوارترین جنبه‌های مسئله تشخیص اشیا "
         "به‌شمار می‌رود.»"),
    ],
    "You Only Look Once Unified, Real-Time Object Detection.pdf": [
        ("processes images in real-time at 45 frames per second", "بند ۱-۳-۲ (ص ۱۹)",
         "«حذف مرحله پیشنهاد ناحیه، سرعت را چند برابر افزایش می‌دهد.»"),
        ("Our system divides the input image into an", "بند ۱-۳-۲ (ص ۱۹)",
         "«تصویر ورودی به یک شبکه مشبک تقسیم می‌شود و هر خانه از شبکه مسئول "
         "پیش‌بینی اشیایی است که مرکزشان درون آن خانه قرار دارد.»"),
    ],
    "Ren 2015 - Faster R-CNN.pdf": [
        ("we introduce a Region Proposal Network", "بند ۱-۳-۱ (ص ۱۸)",
         "«در آن، خودِ شبکه عصبی وظیفه تولید نواحی کاندید را بر عهده می‌گیرد و "
         "بدین ترتیب سرعت مرحله نخست به‌طور چشمگیری افزایش می‌یابد.»"),
    ],
    "Liu 2016 - SSD Single Shot MultiBox Detector.pdf": [
        ("Our approach, named SSD, discretizes the output space", "بند ۱-۳-۲ (ص ۱۹)",
         "«آشکارساز تک‌گذر چندکادره… پیش‌بینی را هم‌زمان روی چند نقشه ویژگی با "
         "تفکیک‌پذیری متفاوت انجام می‌دهد تا اشیا در مقیاس‌های گوناگون بهتر "
         "تشخیص داده شوند.»"),
    ],
    "Loshchilov 2019 - Decoupled Weight Decay Regularization (AdamW).pdf": [
        ("to recover the original formulation of weight decay regularization",
         "بند ۲-۵ (ص ۴۲)، ۳-۲ (ص ۴۹) و ۴-۱-۳ (ص ۶۲)",
         "«افزون بر آن، سازوکار کاهش وزن را به‌صورت مستقل از گرادیان اعمال "
         "می‌کند.»"),
    ],
    "Loshchilov 2017 - SGDR Warm Restarts (Cosine Schedule).pdf": [
        ("warm restart technique for stochastic gradient descent", "بند ۲-۵ (ص ۴۲)",
         "«از زمان‌بند کسینوسی استفاده شد که در مرجع [۱۰] معرفی شده است.»"),
    ],
    "mixup BEYOND EMPIRICAL RISK MINIMIZATION.pdf": [
        ("mixup trains a neural network on convex combinations", "بند ۱-۶-۴ (ص ۲۹) و ۲-۳ (ص ۴۱)",
         "«روش آمیزش… دو تصویر را با یکدیگر ترکیب می‌کند… و برچسب‌ها را نیز "
         "درهم می‌آمیزد.»"),
    ],
    "Lin 2017 - Focal Loss for Dense Object Detection.pdf": [
        ("We propose to address this class imbalance by reshaping",
         "بند ۴-۵-۳ (ص ۶۶)",
         "«خطای کانونی… وزن نمونه‌های آسان را کاهش می‌دهد تا شبکه بر نمونه‌های "
         "دشوار متمرکز شود.»"),
    ],
    "Sapkota 2025 - YOLO Decadal Comprehensive Review.pdf": [
        ("to explore each version", "بند ۱-۳-۳ (ص ۲۰)",
         "«مرور جامعی که اخیراً بر یک دهه تحول این خانواده انجام شده است، نشان "
         "می‌دهد روند کلی این معماری‌ها به‌سمت افزایش دقت، بدون افزایش چشمگیر "
         "بار محاسباتی، بوده است.»"),
    ],
    "YOLOV4 A BREAKTHROUGH IN REAL-TIME OBJECT.pdf": [
        ("With Mosaic augmentation and multi-resolution training", "بند ۲-۳ (ص ۴۱)",
         "«این روش نخستین‌بار در نسخه چهارم این خانواده به‌کار گرفته شد و در "
         "مرجع [۱۴] تشریح شده است.»"),
    ],
}

END = re.compile(r"[.!?]$")


def sentence_rects(page, anchor):
    """مستطیل همه واژه‌های جملهٔ کاملی که لنگر در آن است.

    search_for فقط خودِ عبارت را برمی‌گرداند؛ برای هایلایت‌کردن کل جمله باید از
    روی واژه‌ها تا نقطهٔ پیش و نقطهٔ پس از لنگر گسترش داد. واژه‌ها به ترتیب
    خواندن مرتب می‌شوند تا شکستِ سطر جمله را پاره نکند."""
    words = page.get_text("words")                 # x0,y0,x1,y1,word,block,line,n
    if not words:
        return []
    words.sort(key=lambda w: (w[5], w[6], w[7]))
    toks = [w[4] for w in words]
    starts, acc = [], 0
    for tk in toks:
        starts.append(acc)
        acc += len(tk) + 1
    flat = " ".join(toks)
    at_start = anchor.startswith("^")
    key = " ".join(anchor.lstrip("^").split())
    pos = flat.find(key)
    if pos < 0:
        return []
    start_i = max(i for i, s in enumerate(starts) if s <= pos)
    end_i = max(i for i, s in enumerate(starts) if s < pos + len(key))
    lo = max(0, start_i - 55)
    while not at_start and start_i > lo and not END.search(toks[start_i - 1]):
        start_i -= 1
    hi = min(len(toks) - 1, end_i + 55)
    while end_i < hi and not END.search(toks[end_i]):
        end_i += 1
    lines = {}
    for w in words[start_i:end_i + 1]:
        lines.setdefault((w[5], w[6]), []).append(w)
    rects = []
    for ws in lines.values():
        r = fitz.Rect(ws[0][:4])
        for w in ws[1:]:
            r |= fitz.Rect(w[:4])
        rects.append(r)
    return rects


def run():
    rows, missing = [], []
    for fname, claims in JOBS.items():
        src = os.path.join(HERE, fname)
        if not os.path.exists(src):
            missing.append(("MISSING FILE", fname, "")); continue
        doc = fitz.open(src)
        for anchor, where, sentence in claims:
            done = False
            for page in doc:
                rects = sentence_rects(page, anchor)
                if not rects:
                    continue
                annot = page.add_highlight_annot(rects)
                annot.set_info(title="پایان‌نامه — %s" % where,
                               content=sentence)
                annot.set_colors(stroke=(1, 0.92, 0.23))
                annot.update()
                # پنجره یادداشت را باز نگه می‌دارد تا در هر نمایشگری دیده شود
                r = annot.rect
                annot.set_popup(fitz.Rect(r.x1 + 4, r.y0, r.x1 + 224, r.y0 + 92))
                rows.append((fname, where, page.number + 1, len(rects)))
                done = True
                break                              # فقط نخستین جای هر ادعا
            if not done:
                missing.append(("NOT FOUND", fname, anchor))
        doc.save(os.path.join(OUT, numbered(fname)), garbage=3, deflate=True)
        doc.close()

    out = ["%-44s  %-24s  ص %-3d  %d سطر" % (f[:44], w, p, n) for f, w, p, n in rows]
    out.append("")
    out.append("هایلایت شد: %d جمله از %d ادعا" % (len(rows), len(rows) + len(missing)))
    for s, f, a in missing:
        out.append("  %-11s %-40s %s" % (s, f[:40], a[:46]))
    io.open(os.path.join(HERE, "_highlight_report.txt"), "w",
            encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    run()
