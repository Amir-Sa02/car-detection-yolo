from pathlib import Path
from datetime import datetime
from collections import Counter
from types import SimpleNamespace
from contextlib import redirect_stdout
import ast
import io
import os
import shutil
import textwrap

path = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\01_کدهای مطالعه به ترتیب\02__build_subset_v5.py')
raw = path.read_bytes()
source = raw.decode('utf-8-sig')
start = source.index('    # Print statistics for the selected images.')
end = source.index('\n\n\nif __name__', start)
old = source[start:end]
new = '''    # Print only the basic counts.
    for split in ("train", "val", "test"):
        instances = 0
        for frame in sel[split]:
            instances += len(frame[3])
        print(split, "images:", len(sel[split]), "instances:", instances)

    if DRY_RUN:
        print("DRY_RUN: no files written.")
        return

    # Replace the output folder and save the selected data.
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    for split in ("train", "val", "test"):
        image_dir = os.path.join(OUT, "images", split)
        label_dir = os.path.join(OUT, "labels", split)
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)

        for frame in sel[split]:
            jpg = frame[0]
            txt = frame[1]
            name = frame[2]
            resize_save(jpg, os.path.join(image_dir, name + ".jpg"))
            shutil.copy2(txt, os.path.join(label_dir, name + ".txt"))

        print(split, "saved", flush=True)

    # Write the paths and class names required by YOLO.
    yaml_path = os.path.join(OUT, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("# IADD subset v5 (leakage-free, broken+duplicate videos removed, blind reshuffle)\\n")
        f.write("path: " + COLAB_PATH + "\\n")
        f.write("train: images/train\\n")
        f.write("val: images/val\\n")
        f.write("test: images/test\\n")
        f.write("\\nnc: 6\\n")
        f.write("names:\\n")
        for class_id, name in enumerate(NAMES):
            f.write("  " + str(class_id) + ": " + name + "\\n")

    print("Output:", OUT)
'''

def simulate(block, dry_run):
    calls = []
    buffers = []
    class Buffer(io.StringIO):
        def close(self): pass
    def fake_open(*args, **kwargs):
        b = Buffer()
        buffers.append(b)
        return b
    selected = {
        'train': [('a.jpg', 'a.txt', 'Record001_D__0', [0,1,2]),
                  ('b.jpg', 'b.txt', 'Record002_N__0', [3,4,5])],
        'val': [('c.jpg', 'c.txt', 'Record003_R__0', [0,1,2,3,4,5])],
        'test': [('d.jpg', 'd.txt', 'Record004_A__0', [0,1,2,3,4,5])],
    }
    env = dict(Counter=Counter, sel=selected, tr={'1','2'}, va={'3'}, te={'4'},
               DRY_RUN=dry_run, OUT='simulated_output', COLAB_PATH='/content/data',
               NAMES=['person','car','motorcycle','bus','truck','traffic_light'],
               os=SimpleNamespace(path=SimpleNamespace(join=os.path.join,isdir=lambda p:True),
                                  makedirs=lambda *a,**k:calls.append(('mkdir',a,k))),
               shutil=SimpleNamespace(rmtree=lambda p:calls.append(('delete',p)),
                                      copy2=lambda a,b:calls.append(('label',a,b))),
               resize_save=lambda a,b:calls.append(('image',a,b)),open=fake_open)
    exec('def check():\n'+textwrap.indent(textwrap.dedent(block),'    '),env)
    with redirect_stdout(io.StringIO()): env['check']()
    return calls, [b.getvalue() for b in buffers]

for dry_run in (True,False):
    assert simulate(old,dry_run)==simulate(new,dry_run)
updated=source[:start]+new.rstrip('\n')+source[end:]
ast.parse(updated)
assert updated[:start]==source[:start]
backup=path.parent/'پشتیبان‌ها'/datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
shutil.copy2(path,backup/path.name)
newline='\r\n' if b'\r\n' in raw else '\n'
data=updated.replace('\r\n','\n').replace('\n',newline).encode('utf-8')
if raw.startswith(b'\xef\xbb\xbf'): data=b'\xef\xbb\xbf'+data
path.write_bytes(data)
assert path.read_bytes()==data
print('Changed requested block from',len(old.splitlines()),'to',len(new.splitlines()),'lines.')
print('Syntax valid. Simulated build and dry-run file operations match. No dataset operations executed.')
