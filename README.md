# 🗑️ Waste Vision - Sistem Deteksi Tumpukan Sampah

Sistem deteksi tumpukan sampah berbasis CNN (Convolutional Neural Network) dengan visualisasi Grad-CAM heatmap dan rekomendasi penanganan.

## 📋 Fitur

- ✅ Deteksi 3 kategori: **Bersih**, **Tumpukan Ringan**, **Tumpukan Parah**
- 🔥 **Grad-CAM Heatmap** - Visualisasi area yang terdeteksi
- 📍 **Input Lokasi** - Tracking per zona/lokasi
- 📊 **Rekomendasi Penanganan** - Aksi, timeline, dan resources
- 📈 **Priority Heatmap** - Visualisasi prioritas per lokasi
- 💾 **Riwayat Deteksi** - Logging dan export CSV
- 📄 **Training Datasheet** - Dokumentasi hasil training

## 🏗️ Struktur Project

```
Project Deteksi Tumpukan Sampah/
├── app.py                      # Web application (Streamlit)
├── requirements.txt            # Dependencies
├── data/                       # Dataset (auto-generated)
│   ├── train/
│   │   ├── bersih/
│   │   ├── tumpukan_ringan/
│   │   └── tumpukan_parah/
│   ├── val/
│   └── test/
├── models/                     # Trained models
│   └── waste_mobilenet.h5
├── outputs/                    # Results & logs
│   ├── records.csv
│   ├── training_datasheet_*.json
│   └── training_plot.png
├── src/                        # Source code
│   ├── train.py               # Training script
│   ├── gradcam.py             # Grad-CAM visualization
│   ├── recommendations.py      # Recommendation system
│   ├── training_datasheet.py  # Datasheet generator
│   ├── evaluate.py            # Model evaluation
│   └── utils.py               # Utilities
└── scripts/                    # Helper scripts
    ├── prepare_dataset.py     # Dataset preparation
    ├── split_dataset.py       # Dataset splitting
    └── convert_webp.py        # Format conversion
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd "Project Deteksi Tumpukan Sampah"
pip install -r requirements.txt
```

### 2. Prepare Dataset

Pastikan gambar sudah ada di folder root:
- `../bersih/` - Gambar area bersih
- `../tumpukan_ringan/` - Gambar tumpukan ringan
- `../tumpukan_parah/` - Gambar tumpukan parah

Jalankan script untuk organize dataset:

```bash
python scripts/prepare_dataset.py
```

Script ini akan:
- Copy gambar dari folder root ke `data/`
- Split otomatis: 70% train, 15% val, 15% test
- Support format: `.webp`, `.jpg`, `.jpeg`, `.png`

### 3. Training Model

```bash
python src/train.py
```

Training akan:
- Menggunakan MobileNetV2 (transfer learning)
- 2 stage training (freeze → fine-tune)
- Generate plot training
- Generate datasheet otomatis
- Save model ke `models/waste_mobilenet.h5`

### 4. Jalankan Web Application

