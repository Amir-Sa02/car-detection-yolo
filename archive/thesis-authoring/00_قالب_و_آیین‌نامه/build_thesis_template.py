# -*- coding: utf-8 -*-
"""Front matter of the thesis, built to the current (1387) Sadjad آیین‌نامه.

Covers everything before the first chapter: cover, بسم‌الله, title page,
سپاسگزاری, تقدیم, چکیده, and the list pages. Chapters live in their own folders
and are produced by their own scripts; formatting comes from thesis_style.

Placeholders the student must fill are written in RED inside brackets.

Two points where this follows the current guide rather than the older one:
  * the cover template carries no گرایش line - only «پایان‌نامه دوره [مقطع] کامپیوتر»
  * سپاسگزاری comes BEFORE تقدیم
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["THESIS_OUT"] = os.path.join(HERE, "پایان_نامه_قالب.docx")
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK                   # noqa: E402
from docx.shared import Pt, Cm                                            # noqa: E402
from docx.oxml import OxmlElement                                         # noqa: E402
from thesis_style import (doc, para, finish, TITLE_FONT, RED,             # noqa: E402
                          BLACK, _bidi, _rs)

CENTER = WD_ALIGN_PARAGRAPH.CENTER


def from_top(cm):
    """آیین‌نامه measures from the paper edge, Word from the margin: drop the 3 cm
    top margin and return the remainder as points of space-before."""
    return max(0.0, (cm - 3.0) / 2.54 * 72)


def mid(text, size, bold=True, sb=0, sa=0, font=None):
    return para(text, size=size, bold=bold, color=BLACK, align=CENTER,
                sb=sb, sa=sa, font=font)


def ph(text, size, sb=0, sa=0, font=None):
    return para("[ " + text + " ]", size=size, bold=True, color=RED,
                align=CENTER, sb=sb, sa=sa, font=font)


def page():
    p = doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)


def indent(p, right_cm=0.0, left_cm=0.0):
    p.paragraph_format.right_indent = Cm(right_cm)
    p.paragraph_format.left_indent = Cm(left_cm)
    return p


# ============================================================ روی جلد
ph("آرم جدید مؤسسه - ۲ سانتی‌متر از لبه بالای جلد", 12, sb=6)
mid("پایان‌نامه دوره", 16, sb=from_top(7.5))
ph("مقطع تحصیلی", 16)
mid("کامپیوتر", 16)
mid("موضوع:", 18, sb=40)
ph("عنوان پایان‌نامه - دقیقاً مطابق عنوان تأییدشده هنگام انتخاب پروژه", 20, sb=18)
mid("استاد راهنما:", 18, sb=110)
ph("مهندس/دکتر نام و نام خانوادگی استاد راهنما", 18, sb=4)
mid("نام دانشجو:", 18, sb=70)
ph("نام و نام خانوادگی دانشجو", 18, sb=4)
ph("ماه و سال دفاع", 16, sb=80)

# ============================================================ بسم‌الله
page()
mid("بسم الله الرحمن الرحیم", 20, sb=from_top(11))

# ============================================================ صفحه عنوان
# same as the cover, with the examiner's name added
page()
ph("آرم جدید مؤسسه", 12, sb=6)
mid("پایان‌نامه دوره", 16, sb=from_top(7.5))
ph("مقطع تحصیلی", 16)
mid("کامپیوتر", 16)
mid("موضوع:", 18, sb=28)
ph("عنوان پایان‌نامه", 20, sb=16)
mid("استاد راهنما:", 18, sb=70)
ph("مهندس/دکتر نام استاد راهنما", 18, sb=4)
mid("استاد داور:", 18, sb=24)
ph("مهندس/دکتر نام استاد داور", 18, sb=4)
mid("نام دانشجو:", 18, sb=40)
ph("نام و نام خانوادگی دانشجو", 18, sb=4)
ph("ماه و سال دفاع", 16, sb=50)

# ============================================================ سپاسگزاری
# title 9.5 cm from the top, font 16; body font 14, 4 cm from the right edge and
# 3 cm from the left edge (one extra centimetre of indent on each side).
page()
mid("سپاسگزاری", 16, sb=from_top(9.5), sa=10)
indent(para("[ متن سپاسگزاری - این صفحه اختیاری است ]", size=14, bold=True,
            color=RED, align=WD_ALIGN_PARAGRAPH.JUSTIFY), 1.0, 1.0)

# ============================================================ تقدیم
# «تقدیم به» font 12, 10 cm from the top and 13 cm from the right edge;
# body font 12 with a 5 cm line length; never more than one page.
page()
indent(para("تقدیم به", size=12, bold=True, sb=from_top(10), sa=6), 10.0)
indent(para("[ متن تقدیم - حداکثر یک صفحه ]", size=12, bold=True, color=RED), 10.0)

# ============================================================ چکیده
# «چکیده» font 14 لوتوس سیاه, 4 cm from the top, centred; the project title on the
# next line at the same size; body font 12 زر, 4 cm right / 3 cm left, half a page.
page()
mid("چکیده", 14, sb=from_top(4), sa=4, font=TITLE_FONT)
ph("عنوان پروژه", 14, sa=12, font=TITLE_FONT)
indent(para("[ متن چکیده - حداکثر نصف صفحه. شامل بیان مختصر مسئله مورد بررسی، شرح کلی "
            "مراحل به‌کارگرفته‌شده برای کسب و جمع‌آوری اطلاعات، نحوه عمل و نتیجه کلی "
            "حاصله ]", size=12, bold=True, color=RED,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY), 1.0, 1.0)

indent(para("واژه‌های کلیدی", size=14, bold=True, sb=18, sa=4, font=TITLE_FONT), 1.0)
indent(para("[ واژه یک، واژه دو، واژه سه - حداکثر ده مورد، همگی در یک خط، جدا شده با "
            "ویرگول و با یک نقطه در پایان ]", size=12, bold=True, color=RED), 1.0, 1.0)

# ============================================================ فهرست مطالب
# title 11 cm from the top, font 14 لوتوس سیاه; one centimetre lower the words
# «عنوان» (3 cm from the right) and «صفحه» (2 cm from the left), same size.
page()
mid("فهرست مطالب", 14, sb=from_top(11), sa=14, font=TITLE_FONT)

t = doc.add_table(rows=1, cols=2)
t._tbl.tblPr.append(OxmlElement("w:bidiVisual"))      # first cell on the right
for cell, text, align in ((t.rows[0].cells[0], "عنوان", WD_ALIGN_PARAGRAPH.RIGHT),
                          (t.rows[0].cells[1], "صفحه", WD_ALIGN_PARAGRAPH.LEFT)):
    pp = cell.paragraphs[0]; _bidi(pp); pp.alignment = align
    r = pp.add_run(text); r.bold = True
    r.font.size = Pt(14); r.font.name = TITLE_FONT
    _rs(r, 14, True, font=TITLE_FONT)

para("[ پس از نوشتن فصل‌ها، روی این محل کلیک کنید و کلید F9 را بزنید تا فهرست ساخته شود ]",
     size=11, color=RED, align=CENTER, sb=12)

# ============================================================ فهرست شکل‌ها
page()
mid("فهرست شکل‌ها", 14, sb=from_top(11), sa=14, font=TITLE_FONT)
para("[ از منوی References گزینه Insert Table of Figures با برچسب «شکل» ]",
     size=11, color=RED, align=CENTER)

# ============================================================ فهرست جدول‌ها
page()
mid("فهرست جدول‌ها", 14, sb=from_top(11), sa=14, font=TITLE_FONT)
para("[ از منوی References گزینه Insert Table of Figures با برچسب «جدول» ]",
     size=11, color=RED, align=CENTER)

# ============================================================ لیست علائم
page()
mid("لیست علائم و اختصارات", 14, sb=from_top(11), sa=14, font=TITLE_FONT)
para("[ در صورت نیاز - علامت در سمت چپ و مفهوم آن در سمت راست ]",
     size=11, color=RED, align=CENTER)

finish()
