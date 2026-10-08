# -*- coding: utf-8 -*-
"""Slides 1 to 14."""
import os

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from deck import (A, AMBER, BLUE, CRIMSON, CW, EN, F1, F2, F3, FA, FS, GREEN,
                  H, INK, MARGIN, NAVY, SLATE, TINT_AMBER, TINT_BLUE,
                  TINT_GREEN, TINT_GREY, TINT_RED, TOP, W, WHITE, SLIDES,
                  animate, box, fa_num, line, picture, prs, slide, table,
                  textbox, tile, _run)


def reg(fn):
    SLIDES.append(fn)
    return fn


def divider(num, title, sub, tint):
    sl = slide(bg=tint)
    tb, tf = textbox(sl, MARGIN, Inches(2.55), CW, Inches(2.4))
    line(tf, "بخش " + fa_num(num), 26, True, BLUE, first=True,
         align=PP_ALIGN.CENTER, after=14)
    line(tf, title, 46, True, NAVY, align=PP_ALIGN.CENTER, after=12)
    line(tf, sub, 24, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    return sl


# ----------------------------------------------------------------------- 1
@reg
def cover():
    sl = slide(bg=TINT_BLUE)
    box(sl, Inches(0.80), Inches(0.62), W - Inches(1.6), Inches(6.02), WHITE)

    logo = sl.shapes.add_picture(os.path.join(FS, "cover_image2.png"),
                                 Inches(0), Inches(0.95), height=Inches(1.15))
    logo.left = int((W - logo.width) / 2)

    tb, tf = textbox(sl, Inches(1.2), Inches(2.28), W - Inches(2.4), Inches(0.5))
    line(tf, "دانشکده مهندسی کامپیوتر", 21, False, SLATE, first=True,
         align=PP_ALIGN.CENTER, after=0)

    # the registered title, split over two lines: the wording is unchanged, the
    # parenthetical class list simply sits on its own line at a smaller size
    tb, tf = textbox(sl, Inches(1.2), Inches(2.80), W - Inches(2.4), Inches(1.8))
    line(tf, "دسته‌بندی اشیای ترافیکی با استفاده از YOLO", 34, True, NAVY,
         first=True, align=PP_ALIGN.CENTER, after=6)
    line(tf, "(۶ دسته متفاوت عابر، تریلر، اتوبوس، خودروی سبک، وانت، موتور)",
         19, False, SLATE, align=PP_ALIGN.CENTER, after=10)
    line(tf, "پیاده‌سازی با معماری YOLOv11", 25, True, BLUE,
         align=PP_ALIGN.CENTER, after=0)

    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.87), Inches(4.68),
                              Inches(1.6), Inches(0.045))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background(); bar.shadow.inherit = False

    rows = [("استاد راهنما", "دکتر رضا شمسایی"),
            ("استاد داور", "[نام استاد داور]"),
            ("دانشجو", "محمد امیر صادق‌زاده")]
    y = Inches(4.98)
    for lab, name in rows:
        tb, tf = textbox(sl, Inches(6.95), y, Inches(2.5), Inches(0.5))
        line(tf, lab, 21, False, SLATE, first=True, align=PP_ALIGN.RIGHT, after=0)
        tb, tf = textbox(sl, Inches(3.9), y, Inches(2.85), Inches(0.5))
        line(tf, name, 23, True, INK, first=True, align=PP_ALIGN.RIGHT, after=0)
        y += Inches(0.52)


