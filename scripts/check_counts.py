# scripts/check_counts.py
import os
for split in ['train','val','test']:
    base = os.path.join('data', split)
    if not os.path.exists(base):
        print(split, 'folder missing')
        continue
    print('---', split)
    for cls in sorted(os.listdir(base)):
        p = os.path.join(base, cls)
        if os.path.isdir(p):
            n = len([f for f in os.listdir(p) if f.lower().endswith(('.jpg','.png'))])
            print(f'  {cls}: {n}')