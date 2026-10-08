# -*- coding: utf-8 -*-
"""Slides 15 to 26, plus the build step."""
import os

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import (AMBER, BLUE, CRIMSON, CW, EN, F1, F2, F3, FS, GREEN, H, INK,
                  MARGIN, NAVY, OUT, SLATE, TINT_AMBER, TINT_BLUE, TINT_GREEN,
                  TINT_GREY, TINT_RED, TOP, W, WHITE, SLIDES, animate, box,
                  fa_num, footer, line, picture, prs, slide, table, textbox,
                  tile, _run)
from content_a import divider, reg


# ---------------------------------------------------------------------- 15
@reg
def d3():
    divider(3, "آموزش مدل نهایی", "پیکربندی، آزمایش کنترل‌شده، همگرایی", TINT_AMBER)


# ---------------------------------------------------------------------- 16
@reg
def config():
    sl = slide("پیکربندی نهایی روی پردازنده گرافیکی رایگان اجرا شد")
    rows = [["مقدار", "پارامتر"],
            ["YOLOv11s", "معماری"],
            ["۱۲۸۰", "اندازه ورودی"],
            ["۱۲", "اندازه دسته"],
            ["AdamW", "بهینه‌ساز"],
            ["۰٫۰۰۱", "نرخ یادگیری"],
            ["کسینوسی", "زمان‌بند"],
            ["۱۵۰", "بیشینه دوره"],
            ["۱۰", "شکیبایی توقف"]]
    tw = Inches(6.55)
    table(sl, rows, W - MARGIN - tw, TOP, tw, Inches(4.86), 22, 21)
    items = [("۹٫۴ میلیون", "پارامتر مدل", TINT_BLUE, NAVY),
             ("۶۲ دوره", "توقف زودهنگام فعال شد", TINT_GREEN, GREEN),
             ("پردازنده رایگان", "حافظه محدود", TINT_GREY, SLATE)]
    w = CW - tw - Inches(0.5)
    y = TOP
    for head, sub, tint, ink in items:
        tile(sl, MARGIN, y, w, Inches(1.5), head, sub, tint, ink, 27, 20)
        y += Inches(1.68)


# ---------------------------------------------------------------------- 17
@reg
def code():
    sl = slide("وزن نهایی بر پایه اعتبارسنجی انتخاب شد، نه بخش آزمون")
    sh = box(sl, MARGIN, TOP, CW, Inches(2.75), TINT_GREY)
    tf = sh.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.4)
    src = ["model = YOLO('yolo11s.pt')",
           "model.train(data='iadd_subset_v5/data.yaml',",
           "    epochs=150, patience=10, imgsz=1280, batch=12,",
           "    optimizer='AdamW', lr0=0.001, cos_lr=True,",
           "    mixup=0.1, hsv_v=0.4, degrees=5.0)"]
    for i, s in enumerate(src):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(3)
        r = p.add_run(); r.text = s
        r.font.size = Pt(19); r.font.name = "Consolas"; r.font.color.rgb = INK
    tb, tf = textbox(sl, MARGIN, Inches(4.6), CW, Inches(1.8))
    line(tf, "پس از آموزش اصلی، ریزتنظیم ده دوره‌ای با نرخ یادگیری پایین", 25,
         False, INK, first=True, dot="•", after=12)
    line(tf, "وزن نهایی میان دو نامزد، بر پایه بخش اعتبارسنجی انتخاب شد", 25,
         True, NAVY, dot="•", after=12)
    line(tf, "بخش آزمون تنها یک بار و در پایان دیده شد", 25, True, GREEN,
         dot="•", after=0)


# ---------------------------------------------------------------------- 18
@reg
def optimizer():
    sl = slide("AdamW با زمان‌بند کسینوسی، در هر دو بخش بهتر بود")
    tb, tf = textbox(sl, MARGIN, TOP - Inches(0.08), CW, Inches(0.6))
    line(tf, "همان داده، همان معماری، همان حافظه؛ تنها یک عامل تغییر کرد", 25,
         False, INK, first=True, dot="•", after=0)
    rows = [["اختلاف", "آزمون", "اعتبارسنجی", "پیکربندی"],
            ["مبنا", "۰٫۸۶۷", "۰٫۸۴۶", "گرادیان کاهشی تصادفی"],
            ["۰٫۰۰۷+", "۰٫۸۷۴", "۰٫۸۴۹", "AdamW با زمان‌بند کسینوسی"]]
    t = table(sl, rows, MARGIN, Inches(2.4), CW, Inches(1.75), 23, 22)
    a = box(sl, Inches(6.95), Inches(4.95), Inches(5.75), Inches(1.15), TINT_GREY)
    line(a.text_frame, "بهبود کوچک است، کمتر از یک واحد درصد", 23, True, SLATE,
         first=True, align=PP_ALIGN.CENTER, after=0)
    b = box(sl, MARGIN, Inches(4.95), Inches(5.75), Inches(1.15), TINT_GREEN)
    line(b.text_frame, "ولی در هر دو بخش تکرار شد، پس تصادفی نیست", 23, True,
         GREEN, first=True, align=PP_ALIGN.CENTER, after=0)
    animate(sl, [t, a, b])


