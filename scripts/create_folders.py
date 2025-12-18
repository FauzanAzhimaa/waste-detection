# scripts/create_folders.py
"""
Script untuk membuat folder raw_data otomatis
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / 'raw_data'

def create_folders():
    """
    Buat folder raw_data dengan struktur yang benar
    """
    folders = [
        RAW_DATA_DIR / 'bersih',
        RAW_DATA_DIR / 'tumpukan_ringan',
        RAW_DATA_DIR / 'tumpukan_parah'
    ]
    
    print("=" * 60)
    print("MEMBUAT FOLDER UNTUK DATA TRAINING")
    print("=" * 60)
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {folder.relative_to(BASE_DIR)}")
    
    print("\n" + "=" * 60)
    print("FOLDER BERHASIL DIBUAT!")
    print("=" * 60)
    print("\nStruktur folder:")
    print(f"""
Project Deteksi Tumpukan Sampah/
└── raw_data/
    ├── bersih/               ← Taruh gambar area BERSIH di sini
    ├── tumpukan_ringan/      ← Taruh gambar SAMPAH RINGAN di sini
    └── tumpukan_parah/       ← Taruh gambar SAMPAH PARAH di sini
    """)
    
    print("\n📝 Langkah selanjutnya:")
    print("1. Copy gambar ke folder yang sesuai")
    print("   - Minimal 30 gambar per kategori")
    print("   - Format: jpg, png, webp")
    print("\n2. Jalankan: python scripts/prepare_dataset.py")
    print("3. Jalankan: python src/train.py")
    print("4. Jalankan: streamlit run app.py")
    
    print("\n💡 Tips:")
    print("- Semakin banyak gambar = model semakin akurat")
    print("- Ideal: 100+ gambar per kategori")
    print("- Lihat CARA_TARUH_DATA.md untuk panduan lengkap")

if __name__ == '__main__':
    create_folders()
