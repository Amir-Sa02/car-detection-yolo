# -*- coding: utf-8 -*-
"""Shared formatting layer for every thesis chapter.
All rules here come from the Sadjad آیین‌نامه: A4, margins 3/2/3/2.5 cm,
B Nazanin 14 body with Latin two steps smaller, 0.8 cm first-line indent,
chapter title 18 bold at 11 cm from the page top, headings 16/14 bold,
figure caption below / table caption above at font 10, numbered formulas
as real Word equations, and Latin terms in left-aligned footnotes.
Import it, add content, then call finish().
"""

import os, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("THESIS_OUT", "out.docx")
FIGDIR = os.environ.get("THESIS_FIGDIR", ".")
FA2EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
# آیین‌نامه: body and headings in زر, the چکیده / فهرست titles in لوتوس,
# figure and table captions plus numerals in نازنین, Latin in Times New Roman.
FONT = "B Zar"            # body text and all numbered headings
TITLE_FONT = "B Lotus"    # چکیده، فهرست مطالب، واژه‌های کلیدی
CAPTION_FONT = "B Nazanin"  # شماره و عنوان شکل‌ها و جدول‌ها
LAT = "Times New Roman"
BLACK, RED = RGBColor(0, 0, 0), RGBColor(0xC0, 0, 0)
BODY = 14

doc = Document()
st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(BODY)
st.paragraph_format.line_spacing = 1.5; st.paragraph_format.space_after = Pt(0)
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(3), Cm(2.5)
sec.right_margin, sec.left_margin = Cm(3), Cm(2)
sec.footer_distance = Cm(1.5)
sp = sec._sectPr
if sp.find(qn("w:bidi")) is None:
    b = OxmlElement("w:bidi"); g = sp.find(qn("w:docGrid"))
    (g.addprevious(b) if g is not None else sp.append(b))


CAP_FIG, CAP_TBL = "عنوان شکل", "عنوان جدول"


def _caption_style(name):
    """یک سبک پاراگراف برای زیرنویس شکل و عنوان جدول.

    فهرست شکل‌ها و فهرست جدول‌ها با فیلد TOC 	 ساخته می‌شوند و آن فیلد فقط
    پاراگراف‌هایی را می‌بیند که سبک نام‌بُرده را داشته باشند؛ سوئیچ c\ به فیلد
    SEQ نیاز دارد که در این سند وجود ندارد."""
    try:
        return doc.styles[name]
    except KeyError:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]
        st.quick_style = False
        st.font.name = CAPTION_FONT
        st.font.size = Pt(10)
        st.font.bold = True
        return st


def _bidi(p):
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn("w:bidi")) is None:
        b = OxmlElement("w:bidi"); pPr.insert(0, b)


def _outline(p, lvl):
    ol = OxmlElement("w:outlineLvl"); ol.set(qn("w:val"), str(lvl))
    p._p.get_or_add_pPr().append(ol)


def _rs(run, size, bold, rtl=True, font=None):
    f = font or (FONT if rtl else LAT)
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi"):
        rf.set(qn(a), f)
    rf.set(qn("w:cs"), font or (FONT if rtl else f))
    sc = OxmlElement("w:szCs"); sc.set(qn("w:val"), str(int(size * 2))); rPr.append(sc)
    if bold: rPr.append(OxmlElement("w:bCs"))
    if rtl:  rPr.append(OxmlElement("w:rtl"))


def para(text="", size=BODY, bold=False, color=BLACK, align=None, sb=0, sa=0,
         ind=None, font=None):
    p = doc.add_paragraph(); _bidi(p)
    if align is not None: p.alignment = align
    pf = p.paragraph_format; pf.space_before = Pt(sb); pf.space_after = Pt(sa)
    pf.line_spacing = 1.5
    if ind is not None: pf.first_line_indent = Cm(ind)
    if text:
        _emit(p, text, size, bold, font=font or FONT, color=color)
    return p


_LATIN = re.compile(r"[A-Za-z0-9@._:+\-]*[A-Za-z][A-Za-z0-9@._:+\-]*")


def lat_size(size):
    """اندازه قلم لاتین در برابر قلم فارسی.

    آیین‌نامه سجاد در این باره ساکت است. عرف پایان‌نامه‌های فارسی «دو واحد
    کوچک‌تر» است (فارسی ۱۴ / لاتین ۱۲، فارسی ۱۲ / لاتین ۱۰، عنوان ۱۶ سیاه /
    لاتین ۱۴ سیاه)، چون Times New Roman با همان عدد قلم، درشت‌تر از قلم فارسی
    دیده می‌شود. کف ۱۰ گذاشته شده تا زیرنویس شکل و جدول و متن داخل جدول - که
    خودشان ۱۰ هستند - ریزتر نشوند."""
    return max(10, size - 2)


