"""Restore the recorded V5 image selection, without rerunning the split heuristic."""
from argparse import ArgumentParser
from pathlib import Path
import csv, hashlib, shutil, json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = ArgumentParser()
parser.add_argument('--source', type=Path, required=True, help='Extracted original IADD folder')
parser.add_argument('--output', type=Path, required=True, help='New output directory')
parser.add_argument('--limit', type=int, help='Restore a few entries for a quick check')
args = parser.parse_args()
if args.output.exists() and any(args.output.iterdir()):
    parser.error('Output must be absent or empty; existing files are never deleted.')
index = {}
for part in ['train_part1', 'train_part2', 'train_part3', 'val']:
    for image in (args.source / part).glob('Record*/*.jpg'):
        key = (image.parent.name, image.stem)
        index.setdefault(key, []).append(image)

report = []
with open(ROOT/'dataset manifests/v5-images.csv', newline='', encoding='utf-8') as f:
    for n, row in enumerate(csv.DictReader(f), 1):
        if args.limit and n > args.limit:
            break
        record, stem = row['record'], row['source_stem']
        candidates = list(index.get((record, stem), []))
        # Some source filenames were corrected after the original V5 build.
        if stem.startswith('Record'):
            pieces = stem.split('_', 2)
            if len(pieces) == 3:
                candidates += index.get((record, record + '_' + pieces[2]), [])
        source = None
        for image in candidates:
            label = image.with_suffix('.txt')
            if label.is_file() and hashlib.sha256(label.read_bytes()).hexdigest() == row['label_sha256']:
                source = image
                break
        if source is None:
            raise RuntimeError('Cannot match original image/label for ' + row['filename'])
        target = args.output/'images'/row['split']/row['filename']
        label_target = args.output/'labels'/row['split']/Path(row['filename']).with_suffix('.txt').name
        target.parent.mkdir(parents=True, exist_ok=True)
        label_target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as original:
            image = original.convert('RGB')
            width, height = image.size
            scale = 1280 / max(width, height)
            if scale < 1:
                image = image.resize((max(1,round(width*scale)),max(1,round(height*scale))),Image.Resampling.LANCZOS)
            if image.size != (int(row['width']),int(row['height'])):
                raise RuntimeError('Image dimensions differ: '+row['filename'])
            image.save(target,'JPEG',quality=88)
        shutil.copy2(source.with_suffix('.txt'),label_target)
        exact = hashlib.sha256(target.read_bytes()).hexdigest() == row['image_sha256']
        report.append({'image':row['filename'],'jpeg_bytes_identical':exact})
        if n%2000 == 0:print('Restored',n,flush=True)

names = ['person','car','motorcycle','bus','truck','traffic_light']
import yaml
with open(args.output/'data.yaml','w',encoding='utf-8') as f:
    yaml.safe_dump({'path':str(args.output.resolve()),'train':'images/train','val':'images/val',
                    'test':'images/test','nc':6,'names':names},f,sort_keys=False)
(args.output/'restoration-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Restored',len(report),'images. Exact JPEG matches:',sum(r['jpeg_bytes_identical'] for r in report))
print('Same selection, dimensions and label hashes are required. JPEG bytes can differ between Pillow/libjpeg versions.')
