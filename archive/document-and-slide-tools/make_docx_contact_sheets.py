from pathlib import Path

from PIL import Image, ImageOps, ImageDraw


ROOT = Path(r"C:\Users\amir2\Desktop\cat-claude\qa_thesis_refs")
pages = sorted(ROOT.glob("page-*.png"), key=lambda path: int(path.stem.split("-")[-1]))
out_dir = ROOT / "sheets"
out_dir.mkdir(exist_ok=True)

for start in range(0, len(pages), 4):
    group = pages[start : start + 4]
    loaded = [Image.open(path).convert("RGB") for path in group]
    width = max(image.width for image in loaded)
    height = max(image.height for image in loaded)
    sheet = Image.new("RGB", (width * 2 + 30, height * 2 + 60), "#d6d6d6")
    draw = ImageDraw.Draw(sheet)
    for offset, image in enumerate(loaded):
        row, col = divmod(offset, 2)
        x = col * (width + 30)
        y = row * (height + 30)
        sheet.paste(image, (x, y))
        page_number = start + offset + 1
        draw.rectangle((x, y, x + 52, y + 24), fill="white", outline="black")
        draw.text((x + 4, y + 4), f"p{page_number}", fill="black")
    sheet.save(out_dir / f"sheet-{start // 4 + 1:02d}.png")

print(len(pages), len(list(out_dir.glob("sheet-*.png"))))
