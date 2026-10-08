import json, re, zipfile
from lxml import etree

DOC = r"C:\Users\amir2\Desktop\cat-claude\thesis_working.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

with zipfile.ZipFile(DOC) as z:
    document = etree.fromstring(z.read("word/document.xml"))
    footnotes = etree.fromstring(z.read("word/footnotes.xml"))

def ptext(p):
    out = []
    for node in p.iter():
        if node.tag == W + "t":
            out.append(node.text or "")
        elif node.tag == W + "tab":
            out.append("\t")
        elif node.tag == W + "footnoteReference":
            out.append(f"<FN:{node.get(W+'id')}>")
    return "".join(out).strip()

def fmt_run(r):
    rp = r.find(W + "rPr")
    if rp is None:
        return {"text": "".join(r.itertext())}
    fonts = rp.find(W + "rFonts")
    size = rp.find(W + "sz")
    size_cs = rp.find(W + "szCs")
    return {
        "text": "".join(r.itertext()),
        "ascii": fonts.get(W + "ascii") if fonts is not None else None,
        "cs": fonts.get(W + "cs") if fonts is not None else None,
        "size": size.get(W + "val") if size is not None else None,
        "size_cs": size_cs.get(W + "val") if size_cs is not None else None,
        "italic": rp.find(W + "i") is not None or rp.find(W + "iCs") is not None,
        "rtl": rp.find(W + "rtl") is not None,
    }

body_paras = document.findall(".//" + W + "body/" + W + "p")

started = False
bib = []
for p in body_paras:
    t = ptext(p)
    if t in ("مراجع و منابع", "منابع و مراجع"):
        started = True
        continue
    if not started or not t:
        continue
    if re.match(r"^\[[۰-۹0-9]+\]", t) or t.startswith("http"):
        pp = p.find(W + "pPr")
        jc = pp.find(W + "jc") if pp is not None else None
        bib.append({
            "text": t,
            "align": jc.get(W + "val") if jc is not None else None,
            "runs": [fmt_run(r) for r in p.findall(W + "r") if "".join(r.itertext())],
        })

fn_text = {}
for fn in footnotes.findall(W + "footnote"):
    fid = fn.get(W + "id")
    if fid and int(fid) > 0:
        fn_text[fid] = " | ".join(ptext(p) for p in fn.findall(".//" + W + "p") if ptext(p))

contexts = []
for i, p in enumerate(body_paras):
    t = ptext(p)
    if "<FN:" in t:
        ids = re.findall(r"<FN:(\d+)>", t)
        contexts.append({"p": i, "text": t, "footnotes": {fid: fn_text.get(fid, "") for fid in ids}})

targets = []
needles = [
    "خودروهای خودران و سامانه‌های کمک‌راننده",
    "اهمیت این موضوع دو وجه دارد",
    "به‌روزترین نسخه پایدار",
    "وزن‌های از پیش آموزش‌دیده",
    "هش ادراکی",
    "رویکردهای نیمه‌نظارتی",
    "افزایش داده مجموعه‌ای",
    "توقف زودهنگام",
    "نبود آن، سلامت فرایند آموزش",
    "در بازه‌ای قرار دارد که برای مجموعه‌های هم‌تراز",
]
for i, p in enumerate(body_paras):
    t = ptext(p)
    if any(n in t for n in needles):
        targets.append({"p": i, "text": t})

print(json.dumps({"bib": bib, "footnote_contexts": contexts, "targets": targets}, ensure_ascii=False, indent=2))
