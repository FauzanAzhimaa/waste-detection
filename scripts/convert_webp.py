# scripts/convert_webp_to_jpg_preserve.py
from PIL import Image
import os
from pathlib import Path
from shutil import copy2

SRC_ROOT = r'D:\Semester 5\Kecerdasan Buatan\tumpukan_parah'        # GANTI: folder tempat 3 folder kelas-mu saat ini (bersih, tumpukan_ringan, tumpukan_parah)
DST_ROOT = 'tumpukan_parah'    # Output terkonversi

def ensure_dirs():
    Path(DST_ROOT).mkdir(parents=True, exist_ok=True)

def convert_all():
    ensure_dirs()
    converted = 0
    copied = 0
    errors = []
    for root, dirs, files in os.walk(SRC_ROOT):
        rel = os.path.relpath(root, SRC_ROOT)
        dst_dir = os.path.join(DST_ROOT, rel) if rel != '.' else DST_ROOT
        os.makedirs(dst_dir, exist_ok=True)
        for f in files:
            src_path = os.path.join(root, f)
            name, ext = os.path.splitext(f)
            ext_low = ext.lower()
            try:
                if ext_low == '.webp':
                    img = Image.open(src_path).convert('RGB')  # handle alpha if present
                    dst_path = os.path.join(dst_dir, name + '.jpg')
                    img.save(dst_path, 'JPEG', quality=92)
                    converted += 1
                elif ext_low in ['.jpg', '.jpeg', '.png', '.bmp']:
                    # copy other common formats
                    dst_path = os.path.join(dst_dir, f)
                    copy2(src_path, dst_path)
                    copied += 1
                else:
                    # ignore uncommon files by default
                    print('Skipping unsupported file:', src_path)
            except Exception as e:
                errors.append((src_path, str(e)))
                print('Error processing', src_path, e)
    print(f'Done. Converted {converted} webp files, copied {copied} other images.')
    if errors:
        print('Errors for', len(errors), 'files. First 5:')
        for e in errors[:5]:
            print(e)

if __name__ == '__main__':
    convert_all()
