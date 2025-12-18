# 📁 Cara Taruh Data Gambar untuk Training

## ✅ Opsi 1: Di Dalam Project (RECOMMENDED)

Taruh gambar di folder `raw_data/` di dalam project:

```
Project Deteksi Tumpukan Sampah/
├── raw_data/                  ← BUAT FOLDER INI
│   ├── bersih/               ← Taruh gambar area bersih
│   │   ├── gambar1.jpg
│   │   ├── gambar2.webp
│   │   └── ...
│   ├── tumpukan_ringan/      ← Taruh gambar sampah ringan
│   │   ├── gambar1.jpg
│   │   └── ...
│   └── tumpukan_parah/       ← Taruh gambar sampah parah
│       ├── gambar1.jpg
│       └── ...
├── app.py
├── src/
└── scripts/
```

### Cara Buat Folder:

**Windows:**
```bash
cd "Project Deteksi Tumpukan Sampah"
mkdir raw_data
mkdir raw_data\bersih
mkdir raw_data\tumpukan_ringan
mkdir raw_data\tumpukan_parah
```

**Atau manual:**
1. Buka folder "Project Deteksi Tumpukan Sampah"
2. Klik kanan → New Folder → Nama: `raw_data`
3. Masuk ke folder `raw_data`
4. Buat 3 folder: `bersih`, `tumpukan_ringan`, `tumpukan_parah`
5. Copy gambar ke masing-masing folder

---

## ✅ Opsi 2: Di Root Workspace

Taruh gambar di luar project (sejajar dengan folder project):

```
workspace/
├── bersih/                    ← Taruh gambar area bersih
│   ├── gambar1.jpg
│   └── ...
├── tumpukan_ringan/           ← Taruh gambar sampah ringan
│   └── ...
├── tumpukan_parah/            ← Taruh gambar sampah parah
│   └── ...
└── Project Deteksi Tumpukan Sampah/
    └── ...
```

---

## 📊 Rekomendasi Jumlah Gambar

| Kategori | Minimal | Ideal |
|----------|---------|-------|
| Bersih | 30 gambar | 100+ gambar |
| Tumpukan Ringan | 30 gambar | 100+ gambar |
| Tumpukan Parah | 30 gambar | 100+ gambar |

**Semakin banyak data = Model semakin akurat!**

---

## 🖼️ Format Gambar yang Didukung

- ✅ `.jpg` / `.jpeg`
- ✅ `.png`
- ✅ `.webp`

---

## 🔍 Contoh Gambar per Kategori

### 1. Bersih
- Jalan bersih tanpa sampah
- Taman yang rapi
- Trotoar bersih
- Area publik yang terawat

### 2. Tumpukan Ringan
- Sampah berserakan sedikit (1-5 item)
- 1-2 kantong sampah kecil
- Sampah di pinggir jalan (tidak menumpuk)
- Botol/plastik berserakan

### 3. Tumpukan Parah
- Tumpukan sampah besar
- TPS yang penuh/meluap
- Sampah berserakan banyak (10+ item)
- Illegal dumping
- Sampah menumpuk tinggi

---

## 🚀 Setelah Taruh Gambar

### 1. Prepare Dataset
```bash
cd "Project Deteksi Tumpukan Sampah"
python scripts/prepare_dataset.py
```

Script akan:
- ✅ Otomatis cari gambar di `raw_data/` atau di root workspace
- ✅ Copy ke folder `data/train`, `data/val`, `data/test`
- ✅ Split otomatis: 70% train, 15% val, 15% test

### 2. Training
```bash
python src/train.py
```

### 3. Jalankan Web
```bash
streamlit run app.py
```

---

## 📝 Checklist

- [ ] Buat folder `raw_data/bersih`, `raw_data/tumpukan_ringan`, `raw_data/tumpukan_parah`
- [ ] Download/kumpulkan minimal 30 gambar per kategori
- [ ] Copy gambar ke folder yang sesuai
- [ ] Jalankan `python scripts/prepare_dataset.py`
- [ ] Jalankan `python src/train.py`
- [ ] Jalankan `streamlit run app.py`

---

## 🌐 Sumber Download Gambar

1. **Google Images**
   - Search: "clean street", "garbage pile", "waste accumulation"
   - Klik kanan → Save image

2. **Kaggle Datasets**
   - https://www.kaggle.com/datasets
   - Search: "waste", "garbage", "trash"

3. **Unsplash** (Gratis)
   - https://unsplash.com/s/photos/garbage
   - https://unsplash.com/s/photos/clean-street

4. **Pexels** (Gratis)
   - https://www.pexels.com/search/garbage/
   - https://www.pexels.com/search/clean%20street/

5. **Foto Sendiri**
   - Ambil foto di lingkungan sekitar
   - Pastikan foto jelas dan fokus

---

## ❓ FAQ

**Q: Apakah nama file gambar harus spesifik?**
A: Tidak, nama file bebas. Yang penting ada di folder yang benar.

**Q: Apakah ukuran gambar harus sama?**
A: Tidak, script akan otomatis resize ke 224x224 saat training.

**Q: Boleh campur format (jpg, png, webp)?**
A: Boleh! Semua format didukung.

**Q: Gambar original akan dihapus?**
A: Tidak, hanya di-copy. Gambar original tetap aman.

---

**Selamat mengumpulkan data! 📸**
