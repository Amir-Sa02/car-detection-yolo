from pathlib import Path
import fitz
from PIL import Image, ImageDraw

pdf = Path(r"C:\Users\amir2\Desktop\cat-claude\speaker_notes_render.pdf")
out = Path(r"C:\Users\amir2\Desktop\cat-claude\speaker_notes_pages")
out.mkdir(exist_ok=True)
doc = fitz.open(pdf)
thumbs = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25), alpha=False)
    path = out / f"page-{i+1:02d}.png"
    pix.save(path)
    im = Image.open(path).convert("RGB")
    im.thumbnail((420, 595))
    thumbs.append((i+1, im.copy()))

for start in range(0, len(thumbs), 4):
    group = thumbs[start:start+4]
    sheet = Image.new("RGB", (900, 1280), "#d7dde2")
    draw = ImageDraw.Draw(sheet)
    for k, (num, im) in enumerate(group):
        x = 20 + (k % 2) * 440
        y = 35 + (k // 2) * 620
        sheet.paste(im, (x, y))
        draw.text((x, 10 + (k // 2) * 620), f"Page {num}", fill="#111111")
    sheet.save(out / f"contact-{start+1:02d}-{start+len(group):02d}.png")
print(f"pages={len(doc)}")
