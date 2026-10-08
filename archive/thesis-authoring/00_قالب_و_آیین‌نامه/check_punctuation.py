# -*- coding: utf-8 -*-
"""بازرس نشانه‌گذاری فارسی برای متن پایان‌نامه.

قواعدی که بررسی می‌شوند، از دستور خط فارسی و راهنماهای نشانه‌گذاری گرفته شده‌اند:

  * نشانه‌های ، ؛ : . ؟ ! به کلمه پیش از خود می‌چسبند و پس از آنها یک فاصله است.
  * درون گیومه و پرانتز فاصله نیست؛ بیرون آنها یک فاصله است.
  * پس از «و» و «یا» و پس از «را» ویرگول نمی‌آید.
  * نشانه‌های لاتین , ; ? " در متن فارسی جایی ندارند؛ معادل فارسی‌شان ، ؛ ؟ «» است.
  * «ها»ی جمع، «تر/ترین»، پیشوند «می/نمی» و «ای» نکره با نیم‌فاصله می‌چسبند.
  * فاصله دوتایی و فاصله پیش از پایان جمله خطاست.

فقط رشته‌های متنی فارسیِ داخل کد بررسی می‌شوند، نه خود کد؛ برای همین فایل‌ها با
ast خوانده می‌شوند و تنها گره‌های رشته‌ای که حرف فارسی دارند وارسی می‌گردند.
"""
import ast
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
FA = re.compile(r"[ء-يژپچگیک]")
ZWNJ = "‌"

FILES = [
    ("مقدمه", "مقدمه/کد/build_introduction.py"),
    ("فصل ۱", "فصل1_پیشینه/کد/build_chapter1.py"),
    ("فصل ۲", "فصل2_روش_و_داده/کد/build_chapter2.py"),
    ("فصل ۳", "فصل3_نتایج/کد/build_chapter3.py"),
    ("فصل ۴", "فصل4_بحث_و_نتیجه‌گیری/کد/build_chapter4.py"),
    ("صفحات فرعی", "00_صفحات_فرعی/کد/build_front_matter.py"),
]

# (نام قاعده، الگو، توضیح)
RULES = [
    ("فاصله پیش از نشانه",       r"[ ‌]+[،؛:؟!]", "نشانه به کلمه پیش از خود می‌چسبد"),
    ("نبود فاصله پس از نشانه",   r"[،؛](?=[^\s»\)\]…])", "پس از ، و ؛ باید یک فاصله باشد"),
    ("ویرگول پس از «و»",         r"\bو،", "پس از حرف ربط «و» ویرگول نمی‌آید"),
    ("ویرگول پس از «یا»",        r"\bیا،", "پس از «یا» ویرگول نمی‌آید"),
    ("ویرگول پس از «را»",        r"\bرا،", "پس از «را» ویرگول نمی‌آید"),
    ("نشانه لاتین در متن فارسی", r"[,;?](?![0-9])", "به‌جای , ; ? باید ، ؛ ؟ نوشت"),
    ("گیومه لاتین",              r'"', "به‌جای \" باید « » نوشت"),
    ("فاصله داخل گیومه",         r"«[ ‌]|[ ‌]»", "درون گیومه فاصله نیست"),
    ("فاصله داخل پرانتز",        r"\([ ‌]|[ ‌]\)", "درون پرانتز فاصله نیست"),
    ("فاصله دوتایی",             r"  +", "دو فاصله پشت سر هم"),
    ("«ها»ی جمع با فاصله",       r"[ء-يیکگپچژ] ها[یی]?\b",
                                 "«ها»ی جمع با نیم‌فاصله می‌چسبد"),
    ("«تر/ترین» با فاصله",       r"[ء-يیکگپچژ] (?:تر|ترین)\b",
                                 "«تر» و «ترین» با نیم‌فاصله می‌چسبند"),
    ("پیشوند «می» با فاصله",     r"\b(?:می|نمی) [ء-يیکگپچژ]",
                                 "«می» و «نمی» با نیم‌فاصله به فعل می‌چسبند"),
    ("«ای» نکره با فاصله",       r"[ء-يیکگپچژ] ای\b",
                                 "«ای» نکره با نیم‌فاصله می‌چسبد"),
    ("نقطه پیش از پرانتز بسته",  r"\.\)", "نقطه پس از پرانتز می‌آید، نه پیش از آن"),
]


TEXT_CALLS = {"body", "ptext", "para", "h_ch", "h1", "h2", "fig_ph", "term", "table"}


def strings_of(path):
    """فقط رشته‌هایی که واقعاً به متن پایان‌نامه می‌روند.

    داکیومنت فایل‌ها، دستور فیلدهای Word و نام مسیرها متن پایان‌نامه نیستند و
    نباید بازرسی شوند؛ پس به‌جای پیمودن همه گره‌های رشته‌ای، تنها آرگومان‌های
    توابعی خوانده می‌شوند که خروجی‌شان روی کاغذ می‌نشیند."""
    src = io.open(path, encoding="utf-8").read()
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
        if name not in TEXT_CALLS:
            continue
        for arg in node.args:
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    if FA.search(sub.value):
                        yield sub.lineno, sub.value


def main():
    total = 0
    for label, rel in FILES:
        path = os.path.join(ROOT, *rel.split("/"))
        if not os.path.exists(path):
            continue
        hits = []
        for lineno, text in strings_of(path):
            for name, pat, why in RULES:
                for m in re.finditer(pat, text):
                    a, b = max(0, m.start() - 26), min(len(text), m.end() + 26)
                    frag = text[a:b].replace(ZWNJ, "␣").replace("\n", " ")
                    hits.append((lineno, name, frag, why))
        if hits:
            print(f"\n### {label}  ({len(hits)} مورد)")
            for lineno, name, frag, why in hits:
                print(f"  خط {lineno:>4}  [{name}]")
                print(f"        …{frag}…")
        total += len(hits)
    print(f"\nمجموع: {total} مورد")
    return total


if __name__ == "__main__":
    main()