def _emit(p, txt, size, bold=False, font=None, color=None):
    """یک رشته فارسی را به دنبال‌های فارسی و لاتین می‌شکند و هرکدام را با قلم و
    اندازه خودش می‌نویسد، تا یک واژه لاتین هرجای پایان‌نامه یک شکل داشته باشد."""
    fa_font = font or FONT
    ls = lat_size(size)

    def run(t, latin):
        r = p.add_run(t); r.bold = bold
        r.font.size = Pt(ls if latin else size)
        r.font.name = LAT if latin else fa_font
        if color is not None:
            r.font.color.rgb = color
        _rs(r, ls if latin else size, bold, not latin,
            font=None if latin else fa_font)

    i = 0
    for m in _LATIN.finditer(txt):
        if m.start() > i:
            run(txt[i:m.start()], False)
        run(m.group(0), True)
        i = m.end()
    if i < len(txt):
        run(txt[i:], False)


def rich(parts, align=WD_ALIGN_PARAGRAPH.JUSTIFY, ind=0.8, sa=2, size=BODY):
    """parts: list of (text, kind) where kind in {'fa','en','sup'}"""
    p = doc.add_paragraph(); _bidi(p); p.alignment = align
    pf = p.paragraph_format; pf.line_spacing = 1.5; pf.space_after = Pt(sa)
    pf.first_line_indent = Cm(ind)
    for txt, kind in parts:
        if kind == "fa":
            _emit(p, txt, size)          # واژه‌های لاتینِ درون متن جدا می‌شوند
            continue
        r = p.add_run(txt)
        if kind == "en":
            r.font.size = Pt(lat_size(size)); r.font.name = LAT
            _rs(r, lat_size(size), False, False)
        elif kind == "sup":
            r.font.size = Pt(lat_size(size)); r.font.name = LAT
            r.font.superscript = True; _rs(r, lat_size(size), False, False)
    return p


def body(t): return rich([(t, "fa")])


def disp_num(n):
    """Chapter-first logical number -> a string that renders the way the
    آیین‌نامه requires, in every context.

    The rule is stated three times: «برای شماره‌گذاری عنوان‌های یک فصل، از سمت
    راست ابتدا شماره فصل و سپس شماره عنوان اصلی فصل آورده می‌شود» (ص۱۶),
    «شماره فرمول حاصل ترکیب (از سمت راست به چپ) شماره فصل و شماره ترتیب فرمول
    است» (ص۱۸ بند۵), «قاعده شماره‌گذاری جدول و شکل مانند فرمول‌هاست، یعنی از
    سمت راست ابتدا شماره فصل» (ص۱۸ بند۶). So, reading right to left, the
    chapter number must come first.

    A bare «۱-۲» cannot deliver that. Digits and the hyphen between them form a
    single left-to-right number run, and where that run lands depends on what
    surrounds it: at the head of a paragraph «۱-۲» puts ۲ on the right, but
    inside «شکل ۱-۲: ...» the very same characters put ۱ on the right. One
    source, two opposite readings.

    Putting a RIGHT-TO-LEFT MARK on each side of the hyphen isolates every
    group as its own number, so they are laid out right to left like the
    surrounding Persian. The chapter number then sits on the right in headings,
    captions, cross references and equation numbers alike. The mark is
    invisible and is the standard way to pin bidirectional text.
    """
    return ("‏-‏").join(n.split("-"))


_HEAD_NUM = re.compile(r"^([۰-۹]+(?:-[۰-۹]+)*)-")


def _renum(t):
    """reverse the leading section number of a heading, leave the title alone"""
    m = _HEAD_NUM.match(t)
    return t if not m else disp_num(m.group(1)) + "-" + t[m.end():]


def h_ch(t, drop=True):
    """عنوان فصل: «با فونت ۱۸ زر سیاه در یک صفحه جدید و با فاصله ۱۱cm از بالای
    صفحه» (ص ۱۶). مقدمه فصل نیست — در آیین‌نامه بالای صفحه می‌نشیند — پس با
    drop=False صدا زده می‌شود."""
    p = doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)
    q = para(t, 18, True, align=WD_ALIGN_PARAGRAPH.CENTER,
             sb=226 if drop else 0, sa=18)
    _outline(q, 0); return q


