from zipfile import ZipFile
from pathlib import Path
import hashlib

docx = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\مطالعات قبل از ارائه\اسناد اصلی\پایان‌نامه_نهایی.docx")
figdir = Path(r"D:\projects\car-detection-yolo\thesis\فصل3_نتایج\شکل‌ها")
def sha(b): return hashlib.sha256(b).hexdigest()
with ZipFile(docx) as z:
    media = {Path(n).name: sha(z.read(n)) for n in z.namelist() if n.startswith('word/media/')}
for p in sorted(figdir.glob('fig_3_*.png')):
    h=sha(p.read_bytes())
    matches=[n for n,v in media.items() if v==h]
    print(p.name, 'EXACT_MATCH', matches or '-')
