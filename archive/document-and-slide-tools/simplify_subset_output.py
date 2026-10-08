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
original = path.read_bytes()
source = original.decode('utf-8-sig')
start = source.index('    # ---- stats (condition mix + crowd are the difficulty proxies) ----')
end = source.index('\n\n\nif __name__', start)
old = source[start:end]
new = '''    # Print statistics for the selected images.
    print("\\nSelected data statistics")
    print("Dry run:", DRY_RUN)

    total_images = 0
    for split in sel:
        total_images += len(sel[split])

    print("Videos in train:", len(tr))
    print("Videos in val:", len(va))
    print("Videos in test:", len(te))

    class_counts = {}
    for split in ("train", "val", "test"):
        images = sel[split]
        image_count = len(images)
        instance_count = 0
        conditions = Counter()
        class_counts[split] = Counter()

        for frame in images:
            name = frame[2]
            classes = frame[3]
            instance_count += len(classes)

            record = name.split("__")[0]
            condition = record.split("_")[-1]
            conditions[condition] += 1

            for class_id in classes:
                class_counts[split][class_id] += 1

        image_percent = 100 * image_count / total_images
        instances_per_image = instance_count / image_count

        print("\\nSplit:", split)
        print("Images:", image_count)
        print("Share of all images (%):", round(image_percent, 1))
        print("Instances per image:", round(instances_per_image, 1))
        print("Conditions (%):")
        for condition in sorted(conditions):
            percent = 100 * conditions[condition] / image_count
            print(condition, round(percent))

    print("\\nClass instances per split:")
    for class_id, name in enumerate(NAMES):
        train_count = class_counts["train"][class_id]
        val_count = class_counts["val"][class_id]
        test_count = class_counts["test"][class_id]
        total_count = train_count + val_count + test_count

        print("\\nClass:", name)
        print("Train:", train_count, "Val:", val_count, "Test:", test_count)
        print("Val share (%):", round(100 * val_count / total_count, 1))
        print("Test share (%):", round(100 * test_count / total_count, 1))

    if DRY_RUN:
        print("\\nDRY_RUN: no files written. Set DRY_RUN=False to build.")
        return

    # Replace the output folder and save images and labels.
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    for split in ("train", "val", "test"):
        image_dir = os.path.join(OUT, "images", split)
        label_dir = os.path.join(OUT, "labels", split)
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)

        saved = 0
        for frame in sel[split]:
            jpg = frame[0]
            txt = frame[1]
            name = frame[2]

            image_path = os.path.join(image_dir, name + ".jpg")
            label_path = os.path.join(label_dir, name + ".txt")
            resize_save(jpg, image_path)
            shutil.copy2(txt, label_path)

            saved += 1
            if saved % 2000 == 0:
                print(split, "saved:", saved, "of", len(sel[split]), flush=True)

        print(split, "done:", saved, "images", flush=True)

    # Write the dataset configuration.
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

    print("\\nOutput:", OUT)
    print("To create a ZIP file:")
    command = 'Compress-Archive -Path "' + OUT + '\\\\*" -DestinationPath "' + OUT + '.zip" -Force'
    print(command)
'''

# Compare the old and new output logic using simulated file operations.
# No dataset is read, written, or deleted during verification.
selected = {
    'train': [('a.jpg', 'a.txt', 'Record001_D__0', [0, 1, 2]),
              ('b.jpg', 'b.txt', 'Record002_N__0', [3, 4, 5])],
    'val': [('c.jpg', 'c.txt', 'Record003_R__0', [0, 1, 2, 3, 4, 5])],
    'test': [('d.jpg', 'd.txt', 'Record004_A__0', [0, 1, 2, 3, 4, 5])],
}

def simulate(block, dry_run):
    calls = []
    buffers = []

    class Buffer(io.StringIO):
        def close(self):
            pass

    def fake_open(*args, **kwargs):
        buffer = Buffer()
        buffers.append(buffer)
        return buffer

    env = dict(Counter=Counter, sel=selected, tr={'1', '2'}, va={'3'}, te={'4'},
               DRY_RUN=dry_run, OUT='simulated_output', COLAB_PATH='/content/data',
               NAMES=['person', 'car', 'motorcycle', 'bus', 'truck', 'traffic_light'],
               os=SimpleNamespace(path=SimpleNamespace(join=os.path.join, isdir=lambda p: True),
                                  makedirs=lambda *a, **k: None),
               shutil=SimpleNamespace(rmtree=lambda p: calls.append(('delete', p)),
                                      copy2=lambda a, b: calls.append(('label', a, b))),
               resize_save=lambda a, b: calls.append(('image', a, b)), open=fake_open)
    exec('def check():\n' + textwrap.indent(textwrap.dedent(block), '    '), env)
    with redirect_stdout(io.StringIO()):
        env['check']()
    return calls, [buffer.getvalue() for buffer in buffers]

for dry_run in (True, False):
    assert simulate(old, dry_run) == simulate(new, dry_run)

updated = source[:start] + new.rstrip('\n') + source[end:]
ast.parse(updated)
backup_dir = path.parent / 'پشتیبان‌ها' / datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir.mkdir(parents=True)
shutil.copy2(path, backup_dir / path.name)
newline = '\r\n' if b'\r\n' in original else '\n'
updated_bytes = updated.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
if original.startswith(b'\xef\xbb\xbf'):
    updated_bytes = b'\xef\xbb\xbf' + updated_bytes
path.write_bytes(updated_bytes)
assert path.read_bytes() == updated_bytes
print('Requested block simplified. Syntax and simulated output checks passed. Original dataset untouched.')
