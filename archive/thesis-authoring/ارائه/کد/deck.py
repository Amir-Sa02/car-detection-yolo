# -*- coding: utf-8 -*-
"""Defence slides — built for a projector and a room five metres deep.

Rules the design follows:
  * white ground on content slides, a light tint only on section dividers
  * nothing below 18 pt, headings always larger than the body
  * light fills behind text, dark ink on top, never dark fills under prose
  * short bullets instead of paragraphs
  * Persian in B Zar; Latin uses Times New Roman one point smaller, which
    also keeps symbols out of the Persian font where they would show as boxes
  * page number bottom left
"""
import os
import re

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.normpath(os.path.join(HERE, "..", "ارائه_دفاع.pptx"))
F1 = os.path.join(ROOT, "فصل1_پیشینه", "شکل‌ها")
F2 = os.path.join(ROOT, "فصل2_روش_و_داده", "شکل‌ها")
F3 = os.path.join(ROOT, "فصل3_نتایج", "شکل‌ها")
FS = os.path.normpath(os.path.join(HERE, "..", "شکل‌ها"))
LOGO = os.path.join(FS, "cover_image2.png")

FA = "B Zar"
EN = "Times New Roman"
FA_LETTER = re.compile(r"[؀-ۿ]")
ASCII_ALNUM = re.compile(r"[A-Za-z0-9]")
# PowerPoint eats the space between a Latin token and the Persian word after
# it; a right-to-left mark placed just after the token brings the space back.
RLM = "\u200f"
LATIN_THEN_FA = re.compile(r"([A-Za-z0-9][A-Za-z0-9@._:+/%-]*)(\s+)(?=[؀-ۿ])")

INK = RGBColor(0x19, 0x21, 0x28)
NAVY = RGBColor(0x19, 0x43, 0x5B)
SLATE = RGBColor(0x50, 0x5B, 0x63)
BLUE = RGBColor(0x4A, 0x70, 0x84)
GREEN = RGBColor(0x9D, 0x48, 0x5A)
AMBER = RGBColor(0x75, 0x5D, 0x67)
CRIMSON = RGBColor(0x9D, 0x48, 0x5A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

TINT_BLUE = RGBColor(0xD8, 0xE0, 0xE5)
TINT_GREEN = RGBColor(0xE6, 0xD2, 0xD7)
TINT_AMBER = RGBColor(0xE2, 0xDB, 0xDE)
TINT_RED = RGBColor(0xE6, 0xD2, 0xD7)
TINT_GREY = RGBColor(0xDF, 0xE2, 0xE4)

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.62)
CW = W - 2 * MARGIN                      # content width
TOP = Inches(1.42)                       # first line under the title
NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
SLIDES = []


def fa_num(n):
    return str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


# --------------------------------------------------------------------- text
SEP = re.compile(r"([٫٬]+)")
LATIN_TOKEN = re.compile(r"([A-Za-z][A-Za-z0-9@._:+/%-]*)")
SEP_FONT = EN                # B Zar has no glyph for ٫ or ٬; the thesis
                             # falls back to Times New Roman, so match it here


def _run(p, text, size, bold, colour):
    """Put Latin tokens in separate Times New Roman runs, one point smaller."""
    chunks = []
    for sep_part in (part for part in SEP.split(text) if part):
        chunks.extend(part for part in LATIN_TOKEN.split(sep_part) if part)
    last = None
    for chunk in chunks:
        last = _one(p, chunk, size, bold, colour)
    return last


