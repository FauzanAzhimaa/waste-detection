# 🚀 Quick Start: Training YOLOv8

## 📋 Langkah Cepat (30 menit setup + 1-2 jam training)

### 1️⃣ Upload Notebook ke Google Colab

1. Buka: https://colab.research.google.com
2. File → Upload notebook
3. Pilih: `notebooks/train_yolo_detection.ipynb`
4. Runtime → Change runtime type → **GPU (T4)**

### 2️⃣ Dapatkan API Key Roboflow

1. Buka: https://app.roboflow.com/settings/api
2. Copy API key (contoh: `aBcDeFgHiJkLmNoPqRsTuVwXyZ123456`)

### 3️⃣ Update Notebook

Di **Step 3** (Download Dataset), ganti:
```python
rf = Roboflow(api_key="YOUR_API_KEY")  # ← Paste API key kamu di sini
```

Jadi:
```python
rf = Roboflow(api_key="aBcDeFgHiJkLmNoPqRsTuVwXyZ123456")  # ← API key kamu
```

### 4️⃣ Run Training

1. **Run all cells**: Runtime → Run all (atau Ctrl+F9)
2. **Tunggu proses**:
   - Install dependencies: ~2 menit
   - Download dataset: ~5 menit
   - Training: ~1-2 jam (100 epochs)
3. **Monitor progress**: Lihat loss dan mAP di output

### 5️⃣ Download Model

Setelah training selesai:
1. Klik folder icon di sidebar kiri
2. Navigate ke: `runs/detect/waste_detection/weights/`
3. Klik kanan `best.pt` → Download
4. Rename jadi: `waste_yolo_best.pt`
5. Copy ke folder project: `models/waste_yolo_best.pt`

### 6️⃣ Beritahu Saya!

Setelah model downloaded, beritahu saya. Saya akan:
- ✅ Integrasi YOLO ke app.py
- ✅ Update frontend
- ✅ Test dan deploy

---

## 🎯 Expected Training Output

```
Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
  1/100      2.1G      1.234      2.345      1.567        128        640
  2/100      2.1G      1.123      2.234      1.456        128        640
  ...
 50/100      2.1G      0.456      0.789      0.234        128        640
 ...
100/100      2.1G      0.234      0.456      0.123        128        640

✅ Training completed!
📊 mAP50: 0.856
📊 mAP50-95: 0.623
```

---

## ⚡ Tips untuk Training Lebih Cepat

### Kurangi Epochs (untuk testing)
```python
results = model.train(
    data=str(data_yaml),
    epochs=50,  # ← Ubah dari 100 ke 50
    ...
)
```

### Gunakan GPU Lebih Kuat (jika tersedia)
- Runtime → Change runtime type → **A100 GPU** (jika punya Colab Pro)
- Training bisa 3x lebih cepat!

### Reduce Image Size (untuk memory)
```python
results = model.train(
    data=str(data_yaml),
    imgsz=416,  # ← Ubah dari 640 ke 416
    ...
)
```

---

## 🐛 Troubleshooting

### "Out of Memory" Error?
```python
# Kurangi batch size
results = model.train(
    batch=8,  # ← Ubah dari 16 ke 8
    ...
)
```

### API Key Invalid?
- Pastikan copy API key dengan benar (tidak ada spasi)
- Login ulang ke Roboflow
- Generate API key baru

### Dataset Download Gagal?
- Check internet connection
- Restart runtime: Runtime → Restart runtime
- Run ulang cell download

---

## 📊 Hasil yang Diharapkan

Setelah training, kamu akan punya:
- ✅ Model file: `best.pt` (~6MB)
- ✅ Training curves: loss, mAP, precision, recall
- ✅ Confusion matrix
- ✅ Sample predictions dengan bounding boxes

Model ini bisa detect:
- 🗑️ Berbagai jenis sampah
- 📦 Multiple objects dalam 1 gambar
- 📍 Lokasi spesifik (bounding boxes)
- 🎯 Confidence score per object

---

**Ready to start?** Upload notebook ke Colab dan mulai training! 🚀
