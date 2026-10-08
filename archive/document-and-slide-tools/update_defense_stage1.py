from pathlib import Path


ROOT = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\کد")
A = ROOT / "content_a.py"
B = ROOT / "content_b.py"


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one match, found {count}: {old[:80]!r}")
    return text.replace(old, new, 1)


def replace_function(text: str, name: str, replacement: str) -> str:
    marker = f"@reg\ndef {name}():"
    start = text.index(marker)
    next_start = text.index("\n# ----------------------------------------------------------------", start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[next_start + 1:]


a = A.read_text(encoding="utf-8")

scope = r'''@reg
def scope():
    """Explain why the approved and implemented class sets differ."""
    sl = slide("تفاوت رده‌های مصوب و رده‌های نهایی")

    rows = [["وضعیت", "رده نهایی", "عنوان مصوب"],
            ["گسترده‌تر", "شخص", "عابر"],
            ["یکسان", "اتوبوس", "اتوبوس"],
            ["یکسان", "خودروی سبک", "خودروی سبک"],
            ["یکسان", "موتورسیکلت", "موتور"],
            ["ادغام شد", "خودروی باری", "تریلر"],
            ["ادغام شد", "خودروی باری", "وانت"],
            ["افزوده شد", "چراغ راهنمایی", "—"]]
    table(sl, rows, Inches(6.72), TOP, Inches(6.0), Inches(4.25), 19, 17,
          hcols=())

    items = [("محدودیت آغاز پروژه",
              "قطعی سراسری اینترنت، بررسی منابع و مجموعه‌داده‌های موجود را محدود کرد",
              TINT_GREY, SLATE),
             ("انتخاب مجموعه‌داده",
              "پس از بررسی BDD100K و IADD، با نظر استاد راهنما IADD انتخاب شد؛ زیرا با محیط ترافیکی ایران سازگارتر بود",
              TINT_BLUE, NAVY),
             ("تلاش برای انطباق رده‌ها",
              "بازبرچسب‌گذاری با Label Studio آغاز شد؛ اما حجم داده و نبود دسترسی به روش‌های نیمه‌نظارتی، تکمیل آن را ناممکن کرد",
              TINT_AMBER, AMBER)]
    y = TOP
    for head, body, tint, ink in items:
        tile(sl, MARGIN, y, Inches(5.72), Inches(1.30), head, body,
             tint, ink, 22, 17)
        y += Inches(1.43)

    sh = box(sl, MARGIN, Inches(5.85), CW, Inches(0.85), TINT_GREEN)
    line(sh.text_frame, "رده‌های نهایی بر پایه برچسب‌های موجود IADD تعریف شدند",
         24, True, GREEN, first=True, align=PP_ALIGN.CENTER, after=0)
'''
a = replace_function(a, "scope", scope)

old_agenda = '''    items = [(1, "صورت مسئله و مبانی", TINT_BLUE, BLUE),
             (2, "داده: مسئله اصلی پروژه", TINT_RED, CRIMSON),
             (3, "آموزش مدل نهایی", TINT_AMBER, AMBER),
             (4, "نتایج", TINT_GREEN, GREEN),
             (5, "جمع‌بندی", TINT_GREY, SLATE)]'''
new_agenda = '''    items = [(1, "مبانی و صورت مسئله", TINT_BLUE, BLUE),
             (2, "روش پژوهش و آماده‌سازی داده", TINT_RED, CRIMSON),
             (3, "نتایج و تحلیل", TINT_GREEN, GREEN),
             (4, "جمع‌بندی و پیشنهادها", TINT_AMBER, AMBER)]'''
a = replace_once(a, old_agenda, new_agenda)

a = replace_once(a,
    '    divider(1, "صورت مسئله و مبانی", "چرا این مسئله، چرا داده ایرانی، چرا این مدل",\n',
    '    divider(1, "مبانی و صورت مسئله", "اهمیت مسئله، داده بومی و معماری مدل",\n')
a = replace_once(a,
    '    divider(2, "داده: مسئله اصلی پروژه", "چهار عیب مجموعه‌داده و راه‌حل آن‌ها",\n',
    '    divider(2, "روش پژوهش و آماده‌سازی داده", "چالش‌های داده، ساخت زیرمجموعه و پیکربندی آموزش",\n')

titles_a = {
    "خطای تشخیص، در تمام مراحل بعدی تکثیر می‌شود": "اهمیت تشخیص اشیای ترافیکی",
    "مدل آموزش‌دیده روی داده خارجی، در ایران قابل اتکا نیست": "ضرورت استفاده از داده بومی",
    "IADD تنها مجموعه‌داده عمومی صحنه‌های رانندگی ایران است": "مجموعه‌داده IADD",
    "YOLOv11 یک‌مرحله‌ای است و برای کاربرد بلادرنگ مناسب": "معماری YOLOv11",
    "mAP معیار اصلی است، چون به آستانه اطمینان وابسته نیست": "معیارهای ارزیابی",
    "بالاترین عدد پروژه، همان بود که کنار گذاشتیم": "مسیر تکامل پروژه",
    "مجموعه‌داده چهار عیب داشت، هر چهار مورد برطرف شد": "چالش‌های مجموعه‌داده",
    "فریم‌های یک ویدیو در هر سه بخش پخش شده بودند": "نشت داده در تقسیم‌بندی اولیه",
    "پنج نسخه ساخته شد تا داده سالم به دست آید": "مراحل آماده‌سازی داده نهایی",
    "در داده نهایی، هیچ ویدیویی میان دو بخش مشترک نیست": "ترکیب زیرمجموعه نهایی",
    "توزیع اندازه اشیا، یعنی عامل اصلی سختی، در سه بخش یکسان است": "هم‌ترازی توزیع اندازه اشیا",
    "توزیع رده‌ها و شرایط محیطی نیز در سه بخش هم‌تراز است": "هم‌ترازی رده‌ها و شرایط محیطی",
    "از سیزده ویدیوی مشکوک، تنها دو مورد واقعاً برچسب معیوب داشت": "بازبینی ویدیوهای مشکوک",
}
for old, new in titles_a.items():
    a = replace_once(a, f'sl = slide("{old}")', f'sl = slide("{new}")')

A.write_text(a, encoding="utf-8", newline="\n")

b = B.read_text(encoding="utf-8")
b = replace_once(b,
    '    divider(3, "آموزش مدل نهایی", "پیکربندی، آزمایش کنترل‌شده، همگرایی", TINT_AMBER)',
    '    divider(3, "نتایج و تحلیل", "آزمایش‌ها، عملکرد نهایی و تحلیل خطا", TINT_GREEN)')
b = replace_once(b,
    '    divider(4, "نتایج", "کمی و کیفی، روی بخشی که مدل هرگز ندیده", TINT_GREEN)',
    '    divider(4, "جمع‌بندی و پیشنهادها", "دستاوردها و مسیر ادامه کار", TINT_AMBER)')

titles_b = {
    "پیکربندی نهایی روی پردازنده گرافیکی رایگان اجرا شد": "پیکربندی آموزش نهایی",
    "وزن نهایی بر پایه اعتبارسنجی انتخاب شد، نه بخش آزمون": "انتخاب مدل نهایی",
    "AdamW با زمان‌بند کسینوسی، در هر دو بخش بهتر بود": "مقایسه راهبردهای بهینه‌سازی",
    "افزایش ورودی از ۹۶۰ به ۱۲۸۰، معیار را سه و نیم واحد بالا برد": "اثر اندازه ورودی",
    "آموزش پس از ۶۲ دوره همگرا شد": "روند آموزش مدل",
    "مدل روی بخشی ارزیابی شد که هرگز ندیده بود": "نتایج نهایی روی بخش آزمون",
    "شمار نمونه، تنها عامل دشواری هر رده نیست": "عملکرد مدل به تفکیک رده",
    "بیشترین خطا میان خودروی باری و اتوبوس رخ می‌دهد": "تحلیل ماتریس درهم‌ریختگی",
}
for old, new in titles_b.items():
    b = replace_once(b, f'sl = slide("{old}")', f'sl = slide("{new}")')

old_order = '''    ORDER = ["cover", "agenda", "scope", "d1", "problem", "domain", "iadd", "arch",
             "metrics", "d2", "arc", "flaws", "leakage", "cleaning", "audit",
             "subset", "validity", "balance", "d3", "config", "code",
             "optimizer", "resolution", "d4", "training", "results",
             "per_class", "confusion", "qualitative", "summary", "thanks"]'''
new_order = '''    ORDER = ["cover", "agenda", "scope", "d1", "problem", "domain", "iadd", "arch",
             "metrics", "d2", "arc", "flaws", "leakage", "cleaning", "audit",
             "subset", "validity", "balance", "config", "code", "d3",
             "optimizer", "resolution", "training", "results", "per_class",
             "confusion", "qualitative", "d4", "summary", "thanks"]'''
b = replace_once(b, old_order, new_order)
B.write_text(b, encoding="utf-8", newline="\n")

print("updated content_a.py and content_b.py")