# ---------------------------------------------------------------------- 2b
@reg
def scope():
    """Why the class list differs from the registered title. Comes right after
    the agenda so the examiner has the answer before the first technical slide."""
    sl = slide("شمار رده‌ها همان شش ماند؛ دو رده با داده موجود جایگزین شد")

    rows = [["وضعیت", "رده پروژه", "عنوان مصوب"],
            ["یکسان", "شخص", "عابر"],
            ["یکسان", "اتوبوس", "اتوبوس"],
            ["یکسان", "خودروی سبک", "خودروی سبک"],
            ["یکسان", "موتورسیکلت", "موتور"],
            ["عام‌تر", "خودروی باری", "تریلر"],
            ["در داده نیست", "—", "وانت"],
            ["افزوده شد", "چراغ راهنمایی", "—"]]
    table(sl, rows, Inches(6.95), TOP, Inches(5.76), Inches(4.15), 20, 18)

    items = [("زمان تصویب عنوان",
              "اینترنت کشور حدود یک هفته قطع بود و بررسی مجموعه‌داده‌ها ممکن نشد",
              TINT_GREY, SLATE),
             ("داده در دسترس",
              "IADD تنها همین شش رده را برچسب دارد؛ تریلر و وانت رده مستقل ندارند",
              TINT_BLUE, NAVY),
             ("تلاش برای اصلاح",
              "برچسب‌گذاری دوباره با Label Studio آغاز شد ولی در زمان پروژه شدنی نبود",
              TINT_AMBER, AMBER)]
    y = TOP
    for head, body, tint, ink in items:
        tile(sl, MARGIN, y, Inches(6.1), Inches(1.3), head, body, tint, ink, 24, 18)
        y += Inches(1.43)

    sh = box(sl, MARGIN, Inches(5.85), CW, Inches(0.85), TINT_GREEN)
    line(sh.text_frame, "صورت مسئله عوض نشد: تشخیص شش رده از اشیای ترافیکی در "
         "صحنه رانندگی", 24, True, GREEN, first=True, align=PP_ALIGN.CENTER,
         after=0)


# ----------------------------------------------------------------------- 2
@reg
def agenda():
    sl = slide("فهرست ارائه")
    items = [(1, "صورت مسئله و مبانی", TINT_BLUE, BLUE),
             (2, "داده: مسئله اصلی پروژه", TINT_RED, CRIMSON),
             (3, "آموزش مدل نهایی", TINT_AMBER, AMBER),
             (4, "نتایج", TINT_GREEN, GREEN),
             (5, "جمع‌بندی", TINT_GREY, SLATE)]
    y = TOP + Inches(0.15)
    for num, txt, tint, ink in items:
        sh = box(sl, MARGIN, y, CW, Inches(0.92), tint)
        tf = sh.text_frame
        line(tf, fa_num(num) + "   " + txt, 28, True, ink, first=True,
             align=PP_ALIGN.RIGHT, after=0)
        y += Inches(1.04)


# ----------------------------------------------------------------------- 3
@reg
def d1():
    divider(1, "صورت مسئله و مبانی", "چرا این مسئله، چرا داده ایرانی، چرا این مدل",
            TINT_BLUE)


# ----------------------------------------------------------------------- 4
@reg
def problem():
    sl = slide("خطای تشخیص، در تمام مراحل بعدی تکثیر می‌شود")
    tb, tf = textbox(sl, MARGIN, TOP, CW, Inches(1.7))
    line(tf, "خروجی تشخیص اشیا، ورودی مستقیم تصمیم‌گیری و کنترل خودرو است",
         26, False, INK, first=True, dot="•", after=0)

    steps = [("خطای تشخیص", TINT_RED, CRIMSON),
             ("تصمیم نادرست", TINT_AMBER, AMBER),
             ("فرمان اشتباه", TINT_AMBER, AMBER),
             ("تصادف", TINT_RED, CRIMSON)]
    w, gap = Inches(2.72), Inches(0.32)
    x = W - MARGIN - w
    for txt, tint, ink in steps:
        sh = box(sl, x, Inches(3.6), w, Inches(1.15), tint)
        line(sh.text_frame, txt, 24, True, ink, first=True,
             align=PP_ALIGN.CENTER, after=0)
        x -= (w + gap)

    tb, tf = textbox(sl, MARGIN, Inches(5.35), CW, Inches(1.2))
    line(tf, "هدف: ساخت و ارزیابی صادقانه یک آشکارساز اشیای ترافیکی برای ایران",
         28, True, NAVY, first=True, align=PP_ALIGN.CENTER, after=0)


