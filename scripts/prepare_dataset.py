# scripts/prepare_dataset.py
"""
Script untuk prepare dataset dari folder root ke struktur train/val/test
Mendukung format webp dan jpg
"""
import os
import shutil
from pathlib import Path
import random

# Config
BASE_DIR = Path(__file__).parent.parent
ROOT_DIR = BASE_DIR.parent  # Root workspace

# Source folders - cek di dalam project dulu, kalau tidak ada cek di root
SOURCE_FOLDERS = {}
for class_name in ['bersih', 'tumpukan_ringan', 'tumpukan_parah']:
    # Prioritas 1: Di dalam project folder
    project_path = BASE_DIR / 'raw_data' / class_name
    # Prioritas 2: Di root workspace
    root_path = ROOT_DIR / class_name
    
    if project_path.exists():
        SOURCE_FOLDERS[class_name] = project_path
    elif root_path.exists():
        SOURCE_FOLDERS[class_name] = root_path
    else:
        SOURCE_FOLDERS[class_name] = project_path  # Default ke project path

# Target folder
DATA_DIR = BASE_DIR / 'data'

# Split ratio
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Supported extensions
SUPPORTED_EXTS = ['.webp', '.jpg', '.jpeg', '.png']

def get_image_files(folder_path):
    """Get all image files from folder"""
    if not folder_path.exists():
        return []
    
    files = []
    for ext in SUPPORTED_EXTS:
        files.extend(list(folder_path.glob(f'*{ext}')))
        files.extend(list(folder_path.glob(f'*{ext.upper()}')))
    
    return files

def prepare_dataset(seed=42):
    """
    Prepare dataset dengan split train/val/test
    """
    random.seed(seed)
    
    print("=" * 60)
    print("PREPARING DATASET FOR TRAINING")
    print("=" * 60)
    
    # Create data structure
    for split in ['train', 'val', 'test']:
        for class_name in SOURCE_FOLDERS.keys():
            target_dir = DATA_DIR / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each class
    total_stats = {}
    
    for class_name, source_folder in SOURCE_FOLDERS.items():
        print(f"\n📁 Processing class: {class_name}")
        print(f"   Source: {source_folder}")
        
        if not source_folder.exists():
            print(f"   ⚠️  Folder tidak ditemukan, skip...")
            continue
        
        # Get all images
        image_files = get_image_files(source_folder)
        
        if not image_files:
            print(f"   ⚠️  Tidak ada gambar ditemukan, skip...")
            continue
        
        print(f"   Found {len(image_files)} images")
        
        # Shuffle
        random.shuffle(image_files)
        
        # Calculate split indices
        n_total = len(image_files)
        n_train = int(n_total * TRAIN_RATIO)
        n_val = int(n_total * VAL_RATIO)
        
        train_files = image_files[:n_train]
        val_files = image_files[n_train:n_train + n_val]
        test_files = image_files[n_train + n_val:]
        
        # Copy files
        splits = {
            'train': train_files,
            'val': val_files,
            'test': test_files
        }
        
        class_stats = {}
        
        for split_name, files in splits.items():
            target_dir = DATA_DIR / split_name / class_name
            
            for i, src_file in enumerate(files, 1):
                # Keep original extension
                dst_file = target_dir / f"{class_name}_{i:04d}{src_file.suffix}"
                shutil.copy2(src_file, dst_file)
            
            class_stats[split_name] = len(files)
            print(f"   ✓ {split_name}: {len(files)} images")
        
        total_stats[class_name] = class_stats
    
    # Print summary
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    for class_name, stats in total_stats.items():
        total = sum(stats.values())
        print(f"\n{class_name.upper()}: {total} total")
        for split, count in stats.items():
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  - {split:5s}: {count:3d} ({percentage:.1f}%)")
    
    # Overall summary
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    
    for split in ['train', 'val', 'test']:
        total = sum(stats.get(split, 0) for stats in total_stats.values())
        print(f"{split.upper():5s}: {total} images")
    
    print("\n✅ Dataset preparation complete!")
    print(f"📂 Data location: {DATA_DIR}")
    print("\nNext steps:")
    print("1. Run: python src/train.py")
    print("2. Run: streamlit run app.py")

if __name__ == '__main__':
    prepare_dataset()