# ---------------------------------------------------------------------- 19
@reg
def resolution():
    sl = slide("افزایش ورودی از ۹۶۰ به ۱۲۸۰، معیار را سه و نیم واحد بالا برد")
    tb, tf = textbox(sl, MARGIN, TOP - Inches(0.08), CW, Inches(0.6))
    line(tf, "دو آموزش روی داده کاملاً یکسان، تنها با اندازه ورودی متفاوت", 25,
         False, INK, first=True, dot="•", after=0)
    rows = [["mAP@0.5:0.95", "mAP@0.5", "اندازه ورودی"],
            ["۰٫۵۹۹", "۰٫۷۶۶", "۹۶۰"],
            ["۰٫۶۴۶", "۰٫۸۰۲", "۱۲۸۰"],
            ["۰٫۰۴۷+", "۰٫۰۳۵+", "اختلاف"]]
    table(sl, rows, Inches(3.1), Inches(2.35), Inches(7.1), Inches(2.3), 23, 22)
    tile(sl, Inches(6.95), Inches(5.0), Inches(5.75), Inches(1.3),
         "چرا کار می‌کند", "شیء کوچک در تصویر بزرگ‌تر، پیکسل بیشتری دارد",
         TINT_GREEN, GREEN, 25, 20)
    tile(sl, MARGIN, Inches(5.0), Inches(5.75), Inches(1.3),
         "چرا بیشتر نرفتیم", "سقف داده و محدودیت حافظه", TINT_GREY, SLATE, 25, 20)


# ---------------------------------------------------------------------- 20
@reg
def d4():
    divider(4, "نتایج", "کمی و کیفی، روی بخشی که مدل هرگز ندیده", TINT_GREEN)


# ---------------------------------------------------------------------- 21
@reg
def training():
    sl = slide("آموزش پس از ۶۲ دوره همگرا شد")
    picture(sl, os.path.join(F3, "fig_3_1.png"), TOP, height=Inches(4.05))
    tb, tf = textbox(sl, MARGIN, Inches(5.75), CW, Inches(0.9))
    line(tf, "هر سه مؤلفه خطا یکنواخت کاهش یافت؛ توقف زودهنگام در دوره ۶۲", 25,
         False, INK, first=True, dot="•", after=0)


# ---------------------------------------------------------------------- 22
@reg
def results():
    sl = slide("مدل روی بخشی ارزیابی شد که هرگز ندیده بود")
    a = box(sl, Inches(6.95), TOP + Inches(0.15), Inches(5.75), Inches(2.3),
            TINT_GREEN)
    tf = a.text_frame
    line(tf, "۰٫۸۷۴", 66, True, GREEN, first=True, align=PP_ALIGN.CENTER, after=4)
    line(tf, "mAP@0.5‏ روی بخش آزمون", 24, False, SLATE, align=PP_ALIGN.CENTER,
         after=0)
    b = box(sl, MARGIN, TOP + Inches(0.15), Inches(5.75), Inches(2.3), TINT_BLUE)
    tf = b.text_frame
    line(tf, "۰٫۷۰۷", 66, True, NAVY, first=True, align=PP_ALIGN.CENTER, after=4)
    line(tf, "mAP@0.5:0.95‏ روی بخش آزمون", 24, False, SLATE,
         align=PP_ALIGN.CENTER, after=0)
    tb, tf = textbox(sl, MARGIN, Inches(4.4), CW, Inches(2.0))
    line(tf, "عدد آزمون از اعتبارسنجی بالاتر است", 25, False, INK, first=True,
         dot="•", after=14)
    line(tf, "چون بخش اعتبارسنجی در این تقسیم‌بندی ویدیوهای دشوارتری دارد", 25,
         False, INK, dot="•", after=14)
    line(tf, "هیچ تنظیمی روی بخش آزمون انجام نشد", 25, True, GREEN, dot="•", after=0)


