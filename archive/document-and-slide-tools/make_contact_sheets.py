from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src = Path(r"C:\Users\amir2\Desktop\cat-claude\rendered_defense")
out = Path(r"C:\Users\amir2\Desktop\cat-claude\defense_contact_sheets")
out.mkdir(exist_ok=True)

slides = sorted(src.glob("Slide*.PNG"), key=lambda p: int(p.stem[5:]))
font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 28)
for sheet_no, start in enumerate(range(0, len(slides), 6), 1):
    canvas = Image.new("RGB", (2400, 1520), "white")
    draw = ImageDraw.Draw(canvas)
    for slot, path in enumerate(slides[start:start + 6]):
        image = Image.open(path).convert("RGB")
        image.thumbnail((760, 430))
        col, row = slot % 3, slot // 3
        x, y = 20 + col * 795, 55 + row * 735
        canvas.paste(image, (x, y))
        draw.text((x, y - 38), path.stem, fill="black", font=font)
    canvas.save(out / f"sheet_{sheet_no}.png")
