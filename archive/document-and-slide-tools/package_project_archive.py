from pathlib import Path
import shutil, json, hashlib, zipfile, ast

REPO = Path(r'C:\Users\amir2\Desktop\car-detection-yolo')
SOURCE = Path(r'D:\projects\car-detection-yolo')
EXTRA = Path(r'C:\Users\amir2\Desktop\extra data')
WORK = Path(r'C:\Users\amir2\Desktop\cat-claude')
BACKUP = Path(r'C:\Users\amir2\Desktop\project-archive-backups\2026-10-08')
copied = []

def copy(src, dst):
    src, dst = Path(src), REPO / dst
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append({'source':str(src), 'destination':dst.relative_to(REPO).as_posix(),
                   'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})

# Preserve the user's edited sources before replacing the active entry points.
for p in (REPO/'code').glob('*'):
    if p.is_file(): copy(p, Path('archive/defense-edited-code')/p.name)

for p in (SOURCE/'colab').glob('*'):
    if p.suffix in ('.py','.ipynb','.txt','.md'):
        copy(p, Path('archive/colab-history')/p.name)
for p in (SOURCE/'colab/runs').rglob('*'):
    if p.is_file() and p.suffix not in ('.pt','.cache'):
        copy(p, Path('archive/experiment-results')/p.relative_to(SOURCE/'colab/runs'))

for p in (SOURCE/'thesis').rglob('*.py'):
    if not any(x in p.parts for x in ['پشتیبان‌ها','__pycache__']):
        copy(p, Path('archive/thesis-authoring')/p.relative_to(SOURCE/'thesis'))
for p in WORK.glob('*'):
    if p.suffix in ('.py','.ps1'):
        copy(p, Path('archive/document-and-slide-tools')/p.name)

for name in ['build_subset_v5.py','IADD_YOLOv11_Colab_run8.ipynb','IADD_YOLOv11_Colab_pervideo.ipynb']:
    copy(SOURCE/'colab'/name,Path('code')/name)
for name in ['make_figures_ch2.py','make_figures_ch3.py','render_plain_gt.py','render_plain_boxes.py','export_eval_curves.py']:
    copy(EXTRA/'ارسالی/codes'/name if name not in ['render_plain_gt.py','render_plain_boxes.py'] else SOURCE/'thesis/فصل3_نتایج/کد'/name,Path('code')/name)
copy(SOURCE/'thesis/00_قالب_و_آیین‌نامه/figstyle.py','code/figstyle.py')
copy(EXTRA/'01_کدهای مطالعه به ترتیب/05__audit_duplicate_pairs.py','code/audit_duplicate_pairs.py')
copy(EXTRA/'other codes/audit_duplicate_filenames.py','code/audit_duplicate_filenames.py')
copy(EXTRA/'other codes/make_label_evidence.py','code/make_label_evidence.py')
copy(EXTRA/'codes/demo_boxes.py','code/demo_boxes.py')
copy(SOURCE/'train_iadd_yolov11.py','archive/early-training/train_iadd_yolov11.py')
copy(SOURCE/'pervideo_run5.csv','record review/pervideo_run5.csv')
for p in (SOURCE/'docs/dataset').rglob('*'):
    if p.is_file() and p.suffix in ('.csv','.json'):
        copy(p,Path('record review/historical')/p.relative_to(SOURCE/'docs/dataset'))

for p in (EXTRA/'01_کدهای مطالعه به ترتیب').glob('*'):
    if p.suffix in ('.py','.ipynb'): copy(p,Path('archive/study-code')/p.name)
for p in (EXTRA/'مطالعه').rglob('*.docx'):
    if 'پشتیبان‌ها' not in p.parts: copy(p,Path('docs/study-guides')/p.relative_to(EXTRA/'مطالعه'))
copy(EXTRA/'documents/متن_ارائه_دفاع_۲۵_تا_۳۰_دقیقه.docx','docs/study-guides/defense-speaking-notes.docx')
copy(EXTRA/'documents/پایان‌نامه.docx','presentation and thesis/thesis.docx')
copy(REPO/'presentation and thesis/ارائه-دفاع.pptx','presentation and thesis/presentation.pptx')
for p in (EXTRA/'ارسالی/plots and pictures').glob('*.drawio'):
    copy(p,Path('figures/editable')/p.name)
copy(WORK/'model_verified.json','models/checkpoint-inspection-original.json')
for p in (EXTRA/'other codes/iadd_validity').glob('*'):
    if p.is_file():copy(p,Path('figure and table data/original-iadd')/p.name)

# Use repository-relative paths; the stored original sources above remain unmodified.
p=REPO/'code/build_subset_v5.py'
s=p.read_text(encoding='utf-8-sig')
start=s.index('SRC = '); end=s.index('MAX_SIDE,',start)
s=s[:start]+'''from pathlib import Path
from argparse import ArgumentParser

ROOT = Path(__file__).resolve().parents[1]
parser = ArgumentParser(description="Rebuild the IADD V5 subset (whole-video split).")
parser.add_argument("--source", default=str(ROOT / "dataset/IADD"))
parser.add_argument("--output", default=str(ROOT / "dataset/iadd_subset_v5"))
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--overwrite", action="store_true")
args = parser.parse_args()
SRC = args.source
OUT = args.output
if not Path(SRC).is_dir():
    raise SystemExit("IADD source folder is missing: " + SRC)
if Path(OUT).exists() and any(Path(OUT).iterdir()) and not args.dry_run and not args.overwrite:
    raise SystemExit("Output is not empty. Choose a new folder or explicitly use --overwrite.")
''' +s[end:]
s=s.replace('DRY_RUN = False', 'DRY_RUN = args.dry_run')
s=s.replace('# best val/test balance on object-size + class + weather','# fixed seed retained from the recorded V5 builder')
p.write_text(s,encoding='utf-8')

p=REPO/'code/compute_v5_validity.py'; s=p.read_text(encoding='utf-8-sig')
start=s.index('DS = '); end=s.index('os.makedirs',start)
s=s[:start]+'''from pathlib import Path
from argparse import ArgumentParser
ROOT = Path(__file__).resolve().parents[1]
parser = ArgumentParser(description="Count V5 labels and plot dataset distributions.")
parser.add_argument("--dataset", default=str(ROOT / "dataset/iadd_subset_v5"))
parser.add_argument("--output", default=str(ROOT / "outputs/dataset_validity"))
args = parser.parse_args()
DS, OUT = args.dataset, args.output
if not Path(DS).is_dir():
    raise SystemExit("Dataset folder is missing: " + DS)
''' + s[end:]
p.write_text(s,encoding='utf-8')

for name in ['make_figures_ch2.py','make_figures_ch3.py']:
    p=REPO/'code'/name;s=p.read_text(encoding='utf-8-sig')
    start=s.index('HERE = '); end=s.index('\nimport ',start)
    if name.endswith('ch2.py'):
        prefix='''HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "outputs", "chapter2")
STATS = os.path.join(ROOT, "figure and table data", "stats.json")
os.makedirs(OUT, exist_ok=True)
'''
        s=s.replace('fig_2_1(); fig_2_2(S);','fig_2_2(S);')
        s=s.replace('saved fig_2_1.png .. fig_2_4.png','saved fig_2_2.png .. fig_2_4.png (manual fig_2_1 is archived separately)')
        s=s.replace('متوسط\\n(٪۱ تا ٪۶)','متوسط\\n(۱٪ تا کمتر از ۶٪)').replace('بزرگ\\n(بیش از ٪۶)','بزرگ\\n(۶٪ و بیشتر)')
    else:
        prefix='''HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "outputs", "chapter3")
DATA_DIR = os.path.join(ROOT, "figure and table data")
RUN = os.path.join(ROOT, "runs", "run8", "run8")
LABELS = os.path.join(ROOT, "dataset", "iadd_subset_v5", "labels", "test")
os.makedirs(FIG, exist_ok=True)
'''
        s=s.replace('os.path.join(FIG, "eval_curves.npz")','os.path.join(DATA_DIR, "eval_curves.npz")')
        s=s.replace('os.path.join(FIG, "perclass_metrics.csv")','os.path.join(DATA_DIR, "perclass_metrics.csv")')
        s=s.replace('    fig_3_6(); fig_3_7()','    print("Qualitative figures are preserved in figures/; call their functions only after restoring the required source images.")')
    s=s[:start]+prefix+s[end:]
    p.write_text(s,encoding='utf-8')

# Correct the historical exporter typo and local paths; leave the archived copy intact.
p=REPO/'code/export_eval_curves.py';s=p.read_text(encoding='utf-8-sig')
start=s.index('HERE = ');end=s.index('\nlocal_yaml',start)
s=s[:start]+'''HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEIGHTS = os.path.join(ROOT, "models", "run8_best.pt")
DS = os.environ.get("IADD_V5", os.path.join(ROOT, "dataset", "iadd_subset_v5"))
OUT_DIR = os.path.join(ROOT, "outputs", "evaluation")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "eval_curves.npz")
''' +s[end:]
s=s.replace('verbose=True) ==','verbose=True)')
s=s.replace('    np.savez','    np.savez')
p.write_text(s,encoding='utf-8')

p=REPO/'code/demo_boxes.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace('ROOT = Path(r"D:\\projects\\car-detection-yolo")','ROOT = Path(__file__).resolve().parents[1]')
s=s.replace('ROOT / "colab/runs/run8/run8/weights/best.pt"','ROOT / "models/run8_best.pt"')
p.write_text(s,encoding='utf-8')

# Active notebook: historical execution settings retained, misleading success comment removed.
p=REPO/'code/IADD_YOLOv11_Colab_run8.ipynb'; nb=json.loads(p.read_text(encoding='utf-8'))
for c in nb['cells']:
    if c['cell_type']=='code':
        src=''.join(c['source'])
        src=src.replace('!pip install -q ultralytics','!pip install -q ultralytics==8.4.120')
        src=src.replace('# finish fine-tune: 10 low-LR epochs, mosaic+mixup OFF. Small but real gain (~+0.5 mAP50).',
                        '# Historical optional finish: SGD, mosaic/mixup off. Main won the recorded validation comparison.')
        c['source']=src.splitlines(keepends=True)
        c['outputs']=[];c['execution_count']=None
nb['cells'].insert(0,{'cell_type':'markdown','metadata':{},'source':['# Archived run8 workflow\n','Training checkpoint reports Ultralytics 8.4.120. The optional finish used SGD; main was selected.\n','The weighted fitness cell is a manual diagnostic, not authoritative evidence of the installed trainer\'s early-stopping implementation. See docs/EXPERIMENTS.md.\n']})
p.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')

# Original full checkpoints are kept privately; the public model will be inference-only.
with zipfile.ZipFile(BACKUP/'training-checkpoints-private.zip','w',zipfile.ZIP_DEFLATED) as z:
    for root in [SOURCE/'colab/runs', EXTRA/'results']:
        for p in root.rglob('*.pt'):
            z.write(p,('D-colab' if root==SOURCE/'colab/runs' else 'final-submission')+'/'+p.relative_to(root).as_posix())

(REPO/'docs').mkdir(exist_ok=True)
(REPO/'docs/archive-sources.json').write_text(json.dumps(copied,ensure_ascii=False,indent=2),encoding='utf-8')
print('Copied',len(copied),'files. Full checkpoints privately archived.',flush=True)
