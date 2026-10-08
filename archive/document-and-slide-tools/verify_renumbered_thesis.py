import hashlib
import re
import zipfile

from lxml import etree


SOURCE = r"D:\projects\car-detection-yolo\thesis\پایان.docx"
OUTPUT = r"C:\Users\amir2\Desktop\cat-claude\پایان.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FA_TO_EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
PATTERN = re.compile(r"\[([0-9۰-۹،,\s]+)\]")


with zipfile.ZipFile(SOURCE) as before, zipfile.ZipFile(OUTPUT) as after:
    changed = [
        name
        for name in before.namelist()
        if hashlib.sha256(before.read(name)).digest() != hashlib.sha256(after.read(name)).digest()
    ]
    assert changed == ["word/document.xml"], changed
    root = etree.fromstring(after.read("word/document.xml"))

paragraphs = root.xpath(".//w:body//w:p", namespaces=NS)
texts = ["".join(p.xpath(".//w:t/text()", namespaces=NS)) for p in paragraphs]
heading_index = texts.index("مراجع و منابع")
body_start = max(index for index, text in enumerate(texts[:heading_index]) if text.strip() == "مقدمه")

order = []
first_citations = []
for text in texts[body_start:heading_index]:
    for match in PATTERN.finditer(text):
        for number in re.findall(r"[0-9۰-۹]+", match.group(1)):
            value = int(number.translate(FA_TO_EN))
            if value not in order:
                order.append(value)
            if len(first_citations) < 12:
                first_citations.append((value, text[:180]))

reference_numbers = []
for text in texts[heading_index + 1 :]:
    match = re.match(r"^\[([۰-۹]+)\]", text.strip())
    if match:
        reference_numbers.append(int(match.group(1).translate(FA_TO_EN)))

print("debug_order=" + repr(order))
print("debug_first_citations=" + repr(first_citations))
for text in texts[body_start:body_start + 10]:
    if PATTERN.search(text):
        print("debug_paragraph=" + repr(text))
assert order == list(range(1, 18)), order
assert reference_numbers == list(range(1, 18)), reference_numbers
assert texts[heading_index + 1].startswith("[۱] Khosravian")
assert texts[heading_index + 2].strip() == "https://github.com/ahv1373/IADD"
assert sum("https://github.com/ahv1373/IADD" in text for text in texts) == 1
assert sum("https://docs.ultralytics.com" in text for text in texts) == 1

print("changed_parts=word/document.xml")
print("first_use_order=" + ",".join(map(str, order)))
print("first_citations=" + repr(first_citations))
print("references=" + ",".join(map(str, reference_numbers)))
print("iadd_reference=" + texts[heading_index + 1])
print("iadd_url=" + texts[heading_index + 2].strip())
