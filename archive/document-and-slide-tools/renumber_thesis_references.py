import copy
import os
import re
import zipfile

from lxml import etree


SOURCE = r"D:\projects\car-detection-yolo\thesis\پایان.docx"
OUTPUT = r"C:\Users\amir2\Desktop\cat-claude\پایان.docx"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FA_TO_EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
EN_TO_FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

# Renumbered according to first appearance in the thesis body.
ORDER = [4, 16, 12, 11, 14, 8, 3, 13, 15, 1, 2, 6, 17, 9, 10, 5, 7]
NUMBER_MAP = {old: new for new, old in enumerate(ORDER, 1)}
CITATION_RE = re.compile(r"\[([0-9۰-۹،,\s]+)\]")
REFERENCE_RE = re.compile(r"^\[([۰-۹]+)\]")


def paragraph_text(paragraph):
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def remap_citation(match):
    raw_numbers = re.findall(r"[0-9۰-۹]+", match.group(1))
    mapped = sorted({NUMBER_MAP[int(value.translate(FA_TO_EN))] for value in raw_numbers})
    return "[" + "، ".join(str(value).translate(EN_TO_FA) for value in mapped) + "]"


def remap_paragraph_citations(paragraph):
    text_nodes = paragraph.xpath(".//w:t", namespaces=NS)
    parts = [node.text or "" for node in text_nodes]
    combined = "".join(parts)
    matches = list(CITATION_RE.finditer(combined))
    if not matches:
        return 0

    for match in reversed(matches):
        starts = []
        cursor = 0
        for part in parts:
            starts.append(cursor)
            cursor += len(part)
        start, end = match.span()
        first = max(index for index, position in enumerate(starts) if position <= start)
        last = max(index for index, position in enumerate(starts) if position < end)
        first_offset = start - starts[first]
        last_offset = end - starts[last]
        replacement = remap_citation(match)
        if first == last:
            parts[first] = parts[first][:first_offset] + replacement + parts[first][last_offset:]
        else:
            suffix = parts[last][last_offset:]
            parts[first] = parts[first][:first_offset] + replacement
            for index in range(first + 1, last):
                parts[index] = ""
            parts[last] = suffix

    for node, value in zip(text_nodes, parts):
        node.text = value
    return len(matches)


with zipfile.ZipFile(SOURCE, "r") as source_archive:
    entries = {name: source_archive.read(name) for name in source_archive.namelist()}

root = etree.fromstring(entries["word/document.xml"])
body = root.find(f".//{W}body")
body_paragraphs = body.xpath("./w:p", namespaces=NS)
all_paragraphs = body.xpath(".//w:p", namespaces=NS)

heading = [p for p in all_paragraphs if paragraph_text(p).strip() == "مراجع و منابع"][-1]
heading_pos = list(body).index(heading)
heading_all_pos = max(
    index for index, paragraph in enumerate(all_paragraphs)
    if paragraph_text(paragraph).strip() == "مراجع و منابع"
)

# Update every in-text citation before the reference list, including captions and front lists.
changed_citations = 0
for paragraph in all_paragraphs[:heading_all_pos]:
    changed_citations += remap_paragraph_citations(paragraph)

# Capture the existing reference entries and URL paragraph before rearranging them.
references = {}
docs_url = None
for paragraph in body_paragraphs:
    text = paragraph_text(paragraph).strip()
    match = REFERENCE_RE.match(text)
    if match:
        references[int(match.group(1).translate(FA_TO_EN))] = paragraph
    elif text.startswith("https://docs.ultralytics.com"):
        docs_url = paragraph

if set(references) != set(range(1, 18)):
    raise RuntimeError(f"Expected references 1..17, found {sorted(references)}")
if docs_url is None:
    raise RuntimeError("The existing Ultralytics URL paragraph was not found")

# Use the established URL-line formatting for the IADD repository address.
dataset_url = copy.deepcopy(docs_url)
dataset_text_nodes = dataset_url.xpath(".//w:t", namespaces=NS)
dataset_text_nodes[0].text = "     https://github.com/ahv1373/IADD"
for node in dataset_text_nodes[1:]:
    node.text = ""

# Remove only the 17 entries and the existing documentation URL.
for element in [*references.values(), docs_url]:
    body.remove(element)

# Reinsert entries in citation order and update only their bracketed reference number.
insert_at = list(body).index(heading) + 1
for new_number, old_number in enumerate(ORDER, 1):
    paragraph = references[old_number]
    first_text = paragraph.xpath(".//w:t", namespaces=NS)[1]
    first_text.text = str(new_number).translate(EN_TO_FA)
    body.insert(insert_at, paragraph)
    insert_at += 1
    if old_number == 4:
        body.insert(insert_at, dataset_url)
        insert_at += 1
    if old_number == 17:
        body.insert(insert_at, docs_url)
        insert_at += 1

entries["word/document.xml"] = etree.tostring(
    root, xml_declaration=True, encoding="UTF-8", standalone="yes"
)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with zipfile.ZipFile(OUTPUT, "w") as output_archive:
    with zipfile.ZipFile(SOURCE, "r") as source_archive:
        for item in source_archive.infolist():
            output_archive.writestr(item, entries[item.filename])

print(OUTPUT)
print(f"heading_pos={heading_pos} heading_all_pos={heading_all_pos} changed_citations={changed_citations}")
