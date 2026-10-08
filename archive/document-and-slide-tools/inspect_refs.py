from docx import Document
import re, json

PATH = r"C:\Users\amir2\Desktop\cat-claude\thesis_refs_audit.docx"
doc = Document(PATH)
pars = [p.text.strip() for p in doc.paragraphs]

for i, t in enumerate(pars):
    if t in {"منابع و مراجع", "مراجع", "منابع"} or "منابع و مراجع" in t:
        print("REF_HEADING", i, repr(t))

print("TAIL")
for i, t in list(enumerate(pars))[-80:]:
    if t:
        print(i, repr(t[:400]))

pat = re.compile(r"[\[\[]([۰-۹0-9]+(?:\s*[،,،-]\s*[۰-۹0-9]+)*)[\]\]]")
seen=[]
occ=[]
for i,t in enumerate(pars):
    for m in pat.finditer(t):
        nums=[]
        for x in re.findall(r"[۰-۹0-9]+",m.group(1)):
            nums.append(int(x.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹","0123456789"))))
        occ.append((i,m.group(0),nums,t[:220]))
        for n in nums:
            if n not in seen: seen.append(n)
print("FIRST_ORDER",seen)
print("COUNTS")
from collections import Counter
c=Counter(n for _,_,ns,_ in occ for n in ns)
print(dict(sorted(c.items())))
print("FIRST_OCC")
for n in seen:
    row=next(x for x in occ if n in x[2])
    print(n,row)
