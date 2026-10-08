from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path
from lxml import etree

DOCX = Path(r"C:\Users\amir2\Desktop\cat-claude\map_explanation_working.docx")
MAP = Path(r"C:\Users\amir2\Desktop\cat-claude\footnote_pages_map_final.csv")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W, "r": R}
FA = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def text(el):
    return "".join(el.xpath(".//w:t/text()", namespaces=NS))


with zipfile.ZipFile(DOCX) as z:
    document = etree.fromstring(z.read("word/document.xml"))
    footnotes = etree.fromstring(z.read("word/footnotes.xml"))

# Internal hyperlink targets in all three generated lists and in citations.
all_links = document.xpath(".//w:hyperlink", namespaces=NS)
anchors = [h.get(f"{{{W}}}anchor") for h in all_links if h.get(f"{{{W}}}anchor")]
toc_anchors = [a for a in anchors if a.startswith("_Toc") or a.startswith("_Ref")]
ref_anchors = [a for a in anchors if a.startswith("_ref_")]

# Read each manually displayed Persian footnote number and its run formatting.
footnote_data = {}
font_issues = []
for fn in footnotes.xpath("./w:footnote", namespaces=NS):
    fid = fn.get(f"{{{W}}}id")
    if not fid or int(fid) <= 0:
        continue
    body = text(fn).strip()
    m = re.match(r"([۰-۹]+)", body)
    shown = int(m.group(1).translate(FA)) if m else None
    footnote_data[int(fid)] = (shown, body[:80])
    if m:
        first_t = fn.xpath(".//w:t[starts-with(., $n)]", namespaces=NS, n=m.group(1))
        if first_t:
            run = first_t[0].getparent()
            fonts = run.find("w:rPr/w:rFonts", NS)
            size = run.find("w:rPr/w:sz", NS)
            cs = fonts.get(f"{{{W}}}cs") if fonts is not None else None
            val = size.get(f"{{{W}}}val") if size is not None else None
            if cs != "B Zar" or val != "20":
                font_issues.append((fid, cs, val))

map_rows = []
if MAP.exists():
    with MAP.open(encoding="utf-8-sig", newline="") as f:
        map_rows = list(csv.DictReader(f))

number_mismatches = []
if map_rows:
    # Discover column names because the export may use localized headings.
    keys = list(map_rows[0])
    id_key = next((k for k in keys if "id" in k.lower()), keys[0])
    expected_key = next((k for k in keys if "expected" in k.lower()), keys[-1])
    for row in map_rows:
        try:
            fid = int(row[id_key])
            expected = int(row[expected_key])
        except (ValueError, TypeError):
            continue
        shown = footnote_data.get(fid, (None, ""))[0]
        if shown != expected:
            number_mismatches.append((fid, shown, expected))

print(f"INTERNAL_LINKS={len(anchors)}")
print(f"TOC_LINKS={len(toc_anchors)}")
print(f"REFERENCE_LINKS={len(ref_anchors)}")
print(f"FOOTNOTES_XML={len(footnote_data)}")
print(f"FOOTNOTE_MAP_ROWS={len(map_rows)}")
print(f"FOOTNOTE_NUMBER_MISMATCHES={len(number_mismatches)}")
print(f"FOOTNOTE_NUMBER_DETAILS={number_mismatches[:8]}")
print(f"FOOTNOTE_FONT_ISSUES={len(font_issues)}")
print(f"FOOTNOTE_FONT_DETAILS={font_issues[:8]}")

