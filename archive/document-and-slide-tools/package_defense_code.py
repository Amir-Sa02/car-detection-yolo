"""Copy priority reading files and reviewer evidence without changing originals."""

from hashlib import sha256
from pathlib import Path
import shutil


ROOT = Path(r"C:\Users\amir2\Desktop\نسخه ارسالی")
COLAB = Path(r"D:\projects\car-detection-yolo\colab")
STUDY_SRC = Path(r"D:\projects\car-detection-yolo\thesis\ارائه\مطالعات قبل از ارائه\کدها")
SUPP = next(ROOT.glob("مدارک*")) / "کدهای قابل بررسی"
STUDY = ROOT / "01_کدهای مطالعه به ترتیب"
REVIEW = ROOT / "02_کدهای مستندات داور"


def copy_checked(source: Path, destination: Path):
    assert source.is_file(), f"Missing: {source}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        assert sha256(destination.read_bytes()).digest() == sha256(source.read_bytes()).digest(), destination
    else:
        shutil.copy2(source, destination)
    assert sha256(destination.read_bytes()).digest() == sha256(source.read_bytes()).digest()


study_items = [
    ("01__IADD_YOLOv11_Colab_run8.ipynb", COLAB / "IADD_YOLOv11_Colab_run8.ipynb"),
    ("02__build_subset_v5.py", COLAB / "build_subset_v5.py"),
    ("03__IADD_YOLOv11_Colab_pervideo.ipynb", COLAB / "IADD_YOLOv11_Colab_pervideo.ipynb"),
    ("04__make_label_evidence.py", SUPP / "make_label_evidence.py"),
    ("05__audit_duplicate_pairs.py", SUPP / "audit_duplicate_pairs.py"),
    ("06__compute_v5_validity.py", SUPP / "compute_v5_validity.py"),
    ("07__recount_final_subset.py", SUPP / "recount_final_subset.py"),
    ("08__make_figures_ch2.py", SUPP / "make_figures_ch2.py"),
    ("09__make_figures_ch3.py", SUPP / "make_figures_ch3.py"),
    ("10__export_eval_curves.py", SUPP / "export_eval_curves.py"),
    ("11__demo_boxes_simple.py", STUDY_SRC / "demo_boxes_simple.py"),
    ("12a__render_plain_gt.py", SUPP / "render_plain_gt.py"),
    ("12b__render_plain_boxes.py", SUPP / "render_plain_boxes.py"),
]

review_items = [
    ("01_اجرای_نهایی", COLAB / "IADD_YOLOv11_Colab_run8.ipynb"),
    ("02_ساخت_و_بازبینی_داده", COLAB / "build_subset_v5.py"),
    ("02_ساخت_و_بازبینی_داده", COLAB / "build_subset_v4.py"),
    ("02_ساخت_و_بازبینی_داده", COLAB / "IADD_YOLOv11_Colab_pervideo.ipynb"),
    ("02_ساخت_و_بازبینی_داده", SUPP / "audit_duplicate_pairs.py"),
    ("02_ساخت_و_بازبینی_داده", SUPP / "make_label_evidence.py"),
    ("02_ساخت_و_بازبینی_داده", SUPP / "draw_original_labels.py"),
    ("02_ساخت_و_بازبینی_داده", SUPP / "compute_v5_validity.py"),
    ("02_ساخت_و_بازبینی_داده", SUPP / "recount_final_subset.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "figstyle.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "make_figures_ch1.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "make_figures_ch2.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "make_figures_ch3.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "export_eval_curves.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "figures.ipynb"),
    ("03_آمار_و_شکل‌ها", SUPP / "render_plain_gt.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "render_plain_boxes.py"),
    ("03_آمار_و_شکل‌ها", SUPP / "make_demo_gt_pred.py"),
    ("04_نمونه_آموزشی", STUDY_SRC / "demo_boxes_simple.py"),
]

assert not STUDY.exists() and not REVIEW.exists(), "Target folders already exist; inspect before retrying"
for name, source in study_items:
    copy_checked(source, STUDY / name)
for section, source in review_items:
    copy_checked(source, REVIEW / section / source.name)

study_readme = """ترتیب مطالعه از 01 تا 12 است. شماره 12 دو فایل مکمل دارد: یکی کادر برچسب واقعی و دیگری کادر خروجی مدل. هر فایل، کپی مستقل است؛ فایل اصلی تغییر نکرده است.

01 تا 07: هسته پروژه و شواهد داده. 08 تا 10: منشأ نمودارها و منحنی‌ها. 11 و 12: کادرهای نمایشی.
فایل 11 نسخهٔ آموزشیِ کوتاه‌شده و تازه‌ساخته‌شده است؛ تولیدکنندهٔ تاریخیِ تصاویر پایان‌نامه نیست. برای اجرای دوبارهٔ آن به دادهٔ test و وزن best.pt در مسیرهای داخل کد نیاز است.
"""
(STUDY / "راهنما.txt").write_text(study_readme, encoding="utf-8")

review_readme = """فهرست کدهای پشتیبان پروژه برای بررسی داور

01: دفترچهٔ واقعی ران ۸. مرجع تنظیمات، آموزش، ادامهٔ آموزش و ارزیابی همین فایل و خروجی‌های ثبت‌شدهٔ آن است.
02: ساخت زیرمجموعهٔ v5 و شواهد بازبینی داده. v4 فقط برای نشان‌دادن مسیر رسیدن به v5 آمده است. audit_duplicate_pairs.py یک بررسی بازتولیدپذیرِ پشتیبان است و گزارش ثبت‌شدهٔ کشف اولیهٔ موارد تکراری نیست.
03: محاسبه و ترسیم آمار و شکل‌ها. figstyle.py وابستگیِ کدهای شکل است. figures.ipynb یک دفترچهٔ تولید برخی خروجی‌های تحلیلی است؛ آن را با دفترچهٔ آموزش اصلی اشتباه نگیرید.
04: demo_boxes_simple.py نسخهٔ آموزشیِ تازه‌ساخته‌شده برای نشان‌دادن خواندن برچسب واقعی و خروجی مدل روی یک تصویر است؛ تولیدکنندهٔ تاریخیِ شکل‌های پایان‌نامه نیست.

این پوشه کدها را مستند می‌کند. برای اجرای دوبارهٔ همهٔ فایل‌ها، مجموعه‌داده، وزن مدل و نتایج ثبت‌شده نیز لازم است و برخی مسیرهای داخل کد به ساختار اصلی D:\\projects\\car-detection-yolo اشاره می‌کنند. اجرای build_subset_v5.py مجموعه‌دادهٔ خروجی می‌نویسد؛ پیش از اجرا مسیر OUT را بررسی کنید. کپی‌ها در این بسته بدون تغییر محتوای کد انجام شده‌اند.
"""
(REVIEW / "راهنما.txt").write_text(review_readme, encoding="utf-8")

manifest = []
for path in sorted(REVIEW.rglob("*")):
    if path.is_file() and path.name != "SHA256.txt":
        manifest.append(f"{sha256(path.read_bytes()).hexdigest()}  {path.relative_to(REVIEW)}")
(REVIEW / "SHA256.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")

assert len([p for p in STUDY.iterdir() if p.suffix in (".py", ".ipynb")]) == 13
assert len([p for p in REVIEW.rglob("*") if p.suffix in (".py", ".ipynb")]) == 19
print("Study files: 13, numbered priorities: 01-12")
print("Reviewer code files: 19")
