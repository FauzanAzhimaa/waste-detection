"""
Auto Clean Small Images - Otomatis pindahkan gambar kecil
Kampus 1 UNJANI Yogyakarta
"""
from pathlib import Path
from PIL import Image
import shutil


def auto_clean_small_images(min_size=224):
    """Otomatis pindahkan gambar yang terlalu kecil ke backup"""
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'raw_data'
    backup_dir = base_dir / 'raw_data_backup_small'
    
    categories = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
    
    print("=" * 70)
    print("🧹 AUTO CLEAN SMALL IMAGES")
    print("=" * 70)
    print(f"Minimum size: {min_size}x{min_size} pixels")
    print(f"Backup folder: {backup_dir}\n")
    
    backup_dir.mkdir(exist_ok=True)
    
    total_checked = 0
    total_moved = 0
    moved_by_category = {}
    
    for category in categories:
        category_path = raw_data_dir / category
        if not category_path.exists():
            print(f"⚠️ Folder {category} tidak ditemukan, skip...\n")
            continue
        
        print(f"📂 Processing {category}...")
        
        images = list(category_path.glob('*.jpg')) + \
                list(category_path.glob('*.jpeg')) + \
                list(category_path.glob('*.png')) + \
                list(category_path.glob('*.webp'))
        
        moved_count = 0
        
        for img_path in images:
            total_checked += 1
            try:
                img = Image.open(img_path)
                width, height = img.size
                img.close()
                
                # Cek apakah terlalu kecil
                if width < min_size or height < min_size:
                    # Backup ke folder terpisah
                    backup_category = backup_dir / category
                    backup_category.mkdir(parents=True, exist_ok=True)
                    
                    dest_path = backup_category / img_path.name
                    shutil.move(str(img_path), str(dest_path))
                    
                    print(f"   ⚠️ Moved: {img_path.name} ({width}x{height})")
                    moved_count += 1
                    total_moved += 1
                    
            except Exception as e:
                print(f"   ❌ Error: {img_path.name} - {e}")
        
        moved_by_category[category] = moved_count
        
        if moved_count > 0:
            print(f"   ✅ Moved {moved_count} images to backup\n")
        else:
            print(f"   ✅ All images are valid size\n")
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total checked: {total_checked} images")
    print(f"Total moved to backup: {total_moved} images")
    print(f"Remaining valid: {total_checked - total_moved} images\n")
    
    print("Moved by category:")
    for cat, count in moved_by_category.items():
        remaining = len(list((raw_data_dir / cat).glob('*.*'))) if (raw_data_dir / cat).exists() else 0
        print(f"   {cat:20s}: {count} moved, {remaining} remaining")
    
    if total_moved > 0:
        print(f"\n💾 Backup saved to: {backup_dir}")
        print("   Gambar dapat di-restore jika diperlukan")
    
    print("=" * 70)
    
    return total_moved


if __name__ == '__main__':
    print("\n🚀 Starting automatic cleanup...\n")
    moved = auto_clean_small_images(min_size=224)
    
    if moved > 0:
        print(f"\n✅ Successfully moved {moved} small images to backup!")
    else:
        print("\n✅ No small images found. All images are valid!")
    
    print("\n✨ Cleanup complete!")
