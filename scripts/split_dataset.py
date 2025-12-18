# scripts/split_dataset.py
import os, shutil, random
from pathlib import Path

SRC = 'raw_images_jpg'   # GANTI jika foldermu beda
DST = 'data'             # hasil: data/train, data/val, data/test
SPLIT = (0.7, 0.15, 0.15)
SEED = 42

random.seed(SEED)
Path(DST).mkdir(parents=True, exist_ok=True)

for cls in os.listdir(SRC):
    src_dir = os.path.join(SRC, cls)
    if not os.path.isdir(src_dir):
        continue
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    random.shuffle(files)
    n = len(files)
    n1 = int(n * SPLIT[0])
    n2 = n1 + int(n * SPLIT[1])
    parts = {
        'train': files[:n1],
        'val': files[n1:n2],
        'test': files[n2:]
    }
    for part, flist in parts.items():
        dst_dir = os.path.join(DST, part, cls)
        Path(dst_dir).mkdir(parents=True, exist_ok=True)
        for fname in flist:
            srcp = os.path.join(src_dir, fname)
            dstp = os.path.join(dst_dir, fname)
            shutil.copy2(srcp, dstp)
    print(f'{cls}: total={n}, train={len(parts["train"])}, val={len(parts["val"])}, test={len(parts["test"])}')