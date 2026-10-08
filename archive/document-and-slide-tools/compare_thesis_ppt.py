import re
import zipfile
from pathlib import Path

from lxml import etree


THESIS = Path(r"D:\projects\car-detection-yolo\thesis\پایان‌نامه_نهایی.docx")
DECK = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\ارائه_دفاع.pptx")
OUT = Path(r"C:\Users\amir2\Desktop\cat-claude\comparison_extract.txt")

W = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
A = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def natural_key(name):
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]


lines = []
with zipfile.ZipFile(THESIS) as archive:
    root = etree.fromstring(archive.read("word/document.xml"))
    paragraphs = [
        "".join(paragraph.xpath(".//w:t/text()", namespaces=W)).strip()
        for paragraph in root.xpath(".//w:body//w:p", namespaces=W)
    ]
    paragraphs = [text for text in paragraphs if text]
    lines.append("===== THESIS =====")
    for index, text in enumerate(paragraphs):
        lines.append(f"T{index:04d}\t{text}")

with zipfile.ZipFile(DECK) as archive:
    slide_names = sorted(
        [name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
        key=natural_key,
    )
    lines.append("\n===== SLIDES =====")
    for number, name in enumerate(slide_names, start=1):
        root = etree.fromstring(archive.read(name))
        texts = [text.strip() for text in root.xpath(".//a:t/text()", namespaces=A) if text.strip()]
        lines.append(f"\n--- SLIDE {number} ---")
        lines.extend(texts)

    note_names = sorted(
        [name for name in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)],
        key=natural_key,
    )
    lines.append("\n===== NOTES =====")
    for number, name in enumerate(note_names, start=1):
        root = etree.fromstring(archive.read(name))
        texts = [text.strip() for text in root.xpath(".//a:t/text()", namespaces=A) if text.strip()]
        if texts:
            lines.append(f"\n--- NOTE {number} ---")
            lines.extend(texts)

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"thesis_paragraphs={len(paragraphs)} slides={len(slide_names)} notes={len(note_names)}")
print(OUT)
