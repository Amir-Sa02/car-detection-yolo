from docx import Document
import re

PATH = r"C:\Users\amir2\Desktop\cat-claude\thesis_refs_audit.docx"
doc = Document(PATH)
pat = re.compile(r"\[([۰-۹0-9]+(?:\s*[،,]\s*[۰-۹0-9]+)*)\]")
for i,p in enumerate(doc.paragraphs):
    t=p.text.strip()
    if pat.search(t):
        print(f"\nP{i}: {t}")
