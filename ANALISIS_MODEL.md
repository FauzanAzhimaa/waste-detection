# 📊 ANALISIS PERFORMA MODEL - Kampus 1 UNJANI Yogyakarta

**Generated:** 16 Desember 2025  
**Model:** waste_mobilenet.h5  
**Status:** 🔴 **CRITICAL - PERLU PERBAIKAN SEGERA**

---

## 🚨 MASALAH UTAMA

### **Akurasi Real: 40.54%** ❌
- Validation accuracy 93.75% **MISLEADING** (overfitting parah!)
- Test accuracy hanya **40.54%** (sangat rendah)
- Model **HANYA memprediksi "Tumpukan Parah"** untuk semua gambar!

### **Confusion Matrix:**
```
                    Predicted →
Actual ↓         Bersih  Tumpukan Parah  Tumpukan Ringan
-------------------------------------------------------
Bersih              0         13              0
Tumpukan Parah      0         15              0
Tumpukan Ringan     0          9              0
```

**Artinya:**
- ❌ Semua gambar "Bersih" diprediksi sebagai "Tumpukan Parah"
- ✅ Semua gambar "Tumpukan Parah" benar (tapi karena bias)
- ❌ Semua gambar "Tumpukan Ringan" diprediksi sebagai "Tumpukan Parah"

---

## 📉 ANALISIS DETAIL

### **1. Dataset Terlalu Kecil** 🔴 CRITICAL
```
Training Set:   164 gambar (Target: 900-1500)
Validation Set:  35 gambar
Test Set:        37 gambar
TOTAL:          236 gambar

Kekurangan: 736 gambar lagi!
```

### **2. Dataset Tidak Seimbang** 🟡 HIGH
```
Bersih:             57 gambar (34.8%)
Tumpukan Parah:     70 gambar (42.7%) ← Paling banyak
Tumpukan Ringan:    37 gambar (22.6%) ← Paling sedikit

Ratio: 1.89x (seharusnya < 1.2x)
```

### **3. Model Overfitting Parah** 🔴 CRITICAL
```
Validation Accuracy: 93.75% ← Terlihat bagus
Test Accuracy:       40.54% ← Realita buruk!

Gap: 53.21% (overfitting ekstrem!)
```

Model "menghafal" training data, bukan "belajar" pattern!

### **4. Bias ke Kategori Mayoritas**
Model cenderung memprediksi "Tumpukan Parah" karena:
- Kategori ini paling banyak (70 gambar)
- Dataset terlalu kecil untuk belajar perbedaan
- Model "main aman" dengan prediksi mayoritas

---

## 📊 PER-CLASS PERFORMANCE

### **Bersih:**
- Accuracy: 0.00% ❌
- Precision: 0.00% ❌
- Recall: 0.00% ❌
- F1-Score: 0.00% ❌
- **Status:** Model TIDAK BISA mendeteksi area bersih sama sekali!

### **Tumpukan Parah:**
- Accuracy: 100.00% ✅ (misleading!)
- Precision: 40.54% ⚠️
- Recall: 100.00% ✅
- F1-Score: 57.69% ⚠️
- **Status:** Benar karena bias, bukan karena belajar!

### **Tumpukan Ringan:**
- Accuracy: 0.00% ❌
- Precision: 0.00% ❌
- Recall: 0.00% ❌
- F1-Score: 0.00% ❌
- **Status:** Model TIDAK BISA mendeteksi tumpukan ringan!

---

## 💡 REKOMENDASI PERBAIKAN

### **PRIORITAS 1: Tambah Data** 🔴 CRITICAL

**Target Dataset:**
```
Bersih:             300-500 gambar (sekarang: 57)
Tumpukan Ringan:    300-500 gambar (sekarang: 37) ← PRIORITAS!
Tumpukan Parah:     300-500 gambar (sekarang: 70)

TOTAL TARGET: 900-1500 gambar
KEKURANGAN:   736-1264 gambar
```

**Cara Mengumpulkan:**
1. Gunakan script `scripts/data_collector.py`
2. Foto langsung di berbagai lokasi kampus
3. Berbagai waktu: pagi, siang, sore
4. Berbagai sudut: depan, samping, atas
5. Berbagai kondisi pencahayaan

