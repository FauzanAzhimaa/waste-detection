# 🚀 Panduan Cepat - Waste Vision

## Langkah-Langkah Eksekusi

### ✅ Step 1: Install Dependencies
```bash
cd "Project Deteksi Tumpukan Sampah"
pip install -r requirements.txt
```

### ✅ Step 2: Prepare Dataset
```bash
python scripts/prepare_dataset.py
```

**Output:**
- Dataset akan di-copy dari folder root (`../bersih`, `../tumpukan_ringan`, `../tumpukan_parah`)
- Otomatis split: 70% train, 15% val, 15% test
- Tersimpan di folder `data/train`, `data/val`, `data/test`

### ✅ Step 3: Training Model
```bash
python src/train.py
```

**Output:**
- Model tersimpan: `models/waste_mobilenet.h5`
- Training plot: `outputs/training_plot.png`
- Datasheet: `outputs/training_datasheet_*.json`

**Estimasi waktu:** 10-30 menit (tergantung hardware)

### ✅ Step 4: Jalankan Web App
```bash
streamlit run app.py
```

**Buka browser:** `http://localhost:8501`

---

## 📱 Cara Pakai Web App

### 1️⃣ Deteksi Baru
1. Isi **Nama Lokasi** di sidebar (contoh: "Jl. Sudirman Blok A")
2. Pilih **Kecamatan**
3. **Upload gambar** sampah
4. Lihat hasil:
   - Status deteksi
   - Confidence score
   - **Grad-CAM heatmap** (area merah = sampah terdeteksi)
   - Rekomendasi penanganan
5. Klik **"💾 Simpan Record"**

### 2️⃣ Riwayat & Heatmap
- Lihat statistik total deteksi
- **Priority heatmap** per lokasi
- Download data CSV

---

## 📊 Struktur Data Training

**STEP 0: Taruh gambar di folder `raw_data/`**

```
Project Deteksi Tumpukan Sampah/
├── raw_data/                  ← BUAT FOLDER INI DULU!
│   ├── bersih/               ← Taruh gambar area bersih (min 30)
│   ├── tumpukan_ringan/      ← Taruh gambar sampah ringan (min 30)
│   └── tumpukan_parah/       ← Taruh gambar sampah parah (min 30)
├── app.py
└── scripts/
```

**Cara buat folder (Windows):**
```bash
cd "Project Deteksi Tumpukan Sampah"
mkdir raw_data
mkdir raw_data\bersih
mkdir raw_data\tumpukan_ringan
mkdir raw_data\tumpukan_parah
```

**Setelah prepare_dataset.py:**
```
Project Deteksi Tumpukan Sampah/
└── data/                      ← Dibuat otomatis
    ├── train/                 ← 70% data
    │   ├── bersih/
    │   ├── tumpukan_ringan/
    │   └── tumpukan_parah/
    ├── val/                   ← 15% data
    └── test/                  ← 15% data
```

**📖 Lihat:** `CARA_TARUH_DATA.md` untuk panduan lengkap

---

## 🎯 Output yang Dihasilkan

### Training
- ✅ `models/waste_mobilenet.h5` - Model terlatih
- ✅ `outputs/training_plot.png` - Grafik accuracy & loss
- ✅ `outputs/training_datasheet_*.json` - Metadata training
- ✅ `outputs/confusion_matrix.png` - Confusion matrix

### Deteksi
- ✅ `outputs/records.csv` - Record semua deteksi

**Format CSV:**
```
timestamp,filename,location,district,detection,confidence,priority_score,notes
2024-01-15 10:30:00,sampah1.jpg,Jl. Sudirman,Kecamatan A,tumpukan_parah,0.9523,1.0,Perlu segera ditangani
```

---

## 🔥 Fitur Unggulan

### 1. Grad-CAM Heatmap
Visualisasi area yang dideteksi model:
- **Merah** = Area dengan sampah tinggi
- **Biru** = Area bersih
- Membantu verifikasi apakah model deteksi dengan benar

### 2. Sistem Rekomendasi
Otomatis memberikan:
- ✅ Prioritas (Rendah/Sedang/Tinggi)
- ✅ Timeline penanganan
- ✅ Resources yang dibutuhkan
- ✅ Aksi yang harus dilakukan

### 3. Priority Heatmap per Lokasi
- Tracking lokasi mana yang paling urgent
- Visualisasi bar chart priority score
- Export data untuk laporan

---

## ⚠️ Troubleshooting

### Error: Model tidak ditemukan
```bash
python src/train.py
```

### Error: Data tidak ditemukan
```bash
python scripts/prepare_dataset.py
```

### Error: Module not found
```bash
pip install -r requirements.txt
```

---

## 📞 Checklist Sebelum Demo

- [ ] Dependencies terinstall
- [ ] Dataset sudah di-prepare
- [ ] Model sudah di-training
- [ ] Web app bisa dibuka
- [ ] Test upload 1 gambar
- [ ] Test simpan record
- [ ] Test lihat riwayat

---

**Selamat mencoba! 🎉**