# ----------------------------------------------------------------------- 5
@reg
def domain():
    sl = slide("مدل آموزش‌دیده روی داده خارجی، در ایران قابل اتکا نیست")
    tb, tf = textbox(sl, MARGIN, TOP, CW, Inches(0.8))
    line(tf, "با تغییر دامنه، دقت مدل به‌شدت افت می‌کند", 26, False, INK,
         first=True, dot="•", after=0)
    items = [("الگوی ترافیک", "تراکم و رفتار متفاوت"),
             ("نوع خودروها", "ناوگان داخلی"),
             ("علائم راهنمایی", "شکل و رنگ متفاوت")]
    w, gap = Inches(3.72), Inches(0.38)
    x = W - MARGIN - w
    for head, sub in items:
        tile(sl, x, Inches(2.55), w, Inches(1.85), head, sub, TINT_BLUE, NAVY, 27, 21)
        x -= (w + gap)
    tb, tf = textbox(sl, MARGIN, Inches(4.95), CW, Inches(1.4))
    line(tf, "مدل آموزش‌دیده روی داده خارجی، برای این کاربرد قابل اتکا نیست", 26,
         False, INK, first=True, dot="•", after=12)
    line(tf, "پس به مجموعه‌داده ایرانی نیاز داریم", 26, True, NAVY, dot="•", after=0)


# ----------------------------------------------------------------------- 6
@reg
def iadd():
    sl = slide("IADD تنها مجموعه‌داده عمومی صحنه‌های رانندگی ایران است")
    rows = [["مقدار", "ویژگی"],
            ["۹۷٬۵۲۸", "تصاویر برچسب‌خورده"],
            ["۱۷۱", "ویدیوهای منبع"],
            ["۶", "رده‌ها"],
            ["۸", "شهرهای گردآوری"]]
    table(sl, rows, MARGIN, TOP, Inches(6.4), Inches(2.9), 22, 22)

    tile(sl, Inches(7.4), TOP, Inches(5.3), Inches(1.35),
         "شش رده", "شخص، خودروی سبک، موتورسیکلت، اتوبوس، خودروی باری، چراغ راهنمایی",
         TINT_BLUE, NAVY, 26, 19)
    tile(sl, Inches(7.4), TOP + Inches(1.55), Inches(5.3), Inches(1.35),
         "برچسب‌گذاری", "نیمه‌نظارتی با بازبینی کارشناس", TINT_GREY, SLATE, 26, 20)

    sh = box(sl, MARGIN, Inches(4.9), CW, Inches(1.3), TINT_RED)
    line(sh.text_frame, "اما همین مجموعه‌داده، مسئله اصلی پروژه شد", 30, True,
         CRIMSON, first=True, align=PP_ALIGN.CENTER, after=0)


# ----------------------------------------------------------------------- 7
@reg
def arch():
    sl = slide("YOLOv11 یک‌مرحله‌ای است و برای کاربرد بلادرنگ مناسب")
    picture(sl, os.path.join(F1, "fig_1_2.png"), TOP, height=Inches(3.55))
    items = [("یک‌مرحله‌ای", "بدون پیشنهاد ناحیه", TINT_BLUE, NAVY),
             ("بلوک C3k2", "سبک‌تر و سریع‌تر", TINT_BLUE, NAVY),
             ("بلوک C2PSA", "توجه مکانی برای اشیای کوچک", TINT_GREEN, GREEN)]
    w, gap = Inches(3.72), Inches(0.38)
    x = W - MARGIN - w
    for head, sub, tint, ink in items:
        tile(sl, x, Inches(5.35), w, Inches(1.25), head, sub, tint, ink, 24, 19)
        x -= (w + gap)


# ----------------------------------------------------------------------- 8
@reg
def metrics():
    sl = slide("mAP معیار اصلی است، چون به آستانه اطمینان وابسته نیست")
    items = [("دقت", "چه نسبتی از تشخیص‌ها درست بود", TINT_BLUE, NAVY),
             ("فراخوانی", "چه نسبتی از اشیای واقعی پیدا شد", TINT_BLUE, NAVY),
             ("امتیاز F1", "میانگین هماهنگ آن دو", TINT_AMBER, AMBER),
             ("mAP@0.5", "مساحت زیر منحنی دقت و فراخوانی", TINT_GREEN, GREEN)]
    w, gap = Inches(2.87), Inches(0.30)
    x = W - MARGIN - w
    for head, sub, tint, ink in items:
        tile(sl, x, TOP + Inches(0.2), w, Inches(2.1), head, sub, tint, ink, 27, 19)
        x -= (w + gap)
    tb, tf = textbox(sl, MARGIN, Inches(4.35), CW, Inches(2.0))
    line(tf, "برخلاف دقت و فراخوانی، به آستانه اطمینان وابسته نیست", 24, False,
         INK, dot="•", after=10)
    line(tf, "گونه رایج و گونه سخت‌گیرانه‌تر، هر دو گزارش شدند", 24,
         False, INK, dot="•", after=0)


