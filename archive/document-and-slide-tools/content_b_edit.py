# -*- coding: utf-8 -*-
"""Slides 15 to 26, plus the build step."""
import os

from lxml import etree
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import (A, AMBER, BLUE, CRIMSON, CW, EN, F1, F2, F3, FS, GREEN, H, INK,
                  MARGIN, NAVY, OUT, SLATE, TINT_AMBER, TINT_BLUE, TINT_GREEN,
                  TINT_GREY, TINT_RED, TOP, W, WHITE, SLIDES, animate, box,
                  fa_num, footer, line, picture, prs, slide, table, textbox,
                  tile, _run)
from content_a import plain_item
from content_a import reg, white_divider


# ---------------------------------------------------------------------- 15
@reg
def d3():
    white_divider(3, "نتایج و تحلیل", "آزمایش‌ها، عملکرد نهایی و تحلیل خطا")


# ---------------------------------------------------------------------- 16
@reg
def config():
    sl = slide("پیکربندی آموزش نهایی")
    rows = [["پارامتر", "مقدار"], ["معماری", "YOLOv11s"], ["اندازه ورودی", "۱۲۸۰"],
            ["اندازه دسته", "۱۲"], ["بهینه‌ساز", "AdamW"], ["نرخ یادگیری", "۰٫۰۰۱"],
            ["زمان‌بند", "کسینوسی"], ["بیشینه دوره", "۱۵۰"], ["شکیبایی توقف", "۱۰"]]
    tw = Inches(6.55)
    table(sl, rows, W - MARGIN - tw, TOP, tw, Inches(4.86), 22, 21, hcols=(0,))
    items = [("۹٫۴ میلیون", "پارامتر مدل"), ("۶۲ دوره", "توقف زودهنگام"),
             ("محیط رایگان", "محدودیت حافظه پردازنده گرافیکی")]
    w = CW - tw - Inches(0.5); y = TOP
    for head, sub in items:
        tb, tf = textbox(sl, MARGIN, y, w, Inches(1.12), MSO_ANCHOR.MIDDLE)
        line(tf, head, 27, True, NAVY, first=True, after=4)
        line(tf, sub, 20, False, SLATE, after=0)
        y += Inches(1.68)


# ---------------------------------------------------------------------- 17
@reg
def code():
    sl = slide("انتخاب مدل نهایی")
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
        r.font.size = Pt(19); r.font.name = EN; r.font.color.rgb = INK
        rPr = r._r.get_or_add_rPr()
        for tag in ("cs", "ea", "latin"):
            el = rPr.find(A + tag)
            if el is None:
                el = etree.SubElement(rPr, A + tag)
            el.set("typeface", EN)
    for x, head, body in ((Inches(6.95), "ریزنمایش پایانی", "۱۰ دوره بدون موزاییک و ترکیب وزنی"),
                          (MARGIN, "انتخاب وزن", "بر پایه اعتبارسنجی؛ آزمون فقط در پایان")):
        tb, tf = textbox(sl, x, Inches(4.57), Inches(5.75), Inches(0.90))
        line(tf, head, 23, True, NAVY, first=True, after=3)
        line(tf, body, 19, False, SLATE, after=0)


