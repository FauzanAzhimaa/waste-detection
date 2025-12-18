"""
Data Collection Helper - Kampus 1 UNJANI Yogyakarta
Script untuk membantu mengumpulkan dan mengorganisir data training lebih banyak
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
import json


class DataCollector:
    """Helper untuk mengumpulkan dan mengorganisir data training"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.raw_data_dir = self.base_dir / 'raw_data'
        self.categories = ['bersih', 'tumpukan_ringan', 'tumpukan_parah']
        
        # Target jumlah gambar per kategori
        self.target_per_category = 300
        
    def check_current_status(self):
        """Cek status dataset saat ini"""
        print("=" * 60)
        print("📊 STATUS DATASET SAAT INI")
        print("=" * 60)
        
        status = {}
        total = 0
        
        for category in self.categories:
            category_path = self.raw_data_dir / category
            if category_path.exists():
                images = list(category_path.glob('*.jpg')) + \
                        list(category_path.glob('*.jpeg')) + \
                        list(category_path.glob('*.png')) + \
                        list(category_path.glob('*.webp'))
                count = len(images)
                status[category] = count
                total += count
                
                percentage = (count / self.target_per_category) * 100
                progress_bar = self._create_progress_bar(count, self.target_per_category)
                
                print(f"\n📁 {category.upper()}")
                print(f"   Jumlah: {count}/{self.target_per_category} gambar ({percentage:.1f}%)")
                print(f"   {progress_bar}")
                print(f"   Kurang: {self.target_per_category - count} gambar")
            else:
                status[category] = 0
                print(f"\n📁 {category.upper()}")
                print(f"   ❌ Folder tidak ditemukan!")
        
        print("\n" + "=" * 60)
        print(f"📊 TOTAL: {total} gambar")
        print(f"🎯 TARGET: {self.target_per_category * 3} gambar")
        print(f"📈 Progress: {(total / (self.target_per_category * 3)) * 100:.1f}%")
        print("=" * 60)
        
        return status
    
    def _create_progress_bar(self, current, target, width=40):
        """Buat progress bar visual"""
        filled = int((current / target) * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}]"
    
    def get_recommendations(self):
        """Berikan rekomendasi pengumpulan data"""
        status = self.check_current_status()
        
        print("\n" + "=" * 60)
        print("💡 REKOMENDASI PENGUMPULAN DATA")
        print("=" * 60)
        
        for category, count in status.items():
            needed = self.target_per_category - count
            if needed > 0:
                print(f"\n📸 {category.upper()}")
                print(f"   Perlu tambahan: {needed} gambar")
                print(f"   Tips:")
                
                if category == 'bersih':
                    print("   • Foto area kampus yang bersih dan rapi")
                    print("   • Berbagai lokasi: kelas, koridor, taman, parkiran")
                    print("   • Pastikan tidak ada sampah terlihat")
                    print("   • Foto dari berbagai sudut dan pencahayaan")
                
                elif category == 'tumpukan_ringan':
                    print("   • Foto area dengan sedikit sampah (1-5 item)")
                    print("   • Sampah berserakan tapi belum menumpuk")
                    print("   • Kondisi yang masih mudah dibersihkan")
                    print("   • Berbagai jenis sampah: plastik, kertas, botol")
                
                elif category == 'tumpukan_parah':
                    print("   • Foto area dengan banyak sampah menumpuk")
                    print("   • Tumpukan sampah yang jelas terlihat")
                    print("   • Kondisi yang perlu pembersihan menyeluruh")
                    print("   • Berbagai tingkat keparahan")
        
        print("\n" + "=" * 60)
        print("📋 PANDUAN UMUM PENGAMBILAN FOTO:")
        print("=" * 60)
        print("✅ Gunakan kamera HP dengan resolusi minimal 720p")
        print("✅ Foto di berbagai waktu: pagi, siang, sore")
        print("✅ Berbagai sudut: depan, samping, atas")
        print("✅ Pencahayaan yang cukup (hindari terlalu gelap)")
        print("✅ Fokus pada area sampah, hindari blur")
        print("✅ Foto dari jarak 1-3 meter")
        print("✅ Landscape atau portrait, keduanya OK")
        print("\n❌ Hindari foto yang terlalu gelap atau blur")
        print("❌ Hindari foto dengan watermark besar")
        print("❌ Hindari foto yang terlalu jauh (sampah tidak jelas)")
        
    def organize_new_images(self, source_folder, auto_validate=True):
        """Organisir gambar baru dari folder sumber dengan auto-validation"""
        source_path = Path(source_folder)
        
        if not source_path.exists():
            print(f"❌ Folder {source_folder} tidak ditemukan!")
            return
        
        print("\n" + "=" * 60)
        print("📂 MENGORGANISIR GAMBAR BARU")
        print("=" * 60)
        
        # Cari semua gambar
        images = list(source_path.glob('*.jpg')) + \
                list(source_path.glob('*.jpeg')) + \
                list(source_path.glob('*.png')) + \
                list(source_path.glob('*.webp'))
        
        print(f"\n✅ Ditemukan {len(images)} gambar di {source_folder}")
        
        if len(images) == 0:
            print("⚠️ Tidak ada gambar untuk diorganisir")
            return
        
        print("\n📋 Pilih kategori untuk setiap gambar:")
        print("   1 = Bersih")
        print("   2 = Tumpukan Ringan")
        print("   3 = Tumpukan Parah")
        print("   s = Skip gambar ini")
        print("   q = Quit\n")
        
        organized = {'bersih': 0, 'tumpukan_ringan': 0, 'tumpukan_parah': 0, 'skipped': 0, 'rejected': 0}
        backup_dir = self.base_dir / 'raw_data_backup_small'
        
        for i, img_path in enumerate(images, 1):
            print(f"\n[{i}/{len(images)}] {img_path.name}")
            
            # Validasi gambar
            is_valid = True
            width, height = 0, 0
            
            try:
                img = Image.open(img_path)
                width, height = img.size
                print(f"   Ukuran: {width}x{height} pixels")
                print(f"   Format: {img.format}")
                
                # Auto-validate size
                if auto_validate and (width < 224 or height < 224):
                    print(f"   ⚠️ REJECTED: Ukuran terlalu kecil (min: 224x224)")
                    is_valid = False
                    
                img.close()
            except Exception as e:
                print(f"   ⚠️ Error membaca gambar: {e}")
                is_valid = False
            
            if not is_valid:
                # Pindahkan ke backup otomatis
                backup_dir.mkdir(exist_ok=True)
                backup_rejected = backup_dir / 'rejected'
                backup_rejected.mkdir(exist_ok=True)
                
                try:
                    shutil.move(str(img_path), str(backup_rejected / img_path.name))
                    print(f"   📦 Dipindahkan ke backup/rejected")
                    organized['rejected'] += 1
                except:
                    print(f"   ❌ Gagal memindahkan ke backup")
                    organized['skipped'] += 1
                continue
            
            choice = input("   Kategori (1/2/3/s/q): ").strip().lower()
            
            if choice == 'q':
                print("\n⏹️ Berhenti mengorganisir")
                break
            elif choice == 's':
                organized['skipped'] += 1
                continue
            elif choice in ['1', '2', '3']:
                category_map = {'1': 'bersih', '2': 'tumpukan_ringan', '3': 'tumpukan_parah'}
                category = category_map[choice]
                
                # Copy ke folder kategori
                dest_folder = self.raw_data_dir / category
                dest_folder.mkdir(parents=True, exist_ok=True)
                
                # Generate nama file unik
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                dest_path = dest_folder / f"{timestamp}_{img_path.name}"
                
                # Copy file
                shutil.copy2(img_path, dest_path)
                organized[category] += 1
                print(f"   ✅ Disimpan ke: {category}/{dest_path.name}")
            else:
                print("   ⚠️ Pilihan tidak valid, skip")
                organized['skipped'] += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"✅ Bersih: {organized['bersih']} gambar")
        print(f"✅ Tumpukan Ringan: {organized['tumpukan_ringan']} gambar")
        print(f"✅ Tumpukan Parah: {organized['tumpukan_parah']} gambar")
        print(f"⏭️ Skipped: {organized['skipped']} gambar")
        print(f"❌ Rejected (too small): {organized['rejected']} gambar")
        print("=" * 60)
    
    def validate_images(self):
        """Validasi semua gambar di raw_data"""
        print("\n" + "=" * 60)
        print("🔍 VALIDASI GAMBAR")
        print("=" * 60)
        
        issues = []
        total_checked = 0
        
        for category in self.categories:
            category_path = self.raw_data_dir / category
            if not category_path.exists():
                continue
            
            print(f"\n📁 Memeriksa {category}...")
            images = list(category_path.glob('*.*'))
            
            for img_path in images:
                total_checked += 1
                try:
                    img = Image.open(img_path)
                    
                    # Cek ukuran minimum
                    if img.size[0] < 224 or img.size[1] < 224:
                        issues.append({
                            'file': str(img_path),
                            'issue': f'Ukuran terlalu kecil: {img.size[0]}x{img.size[1]} (min: 224x224)'
                        })
                    
                    # Cek format
                    if img.format not in ['JPEG', 'PNG', 'WEBP']:
                        issues.append({
                            'file': str(img_path),
                            'issue': f'Format tidak didukung: {img.format}'
                        })
                    
                    img.close()
                    
                except Exception as e:
                    issues.append({
                        'file': str(img_path),
                        'issue': f'Error membaca file: {str(e)}'
                    })
        
        print(f"\n✅ Total diperiksa: {total_checked} gambar")
        
        if issues:
            print(f"⚠️ Ditemukan {len(issues)} masalah:\n")
            for issue in issues:
                print(f"   ❌ {Path(issue['file']).name}")
                print(f"      {issue['issue']}\n")
        else:
            print("✅ Semua gambar valid!")
        
        return issues
    
    def generate_report(self):
        """Generate laporan lengkap dataset"""
        report_path = self.base_dir / 'dataset_report.json'
        
        status = {}
        for category in self.categories:
            category_path = self.raw_data_dir / category
            if category_path.exists():
                images = list(category_path.glob('*.jpg')) + \
                        list(category_path.glob('*.jpeg')) + \
                        list(category_path.glob('*.png')) + \
                        list(category_path.glob('*.webp'))
                status[category] = {
                    'count': len(images),
                    'target': self.target_per_category,
                    'percentage': (len(images) / self.target_per_category) * 100,
                    'needed': self.target_per_category - len(images)
                }
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'categories': status,
            'total_images': sum(s['count'] for s in status.values()),
            'total_target': self.target_per_category * 3,
            'overall_percentage': (sum(s['count'] for s in status.values()) / (self.target_per_category * 3)) * 100
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Laporan disimpan ke: {report_path}")
        return report


def main():
    """Main function"""
    collector = DataCollector()
    
    print("\n" + "=" * 60)
    print("🎯 DATA COLLECTION HELPER")
    print("   Kampus 1 UNJANI Yogyakarta")
    print("=" * 60)
    
    while True:
        print("\n📋 MENU:")
        print("   1. Cek status dataset saat ini")
        print("   2. Lihat rekomendasi pengumpulan data")
        print("   3. Organisir gambar baru dari folder")
        print("   4. Validasi semua gambar")
        print("   5. Generate laporan dataset")
        print("   0. Keluar")
        
        choice = input("\nPilih menu (0-5): ").strip()
        
        if choice == '1':
            collector.check_current_status()
        
        elif choice == '2':
            collector.get_recommendations()
        
        elif choice == '3':
            folder = input("\nMasukkan path folder gambar baru: ").strip()
            collector.organize_new_images(folder)
        
        elif choice == '4':
            collector.validate_images()
        
        elif choice == '5':
            collector.generate_report()
        
        elif choice == '0':
            print("\n👋 Terima kasih!")
            break
        
        else:
            print("\n❌ Pilihan tidak valid!")


if __name__ == '__main__':
    main()