# ----------------------------------------------------------------------- 9
@reg
def d2():
    divider(2, "داده: مسئله اصلی پروژه", "چهار عیب مجموعه‌داده و راه‌حل آن‌ها",
            TINT_RED)


# ---------------------------------------------------------------------- 10
@reg
def arc():
    sl = slide("بالاترین عدد پروژه، همان بود که کنار گذاشتیم")
    picture(sl, os.path.join(FS, "slide_runs.png"), TOP - Inches(0.05),
            height=Inches(4.15))
    a = box(sl, Inches(8.85), Inches(5.75), Inches(3.85), Inches(1.05), TINT_RED)
    line(a.text_frame, "۰٫۸۹۶ روی داده نشت‌دار بود و کنار گذاشته شد", 20, True,
         CRIMSON, first=True, align=PP_ALIGN.CENTER, after=0)
    c = box(sl, Inches(4.66), Inches(5.75), Inches(3.85), Inches(1.05), TINT_GREY)
    line(c.text_frame, "run6 مدل متوسط بود؛ حافظه اجازه نداد و رها شد", 20, True,
         SLATE, first=True, align=PP_ALIGN.CENTER, after=0)
    b = box(sl, MARGIN, Inches(5.75), Inches(3.85), Inches(1.05), TINT_GREEN)
    line(b.text_frame, "۰٫۸۷۴ روی داده سالم، قابل استناد", 20, True, GREEN,
         first=True, align=PP_ALIGN.CENTER, after=0)
    animate(sl, [a, c, b])


# ---------------------------------------------------------------------- 11
@reg
def flaws():
    sl = slide("مجموعه‌داده چهار عیب داشت، هر چهار مورد برطرف شد")
    items = [("نشت داده", "فریم‌های یک ویدیو در هر سه بخش", TINT_RED, CRIMSON),
             ("ویدیوی تکراری", "یک ویدیو با دو شناسه", TINT_AMBER, AMBER),
             ("برچسب معیوب", "برچسب‌های جابه‌جا یا ناقص", TINT_AMBER, AMBER),
             ("ناهم‌ترازی دشواری", "اعتبارسنجی و آزمون هم‌تراز نبودند", TINT_BLUE, NAVY)]
    w, gap = Inches(5.8), Inches(0.33)
    shapes = []
    for i, (head, sub, tint, ink) in enumerate(items):
        x = W - MARGIN - w if i % 2 == 0 else MARGIN
        y = TOP + Inches(0.15) + (Inches(1.75) if i > 1 else 0)
        shapes.append(tile(sl, x, y, w, Inches(1.55), head, sub, tint, ink, 28, 20))
    end = box(sl, MARGIN, Inches(5.5), CW, Inches(1.1), TINT_GREEN)
    line(end.text_frame, "هر چهار مورد پیش از آموزش نهایی برطرف شد", 28, True,
         GREEN, first=True, align=PP_ALIGN.CENTER, after=0)
    shapes.append(end)
    animate(sl, shapes)


