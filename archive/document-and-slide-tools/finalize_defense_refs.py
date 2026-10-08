from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import os
import re
import tempfile

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


SRC = Path(r"C:\Users\amir2\Desktop\نسخه ارسالی\documents\ارائه_دفاع_نهایی_جلسه.pptx")
BACKUPS = SRC.parent / "پشتیبان‌ها"
assert SRC.exists()
assert list(BACKUPS.glob("ارائه_دفاع_نهایی_جلسه_پیش_از_اصلاح_مراجع_*.pptx")), "Backup missing"

prs = Presentation(SRC)
assert len(prs.slides) == 30
changed = set()


def shape_text(slide_num, index, expected=None):
    sh = prs.slides[slide_num - 1].shapes[index]
    assert sh.has_text_frame
    if expected is not None:
        assert expected in sh.text, (slide_num, index, sh.text)
    return sh


def replace_in_runs(sh, old, new):
    found = False
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            if old in r.text:
                r.text = r.text.replace(old, new)
                found = True
    assert found, (sh.name, old)


def replace_whole(sh, new, use_last=False):
    runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
    assert runs
    chosen = runs[-1] if use_last else runs[0]
    for r in runs:
        r.text = ""
    chosen.text = new


# Retain the user’s slide styling and update only the actual source numbers.
replace_in_runs(shape_text(3, 3, "مرجع"), "1", "۱")
changed.add(3)
replace_in_runs(shape_text(9, 4, "[۹]"), "۹", "۵")
changed.add(9)
replace_in_runs(shape_text(11, 11, "[2]"), "[2]", "[۲]")
changed.add(11)

# Section 1-4 in the final thesis cites [5] for IoU, precision, recall and F1,
# and [9] for AP and mAP. Keep the on-slide lines small and unobtrusive.
for slide_num, label in ((6, "منبع فرمول: ساپکوتا و همکاران، ۲۰۲۵ [۵]"),
                         (7, "منبع فرمول‌ها: ساپکوتا و همکاران، ۲۰۲۵ [۵]"),
                         (8, "منبع فرمول‌ها: لین و همکاران، ۲۰۲۶ [۹]")):
    slide = prs.slides[slide_num - 1]
    box = slide.shapes.add_textbox(Inches(6.5), Inches(7.04), Inches(6.27), Inches(0.29))
    box.name = "ارجاع فرمول‌ها"
    tf = box.text_frame
    tf.clear()
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = label
    run.font.name = "B Zar"
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(38, 61, 79)
    rpr = run._r.get_or_add_rPr()
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    for tag in ("latin", "ea", "cs"):
        el = rpr.find(ns + tag)
        if el is None:
            el = etree.SubElement(rpr, ns + tag)
        el.set("typeface", "B Zar")
    changed.add(slide_num)


# Screening was by per-video mAP@0.5, not by IoU. State the metric once in
# Persian and give the two decisive values as short bullets.
replace_whole(shape_text(14, 5, "هم‌پوشانی"),
              "۱۳ ویدیو با میانگین دقت متوسط کمتر از ۰٫۶۳")
replace_whole(shape_text(14, 7, "mAP@0.5"),
              "ویدیوی ۴۲۶: برچسب نادرست؛ امتیاز ۰٫۰۰۷", use_last=True)
replace_whole(shape_text(14, 8, "mAP@0.5"),
              "ویدیوی ۴۶: برچسب ناقص؛ امتیاز ۰٫۴۵۱", use_last=True)
changed.add(14)

# Match slide 16: show the original notebook filename under the core training
# settings on slide 21, with the same typeface and size as the earlier code file.
s16 = shape_text(16, 5, "build_subset_v5.py")
s21 = shape_text(21, 4, "اعتبارسنجی")
source_par = s16.text_frame.paragraphs[3]
dest_body = s21.text_frame._txBody
dest_body.append(deepcopy(source_par._p))
s21.height = s16.height
for p in s21.text_frame.paragraphs:
    if "build_subset_v5.py" in p.text:
        for r in p.runs:
            r.text = r.text.replace("build_subset_v5.py", "IADD_YOLOv11_Colab_run8.ipynb")
changed.add(21)

# The bibliography is an unspoken backup slide after thanks/questions.
# Include only the four sources actually cited on the slides.
refs = (
    "[1] Khosravian et al., Multi-domain autonomous driving dataset, IET Image Processing, 2023.",
    "[2] Kaufman et al., Leakage in Data Mining, ACM TKDD, 2012.",
    "[5] Sapkota et al., YOLO advances to its genesis, Artificial Intelligence Review, 2025.",
    "[9] Lin et al., YOLO11-WLBS, Scientific Reports, 2026.",
)
slide30 = prs.slides[29]
keep_text_idx = (2, 4, 10, 12)
keep_bar_idx = (1, 3, 9, 11)
for idx, label in zip(keep_text_idx, refs):
    replace_whole(slide30.shapes[idx], label)

for idx in sorted(set(range(1, 25)) - set(keep_text_idx) - set(keep_bar_idx), reverse=True):
    el = slide30.shapes[idx]._element
    el.getparent().remove(el)

# Reflow retained 2x2 references into the same two-column design.
positions = ((0.76, 1.65), (0.76, 3.70), (7.06, 1.65), (7.06, 3.70))
for idx, (x, y) in zip(keep_text_idx, positions):
    sh = next(s for s in slide30.shapes if s.name == f"Rectangle {idx + 6}")
    sh.left, sh.top, sh.height = Inches(x), Inches(y), Inches(1.25)
for idx, (x, y) in zip(keep_bar_idx, positions):
    sh = next(s for s in slide30.shapes if s.name == f"Rectangle {idx + 6}")
    sh.top, sh.height = Inches(y), Inches(1.25)
changed.add(30)

# Existing footers were left behind when slides were inserted. Keep their
# styling and position, but make their numbers match physical slide order.
footer_re = re.compile(r"صفحه\s+[۰-۹0-9]+\s+از\s+[۰-۹0-9]+")
for slide_num, slide in enumerate(prs.slides, 1):
    for sh in slide.shapes:
        if not sh.has_text_frame or not footer_re.search(sh.text):
            continue
        target = f"صفحه {str(slide_num).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))} از ۳۰"
        old = footer_re.search(sh.text).group(0)
        replace_in_runs(sh, old, target)
        changed.add(slide_num)

# Change only targeted slide XML parts; preserve every other PPTX member.
modified = {}
for n in changed:
    modified[f"ppt/slides/slide{n}.xml"] = etree.tostring(
        prs.slides[n - 1].part._element, xml_declaration=True, encoding="UTF-8", standalone=True
    )

fd, temp_name = tempfile.mkstemp(prefix="defense_refs_", suffix=".pptx", dir=SRC.parent)
os.close(fd)
try:
    with ZipFile(SRC) as original, ZipFile(temp_name, "w") as revised:
        for info in original.infolist():
            data = modified.get(info.filename)
            if data is None:
                data = original.read(info.filename)
            revised.writestr(info, data)
    with ZipFile(temp_name) as check:
        assert check.testzip() is None
    os.replace(temp_name, SRC)
except BaseException:
    Path(temp_name).unlink(missing_ok=True)
    raise

print("Changed slides:", sorted(changed))
print("Output:", SRC)
