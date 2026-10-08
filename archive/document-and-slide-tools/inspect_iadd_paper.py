from pathlib import Path
from pypdf import PdfReader

pdf = Path(r"D:\projects\car-detection-yolo\thesis\مراجع\IET Image Processing - 2022 - Khosravian - Multi‐domain autonomous driving dataset  Towards enhancing the generalization of.pdf")
doc = PdfReader(str(pdf))
for page_no, page in enumerate(doc.pages, 1):
    text = " ".join((page.extract_text() or "").split())
    if any(key in text for key in ("97,528", "97528", "171 videos", "eight cities", "8 cities")):
        print(f"PAGE {page_no}: {text}")