# ---------------------------------------------------------------------- 12
@reg
def leakage():
    sl = slide("فریم‌های یک ویدیو در هر سه بخش پخش شده بودند")
    tb, tf = textbox(sl, MARGIN, TOP - Inches(0.08), CW, Inches(0.6))
    line(tf, "فریم‌های نزدیک یک ویدیو، عملاً یک صحنه‌اند", 26, False, INK,
         first=True, dot="•", after=0)

    labels = ["آموزش", "آموزش", "آزمون", "آموزش", "آزمون", "اعتبارسنجی"]
    tints = {"آموزش": (TINT_BLUE, NAVY), "آزمون": (TINT_RED, CRIMSON),
             "اعتبارسنجی": (TINT_AMBER, AMBER)}
    w, gap = Inches(1.83), Inches(0.19)
    x = W - MARGIN - w
    marks = []
    for i, lab in enumerate(labels):
        f = box(sl, x, Inches(2.32), w, Inches(0.72), TINT_GREY)
        line(f.text_frame, "فریم " + fa_num(i), 21, True, SLATE, first=True,
             align=PP_ALIGN.CENTER, after=0)
        tint, ink = tints[lab]
        m = box(sl, x, Inches(3.12), w, Inches(0.72), tint)
        line(m.text_frame, lab, 21, True, ink, first=True,
             align=PP_ALIGN.CENTER, after=0)
        marks.append(m)
        x -= (w + gap)

    bad = box(sl, MARGIN, Inches(4.12), CW, Inches(1.1), TINT_RED)
    line(bad.text_frame, "تقسیم در سطح تصویر، یعنی مدل در ارزیابی تصویری را می‌بیند که "
         "تقریباً همان را در آموزش دیده است", 23, True, CRIMSON, first=True,
         align=PP_ALIGN.CENTER, after=0)
    good = box(sl, MARGIN, Inches(5.4), CW, Inches(1.25), TINT_GREEN)
    line(good.text_frame, "راه‌حل، تقسیم در سطح کل ویدیو است؛ تمام فریم‌های یک ویدیو "
         "تنها در یکی از سه بخش قرار می‌گیرند", 23, True, GREEN, first=True,
         align=PP_ALIGN.CENTER, after=0)
    animate(sl, marks + [bad, good])


# ---------------------------------------------------------------------- 13
@reg
def cleaning():
    sl = slide("پنج نسخه ساخته شد تا داده سالم به دست آید")
    steps = ["داده خام", "حذف تکراری با هش ادراکی",
             "حذف برچسب معیوب", "تقسیم در سطح ویدیو",
             "متوازن‌سازی ارزیابی", "داده نهایی"]
    tints = [TINT_GREY, TINT_RED, TINT_RED, TINT_BLUE, TINT_AMBER, TINT_GREEN]
    inks = [SLATE, CRIMSON, CRIMSON, NAVY, AMBER, GREEN]
    w, gap = Inches(1.79), Inches(0.24)
    x = W - MARGIN - w
    shapes = []
    for txt, tint, ink in zip(steps, tints, inks):
        sh = box(sl, x, Inches(2.4), w, Inches(1.95), tint)
        line(sh.text_frame, txt, 19, True, ink, first=True,
             align=PP_ALIGN.CENTER, after=0)
        shapes.append(sh)
        x -= (w + gap)
    tb, tf = textbox(sl, MARGIN, Inches(4.75), CW, Inches(1.7))
    line(tf, "پنج ویدیو حذف شد؛ سه نسخه تکراری و دو مورد با برچسب معیوب یا ناقص",
         24, False, INK, first=True, dot="•", after=12)
    line(tf, "ویدیوهای صرفاً دشوار عمداً نگه داشته شدند؛ حذفشان تقلب بود", 24,
         True, CRIMSON, dot="•", after=12)
    line(tf, "هر بار عدد گزارش‌شده پایین‌تر آمد، چون تقلب کمتر شد", 24, True,
         NAVY, dot="•", after=0)
    animate(sl, shapes)


# ---------------------------------------------------------------------- 14
@reg
def subset():
    sl = slide("در داده نهایی، هیچ ویدیویی میان دو بخش مشترک نیست")
    rows = [["نمونه", "تصویر", "ویدیو", "بخش"],
            ["۲۰۴٬۰۰۹", "۲۶٬۰۰۰", "۷۹", "آموزش"],
            ["۳۶٬۸۱۰", "۵٬۵۷۱", "۳۹", "اعتبارسنجی"],
            ["۳۴٬۹۹۴", "۵٬۵۷۱", "۴۲", "آزمون"]]
    table(sl, rows, MARGIN, TOP, CW, Inches(2.3), 23, 22)
    items = [("۱۶۰ ویدیو", "هیچ ویدیویی در دو بخش نیست", TINT_GREEN, GREEN),
             ("۷۰ / ۱۵ / ۱۵", "درصد تقسیم سه بخش", TINT_BLUE, NAVY),
             ("بخش آزمون سخت‌تر", "سهم شب و باران بیشتر", TINT_AMBER, AMBER)]
    w, gap = Inches(3.72), Inches(0.38)
    x = W - MARGIN - w
    for head, sub, tint, ink in items:
        tile(sl, x, Inches(4.35), w, Inches(1.75), head, sub, tint, ink, 27, 20)
        x -= (w + gap)


