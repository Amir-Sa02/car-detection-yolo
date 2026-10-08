import json, sys, zipfile, inspect
from pathlib import Path
import torch
import ultralytics
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'C:\Users\amir2\Desktop\cat-claude')
CKPT=Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\results\run8\run8\weights\best.pt')
c=torch.load(CKPT,map_location='cpu',weights_only=False)
model=(c.get('ema') or c['model']).float().eval()
meta={k:c.get(k) for k in ['epoch','version','date','best_fitness','train_metrics']}
meta['local_ultralytics']=ultralytics.__version__
meta['params']=sum(p.numel() for p in model.parameters())
meta['modules']=len(list(model.modules()))
meta['leaves']=sum(1 for m in model.modules() if not list(m.children()))
meta['conv2d_count']=sum(isinstance(m,torch.nn.Conv2d) for m in model.modules())
meta['yaml']=model.yaml
meta['names']=model.names
meta['stride']=model.stride.tolist()
meta['first_conv']=str(model.model[0])
meta['last_head']=str(model.model[-1])
layers=[]
def shape(x):
    if isinstance(x,torch.Tensor): return list(x.shape)
    if isinstance(x,(tuple,list)):return [shape(a) for a in x]
    if isinstance(x,dict): return {k:shape(v) for k,v in x.items()}
    return str(type(x))
for m in model.model:
    item={'i':m.i,'from':m.f,'type':type(m).__name__,'params':sum(p.numel() for p in m.parameters()),'repr':str(m)}
    layers.append(item)
    m.register_forward_hook(lambda mod, inp, out, item=item: item.update(input=shape(inp),output=shape(out)))
torch.set_num_threads(4)
with torch.no_grad(): model(torch.zeros(1,3,1280,1280))
meta['layers']=layers
(ROOT/'model_verified.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k not in ['yaml','first_conv','last_head','layers']},ensure_ascii=False,indent=2))
for m in layers: print(m['i'],m['type'],m['from'],m['params'],m['output'])
wheel=Path(r'D:\projects\car-detection-yolo\packages\ultralytics-8.4.42-py3-none-any.whl')
out=ROOT/'verified_source';out.mkdir(exist_ok=True)
with zipfile.ZipFile(wheel) as z:
    for name in ['ultralytics/cfg/models/11/yolo11.yaml','ultralytics/cfg/models/v8/yolov8.yaml','ultralytics/nn/modules/block.py','ultralytics/nn/modules/head.py','ultralytics/utils/loss.py','ultralytics/utils/tal.py','ultralytics/engine/trainer.py','ultralytics/models/yolo/detect/val.py','ultralytics/utils/metrics.py','ultralytics/nn/modules/conv.py','ultralytics/nn/tasks.py','ultralytics/data/augment.py']:
        (out/Path(name).name).write_bytes(z.read(name))