```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

## 📊 Cara Menggunakan Web App

### Menu: 🔍 Deteksi Baru

1. **Input Lokasi** (sidebar):
   - Nama Lokasi/Zona
   - Kecamatan
   - Catatan tambahan (opsional)

2. **Upload Gambar**:
   - Format: JPG, PNG, JPEG, WEBP
   - Klik "Browse files" atau drag & drop

3. **Hasil Deteksi**:
   - Status deteksi (Bersih/Ringan/Parah)
   - Confidence score
   - Probabilitas per kelas
   - **Grad-CAM Heatmap** (area merah = terdeteksi sampah)

4. **Rekomendasi**:
   - Prioritas penanganan
   - Timeline
   - Resources yang dibutuhkan
   - Aksi yang direkomendasikan

5. **Simpan Record**:
   - Klik tombol "💾 Simpan Record"
   - Data tersimpan di `outputs/records.csv`

### Menu: 📈 Riwayat & Heatmap

- **Statistik**: Total deteksi per kategori
- **Priority Heatmap**: Visualisasi prioritas per lokasi
- **Distribusi Deteksi**: Chart distribusi kategori
- **Riwayat Lengkap**: Tabel semua deteksi
- **Download CSV**: Export data untuk analisis

## 🎯 Sistem Rekomendasi

### Bersih ✅
- **Prioritas**: Rendah (0.1)
- **Timeline**: Monitoring rutin 7 hari
- **Resources**: 1 petugas monitoring
- **Aksi**: Pertahankan kebersihan, monitoring rutin

### Tumpukan Ringan ⚠️
- **Prioritas**: Sedang (0.6)
- **Timeline**: 24-48 jam
- **Resources**: 2-3 petugas, 1 kendaraan
- **Aksi**: Pembersihan, tambah tempat sampah, sosialisasi

### Tumpukan Parah 🚨
- **Prioritas**: Tinggi (1.0)
- **Timeline**: SEGERA dalam 24 jam
- **Resources**: 5+ petugas, 2+ kendaraan, alat berat
- **Aksi**: Pembersihan darurat, koordinasi Dinas, CCTV, laporan

## 📁 Dataset

### Struktur yang Dibutuhkan

Letakkan gambar di folder root workspace:

```
workspace/
├── bersih/
│   ├── download.webp
│   ├── download (1).webp
│   └── ...
├── tumpukan_ringan/
│   ├── OIP.webp
│   ├── OIP (1).webp
│   └── ...
└── tumpukan_parah/
    ├── download.jpg
    ├── images.jpg
    └── ...
```

### Format Gambar yang Didukung

- `.webp` ✅
- `.jpg` / `.jpeg` ✅
- `.png` ✅

## 🔧 Scripts Tambahan

### Evaluate Model

```bash
python src/evaluate.py
```

Generate confusion matrix dan classification report.

### Generate Datasheet

```bash
python src/training_datasheet.py
```

Generate datasheet tanpa training ulang.

### Convert WebP to JPG (opsional)

```bash
python scripts/convert_webp.py
```

## 📊 Output Files

### Training Outputs
- `models/waste_mobilenet.h5` - Trained model
- `outputs/training_plot.png` - Accuracy & loss curves
- `outputs/training_datasheet_*.json` - Training metadata
- `outputs/training_summary_*.csv` - Dataset summary
- `outputs/confusion_matrix.png` - Confusion matrix

### Detection Outputs
- `outputs/records.csv` - Detection records dengan kolom:
  - timestamp
  - filename
  - location
  - district
  - detection (bersih/ringan/parah)
  - confidence
  - priority_score
  - notes

## 🛠️ Troubleshooting

### Model belum tersedia
```
⚠️ Model belum tersedia. Silakan training model terlebih dahulu.
```
**Solusi**: Jalankan `python src/train.py`

### Dataset tidak ditemukan
```
FileNotFoundError: data/train not found
```
**Solusi**: Jalankan `python scripts/prepare_dataset.py`

### Import error
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Solusi**: Install dependencies `pip install -r requirements.txt`

## 📝 Requirements

- Python 3.8+
- TensorFlow 2.10+
- Streamlit
- OpenCV
- Pandas, NumPy, Matplotlib, Seaborn
- Pillow

## 🎓 Model Architecture

- **Base Model**: MobileNetV2 (ImageNet pretrained)
- **Input Size**: 224x224x3
- **Output**: 3 classes (softmax)
- **Training Strategy**: 
  1. Stage 1: Freeze base, train head (10 epochs)
  2. Stage 2: Fine-tune last 30 layers (10 epochs)
- **Augmentation**: Rotation, shift, zoom, flip

## 📈 Performance Metrics

Setelah training, lihat:
- `outputs/training_plot.png` - Training curves
- `outputs/confusion_matrix.png` - Confusion matrix
- `outputs/training_datasheet_*.json` - Detailed metrics

## 🤝 Contributing

Untuk menambah fitur atau improve model:
1. Tambah data training di folder yang sesuai
2. Re-run `prepare_dataset.py`
3. Re-train model dengan `train.py`
4. Test di web app

## 📄 License

Educational Project - Deteksi Tumpukan Sampah

---

**Waste Vision** - Sistem Deteksi Tumpukan Sampah Berbasis CNN
