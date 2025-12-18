# ⚡ Quick Start: Download Raw Data dari Google Drive

## 🎯 **3 Langkah Mudah:**

### **1. Upload ke Google Drive** (5 menit)
```
1. Buka https://drive.google.com
2. Upload folder raw_data/
3. Right click → Share → Anyone with link
4. Copy link
```

### **2. Install gdown** (1 menit)
```bash
pip install gdown
```

### **3. Download** (5-10 menit)
```bash
python scripts/download_from_gdrive.py
```
Paste Google Drive URL → Done!

---

## 📖 **Dokumentasi Lengkap:**
- **`SETUP_GOOGLE_DRIVE.md`** - Panduan detail
- **`scripts/download_from_gdrive.py`** - Script download

---

## 💡 **Kenapa Pakai Google Drive?**

**Sebelum:**
```
Laptop A → raw_data (2GB)
Laptop B → Download manual → raw_data (2GB)
Laptop C → Download manual → raw_data (2GB)
Total: 6GB storage terpakai!
```

**Sesudah:**
```
Google Drive → raw_data (2GB)
Laptop A → Download saat perlu → Delete setelah training
Laptop B → Download saat perlu → Delete setelah training
Laptop C → Download saat perlu → Delete setelah training
Total: 2GB storage (hemat 4GB!)
```

**Plus:**
- ✅ Backup otomatis
- ✅ Akses dari mana saja
- ✅ Share dengan team
- ✅ No manual download

---

## 🚀 **Workflow:**

### **Collect Data:**
```bash
python scripts/data_collector.py
```

### **Upload to Google Drive:**
Drag & drop ke Google Drive

### **Download on Training Machine:**
```bash
python scripts/download_from_gdrive.py
```

### **Train Model:**
```bash
python scripts/prepare_dataset.py
python src/train.py
```

### **Deploy New Model:**
```bash
# Copy new model
cp models/waste_mobilenet.h5 models/waste_mobilenet_v2.h5

# Update app.py to use new model
# Deploy to Railway
railway up --detach
```

---

## ✅ **Done!**

Sekarang kamu bisa:
- ✅ Upload data ke Google Drive
- ✅ Download dari mana saja
- ✅ Train model tanpa download manual
- ✅ Hemat storage laptop

**Happy training! 🎉**
