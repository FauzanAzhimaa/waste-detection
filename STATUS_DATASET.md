# 📊 STATUS DATASET - Kampus 1 UNJANI Yogyakarta

**Updated:** 16 Desember 2025  
**Status:** 🔴 CRITICAL - Perlu Tambah Data

---

## ✅ **CLEANING SELESAI!**

### **Hasil Cleaning:**
```
Total diperiksa:     118 gambar
Gambar kecil:         66 gambar (56%)
Dipindahkan ke:      raw_data_backup_small/
Gambar valid:         52 gambar (44%)
```

### **Gambar yang Dipindahkan:**
- **Bersih:** 1 gambar kecil
- **Tumpukan Ringan:** 16 gambar kecil
- **Tumpukan Parah:** 49 gambar kecil

**Lokasi Backup:** `raw_data_backup_small/`

---

## 📊 **STATUS DATASET SAAT INI**

### **Setelah Cleaning:**

```
┌─────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Kategori            │ Sekarang │ Target   │ Progress │ Kurang   │
├─────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ Bersih              │    40    │   300    │  13.3%   │   260    │
│ Tumpukan Ringan     │    11    │   300    │   3.7%   │   289    │
│ Tumpukan Parah      │     1    │   300    │   0.3%   │   299    │
├─────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ TOTAL               │    52    │   900    │   5.8%   │   848    │
└─────────────────────┴──────────┴──────────┴──────────┴──────────┘
```

### **Progress Bar:**
```
Bersih:           [█████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 13.3%
Tumpukan Ringan:  [█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  3.7%
Tumpukan Parah:   [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  0.3%
```

---

## 🚨 **PRIORITAS PENGUMPULAN DATA**

### **Urutan Prioritas:**

1. **🔴 CRITICAL: Tumpukan Parah** (hanya 1 gambar!)
   - Target: 299 gambar lagi
   - Tips: Foto area dengan banyak sampah menumpuk

2. **🔴 CRITICAL: Tumpukan Ringan** (hanya 11 gambar!)
   - Target: 289 gambar lagi
   - Tips: Foto area dengan sedikit sampah (1-5 item)

3. **🟡 HIGH: Bersih** (40 gambar)
   - Target: 260 gambar lagi
   - Tips: Foto area kampus yang bersih dan rapi

---

## 📸 **PANDUAN FOTO**

### **Spesifikasi Minimum:**
- ✅ Resolusi: **≥224x224 pixels** (idealnya 720p atau 1080p)
- ✅ Format: JPG, PNG, WEBP
- ✅ Ukuran file: < 16MB
- ✅ Pencahayaan: Cukup terang (tidak gelap)
- ✅ Fokus: Jelas (tidak blur)

### **Tips Pengambilan Foto:**

**Untuk "Bersih":**
- Area kampus yang bersih dan rapi
- Tidak ada sampah terlihat
- Berbagai lokasi: kelas, koridor, taman, parkiran
- Berbagai sudut dan pencahayaan

**Untuk "Tumpukan Ringan":**
- Area dengan sedikit sampah (1-5 item)
- Sampah berserakan tapi belum menumpuk
- Kondisi yang masih mudah dibersihkan
- Berbagai jenis sampah: plastik, kertas, botol

**Untuk "Tumpukan Parah":**
- Area dengan banyak sampah menumpuk
- Tumpukan sampah yang jelas terlihat
- Kondisi yang perlu pembersihan menyeluruh
- Berbagai tingkat keparahan

### **Lokasi Rekomendasi di Kampus:**
- Ruang Kelas (2H, 2G, 3A, dll)
- Lab Komputer (3A, 3B)
- Lab Bahasa
- Kantin
- Perpustakaan
- Masjid
- Parkiran Motor & Mobil
- Taman Depan & Belakang
- Koridor Lantai 1, 2, 3
- Toilet Lantai 1, 2, 3
- Area Ruang Dosen
- Aula

