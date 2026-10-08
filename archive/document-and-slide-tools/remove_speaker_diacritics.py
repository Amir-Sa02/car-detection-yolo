from collections import Counter
from datetime import datetime
from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import os
import re

from lxml import etree


DOC = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\documents\متن_ارائه_دفاع_۲۵_تا_۳۰_دقیقه.docx')
BACKUPS = DOC.parent / 'پشتیبان‌ها'
MARKS = re.compile(r'[\u064b-\u065f\u0670\u06d6-\u06ed]')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def main():
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = BACKUPS / f'{DOC.stem}_قبل_حذف_اعراب_{stamp}.docx'
    copy2(DOC, backup)
    counts = Counter()

    with NamedTemporaryFile(prefix='speaker_clean_', suffix='.docx', dir=DOC.parent, delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        with ZipFile(DOC, 'r') as source, ZipFile(temp_path, 'w') as target:
            for info in source.infolist():
                data = source.read(info.filename)
                if info.filename.startswith('word/') and info.filename.endswith('.xml'):
                    root = etree.fromstring(data)
                    changed = False
                    for node in root.iter():
                        if node.tag in {W + 't', W + 'instrText', W + 'delText'} and node.text:
                            cleaned, n = MARKS.subn('', node.text)
                            if n:
                                counts[info.filename] += n
                                node.text = cleaned
                                changed = True
                    if changed:
                        data = etree.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
                target.writestr(info, data)
        os.replace(temp_path, DOC)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    print('REMOVED', sum(counts.values()))
    print('PARTS', dict(counts))
    print('BACKUP', backup)
    print('OUTPUT', DOC)


if __name__ == '__main__':
    main()
