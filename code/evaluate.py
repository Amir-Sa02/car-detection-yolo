"""Re-evaluate an archived model; keep metric curves and operating-point matrices separate."""
from argparse import ArgumentParser
from pathlib import Path
import json
import numpy as np
import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
parser=ArgumentParser()
parser.add_argument('--dataset',type=Path,required=True)
parser.add_argument('--weights',type=Path,default=ROOT/'models/run8_best.pt')
parser.add_argument('--split',choices=['val','test'],default='test')
parser.add_argument('--device',default='cpu')
parser.add_argument('--batch',type=int,default=1)
parser.add_argument('--conf',type=float,default=0.406,help='Operating-point confidence, fixed from recorded validation')
parser.add_argument('--output',type=Path,default=ROOT/'outputs/evaluation')
args=parser.parse_args()
args.output = args.output.resolve()
if not 0 <= args.conf <= 1 or args.batch < 1:
    parser.error('Confidence must be between 0 and 1; batch must be positive.')
args.output.mkdir(parents=True,exist_ok=True)
config = args.dataset / 'data.yaml' if args.dataset.is_dir() else args.dataset
cfg=yaml.safe_load(config.read_text(encoding='utf-8'))
cfg['path']=str(config.parent.resolve())
data=args.output/'data-local.yaml'
data.write_text(yaml.safe_dump(cfg,sort_keys=False),encoding='utf-8')
model=YOLO(args.weights)
metrics=model.val(data=str(data),split=args.split,imgsz=1280,batch=args.batch,device=args.device,
                  conf=0.001,plots=True,project=str(args.output),name=args.split+'_metrics',exist_ok=True)
arrays={'names':np.array([model.names[i] for i in sorted(model.names)]),
        'ap50':np.asarray(metrics.box.ap50),'map50':np.float64(metrics.box.map50)}
for x,y,xl,yl in metrics.curves_results:
    key=f'{xl}_{yl}'.lower()
    arrays['x_'+key]=np.asarray(x)
    arrays['y_'+key]=np.asarray(y)
arrays['pr_recall']=arrays['x_recall_precision']
arrays['pr_precision']=arrays['y_recall_precision']
op=model.val(data=str(data),split=args.split,imgsz=1280,batch=args.batch,device=args.device,
             conf=args.conf,plots=True,project=str(args.output),name=args.split+'_operating_point',exist_ok=True)
arrays['confusion']=np.asarray(op.confusion_matrix.matrix)
arrays['operating_confidence']=np.float64(args.conf)
np.savez_compressed(args.output/(args.split+'_curves.npz'),**arrays)
summary={'split':args.split,'map50':float(metrics.box.map50),'map50_95':float(metrics.box.map),
         'precision_reported_by_library':float(metrics.box.mp),'recall_reported_by_library':float(metrics.box.mr),
         'operating_confidence':args.conf,'weights':str(args.weights)}
(args.output/(args.split+'_metrics.json')).write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