**Fokus Khusus:**
- **Tumpukan Ringan:** Paling sedikit, perlu 263+ gambar lagi
- **Bersih:** Perlu 243+ gambar lagi
- **Tumpukan Parah:** Perlu 230+ gambar lagi

### **PRIORITAS 2: Balance Dataset** 🟡 HIGH

Pastikan setiap kategori punya jumlah gambar yang **hampir sama**:
```
Ideal Ratio: 1:1:1
Current Ratio: 1.5:1.9:1 (tidak seimbang!)
```

### **PRIORITAS 3: Retrain Model** 🟢 MEDIUM

Setelah data cukup:
1. Jalankan `scripts/prepare_dataset.py` untuk split ulang
2. Jalankan `src/train.py` dengan epochs lebih banyak (20-30)
3. Monitor validation loss untuk deteksi overfitting
4. Gunakan early stopping

### **PRIORITAS 4: Validasi Ulang** 🟢 MEDIUM

Setelah retrain:
1. Jalankan `src/model_analysis.py` lagi
2. Cek confusion matrix
3. Target accuracy: > 80% pada test set
4. Pastikan tidak ada bias ke satu kategori

---

## 🎯 TARGET IMPROVEMENT

### **Sekarang:**
```
Test Accuracy:        40.54% ❌
Bersih Detection:      0.00% ❌
Tumpukan Ringan:       0.00% ❌
Dataset Size:          236 gambar
```

### **Target Setelah Perbaikan:**
```
Test Accuracy:        > 80% ✅
Bersih Detection:     > 75% ✅
Tumpukan Ringan:      > 75% ✅
Dataset Size:         900-1500 gambar
```

---

## 📝 ACTION PLAN

### **Minggu 1-2: Data Collection**
- [ ] Kumpulkan 250 gambar "Bersih"
- [ ] Kumpulkan 270 gambar "Tumpukan Ringan" (prioritas!)
- [ ] Kumpulkan 230 gambar "Tumpukan Parah"
- [ ] Gunakan `scripts/data_collector.py` untuk organisir

### **Minggu 3: Retraining**
- [ ] Jalankan `scripts/prepare_dataset.py`
- [ ] Jalankan `src/train.py` dengan 20-30 epochs
- [ ] Monitor training progress
- [ ] Simpan model terbaik

### **Minggu 4: Validation**
- [ ] Jalankan `src/model_analysis.py`
- [ ] Cek improvement
- [ ] Test di real-world scenarios
- [ ] Deploy jika accuracy > 80%

---

## 🛠️ TOOLS YANG TERSEDIA

### **1. Data Collection Helper**
```bash
python scripts/data_collector.py
```
Fitur:
- Cek status dataset
- Rekomendasi pengumpulan data
- Organisir gambar baru
- Validasi gambar
- Generate laporan

### **2. Model Analysis**
```bash
python src/model_analysis.py
```
Fitur:
- Analisis distribusi dataset
- Evaluasi pada test set
- Confusion matrix
- Per-class metrics
- Confidence distribution
- Rekomendasi perbaikan

### **3. Training**
```bash
python src/train.py
```
Fitur:
- Transfer learning MobileNetV2
- Data augmentation
- 2-stage training
- Model checkpointing

---

## 📞 KESIMPULAN

**Status Saat Ini:** Model **TIDAK LAYAK** untuk production!

**Masalah Utama:**
1. Dataset terlalu kecil (236 vs 900-1500 target)
2. Overfitting parah (93% val vs 40% test)
3. Bias ke "Tumpukan Parah"
4. Tidak bisa deteksi "Bersih" dan "Tumpukan Ringan"

**Solusi:**
1. Kumpulkan 736+ gambar lagi
2. Balance dataset (sama rata per kategori)
3. Retrain model
4. Validasi ulang

**Timeline:** 3-4 minggu untuk perbaikan lengkap

**Catatan:** Model saat ini bisa digunakan untuk **DEMO/PROTOTYPE** saja, tapi harus dijelaskan keterbatasannya!

---

**Generated by:** Model Analysis Script  
**Date:** 16 Desember 2025  
**Report File:** `model_analysis_report.json`