# ---------------------------------------------------------------------- 18
@reg
def optimizer():
    sl = slide("مقایسه پیکربندی‌های run7 و run8", size=28)
    rows = [["اجرا", "بهینه‌ساز", "نرخ آغازین", "زمان‌بند", "اعتبارسنجی", "آزمون"],
            ["run7", "خودکار، SGD", "۰٫۰۱", "ثابت", "۰٫۸۴۶", "۰٫۸۶۷"],
            ["run8", "AdamW", "۰٫۰۰۱", "کسینوسی", "۰٫۸۴۹", "۰٫۸۷۴"]]
    t = table(sl, rows, MARGIN, TOP + Inches(0.12), CW, Inches(2.25), 21, 20, hcols=(0,))
    tb, tf = textbox(sl, Inches(6.95), Inches(4.28), Inches(5.75), Inches(1.25))
    line(tf, "تغییرات هم‌زمان", 24, True, NAVY, first=True, align=PP_ALIGN.CENTER, after=5)
    line(tf, "بهینه‌ساز، نرخ یادگیری و زمان‌بند", 20, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    tb2, tf2 = textbox(sl, MARGIN, Inches(4.28), Inches(5.75), Inches(1.25))
    line(tf2, "انتخاب نهایی", 24, True, NAVY, first=True, align=PP_ALIGN.CENTER, after=5)
    line(tf2, "run8 بر پایه نتیجه اعتبارسنجی", 20, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    animate(sl, [t, tb, tb2])


# ---------------------------------------------------------------------- 19
@reg
def resolution():
    sl = slide("اثر اندازه ورودی")
    tb, tf = textbox(sl, MARGIN, TOP - Inches(0.08), CW, Inches(0.6))
    line(tf, "داده و معماری یکسان؛ اندازه ورودی متفاوت", 25,
         False, INK, first=True, dot="•", after=0)
    rows = [["اندازه ورودی", "mAP@0.5", "mAP@0.5:0.95"],
            ["۹۶۰", "۰٫۷۶۶", "۰٫۵۹۹"],
            ["۱۲۸۰", "۰٫۸۰۲", "۰٫۶۴۶"],
            ["اختلاف", "۰٫۰۳۵+", "۰٫۰۴۷+"]]
    table(sl, rows, Inches(3.1), Inches(2.35), Inches(7.1), Inches(2.3), 23, 22)
    tile(sl, Inches(6.95), Inches(5.0), Inches(5.75), Inches(1.3),
         "چرا کار می‌کند", "شیء کوچک در تصویر بزرگ‌تر، پیکسل بیشتری دارد",
         TINT_GREEN, GREEN, 25, 20)
    tile(sl, MARGIN, Inches(5.0), Inches(5.75), Inches(1.3),
         "چرا بیشتر نرفتیم", "سقف داده و محدودیت حافظه", TINT_GREY, SLATE, 25, 20)


# ---------------------------------------------------------------------- 20
@reg
def d4():
    white_divider(4, "جمع‌بندی و پیشنهادها", "دستاوردها و مسیر ادامه کار")


# ---------------------------------------------------------------------- 21
@reg
def training():
    sl = slide("روند آموزش مدل")
    picture(sl, os.path.join(F3, "fig_3_1.png"), TOP, height=Inches(4.05))
    tb, tf = textbox(sl, MARGIN, Inches(5.75), CW, Inches(0.9))
    line(tf, "هر سه مؤلفه خطا یکنواخت کاهش یافت؛ توقف زودهنگام در دوره ۶۲", 25,
         False, INK, first=True, dot="•", after=0)


# ---------------------------------------------------------------------- 22
@reg
def results():
    sl = slide("نتایج نهایی روی بخش آزمون")
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
    sl = slide("عملکرد مدل به تفکیک رده")
    picture(sl, os.path.join(F3, "fig_3_3.png"), TOP, height=Inches(3.7),
            left=Inches(6.85))
    rows = [["رده", "AP@0.5"],
            ["خودروی سبک", "۰٫۹۶۹"],
            ["موتورسیکلت", "۰٫۹۲۸"],
            ["شخص", "۰٫۸۶۸"],
            ["خودروی باری", "۰٫۸۶۷"],
            ["چراغ راهنمایی", "۰٫۸۱۳"],
            ["اتوبوس", "۰٫۷۹۸"]]
    table(sl, rows, MARGIN, TOP, Inches(5.9), Inches(3.7), 22, 21)
    tb, tf = textbox(sl, MARGIN, Inches(5.5), CW, Inches(1.2))
    line(tf, "موتورسیکلت با نمونه کمتر از اتوبوس، نتیجه بسیار بهتری دارد", 25,
         False, INK, first=True, dot="•", after=0)


# ---------------------------------------------------------------------- 24
@reg
def confusion():
    sl = slide("تحلیل ماتریس درهم‌ریختگی")
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
             "subset", "validity", "balance", "config", "code", "d3",
             "optimizer", "resolution", "training", "results", "per_class",
             "confusion", "qualitative", "d4", "summary", "thanks"]
    by_name = {fn.__name__: fn for fn in SLIDES}
    n = len(ORDER)
    for name in ORDER:
        by_name[name]()
    for i, sl in enumerate(prs.slides, start=1):
        footer(sl, i, n)
    prs.save(OUT)
    print("saved %d slides" % n)