def h1(t):
    """main heading; keepNext stops Word leaving it alone at the foot of a page"""
    p = para(_renum(t), 16, True, sb=14, sa=6); _outline(p, 1); _keep_with_next(p); return p


def h2(t):
    p = para(_renum(t), 14, True, sb=10, sa=4); _outline(p, 2); _keep_with_next(p); return p


MATH_NS = ('xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
           'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"')


def _mr(t, sty="i"):
    """OMML run; sty 'i' = italic variable, 'p' = upright text/operator"""
    return (f'<m:r><m:rPr><m:sty m:val="{sty}"/></m:rPr>'
            f'<m:t xml:space="preserve">{t}</m:t></m:r>')


def _mfrac(n, d):
    return f'<m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num>{n}</m:num><m:den>{d}</m:den></m:f>'


def _msub(b, sb):
    return f'<m:sSub><m:e>{b}</m:e><m:sub>{sb}</m:sub></m:sSub>'


def _mnary(ch, sub, sup, e, loc="subSup"):
    return (f'<m:nary><m:naryPr><m:chr m:val="{ch}"/><m:limLoc m:val="{loc}"/>'
            f'<m:subHide m:val="0"/><m:supHide m:val="0"/></m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{e}</m:e></m:nary>')


def _bx(tag):
    return _msub(_mr("B"), _mr(tag, "p"))


EQ = {
    "۱-۱": _mr("IoU", "p") + _mr(" = ", "p") + _mfrac(
        _mr("area", "p") + _mr("(", "p") + _bx("pred") + _mr(" \u2229 ", "p") + _bx("gt") + _mr(")", "p"),
        _mr("area", "p") + _mr("(", "p") + _bx("pred") + _mr(" \u222a ", "p") + _bx("gt") + _mr(")", "p")),
    "۱-۲": _mr("Precision", "p") + _mr(" = ", "p") + _mfrac(_mr("TP", "p"), _mr("TP + FP", "p")),
    "۱-۳": _mr("Recall", "p") + _mr(" = ", "p") + _mfrac(_mr("TP", "p"), _mr("TP + FN", "p")),
    "۱-۴": _msub(_mr("F", "p"), _mr("1", "p")) + _mr(" = 2 \u00d7 ", "p") + _mfrac(
        _mr("Precision \u00d7 Recall", "p"), _mr("Precision + Recall", "p")),
    "۱-۵": _mr("AP", "p") + _mr(" = ", "p") + _mnary(
        "\u222b", _mr("0", "p"), _mr("1", "p"),
        _mr("p") + _mr("(", "p") + _mr("r") + _mr(")", "p") + _mr(" d", "p") + _mr("r")),
    "۱-۶": _mr("mAP", "p") + _mr(" = ", "p") + _mfrac(_mr("1", "p"), _mr("N")) + _mnary(
        "\u2211", _mr("i") + _mr(" = 1", "p"), _mr("N"),
        _msub(_mr("AP", "p"), _mr("i")), loc="undOvr"),
}


def formula(latin, num, omml=None):
    """numbered equation as a real Word (OMML) object.
    `omml` lets a chapter supply its own markup (built with mr/mfrac/msub/mnary);
    when omitted the equation is looked up in EQ.
    Laid out in a borderless 2-cell RTL table so the number sits at the right
    margin (as the guide requires) and the equation stays centred."""
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t._tbl.tblPr.append(OxmlElement("w:bidiVisual"))       # cell 0 -> right side
    t.columns[0].width = Cm(2.0); t.columns[1].width = Cm(13.5)
    c_num, c_eq = t.rows[0].cells
    c_num.width = Cm(2.0); c_eq.width = Cm(13.5)

    pn = c_num.paragraphs[0]; _bidi(pn); pn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pn.add_run(f"({disp_num(num)})"); r.font.size = Pt(BODY); _rs(r, BODY, False, True)

    pe = c_eq.paragraphs[0]; pe.alignment = WD_ALIGN_PARAGRAPH.CENTER
    xml = omml if omml is not None else EQ[num]
    pe._p.append(parse_xml(f'<m:oMath {MATH_NS}>{xml}</m:oMath>'))

    para("", sa=4)
    return t


