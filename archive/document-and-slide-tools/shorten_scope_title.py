from pathlib import Path

p = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\کد\content_a.py")
text = p.read_text(encoding="utf-8")
old = 'sl = slide("تفاوت رده‌های مصوب و رده‌های نهایی")'
new = 'sl = slide("رده‌های مصوب و نهایی")'
if text.count(old) != 1:
    raise RuntimeError("scope title was not found exactly once")
p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
