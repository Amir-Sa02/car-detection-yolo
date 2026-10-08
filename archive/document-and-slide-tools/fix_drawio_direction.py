from copy import deepcopy
from pathlib import Path
from lxml import etree
import os
import shutil
import tempfile


BASE = Path(r"C:\Users\amir2\Desktop\نسخه ارسالی\مدارک تکمیلی و منابع شکل‌ها\شکل‌های قابل ویرایش")
FILES = (
    ("شکل_۱-۱_بازسازی_قابل_ویرایش.drawio", ("a", "b", "c", "d", "e", "f", "g", "h", "i")),
    ("شکل_۲-۱_بازسازی_قابل_ویرایش.drawio", ("a", "b", "c", "d", "e", "f")),
)
BACKUP = BASE / "پشتیبان_پیش_از_اصلاح_جهت"
BACKUP.mkdir(exist_ok=True)

for filename, expected_ids in FILES:
    path = BASE / filename
    backup = BACKUP / filename
    assert path.is_file() and not backup.exists()
    tree = etree.parse(str(path))
    cells = tree.xpath("//mxCell[@vertex='1']")
    assert tuple(c.get("id") for c in cells) == expected_ids
    geometries = [c.find("mxGeometry") for c in cells]
    assert all(g is not None and g.get("x") and g.get("width") for g in geometries)
    right_edge = max(float(g.get("x")) + float(g.get("width")) for g in geometries)
    for g in geometries:
        new_x = right_edge - float(g.get("x")) - float(g.get("width"))
        g.set("x", f"{new_x:g}")
    shutil.copy2(path, backup)
    fd, temp_name = tempfile.mkstemp(suffix=".drawio", dir=BASE)
    os.close(fd)
    try:
        tree.write(temp_name, encoding="utf-8", xml_declaration=True)
        etree.parse(temp_name)
        os.replace(temp_name, path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise
    print(filename, "mirrored across", right_edge)
