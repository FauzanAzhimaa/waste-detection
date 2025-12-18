"""
Clean Small Images - Hapus gambar yang terlalu kecil
Kampus 1 UNJANI Yogyakarta
"""
from pathlib import Path
from PIL import Image
import shutil


def clean_small_images(min_size=224, backup=True):
    """Hapus atau pindahkan gambar yang terlalu kecil"""
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'raw_data'
    backup_dir = base_dir / 'raw_data_backup_small'
    
    categories = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
    
    print("=" * 70)
    print("🧹 CLEAN SMALL IMAGES")
    print("=" * 70)
    print(f"\nMinimum size: {min_size}x{min_size} pixels")
    print(f"Backup: {'Yes' if backup else 'No (PERMANENT DELETE!)'}\n")
    
    if backup:
        backup_dir.mkdir(exist_ok=True)
        print(f"📁 Backup folder: {backup_dir}\n")
    
    total_checked = 0
    total_removed = 0
    removed_by_category = {}
    
    for category in categories:
        category_path = raw_data_dir / category
        if not category_path.exists():
            continue
        
        print(f"📂 Checking {category}...")
        
        images = list(category_path.glob('*.jpg')) + \
                list(category_path.glob('*.jpeg')) + \
                list(category_path.glob('*.png')) + \
                list(category_path.glob('*.webp'))
        
        removed_count = 0
        
        for img_path in images:
            total_checked += 1
            try:
                img = Image.open(img_path)
                width, height = img.size
                img.close()
                
                # Cek apakah terlalu kecil
                if width < min_size or height < min_size:
                    if backup:
                        # Backup ke folder terpisah
                        backup_category = backup_dir / category
                        backup_category.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(img_path), str(backup_category / img_path.name))
                        print(f"   ⚠️ Moved: {img_path.name} ({width}x{height})")
                    else:
                        # Hapus permanent
                        img_path.unlink()
                        print(f"   ❌ Deleted: {img_path.name} ({width}x{height})")
                    
                    removed_count += 1
                    total_removed += 1
                    
            except Exception as e:
                print(f"   ⚠️ Error processing {img_path.name}: {e}")
        
        removed_by_category[category] = removed_count
        
        if removed_count > 0:
            print(f"   Removed: {removed_count} images\n")
        else:
            print(f"   ✅ All images OK\n")
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total checked: {total_checked} images")
    print(f"Total removed: {total_removed} images")
    print(f"\nRemoved by category:")
    for cat, count in removed_by_category.items():
        print(f"   {cat:20s}: {count} images")
    
    if backup and total_removed > 0:
        print(f"\n💾 Backup saved to: {backup_dir}")
        print("   You can restore them if needed")
    
    print("=" * 70)
    
    return total_removed


def restore_from_backup():
    """Restore gambar dari backup"""
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'raw_data'
    backup_dir = base_dir / 'raw_data_backup_small'
    
    if not backup_dir.exists():
        print("❌ Backup folder tidak ditemukan!")
        return
    
    print("=" * 70)
    print("♻️ RESTORE FROM BACKUP")
    print("=" * 70)
    
    categories = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
    total_restored = 0
    
    for category in categories:
        backup_category = backup_dir / category
        if not backup_category.exists():
            continue
        
        images = list(backup_category.glob('*.*'))
        if not images:
            continue
        
        print(f"\n📂 Restoring {category}...")
        
        dest_folder = raw_data_dir / category
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        for img_path in images:
            dest_path = dest_folder / img_path.name
            shutil.move(str(img_path), str(dest_path))
            print(f"   ✅ Restored: {img_path.name}")
            total_restored += 1
    
    print(f"\n✅ Total restored: {total_restored} images")
    print("=" * 70)


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("🧹 IMAGE CLEANER")
    print("   Kampus 1 UNJANI Yogyakarta")
    print("=" * 70)
    
    while True:
        print("\n📋 MENU:")
        print("   1. Clean small images (with backup)")
        print("   2. Clean small images (PERMANENT DELETE)")
        print("   3. Restore from backup")
        print("   4. Check status only (no delete)")
        print("   0. Exit")
        
        choice = input("\nPilih menu (0-4): ").strip()
        
        if choice == '1':
            confirm = input("\n⚠️ Pindahkan gambar kecil ke backup? (y/n): ").strip().lower()
            if confirm == 'y':
                clean_small_images(min_size=224, backup=True)
        
        elif choice == '2':
            print("\n🚨 WARNING: Ini akan HAPUS PERMANENT gambar kecil!")
            confirm = input("Ketik 'DELETE' untuk konfirmasi: ").strip()
            if confirm == 'DELETE':
                clean_small_images(min_size=224, backup=False)
            else:
                print("❌ Cancelled")
        
        elif choice == '3':
            restore_from_backup()
        
        elif choice == '4':
            # Just check, don't delete
            base_dir = Path(__file__).parent.parent
            raw_data_dir = base_dir / 'raw_data'
            categories = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
            
            print("\n" + "=" * 70)
            print("🔍 CHECK STATUS")
            print("=" * 70)
            
            total_small = 0
            
            for category in categories:
                category_path = raw_data_dir / category
                if not category_path.exists():
                    continue
                
                images = list(category_path.glob('*.jpg')) + \
                        list(category_path.glob('*.jpeg')) + \
                        list(category_path.glob('*.png')) + \
                        list(category_path.glob('*.webp'))
                
                small_count = 0
                
                for img_path in images:
                    try:
                        img = Image.open(img_path)
                        width, height = img.size
                        img.close()
                        
                        if width < 224 or height < 224:
                            small_count += 1
                    except:
                        pass
                
                total_small += small_count
                print(f"\n{category}:")
                print(f"   Total: {len(images)} images")
                print(f"   Small (<224x224): {small_count} images")
                print(f"   Valid (≥224x224): {len(images) - small_count} images")
            
            print(f"\n📊 Total small images: {total_small}")
            print("=" * 70)
        
        elif choice == '0':
            print("\n👋 Selesai!")
            break
        
        else:
            print("\n❌ Pilihan tidak valid!")


if __name__ == '__main__':
    main()
