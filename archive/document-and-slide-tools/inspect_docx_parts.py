import re
import zipfile

from lxml import etree


PATH = r"D:\projects\car-detection-yolo\thesis\پایان.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

with zipfile.ZipFile(PATH) as archive:
    for name in archive.namelist():
        if not name.endswith(".xml"):
            continue
        data = archive.read(name)
        if re.search(rb"\[[0-9\xdb\xdc\xdd\xde\xdf]", data):
            print("POSSIBLE", name)

    root = etree.fromstring(archive.read("word/document.xml"))
    whole = "\n".join("".join(p.xpath(".//w:t/text()", namespaces=NS)) for p in root.xpath(".//w:body//w:p", namespaces=NS))
    by_node = "\n".join(root.xpath(".//w:t/text()", namespaces=NS))
    pattern = r"\[([0-9۰-۹,\-،–—\s]+)\]"
    print("citation matches paragraph/tnode", len(re.findall(pattern, whole)), len(re.findall(pattern, by_node)))
    paragraphs = root.xpath(".//w:body//w:p", namespaces=NS)
    for idx in (196, 206, 207, 209, 211, 213):
        if idx < len(paragraphs):
            print("PARA", idx, [repr(t) for t in paragraphs[idx].xpath(".//w:t/text()", namespaces=NS) if "[" in t or "]" in t])
    for index in range(660, 679):
        paragraph = paragraphs[index]
        texts = paragraph.xpath(".//w:t/text()", namespaces=NS)
        style = paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
        align = paragraph.xpath("./w:pPr/w:jc/@w:val", namespaces=NS)
        bidi = paragraph.xpath("./w:pPr/w:bidi/@w:val", namespaces=NS)
        hyperlinks = paragraph.xpath(".//w:hyperlink/@r:id", namespaces={**NS, "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"})
        print(index, "style", style, "align", align, "bidi", bidi, "hyperlinks", hyperlinks, "texts", texts)
