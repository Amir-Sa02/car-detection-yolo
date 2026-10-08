from pathlib import Path


ROOT = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\کد")
A = ROOT / "content_a.py"


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one match, found {count}: {old[:90]!r}")
    return text.replace(old, new, 1)


def replace_function(text: str, name: str, replacement: str) -> str:
    marker = f"@reg\ndef {name}():"
    start = text.index(marker)
    next_start = text.index("\n# ----------------------------------------------------------------", start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[next_start + 1:]


a = A.read_text(encoding="utf-8")

# Spread the four agenda rows over the available height.
a = replace_once(a, "    y = TOP + Inches(0.15)\n    for num, txt, tint, ink in items:\n"
                     "        sh = box(sl, MARGIN, y, CW, Inches(0.92), tint)\n",
                     "    y = TOP + Inches(0.20)\n    for num, txt, tint, ink in items:\n"
                     "        sh = box(sl, MARGIN, y, CW, Inches(1.08), tint)\n")
a = replace_once(a, "        y += Inches(1.04)\n", "        y += Inches(1.25)\n")

# Keep only short cues on the class-mapping slide; details belong in the script.
scope_start = a.index("@reg\ndef scope():")
scope_end = a.index("\n# ----------------------------------------------------------------", scope_start)
scope = a[scope_start:scope_end]
scope = replace_once(scope,
    "قطعی سراسری اینترنت، بررسی منابع و مجموعه‌داده‌های موجود را محدود کرد",
    "تصویب موضوع هم‌زمان با قطعی سراسری اینترنت")
scope = replace_once(scope,
    "پس از بررسی BDD100K و IADD، با نظر استاد راهنما IADD انتخاب شد؛ زیرا با محیط ترافیکی ایران سازگارتر بود",
    "انتخاب IADD به‌جای BDD100K، با نظر استاد راهنما")
scope = replace_once(scope,
    "بازبرچسب‌گذاری با Label Studio آغاز شد؛ اما حجم داده و نبود دسترسی به روش‌های نیمه‌نظارتی، تکمیل آن را ناممکن کرد",
    "بازبرچسب‌گذاری کامل در زمان پروژه عملی نبود")
scope = replace_once(scope, "tint, ink, 22, 17)", "tint, ink, 23, 19)")
a = a[:scope_start] + scope + a[scope_end:]

problem = r'''@reg
def problem():
    sl = slide("اهمیت مسئله تشخیص اشیا")
    items = [("درک صحنه", "تعیین رده و موقعیت هر شیء در تصویر", TINT_BLUE, NAVY),
             ("ورودی تصمیم‌گیری", "فراهم‌کردن اطلاعات لازم برای سامانه‌های کمک‌راننده", TINT_GREY, SLATE),
             ("چالش محیط واقعی", "تفاوت نور، فاصله، اندازه و هم‌پوشانی اشیا", TINT_AMBER, AMBER),
             ("هدف پروژه", "تشخیص شش رده ترافیکی و ارزیابی قابل‌اتکای مدل", TINT_GREEN, GREEN)]
    y = TOP + Inches(0.02)
    shapes = []
    for head, body, tint, ink in items:
        shapes.append(tile(sl, MARGIN, y, CW, Inches(1.12), head, body,
                           tint, ink, 25, 20))
        y += Inches(1.27)
    animate(sl, shapes)
'''
a = replace_function(a, "problem", problem)

domain = r'''@reg
def domain():
    sl = slide("انتخاب داده بومی برای تنظیم دقیق مدل")

    start = box(sl, MARGIN, TOP, CW, Inches(1.00), TINT_GREY)
    line(start.text_frame, "نقطه آغاز: وزن‌های ازپیش‌آموخته YOLOv11s روی COCO",
         25, True, SLATE, first=True, align=PP_ALIGN.CENTER, after=0)

    items = [("الگوی ترافیک", "صحنه‌های واقعی ایران"),
             ("وسایل نقلیه رایج", "خودروهای موجود در معابر کشور"),
             ("شرایط محیطی", "روز، شب، باران و مسیرهای متنوع")]
    w, gap = Inches(3.72), Inches(0.38)
    x = W - MARGIN - w
    cards = []
    for head, sub in items:
        cards.append(tile(sl, x, Inches(2.78), w, Inches(1.65), head, sub,
                          TINT_BLUE, NAVY, 26, 20))
        x -= (w + gap)

    end = box(sl, MARGIN, Inches(5.10), CW, Inches(1.25), TINT_GREEN)
    line(end.text_frame, "مرحله پروژه: تنظیم دقیق مدل با تصاویر و برچسب‌های IADD",
         26, True, GREEN, first=True, align=PP_ALIGN.CENTER, after=4)
    line(end.text_frame, "هدف: انطباق مدل با شش رده و صحنه‌های ترافیکی مورد مطالعه",
         21, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    animate(sl, [start] + cards + [end])
'''
a = replace_function(a, "domain", domain)

A.write_text(a, encoding="utf-8", newline="\n")
print("updated slides 2, 3, 5 and 6")