def fig_ph(num, caption, note=None, width=15.5):
    """insert the generated figure inside a closed frame, caption BELOW it"""
    _disp = disp_num(num)          # file name stays on the logical number
    fname = "fig_" + num.translate(FA2EN).replace("-", "_") + ".png"
    # read at call time so one process can build several chapters in a row
    path = os.path.join(os.environ.get("THESIS_FIGDIR", FIGDIR), fname)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2)
    if os.path.exists(path):
        p.add_run().add_picture(path, width=Cm(width))
    else:
        r = p.add_run(f"[ فایل شکل یافت نشد: {fname} ]")
        r.font.size = Pt(BODY); r.bold = True; r.font.color.rgb = RED
        _rs(r, BODY, True, True)
    pPr = p._p.get_or_add_pPr(); bd = OxmlElement("w:pBdr")
    for side in ("top", "bottom", "left", "right"):
        e = OxmlElement("w:" + side)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "6"); e.set(qn("w:color"), "808080"); bd.append(e)
    pPr.append(bd)
    _keep_with_next(p)
    cap = para(f"شکل {_disp}: {caption}", 10, True, align=WD_ALIGN_PARAGRAPH.CENTER,
               sb=2, sa=10, font=CAPTION_FONT)
    cap.style = _caption_style(CAP_FIG)


def _shade(cell, fill="D9D9D9"):
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(sh)


def _keep_with_next(p):
    """stop Word from stranding a caption at the foot of a page"""
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepNext"))
    return p


def table(num, caption, headers, rows, widths=None, row_header=True):
    """caption above the table (آیین‌نامه). The last column is the row label, so
    it is shaded and bold like the header unless row_header is turned off.
    Caption and every row carry keepNext, so the table never splits from its
    caption or across a page break."""
    _disp = disp_num(num)
    cap = para(f"جدول {_disp}: {caption}", 10, True, align=WD_ALIGN_PARAGRAPH.CENTER,
               sb=10, sa=2, font=CAPTION_FONT)
    cap.style = _caption_style(CAP_TBL)
    _keep_with_next(cap)

    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; p = c.paragraphs[0]; _bidi(p)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _emit(p, str(h), 10, bold=True)
        _shade(c)

    label_col = len(headers) - 1        # RTL: the rightmost column is the row label
    for row in rows:
        cs = t.add_row().cells
        for i, v in enumerate(row):
            p = cs[i].paragraphs[0]; _bidi(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            is_label = row_header and i == label_col
            _emit(p, str(v), 10, bold=is_label)
            if is_label:
                _shade(cs[i], "F2F2F2")

    for r_ in t.rows:                   # keep the whole table together
        trPr = r_._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        for cell in r_.cells:
            for pp in cell.paragraphs:
                _keep_with_next(pp)
    para("", sa=8)


# ---------------------------------------------------------------- footnotes
# python-docx has no footnote API; build the footnotes part directly so that
# Latin terms can sit in real Word footnotes (آیین‌نامه: no Latin words in body text).
from docx.opc.part import Part
from docx.opc.packuri import PackURI

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
FN_CT = ("application/vnd.openxmlformats-officedocument"
         ".wordprocessingml.footnotes+xml")
FN_RT = ("http://schemas.openxmlformats.org/officeDocument"
         "/2006/relationships/footnotes")

_fn_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    f'<w:footnotes xmlns:w="{W}">'
    '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="16"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="16"/></w:rPr><w:t>______________________________________________</w:t></w:r></w:p></w:footnote>'
    '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="16"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="16"/></w:rPr><w:t>______________________________________________</w:t></w:r></w:p></w:footnote>'
    '</w:footnotes>')

from lxml import etree
_fn_root = etree.fromstring(_fn_xml.encode("utf-8"))
_fn_counter = [0]


def _fn_add(text):
    """append a footnote body, return its id"""
    _fn_counter[0] += 1
    fid = _fn_counter[0]
    fn = etree.SubElement(_fn_root, qn("w:footnote"))
    fn.set(qn("w:id"), str(fid))
    p = etree.SubElement(fn, qn("w:p"))
    pPr = etree.SubElement(p, qn("w:pPr"))
    ps = etree.SubElement(pPr, qn("w:pStyle")); ps.set(qn("w:val"), "FootnoteText")
    jc = etree.SubElement(pPr, qn("w:jc")); jc.set(qn("w:val"), "left")   # Latin-only note
    r1 = etree.SubElement(p, qn("w:r"))
    rPr1 = etree.SubElement(r1, qn("w:rPr"))
    rs = etree.SubElement(rPr1, qn("w:rStyle")); rs.set(qn("w:val"), "FootnoteReference")
    etree.SubElement(r1, qn("w:footnoteRef"))
    r2 = etree.SubElement(p, qn("w:r"))
    rPr2 = etree.SubElement(r2, qn("w:rPr"))
    rf = etree.SubElement(rPr2, qn("w:rFonts"))
    rf.set(qn("w:ascii"), LAT); rf.set(qn("w:hAnsi"), LAT)
    sz = etree.SubElement(rPr2, qn("w:sz")); sz.set(qn("w:val"), "20")
    t = etree.SubElement(r2, qn("w:t")); t.set(qn("xml:space"), "preserve")
    t.text = " " + text
    return fid


