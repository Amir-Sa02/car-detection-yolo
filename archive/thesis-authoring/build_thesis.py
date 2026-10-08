# -*- coding: utf-8 -*-
"""پایان‌نامه کامل را در یک فایل واحد می‌سازد.

ترتیب دقیقاً همان است که آیین‌نامه ۱۳۸۷ خواسته:
  صفحه‌های فرعی (شماره‌گذاری با حروف فارسی) — ص ۱۴
    آ بسم الله · ب صفحه عنوان · پ سپاسگزاری · ت تقدیم · ث چکیده و واژه‌های کلیدی
    ج فهرست مطالب · چ فهرست شکل‌ها · ح فهرست جدول‌ها · خ لیست علائم و اختصارات
  صفحه‌های اصلی (شماره‌گذاری با اعداد، از ۱) — ص ۱۶ و ۱۷
    مقدمه · فصل اول · فصل دوم · فصل سوم · فصل چهارم · مراجع و منابع

روش ساخت: به‌جای چسباندن چند فایل docx به هم — که تصویر، پانویس و شماره‌گذاری را
خراب می‌کند — همه‌چیز در یک فرایند و داخل یک سند ساخته می‌شود. thesis_style فقط
یک بار وارد می‌شود، پس سند، سبک‌ها و شمارنده پانویس‌ها در تمام فصل‌ها مشترک‌اند.

پس از باز کردن فایل در Word: یک‌بار Ctrl+A سپس F9 تا هر سه فهرست پر شوند.
"""
import io
import os
import sys as _sys
_sys.stdout = io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8")
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = os.path.join(HERE, "00_قالب_و_آیین‌نامه")
FRONT = os.path.join(HERE, "00_صفحات_فرعی", "کد")
OUT = os.path.join(HERE, "پایان‌نامه_نهایی.docx")

sys.path.insert(0, STYLE)
sys.path.insert(0, FRONT)

# thesis_style reads THESIS_OUT once, at import; point it at the final file
os.environ["THESIS_OUT"] = OUT
os.environ["THESIS_FIGDIR"] = HERE

import thesis_style as T                                              # noqa: E402
from docx.shared import Pt, Cm                                        # noqa: E402
from docx.enum.section import WD_SECTION                              # noqa: E402
from docx.oxml.ns import qn                                           # noqa: E402
from docx.oxml import OxmlElement                                     # noqa: E402
import build_front_matter as F                                        # noqa: E402

doc = T.doc

# ------------------------------------------------------------------ page number
def _page_number_footer(section, start_at=None):
    """شماره صفحه با عدد، وسط، ۱٫۵cm بالاتر از پایین صفحه (ص ۱۵).

    فیلد PAGE با زبان فارسی نوشته می‌شود؛ Word ارقام را بر پایه تنظیم Numeral
    خودش (Context یا Hindi) به شکل فارسی نشان می‌دهد."""
    section.footer.is_linked_to_previous = False
    p = section.footer.paragraphs[0]
    p.text = ""
    F._bidi(p); F._jc(p, "center")
    for tag, attr, txt in (("w:fldChar", "w:fldCharType", "begin"),
                           ("w:instrText", None, "PAGE"),
                           ("w:fldChar", "w:fldCharType", "end")):
        r = p.add_run()
        r.font.size = Pt(12)
        F._rs(r, 12)
        rPr = r._r.get_or_add_rPr()
        rPr.append(OxmlElement("w:rtl"))
        lang = OxmlElement("w:lang"); lang.set(qn("w:bidi"), "fa-IR"); rPr.append(lang)
        e = OxmlElement(tag)
        if attr:
            e.set(qn(attr), txt)
        else:
            e.set(qn("xml:space"), "preserve"); e.text = txt
        r._r.append(e)
    if start_at is not None:
        sp = section._sectPr
        for old in sp.findall(qn("w:pgNumType")):
            sp.remove(old)
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), str(start_at))
        pg.set(qn("w:fmt"), "decimal")
        sp.append(pg)


# ============================================================ صفحه‌های فرعی
# سکشن ۰ همان صفحه بسم الله می‌شود؛ باقی صفحه‌ها را build_front می‌سازد.
F.build_front(doc)

# ============================================================ صفحه‌های اصلی
main = doc.add_section(WD_SECTION.NEW_PAGE)
F._page_setup(main, top=3.0, bottom=2.5)
_page_number_footer(main, start_at=1)

CONTENT = [
    ("مقدمه",                    "کد/build_introduction.py",  "شکل‌ها"),
    ("فصل1_پیشینه",              "کد/build_chapter1.py",      "شکل‌ها"),
    ("فصل2_روش_و_داده",          "کد/build_chapter2.py",      "شکل‌ها"),
    ("فصل3_نتایج",               "کد/build_chapter3.py",      "شکل‌ها"),
    ("فصل4_بحث_و_نتیجه‌گیری",    "کد/build_chapter4.py",      "شکل‌ها"),
]

_real_finish = T.finish
T.finish = lambda: None            # هر فصل خودش ذخیره نکند؛ آخر کار یک‌بار

# h_ch هر فصل را با یک شکست صفحه آغاز می‌کند، ولی مقدمه همین حالا بعد از شکست
# سکشن می‌آید؛ آن شکست اضافی یک صفحه سفید می‌سازد، پس فقط برای اولین فصل حذفش
# می‌کنیم.
_real_h_ch = T.h_ch


def _h_ch_first(t, **kw):
    T.h_ch = _real_h_ch
    q = _real_h_ch(t, **kw)
    prev = q._p.getprevious()
    if prev is not None and prev.tag == qn("w:p") and not prev.findall(".//" + qn("w:t")):
        prev.getparent().remove(prev)
    return q


T.h_ch = _h_ch_first

for folder, script, figdir in CONTENT:
    os.environ["THESIS_FIGDIR"] = os.path.join(HERE, folder, figdir)
    path = os.path.join(HERE, folder, *script.split("/"))
    src = io.open(path, encoding="utf-8").read()
    # حذف سطرهایی که THESIS_OUT را عوض می‌کنند یا دوباره sys.path می‌سازند
    src = "\n".join(l for l in src.split("\n")
                    if "THESIS_OUT" not in l and "THESIS_FIGDIR" not in l)
    g = {"__name__": "__thesis_part__", "__file__": path}
    exec(compile(src, path, "exec"), g)
    print(f"  + {folder}")

# ------------------------------------------------------------------ مراجع
os.environ["THESIS_FIGDIR"] = HERE
ref_src = io.open(os.path.join(HERE, "مراجع", "build_references.py"),
                  encoding="utf-8").read()
ref_src = "\n".join(l for l in ref_src.split("\n")
                    if "THESIS_OUT" not in l and "THESIS_FIGDIR" not in l)
exec(compile(ref_src, "build_references.py", "exec"),
     {"__name__": "__thesis_part__",
      "__file__": os.path.join(HERE, "مراجع", "build_references.py")})
print("  + مراجع و منابع")

T.finish = _real_finish
T.finish()
print("\nنوشته شد:", os.path.basename(OUT))
print("در Word یک‌بار Ctrl+A سپس F9 بزنید تا هر سه فهرست پر شوند.")
