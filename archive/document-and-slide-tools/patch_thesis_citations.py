import copy, re, sys, zipfile
from pathlib import Path
from lxml import etree

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XML = "{http://www.w3.org/XML/1998/namespace}"
DIGIT_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
CITE = re.compile(r"\[\s*([۰-۹٠-٩0-9]+(?:\s*[,،؛;]\s*[۰-۹٠-٩0-9]+)*)\s*\]")
NUM = re.compile(r"[۰-۹٠-٩0-9]+")

def text_of(el):
    return "".join(el.itertext())

def as_int(s):
    return int(s.translate(DIGIT_MAP))

def set_run_text(run, value):
    ts = run.findall(W + "t")
    if len(ts) != 1:
        raise RuntimeError("Unexpected run structure while splitting citation")
    t = ts[0]
    t.text = value
    if value.startswith(" ") or value.endswith(" "):
        t.set(XML + "space", "preserve")
    elif XML + "space" in t.attrib:
        del t.attrib[XML + "space"]

def split_run_with_links(run, intervals):
    # intervals: (start, end, reference_number), non-overlapping, local to run text
    parent = run.getparent()
    idx = parent.index(run)
    original = run.find(W + "t").text or ""
    cursor = 0
    pieces = []
    for start, end, ref_no in sorted(intervals):
        if start > cursor:
            plain = copy.deepcopy(run)
            set_run_text(plain, original[cursor:start])
            pieces.append(plain)
        linked_run = copy.deepcopy(run)
        set_run_text(linked_run, original[start:end])
        link = etree.Element(W + "hyperlink")
        link.set(W + "anchor", f"_ref_{ref_no}")
        link.set(W + "history", "1")
        link.append(linked_run)
        pieces.append(link)
        cursor = end
    if cursor < len(original):
        plain = copy.deepcopy(run)
        set_run_text(plain, original[cursor:])
        pieces.append(plain)
    parent.remove(run)
    for off, piece in enumerate(pieces):
        parent.insert(idx + off, piece)

with zipfile.ZipFile(SRC, "r") as zin:
    infos = zin.infolist()
    blobs = {i.filename: zin.read(i.filename) for i in infos}

root = etree.fromstring(blobs["word/document.xml"])
paras = list(root.iter(W + "p"))
bib_heading = next(p for p in paras if text_of(p).strip() in {"مراجع و منابع", "منابع و مراجع"})
body = root.find(".//" + W + "body")
all_paras = list(root.iter(W + "p"))
bib_pos = all_paras.index(bib_heading)

# Fix the wrong SPPF citation: SGDR does not support an architecture claim.
for p in all_paras[:bib_pos]:
    if "این بلوک در YOLOv8 نیز وجود دارد" in text_of(p):
        changed = False
        for t in p.iter(W + "t"):
            if t.text and "[17]" in t.text:
                t.text = t.text.replace("[17]", "[۸، ۹]")
                changed = True
        if not changed:
            raise RuntimeError("Could not locate [17] in SPPF paragraph")
        break
else:
    raise RuntimeError("Could not locate SPPF paragraph")

# Locate bibliography entries, remove unused old ref 19, and renumber old 20 to 19.
all_paras = list(root.iter(W + "p"))
bib_pos = all_paras.index(bib_heading)
entries = {}
for p in all_paras[bib_pos + 1:]:
    m = re.match(r"\s*\[([۰-۹٠-٩0-9]+)\]", text_of(p))
    if m:
        entries[as_int(m.group(1))] = p
if sorted(entries) != list(range(1, 21)):
    raise RuntimeError(f"Unexpected bibliography numbers: {sorted(entries)}")
unused = entries[19]
unused.getparent().remove(unused)
for t in entries[20].iter(W + "t"):
    if t.text and ("[۲۰]" in t.text or t.text == "۲۰"):
        t.text = t.text.replace("[۲۰]", "[۱۹]", 1) if "[۲۰]" in t.text else "۱۹"
        break
else:
    raise RuntimeError("Could not renumber bibliography entry 20")

# Renumber the sole in-text use of old ref 20.
all_paras = list(root.iter(W + "p"))
bib_pos = all_paras.index(bib_heading)
for p in all_paras[:bib_pos]:
    full = text_of(p)
    if "[۲۰]" in full:
        for t in p.iter(W + "t"):
            if t.text and "۲۰" in t.text:
                t.text = t.text.replace("۲۰", "۱۹")

# Add one bookmark around each final bibliography entry.
existing_ids = [int(x) for x in root.xpath("//w:bookmarkStart/@w:id", namespaces={"w": W[1:-1]}) if str(x).isdigit()]
next_id = max(existing_ids, default=0) + 1
all_paras = list(root.iter(W + "p"))
bib_pos = all_paras.index(bib_heading)
final_entries = {}
for p in all_paras[bib_pos + 1:]:
    m = re.match(r"\s*\[([۰-۹٠-٩0-9]+)\]", text_of(p))
    if m:
        final_entries[as_int(m.group(1))] = p
if sorted(final_entries) != list(range(1, 20)):
    raise RuntimeError(f"Unexpected final bibliography numbers: {sorted(final_entries)}")
for n, p in final_entries.items():
    start = etree.Element(W + "bookmarkStart")
    start.set(W + "id", str(next_id))
    start.set(W + "name", f"_ref_{n}")
    end = etree.Element(W + "bookmarkEnd")
    end.set(W + "id", str(next_id))
    next_id += 1
    insert_at = 1 if len(p) and p[0].tag == W + "pPr" else 0
    p.insert(insert_at, start)
    p.append(end)

# Hyperlink each numeric component of every in-text citation.
all_paras = list(root.iter(W + "p"))
bib_pos = all_paras.index(bib_heading)
link_count = 0
for p in all_paras[:bib_pos]:
    st = p.find("./" + W + "pPr/" + W + "pStyle")
    style = (st.get(W + "val") if st is not None else "").lower()
    if style.startswith("toc"):
        continue
    ts = list(p.iter(W + "t"))
    starts, pos = [], 0
    for t in ts:
        starts.append(pos)
        pos += len(t.text or "")
    full = "".join(t.text or "" for t in ts)
    by_run = {}
    for cm in CITE.finditer(full):
        for nm in NUM.finditer(cm.group(0)):
            a = cm.start() + nm.start()
            b = cm.start() + nm.end()
            ref_no = as_int(nm.group(0))
            if ref_no not in final_entries:
                raise RuntimeError(f"Citation targets missing ref {ref_no}: {full}")
            found = False
            for start, t in zip(starts, ts):
                val = t.text or ""
                if start <= a and b <= start + len(val):
                    run = t.getparent()
                    if run.tag != W + "r" or len(run.findall(W + "t")) != 1:
                        raise RuntimeError("Unsupported citation run")
                    by_run.setdefault(run, []).append((a - start, b - start, ref_no))
                    found = True
                    link_count += 1
                    break
            if not found:
                raise RuntimeError(f"Citation token crosses text nodes: {nm.group(0)}")
    for run, intervals in list(by_run.items()):
        split_run_with_links(run, intervals)

blobs["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
with zipfile.ZipFile(OUT, "w") as zout:
    for info in infos:
        if info.filename == "word/document.xml":
            zout.writestr(info, blobs[info.filename])
        else:
            zout.writestr(info, blobs[info.filename])
print(f"wrote={OUT}")
print(f"hyperlinked_numbers={link_count}")