def _one(p, text, size, bold, colour):
    r = p.add_run()
    r.text = LATIN_THEN_FA.sub(lambda m: m.group(1) + RLM + m.group(2), text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = colour
    rPr = r._r.get_or_add_rPr()
    # en-US stops PowerPoint redrawing Latin digits as Persian ones, but it also
    # stops brackets from mirroring. A run with no ASCII has no digit to protect,
    # so it is tagged Persian and gets correct bidi instead.
    rPr.set("lang", "en-US" if ASCII_ALNUM.search(text) else "fa-IR")
    sep = bool(SEP.fullmatch(text))
    for tag, face in (("cs", SEP_FONT if sep else FA),
                      ("ea", SEP_FONT if sep else FA),
                      ("latin", SEP_FONT if sep else EN)):
        el = rPr.find(A + tag)
        if el is None:
            el = etree.SubElement(rPr, A + tag)
        el.set("typeface", face)
    # Latin words use Times New Roman one point smaller than nearby Persian.
    if ASCII_ALNUM.search(text) and not FA_LETTER.search(text):
        r.font.size = Pt(max(1, size - 1))
    return r


def line(tf, text, size=22, bold=False, colour=INK, first=False,
         align=PP_ALIGN.RIGHT, after=10, dot=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if FA_LETTER.search(text) or dot:
        p._pPr.set("rtl", "1")
    p.space_after = Pt(after)
    if dot:
        _run(p, dot + "  ", size, True, colour if colour is not INK else BLUE)
    _run(p, text, size, bold, colour)
    return p


def box(sl, x, y, w, h, fill=None, line_col=None):
    sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sh.adjustments[0] = 0.08
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line_col is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_col; sh.line.width = Pt(1.25)
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.16)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    return sh


def tile(sl, x, y, w, h, head, body, tint, ink, hs=24, bs=19):
    sh = box(sl, x, y, w, h, tint)
    line(sh.text_frame, head, hs, True, ink, first=True,
         align=PP_ALIGN.CENTER, after=4)
    if body:
        line(sh.text_frame, body, bs, False, SLATE, align=PP_ALIGN.CENTER, after=0)
    return sh


def textbox(sl, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = sl.shapes.add_textbox(x, y, w, h)
    tb.text_frame.word_wrap = True
    tb.text_frame.vertical_anchor = anchor
    return tb, tb.text_frame


# ------------------------------------------------------------------- chrome
def slide(title=None, bg=None, size=31):
    """A content slide.

    The title carries the slide's claim rather than its topic: the audience
    should be able to follow the argument by reading titles alone. The logo sits
    top left on every slide, which also balances a layout that would otherwise
    be heavy on the right.
    """
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    if bg is not None:
        r = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
        r.fill.solid(); r.fill.fore_color.rgb = bg
        r.line.fill.background(); r.shadow.inherit = False
    if title:
        sl.shapes.add_picture(LOGO, MARGIN, Inches(0.32), height=Inches(0.80))
        mark = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, W - MARGIN - Inches(0.18),
                                   Inches(0.36), Inches(0.18), Inches(0.72))
        mark.fill.solid(); mark.fill.fore_color.rgb = BLUE
        mark.line.fill.background(); mark.shadow.inherit = False
        tb, tf = textbox(sl, MARGIN + Inches(1.0), Inches(0.30),
                         CW - Inches(1.42), Inches(0.86), MSO_ANCHOR.MIDDLE)
        line(tf, title, size, True, NAVY, first=True, after=0)
    return sl


def footer(sl, i, n):
    tb, tf = textbox(sl, MARGIN, Inches(6.92), Inches(3.2), Inches(0.4))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p._pPr.set("rtl", "1")
    _run(p, "صفحه  %s  از  %s"
         % (fa_num(i), fa_num(n)), 15, False, SLATE)


def picture(sl, path, top, height=None, width=None, left=None):
    pic = sl.shapes.add_picture(path, Inches(0), top, width=width, height=height)
    pic.left = int((W - pic.width) / 2) if left is None else left
    return pic


def table(sl, rows, x, y, w, h, hs=21, bs=20, hcols=(0,)):
    """hcols counts from the right edge, so column zero is the label column."""
    frame = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    frame.adjustments[0] = 0.06
    frame.fill.solid(); frame.fill.fore_color.rgb = WHITE
    frame.line.color.rgb = NAVY; frame.line.width = Pt(1.5)
    frame.shadow.inherit = False
    pad = Inches(0.025)
    shp = sl.shapes.add_table(len(rows), len(rows[0]), x + pad, y + pad,
                              w - 2 * pad, h - 2 * pad)
    tbl = shp.table
    # Persian tables read right to left: column zero must sit on the right edge
    ncols = len(rows[0])
    visual_rows = [list(reversed(row)) for row in rows]
    for ri, row in enumerate(visual_rows):
        for ci, val in enumerate(row):
            source_ci = ncols - 1 - ci
            cell = tbl.cell(ri, ci)
            cell.margin_top = cell.margin_bottom = Inches(0.06)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            head = ri == 0 or source_ci in hcols
            cell.fill.fore_color.rgb = (NAVY if ri == 0 else
                                        (CRIMSON if source_ci in hcols else
                                         (WHITE if ri % 2 else TINT_GREY)))
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            if FA_LETTER.search(str(val)):
                p._pPr.set("rtl", "1")
            _run(p, str(val), hs if ri == 0 else bs, head,
                 WHITE if head else INK)
    return shp


# --------------------------------------------------------------- animation
CLICK = """<p:par xmlns:p="{ns}"><p:cTn id="{a}" fill="hold">
 <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>
 <p:par><p:cTn id="{b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
 <p:par><p:cTn id="{c}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold"
   grpId="0" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
 <p:set><p:cBhvr><p:cTn id="{d}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
   <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
   <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>
   <p:to><p:strVal val="visible"/></p:to></p:set>
 <p:animEffect transition="in" filter="fade"><p:cBhvr>
   <p:cTn id="{e}" dur="400"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
 </p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>
 </p:childTnLst></p:cTn></p:par>"""

TIMING = """<p:timing xmlns:p="{ns}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite"
 restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek">
 <p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{clicks}</p:childTnLst></p:cTn>
 <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
 <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
 </p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"""


def animate(sl, shapes):
    clicks, nid = [], 10
    for sh in shapes:
        clicks.append(CLICK.format(ns=NS, a=nid, b=nid + 1, c=nid + 2,
                                   d=nid + 3, e=nid + 4, spid=sh.shape_id))
        nid += 10
    sl._element.append(etree.fromstring(TIMING.format(ns=NS, clicks="".join(clicks))))