### **Waktu Pengambilan:**
- Pagi (07:00 - 10:00)
- Siang (10:00 - 14:00)
- Sore (14:00 - 17:00)

---

## 🛠️ **TOOLS YANG TERSEDIA**

### **1. Auto Clean Small Images** (Sudah Dijalankan ✅)
```bash
python scripts/auto_clean_small_images.py
```
Otomatis pindahkan gambar <224x224 ke backup.

### **2. Data Collector** (Dengan Auto-Validation)
```bash
python scripts/data_collector.py
```
Fitur baru:
- ✅ Auto-reject gambar kecil (<224x224)
- ✅ Pindahkan otomatis ke backup/rejected
- ✅ Validasi format dan ukuran
- ✅ Organisir gambar baru

### **3. Check Status**
```bash
python -c "from scripts.data_collector import DataCollector; dc = DataCollector(); dc.check_current_status()"
```

---

## 📋 **WORKFLOW PENGUMPULAN DATA**

### **Step 1: Ambil Foto di Kampus** 📸
- Gunakan HP (minimal 720p)
- Foto berbagai lokasi dan kondisi
- Simpan semua foto di satu folder

### **Step 2: Transfer ke Komputer** 💻
- Copy semua foto ke folder, misal: `D:\foto_kampus`

### **Step 3: Organisir dengan Data Collector** 📂
```bash
python scripts/data_collector.py
# Pilih menu 3: Organisir gambar baru
# Masukkan path folder: D:\foto_kampus
```

Script akan:
- ✅ Cek ukuran gambar otomatis
- ❌ Reject gambar <224x224 (pindah ke backup)
- ✅ Tanya kategori untuk gambar valid
- ✅ Copy ke folder yang sesuai

### **Step 4: Cek Progress** 📊
```bash
python scripts/data_collector.py
# Pilih menu 1: Cek status dataset
```

### **Step 5: Ulangi Sampai Target Tercapai** 🔄
Target: 300 gambar per kategori (900 total)

---

## 🎯 **TARGET & TIMELINE**

### **Minggu 1-2: Pengumpulan Data Intensif**
- [ ] Kumpulkan 150 foto "Tumpukan Parah"
- [ ] Kumpulkan 150 foto "Tumpukan Ringan"
- [ ] Kumpulkan 130 foto "Bersih"
- **Target:** 430 gambar (total 482)

### **Minggu 3: Lanjutan Pengumpulan**
- [ ] Kumpulkan 149 foto "Tumpukan Parah" (total 300)
- [ ] Kumpulkan 139 foto "Tumpukan Ringan" (total 300)
- [ ] Kumpulkan 130 foto "Bersih" (total 300)
- **Target:** 900 gambar total

### **Minggu 4: Retrain & Validasi**
- [ ] Jalankan `scripts/prepare_dataset.py`
- [ ] Jalankan `src/train.py`
- [ ] Jalankan `src/model_analysis.py`
- [ ] Target accuracy: >80%

---

## 📞 **KESIMPULAN**

**Status Saat Ini:**
- ✅ Cleaning selesai (66 gambar kecil dipindahkan)
- ✅ Dataset bersih (52 gambar valid)
- ❌ Masih sangat kurang (perlu 848 gambar lagi!)

**Next Steps:**
1. 📸 Mulai foto di kampus (prioritas: Tumpukan Parah & Ringan)
2. 📂 Organisir dengan data_collector.py (auto-validation aktif)
3. 📊 Monitor progress secara berkala
4. 🔄 Retrain setelah data cukup (≥300 per kategori)

**Auto-Validation Aktif:**
- ✅ Gambar baru akan otomatis dicek ukurannya
- ✅ Gambar <224x224 otomatis di-reject
- ✅ Hanya gambar valid yang masuk dataset

---

**Generated:** 16 Desember 2025  
**Tools:** auto_clean_small_images.py, data_collector.py (updated)