# ---------------------------------------------------------------------- 23
@reg
def per_class():
    sl = slide("شمار نمونه، تنها عامل دشواری هر رده نیست")
    picture(sl, os.path.join(F3, "fig_3_3.png"), TOP, height=Inches(3.7),
            left=Inches(6.85))
    rows = [["AP@0.5", "رده"],
            ["۰٫۹۶۹", "خودروی سبک"],
            ["۰٫۹۲۸", "موتورسیکلت"],
            ["۰٫۸۶۸", "شخص"],
            ["۰٫۸۶۷", "خودروی باری"],
            ["۰٫۸۱۳", "چراغ راهنمایی"],
            ["۰٫۷۹۸", "اتوبوس"]]
    table(sl, rows, MARGIN, TOP, Inches(5.9), Inches(3.7), 22, 21)
    tb, tf = textbox(sl, MARGIN, Inches(5.5), CW, Inches(1.2))
    line(tf, "موتورسیکلت با نمونه کمتر از اتوبوس، نتیجه بسیار بهتری دارد", 25,
         False, INK, first=True, dot="•", after=0)


# ---------------------------------------------------------------------- 24
@reg
def confusion():
    sl = slide("بیشترین خطا میان خودروی باری و اتوبوس رخ می‌دهد")
    tb, tf = textbox(sl, MARGIN, TOP - Inches(0.08), CW, Inches(0.6))
    line(tf, "نقطه کاری: آستانه اطمینان ۰٫۴۰۶، برگرفته از بیشینه امتیاز هماهنگ روی "
         "بخش اعتبارسنجی", 25, False, INK, first=True, dot="•", after=0)
    picture(sl, os.path.join(F3, "fig_3_5.png"), Inches(1.95), height=Inches(4.7))


# ---------------------------------------------------------------------- 25
@reg
def qualitative():
    sl = slide()                      # no header: the images take the whole slide
    a = picture(sl, os.path.join(F3, "fig_3_6.png"), Inches(0.30), height=Inches(6.5))
    b = picture(sl, os.path.join(F3, "fig_3_7.png"), Inches(0.30), height=Inches(6.5))
    gap = Inches(0.45)
    total = a.width + gap + b.width
    b.left = int((W - total) / 2)
    a.left = b.left + b.width + gap
    for pic, cap in ((a, "روز و شب"), (b, "باران و روز ابری")):
        tb, tf = textbox(sl, pic.left, Inches(6.85), pic.width, Inches(0.5))
        line(tf, cap, 24, True, NAVY, first=True, align=PP_ALIGN.CENTER, after=0)


# ---------------------------------------------------------------------- 26
@reg
def summary():
    sl = slide("جمع‌بندی")
    items = [("دستاورد اصلی", "چهار عیب مجموعه‌داده شناسایی و برطرف شد",
              TINT_BLUE, NAVY),
             ("روش ارزیابی", "تقسیم در سطح ویدیو، بدون نشت داده", TINT_BLUE, NAVY),
             ("مدل نهایی", "mAP@0.5‏ برابر ۰٫۸۷۴ روی بخش آزمون", TINT_GREEN, GREEN),
             ("کار بعدی", "تفکیک‌پذیری بالاتر و داده بیشتر برای رده‌های نادر",
              TINT_AMBER, AMBER)]
    y = TOP + Inches(0.1)
    for head, sub, tint, ink in items:
        sh = box(sl, MARGIN, y, CW, Inches(1.15), tint)
        tf = sh.text_frame
        line(tf, head, 26, True, ink, first=True, after=2)
        line(tf, sub, 22, False, SLATE, after=0)
        y += Inches(1.28)


# ---------------------------------------------------------------------- 27
@reg
def thanks():
    sl = slide(bg=TINT_BLUE)
    card = box(sl, Inches(1.6), Inches(1.30), W - Inches(3.2), Inches(4.9), WHITE)
    logo = sl.shapes.add_picture(os.path.join(FS, "cover_image2.png"),
                                 Inches(0), Inches(1.75), height=Inches(1.05))
    logo.left = int((W - logo.width) / 2)
    tb, tf = textbox(sl, Inches(2.0), Inches(3.15), W - Inches(4.0), Inches(2.8))
    line(tf, "با تشکر از توجه شما", 48, True, NAVY, first=True,
         align=PP_ALIGN.CENTER, after=22)
    line(tf, "پرسش‌های شما", 32, True, BLUE, align=PP_ALIGN.CENTER, after=22)
    line(tf, "محمد امیر صادق‌زاده", 24, False, SLATE, align=PP_ALIGN.CENTER,
         after=0)


if __name__ == "__main__":
    ORDER = ["cover", "agenda", "scope", "d1", "problem", "domain", "iadd", "arch",
             "metrics", "d2", "arc", "flaws", "leakage", "cleaning", "audit",
             "subset", "validity", "balance", "d3", "config", "code",
             "optimizer", "resolution", "d4", "training", "results",
             "per_class", "confusion", "qualitative", "summary", "thanks"]
    by_name = {fn.__name__: fn for fn in SLIDES}
    n = len(ORDER)
    for name in ORDER:
        by_name[name]()
    for i, sl in enumerate(prs.slides, start=1):
        footer(sl, i, n)
    prs.save(OUT)
    print("saved %d slides" % n)
