from pathlib import Path


ROOT = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\کد")
A = ROOT / "content_a.py"
D = ROOT / "deck.py"


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one match, found {count}: {old[:100]!r}")
    return text.replace(old, new, 1)


def replace_function(text: str, name: str, replacement: str) -> str:
    marker = f"@reg\ndef {name}():"
    start = text.index(marker)
    next_start = text.index("\n# ----------------------------------------------------------------", start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[next_start + 1:]


# Split Latin tokens into their own runs and render them one point smaller.
deck = D.read_text(encoding="utf-8")
deck = replace_once(
    deck,
    'SEP = re.compile(r"([٫٬]+)")\n',
    'SEP = re.compile(r"([٫٬]+)")\nLATIN_TOKEN = re.compile(r"([A-Za-z][A-Za-z0-9@._:+/%-]*)")\n')
old_run = '''def _run(p, text, size, bold, colour):
    """Persian separators get their own run: the deck font falls back on them
    and the fallback draws a comma with a wide gap instead of a tight mark."""
    parts = [t for t in SEP.split(text) if t]
    for part in parts[:-1]:
        _one(p, part, size, bold, colour)
    return _one(p, parts[-1], size, bold, colour) if parts else None
'''
new_run = '''def _run(p, text, size, bold, colour):
    """Put Latin tokens in separate Times New Roman runs, one point smaller."""
    chunks = []
    for sep_part in (part for part in SEP.split(text) if part):
        chunks.extend(part for part in LATIN_TOKEN.split(sep_part) if part)
    last = None
    for chunk in chunks:
        last = _one(p, chunk, size, bold, colour)
    return last
'''
deck = replace_once(deck, old_run, new_run)
deck = replace_once(
    deck,
    '    # Latin words ride two points lower so they sit level with Persian\n'
    '    if not FA_LETTER.search(text):\n'
    '        r.font.size = Pt(max(17, size - 2))\n',
    '    # Latin words use Times New Roman one point smaller than nearby Persian.\n'
    '    if ASCII_ALNUM.search(text) and not FA_LETTER.search(text):\n'
    '        r.font.size = Pt(max(1, size - 1))\n')
D.write_text(deck, encoding="utf-8", newline="\n")

a = A.read_text(encoding="utf-8")

# Academic, high-contrast helpers used only by slides 1 to 7.
helpers = r'''

def academic_tile(sl, x, y, w, h, head, body, accent=NAVY, hs=25, bs=20):
    sh = box(sl, x, y, w, h, WHITE, accent)
    sh.line.width = Pt(1.7)
    line(sh.text_frame, head, hs, True, accent, first=True,
         align=PP_ALIGN.CENTER, after=4)
    if body:
        line(sh.text_frame, body, bs, False, SLATE,
             align=PP_ALIGN.CENTER, after=0)
    return sh


def strong_table(sl, rows, x, y, w, h, hs=20, bs=19, hcols=()):
    """High-contrast table for low-quality projectors."""
    frame = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    frame.fill.solid(); frame.fill.fore_color.rgb = WHITE
    frame.line.color.rgb = NAVY; frame.line.width = Pt(1.5)
    frame.shadow.inherit = False
    shp = table(sl, rows, x, y, w, h, hs, bs, hcols=hcols)
    tbl = shp.table
    for ri, row in enumerate(tbl.rows):
        for ci, cell in enumerate(row.cells):
            is_head = ri == 0
            is_label = ci in hcols and ri > 0
            cell.fill.solid()
            cell.fill.fore_color.rgb = (NAVY if is_head else
                                        (TINT_GREY if (is_label or ri % 2 == 0) else WHITE))
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb = WHITE if is_head else (NAVY if is_label else INK)
                    run.font.bold = is_head or is_label
            tc_pr = cell._tc.get_or_add_tcPr()
            for edge in ("lnL", "lnR", "lnT", "lnB"):
                old = tc_pr.find(A + edge)
                if old is not None:
                    tc_pr.remove(old)
                ln = etree.SubElement(tc_pr, A + edge)
                ln.set("w", "12700")
                solid = etree.SubElement(ln, A + "solidFill")
                colour = etree.SubElement(solid, A + "srgbClr")
                colour.set("val", "AAB5BE")
                etree.SubElement(ln, A + "prstDash").set("val", "solid")
    return shp
'''
# content_a already imports etree indirectly? Add explicit import for table borders.
a = replace_once(a, "import os\n\n", "import os\n\nfrom lxml import etree\nfrom pptx.dml.color import RGBColor\n")
insert_at = a.index("\n\n# ----------------------------------------------------------------------- 1")
a = a[:insert_at] + helpers + a[insert_at:]

cover = r'''@reg
def cover():
    sl = slide(bg=WHITE)
    top_rule = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.16))
    top_rule.fill.solid(); top_rule.fill.fore_color.rgb = NAVY
    top_rule.line.fill.background(); top_rule.shadow.inherit = False

    logo = sl.shapes.add_picture(os.path.join(FS, "cover_image2.png"),
                                 Inches(0), Inches(0.40), height=Inches(1.05))
    logo.left = int((W - logo.width) / 2)

    tb, tf = textbox(sl, Inches(1.1), Inches(1.52), W - Inches(2.2), Inches(0.45))
    line(tf, "دانشکده مهندسی کامپیوتر", 21, False, SLATE, first=True,
         align=PP_ALIGN.CENTER, after=0)

    tb, tf = textbox(sl, Inches(1.0), Inches(2.05), W - Inches(2.0), Inches(1.75))
    line(tf, "دسته‌بندی اشیای ترافیکی با استفاده از YOLO", 34, True, NAVY,
         first=True, align=PP_ALIGN.CENTER, after=8)
    line(tf, "۶ دسته متفاوت: عابر، تریلر، اتوبوس، خودروی سبک، وانت و موتور",
         20, False, INK, align=PP_ALIGN.CENTER, after=8)
    line(tf, "پیاده‌سازی با معماری YOLOv11", 25, True, BLUE,
         align=PP_ALIGN.CENTER, after=0)

    rule = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.35), Inches(4.05),
                               Inches(4.63), Inches(0.035))
    rule.fill.solid(); rule.fill.fore_color.rgb = NAVY
    rule.line.fill.background(); rule.shadow.inherit = False

    rows = [("استاد راهنما", "دکتر رضا شمسایی"),
            ("استاد داور", "[نام استاد داور]"),
            ("دانشجو", "محمد امیر صادق‌زاده")]
    y = Inches(4.42)
    for lab, name in rows:
        tb, tf = textbox(sl, Inches(7.2), y, Inches(2.2), Inches(0.45))
        line(tf, lab, 20, False, SLATE, first=True, align=PP_ALIGN.RIGHT, after=0)
        tb, tf = textbox(sl, Inches(3.65), y, Inches(3.25), Inches(0.45))
        line(tf, name, 22, True, INK, first=True, align=PP_ALIGN.RIGHT, after=0)
        sep = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.65), y + Inches(0.47),
                                  Inches(5.75), Inches(0.012))
        sep.fill.solid(); sep.fill.fore_color.rgb = RGBColor(0xB8, 0xC0, 0xC7)
        sep.line.fill.background(); sep.shadow.inherit = False
        y += Inches(0.63)
'''
a = replace_function(a, "cover", cover)

agenda = r'''@reg
def agenda():
    sl = slide("فهرست ارائه")
    items = [(1, "مبانی و صورت مسئله"),
             (2, "روش پژوهش و آماده‌سازی داده"),
             (3, "نتایج و تحلیل"),
             (4, "جمع‌بندی و پیشنهادها")]
    y = TOP + Inches(0.16)
    for num, txt in items:
        sh = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, MARGIN, y, CW, Inches(1.08))
        sh.fill.solid(); sh.fill.fore_color.rgb = WHITE
        sh.line.color.rgb = NAVY; sh.line.width = Pt(1.6); sh.shadow.inherit = False
        nbox = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   W - MARGIN - Inches(0.92), y,
                                   Inches(0.92), Inches(1.08))
        nbox.fill.solid(); nbox.fill.fore_color.rgb = NAVY
        nbox.line.fill.background(); nbox.shadow.inherit = False
        line(nbox.text_frame, fa_num(num), 27, True, WHITE, first=True,
             align=PP_ALIGN.CENTER, after=0)
        tb, tf = textbox(sl, MARGIN + Inches(0.35), y + Inches(0.05),
                         CW - Inches(1.55), Inches(0.92), MSO_ANCHOR.MIDDLE)
        line(tf, txt, 28, True, NAVY, first=True, align=PP_ALIGN.RIGHT, after=0)
        y += Inches(1.25)
'''
a = replace_function(a, "agenda", agenda)

scope = r'''@reg
def scope():
    sl = slide("رده‌های مصوب و نهایی")
    rows = [["وضعیت", "رده نهایی", "عنوان مصوب"],
            ["گسترده‌تر", "شخص", "عابر"],
            ["یکسان", "اتوبوس", "اتوبوس"],
            ["یکسان", "خودروی سبک", "خودروی سبک"],
            ["یکسان", "موتورسیکلت", "موتور"],
            ["ادغام شد", "خودروی باری", "تریلر"],
            ["ادغام شد", "خودروی باری", "وانت"],
            ["افزوده شد", "چراغ راهنمایی", "—"]]
    strong_table(sl, rows, Inches(6.72), TOP, Inches(6.0), Inches(4.25),
                 19, 19, hcols=())

    items = [("محدودیت آغاز پروژه", "تصویب موضوع هم‌زمان با قطعی سراسری اینترنت"),
             ("انتخاب مجموعه‌داده", "انتخاب IADD به‌جای BDD100K، با نظر استاد راهنما"),
             ("تلاش برای انطباق رده‌ها", "بازبرچسب‌گذاری کامل در زمان پروژه عملی نبود")]
    y = TOP
    for head, body in items:
        academic_tile(sl, MARGIN, y, Inches(5.72), Inches(1.30),
                      head, body, NAVY, 23, 19)
        y += Inches(1.43)

    sh = box(sl, MARGIN, Inches(5.85), CW, Inches(0.85), WHITE, GREEN)
    sh.line.width = Pt(1.8)
    line(sh.text_frame, "رده‌های نهایی بر پایه برچسب‌های موجود IADD تعریف شدند",
         24, True, GREEN, first=True, align=PP_ALIGN.CENTER, after=0)
'''
a = replace_function(a, "scope", scope)

d1 = r'''@reg
def d1():
    sl = slide(bg=WHITE)
    mark = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, W - Inches(0.42), 0,
                               Inches(0.42), H)
    mark.fill.solid(); mark.fill.fore_color.rgb = NAVY
    mark.line.fill.background(); mark.shadow.inherit = False
    tb, tf = textbox(sl, Inches(1.25), Inches(1.75), W - Inches(2.5), Inches(0.65))
    line(tf, "بخش ۱", 27, True, BLUE, first=True, align=PP_ALIGN.CENTER, after=0)
    tb, tf = textbox(sl, Inches(1.25), Inches(2.55), W - Inches(2.5), Inches(1.0))
    line(tf, "مبانی و صورت مسئله", 46, True, NAVY, first=True,
         align=PP_ALIGN.CENTER, after=0)
    rule = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.2), Inches(3.72),
                               Inches(4.93), Inches(0.035))
    rule.fill.solid(); rule.fill.fore_color.rgb = NAVY
    rule.line.fill.background(); rule.shadow.inherit = False
    tb, tf = textbox(sl, Inches(1.25), Inches(4.05), W - Inches(2.5), Inches(0.7))
    line(tf, "اهمیت مسئله، داده بومی و معماری مدل", 24, False, SLATE,
         first=True, align=PP_ALIGN.CENTER, after=0)
'''
a = replace_function(a, "d1", d1)

problem = r'''@reg
def problem():
    sl = slide("اهمیت مسئله تشخیص اشیا")
    items = [("درک صحنه", "تعیین رده و موقعیت هر شیء در تصویر"),
             ("ورودی تصمیم‌گیری", "اطلاعات لازم برای سامانه‌های کمک‌راننده"),
             ("چالش محیط واقعی", "تفاوت نور، فاصله، اندازه و هم‌پوشانی اشیا"),
             ("هدف پروژه", "تشخیص شش رده ترافیکی و ارزیابی قابل‌اتکای مدل")]
    y = TOP + Inches(0.02)
    shapes = []
    for i, (head, body) in enumerate(items):
        accent = GREEN if i == len(items) - 1 else NAVY
        shapes.append(academic_tile(sl, MARGIN, y, CW, Inches(1.12),
                                    head, body, accent, 25, 20))
        y += Inches(1.27)
    animate(sl, shapes)
'''
a = replace_function(a, "problem", problem)

domain = r'''@reg
def domain():
    sl = slide("تنظیم دقیق مدل با IADD")
    start = academic_tile(sl, MARGIN, TOP, CW, Inches(1.00),
                          "نقطه آغاز", "وزن‌های ازپیش‌آموخته YOLOv11s روی COCO",
                          NAVY, 24, 21)

    items = [("الگوی ترافیک", "صحنه‌های واقعی ایران"),
             ("وسایل نقلیه رایج", "خودروهای موجود در معابر کشور"),
             ("شرایط محیطی", "روز، شب، باران و ابری")]
    w, gap = Inches(3.72), Inches(0.38)
    x = W - MARGIN - w
    cards = []
    for head, sub in items:
        cards.append(academic_tile(sl, x, Inches(2.78), w, Inches(1.65),
                                   head, sub, NAVY, 26, 20))
        x -= (w + gap)

    end = box(sl, MARGIN, Inches(5.10), CW, Inches(1.25), WHITE, GREEN)
    end.line.width = Pt(1.8)
    line(end.text_frame, "مرحله پروژه: تنظیم دقیق مدل با تصاویر و برچسب‌های IADD",
         26, True, GREEN, first=True, align=PP_ALIGN.CENTER, after=4)
    line(end.text_frame, "هدف: انطباق مدل با شش رده و صحنه‌های ترافیکی مورد مطالعه",
         21, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    animate(sl, [start] + cards + [end])
'''
a = replace_function(a, "domain", domain)

iadd = r'''@reg
def iadd():
    sl = slide("مقایسه IADD و داده مورد استفاده")
    rows = [["زیرمجموعه نهایی", "نسخه برچسب‌دار در دسترس", "IADD در مقاله", "ویژگی"],
            ["۳۷٬۱۴۲", "۸۳٬۰۴۲", "۹۷٬۵۲۸", "تصویر"],
            ["۱۶۰", "۱۶۶", "۱۷۱", "ویدیو"],
            ["۶", "۶", "۶", "رده"]]
    strong_table(sl, rows, MARGIN, TOP, CW, Inches(3.15), 20, 20, hcols=(0,))

    note = box(sl, MARGIN, Inches(4.85), CW, Inches(0.86), WHITE, CRIMSON)
    note.line.width = Pt(1.7)
    line(note.text_frame,
         "در نسخه دریافت‌شده، ۱۴٬۴۸۶ تصویر بخش آزمون فایل برچسب نداشتند",
         23, True, CRIMSON, first=True, align=PP_ALIGN.CENTER, after=0)

    left = academic_tile(sl, MARGIN, Inches(5.92), Inches(5.75), Inches(0.78),
                         "شش رده", "رده‌های اصلی IADD", NAVY, 22, 19)
    right = academic_tile(sl, Inches(6.95), Inches(5.92), Inches(5.75), Inches(0.78),
                          "هشت شهر ایران", "مبدأ گردآوری مجموعه اصلی", NAVY, 22, 19)
    tb, tf = textbox(sl, Inches(4.25), Inches(6.63), Inches(4.8), Inches(0.25))
    line(tf, "منبع آمار IADD: مرجع [۱] پایان‌نامه", 16, False, SLATE,
         first=True, align=PP_ALIGN.CENTER, after=0)
'''
a = replace_function(a, "iadd", iadd)

A.write_text(a, encoding="utf-8", newline="\n")
print("redesigned slides 1-7 and updated mixed-script typography")