# --------------------------------------------------------------------- 14b
@reg
def validity():
    sl = slide("توزیع اندازه اشیا، یعنی عامل اصلی سختی، در سه بخش یکسان است")
    picture(sl, os.path.join(F2, "fig_2_3.png"), TOP, height=Inches(3.85),
            left=Inches(5.9))
    items = [("سه‌چهارم اشیا کوچک‌اند", "زیر یک درصد مساحت تصویر", TINT_AMBER, AMBER),
             ("اختلاف اعتبارسنجی و آزمون", "کمتر از یک واحد درصد", TINT_GREEN, GREEN),
             ("اشتراک ویدیو و تصویر", "میان سه بخش، صفر", TINT_GREEN, GREEN)]
    y = TOP
    for head, sub, tint, ink in items:
        tile(sl, MARGIN, y, Inches(5.0), Inches(1.15), head, sub, tint, ink, 24, 20)
        y += Inches(1.35)
    tb, tf = textbox(sl, MARGIN, Inches(5.6), CW, Inches(1.0))
    line(tf, "پس دو بخش ارزیابی از نظر دشواری هم‌ترازند و مقایسه معیارهایشان معنادار است",
         24, True, NAVY, first=True, dot="•", after=0)


# --------------------------------------------------------------------- 14c
@reg
def balance():
    sl = slide("توزیع رده‌ها و شرایط محیطی نیز در سه بخش هم‌تراز است")
    a = picture(sl, os.path.join(F2, "fig_2_2.png"), TOP, height=Inches(3.6),
                left=Inches(6.55))
    b = picture(sl, os.path.join(F2, "fig_2_4.png"), TOP, height=Inches(3.6),
                left=MARGIN)
    tb, tf = textbox(sl, MARGIN, Inches(5.2), CW, Inches(1.5))
    line(tf, "عدم توازن رده‌ها ویژگی ذاتی ترافیک واقعی است، نه خطای تقسیم", 24,
         False, INK, first=True, dot="•", after=12)
    line(tf, "سهم شب در بخش آزمون بیشتر است؛ آزمون عمداً آسان نشده", 24, True,
         NAVY, dot="•", after=0)


# --------------------------------------------------------------------- 13b
@reg
def audit():
    sl = slide("از سیزده ویدیوی مشکوک، تنها دو مورد واقعاً برچسب معیوب داشت")
    pic = picture(sl, os.path.join(FS, "label_noise.png"), TOP, height=Inches(3.3),
                  left=MARGIN)
    rows = [["شمار", "وضعیت"],
            ["۱۳", "زیر آستانه ۰٫۶۳"],
            ["۲", "برچسب معیوب، حذف شد"],
            ["۱۱", "دشوار ولی سالم، ماند"]]
    t = table(sl, rows, Inches(7.4), TOP, Inches(5.3), Inches(2.6), 22, 21)
    cap = box(sl, MARGIN, Inches(4.85), Inches(6.7), Inches(0.8), TINT_RED)
    line(cap.text_frame, "برچسب خودروی سبک روی ساختمان و کاپوت خودِ خودرو", 20, True,
         CRIMSON, first=True, align=PP_ALIGN.CENTER, after=0)
    note = box(sl, Inches(7.4), Inches(4.3), Inches(5.3), Inches(1.3), TINT_GREEN)
    line(note.text_frame, "یازده ویدیوی دشوار نگه داشته شدند؛ حذفشان عدد را "
         "بالا می‌برد ولی تقلب بود", 21, True, GREEN, first=True,
         align=PP_ALIGN.CENTER, after=0)
    tb, tf = textbox(sl, MARGIN, Inches(5.85), CW, Inches(0.8))
    line(tf, "روش، محاسبه معیار برای هر ویدیو جداگانه و بازبینی چشمی موارد زیر آستانه بود",
         22, False, INK, first=True, dot="•", after=0)
    animate(sl, [t, note])