def fn_ref(par, fid):
    """insert the superscript reference mark into a paragraph"""
    r = par.add_run()
    rPr = r._element.get_or_add_rPr()
    rs = OxmlElement("w:rStyle"); rs.set(qn("w:val"), "FootnoteReference"); rPr.append(rs)
    ref = OxmlElement("w:footnoteReference"); ref.set(qn("w:id"), str(fid))
    r._element.append(ref)


def term(par, fa, latin):
    """Persian term in the body + its Latin equivalent as a real footnote."""
    r = par.add_run(fa); r.font.size = Pt(BODY); _rs(r, BODY, False, True)
    fn_ref(par, _fn_add(latin))


def ptext(par, t, rtl=True, size=BODY, bold=False):
    if rtl:
        _emit(par, t, size, bold)             # لاتینِ داخل متن، دو واحد کوچک‌تر
        return par.runs[-1] if par.runs else None
    r = par.add_run(t); r.font.size = Pt(lat_size(size)); r.bold = bold
    _rs(r, lat_size(size), bold, False); return r


def newp(ind=0.8, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sa=2):
    p = doc.add_paragraph(); _bidi(p); p.alignment = align
    pf = p.paragraph_format; pf.line_spacing = 1.5
    pf.space_after = Pt(sa); pf.first_line_indent = Cm(ind)
    return p


def finalize_footnotes():
    """attach the footnotes part + restart numbering on every page"""
    fpr = OxmlElement("w:footnotePr")
    nr = OxmlElement("w:numRestart"); nr.set(qn("w:val"), "eachPage")
    fpr.append(nr)
    sec._sectPr.insert(0, fpr)
    blob = etree.tostring(_fn_root, xml_declaration=True,
                          encoding="UTF-8", standalone=True)
    part = Part(PackURI("/word/footnotes.xml"), FN_CT, blob, doc.part.package)
    doc.part.relate_to(part, FN_RT)


# ================================================================ CONTENT

def add_footnote_styles():
    """the default python-docx template lacks these two styles; Word needs them
    so the reference mark is superscript and the footnote text is 10pt."""
    styles = doc.styles.element
    fr = etree.SubElement(styles, qn("w:style"))
    fr.set(qn("w:type"), "character"); fr.set(qn("w:styleId"), "FootnoteReference")
    n = etree.SubElement(fr, qn("w:name")); n.set(qn("w:val"), "footnote reference")
    rPr = etree.SubElement(fr, qn("w:rPr"))
    va = etree.SubElement(rPr, qn("w:vertAlign")); va.set(qn("w:val"), "superscript")

    ft = etree.SubElement(styles, qn("w:style"))
    ft.set(qn("w:type"), "paragraph"); ft.set(qn("w:styleId"), "FootnoteText")
    n2 = etree.SubElement(ft, qn("w:name")); n2.set(qn("w:val"), "footnote text")
    pPr = etree.SubElement(ft, qn("w:pPr"))
    sp2 = etree.SubElement(pPr, qn("w:spacing"))
    sp2.set(qn("w:after"), "0"); sp2.set(qn("w:line"), "240"); sp2.set(qn("w:lineRule"), "auto")
    rPr2 = etree.SubElement(ft, qn("w:rPr"))
    sz = etree.SubElement(rPr2, qn("w:sz")); sz.set(qn("w:val"), "20")
    szcs = etree.SubElement(rPr2, qn("w:szCs")); szcs.set(qn("w:val"), "20")



def finish():
    """write the document: footnote styles + footnotes part + save"""
    add_footnote_styles()
    finalize_footnotes()
    doc.save(OUT)
    print("saved |", len(doc.paragraphs), "paragraphs |", _fn_counter[0], "footnotes")


# public names for the OMML builders, so each chapter can define its own equations
mr, mfrac, msub, mnary = _mr, _mfrac, _msub, _mnary
