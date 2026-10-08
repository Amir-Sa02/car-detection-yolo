from zipfile import ZipFile
from lxml import etree
from pathlib import Path
import sys, re, shutil

sys.stdout.reconfigure(encoding="utf-8")
docx = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\مطالعات قبل از ارائه\اسناد اصلی\پایان‌نامه_نهایی.docx")
out = Path(r"C:\Users\amir2\Desktop\cat-claude\figure_1_3")
out.mkdir(exist_ok=True)
ns = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
with ZipFile(docx) as z:
    root = etree.fromstring(z.read("word/document.xml"))
    relroot = etree.fromstring(z.read("word/_rels/document.xml.rels"))
    rels = {x.get("Id"): x.get("Target") for x in relroot}
    body = root.find("w:body", ns)
    elems = list(body)
    for i, elem in enumerate(elems):
        if etree.QName(elem).localname != "p":
            continue
        text = "".join(elem.xpath(".//w:t/text()", namespaces=ns)).strip()
        if "شکل" in text and ("۱" in text or "1" in text) and ("۳" in text or "3" in text):
            print("candidate", i, text)
            for j in range(max(0, i-4), i+1):
                p = elems[j]
                blips = p.xpath(".//a:blip/@r:embed", namespaces=ns)
                if blips:
                    rid = blips[-1]
                    target = rels[rid]
                    member = "word/" + target.replace("../", "")
                    data = z.read(member)
                    dest = out / Path(target).name
                    dest.write_bytes(data)
                    print("extracted", j, rid, target, dest)
