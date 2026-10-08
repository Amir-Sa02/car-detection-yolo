from pathlib import Path
from datetime import datetime
import ast
import shutil
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p = Path(r'C:\Users\amir2\Desktop\نسخه ارسالی\01_کدهای مطالعه به ترتیب\06__compute_v5_validity_simple.py')
raw = p.read_bytes()
source = raw.decode('utf-8-sig')
start = source.index('# ---- chart 2: object-size distribution ----')
end = source.index('print("=== iadd_subset_v5 stats ===")', start)
replacement = '''# chart 2: object-size distribution
# Plot each size group's share of all object instances within each split.
# Place the split bars side by side and save the chart as size_dist.png.
fig, ax = plt.subplots(figsize=(6, 4))
bins = ["small\\n(<1%)", "medium\\n(1% to <6%)", "large\\n(>=6%)"]
x = range(3)
w = 0.26

for i, sp in enumerate(SPLITS):
    tot = 0
    for count in S[sp]["size"].values():
        tot += count

    vals = []
    for k in range(3):
        count = S[sp]["size"][k]
        percent = 100 * count / tot
        vals.append(percent)

    positions = []
    for xx in x:
        position = xx + (i - 1) * w
        positions.append(position)

    ax.bar(positions, vals, w, label=sp, color=COL[sp])

ax.set_xticks(list(x))
ax.set_xticklabels(bins)
ax.set_ylabel("% of instances")
ax.set_title("Object-size distribution per split")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/size_dist.png", dpi=140)
plt.close()

# chart 3: condition distribution
# Plot each condition's share of all images within each split.
# Place the split bars side by side and save the chart as cond_dist.png.
fig, ax = plt.subplots(figsize=(6, 4))
conds = ["D", "N", "R", "A"]
condition_names = ["day", "night", "rain", "cloudy"]
x = range(4)
w = 0.26

for i, sp in enumerate(SPLITS):
    tot = S[sp]["images"]

    vals = []
    for c in conds:
        count = S[sp]["cond"].get(c, 0)
        percent = 100 * count / tot
        vals.append(percent)

    positions = []
    for xx in x:
        position = xx + (i - 1) * w
        positions.append(position)

    ax.bar(positions, vals, w, label=sp, color=COL[sp])

ax.set_xticks(list(x))
ax.set_xticklabels(condition_names)
ax.set_ylabel("% of images")
ax.set_title("Condition distribution per split")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/cond_dist.png", dpi=140)
plt.close()

'''
updated = source[:start] + replacement + source[end:]
ast.parse(updated)

# Test only chart code with saved statistics and isolated output paths.
stats = json.loads(Path(r'D:\projects\car-detection-yolo\docs\dataset_validity\stats.json').read_text())
for data in stats.values():
    for key in ('cls', 'size'):
        data[key] = {int(k):v for k,v in data[key].items()}
qa = Path(r'C:\Users\amir2\Desktop\cat-claude\validity_charts_qa')
qa.mkdir(exist_ok=True)
splits = ['train', 'val', 'test']
colors = {'train':'#1f4e79','val':'#2eb669','test':'#e08a00'}
blocks = [
    updated[updated.index('# chart 1:'):updated.index('# chart 2:')],
    updated[updated.index('# chart 2:'):updated.index('# chart 3:')],
    updated[updated.index('# chart 3:'):updated.index('print("=== iadd_subset_v5 stats ===")')],
]
for index, block in enumerate(blocks):
    env = dict(S=stats, SPLITS=splits, COL=colors, OUT=str(qa), plt=plt,
               NAMES=['person','car','motorcycle','bus','truck','traffic_light'])
    exec(block,env)
    bars = env['ax'].patches
    groups = [6,3,4][index]
    assert len(bars) == 3 * groups
    for i, sp in enumerate(splits):
        if index == 0:
            counts = [stats[sp]['cls'][c] for c in range(6)]
            total = stats[sp]['instances']
        elif index == 1:
            counts = [stats[sp]['size'][k] for k in range(3)]
            total = sum(counts)
        else:
            counts = [stats[sp]['cond'].get(c,0) for c in ['D','N','R','A']]
            total = stats[sp]['images']
        for j, count in enumerate(counts):
            bar = bars[i * groups + j]
            assert math.isclose(bar.get_height(),100 * count / total)
            assert math.isclose(bar.get_x()+bar.get_width()/2,j+(i-1)*0.26,abs_tol=1e-12)

backup = p.parent/'پشتیبان‌ها'/datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True)
shutil.copy2(p,backup/p.name)
nl = '\r\n' if b'\r\n' in raw else '\n'
data = updated.replace('\r\n','\n').replace('\n',nl).encode('utf-8')
if raw.startswith(b'\xef\xbb\xbf'): data=b'\xef\xbb\xbf'+data
p.write_bytes(data)
assert p.read_bytes()==data
assert updated[:start]==source[:start]
print('Chart 1 verified and unchanged. Charts 2 and 3 simplified. All bar heights and positions verified against saved statistics. Backup created. No dataset or original chart outputs modified.')
