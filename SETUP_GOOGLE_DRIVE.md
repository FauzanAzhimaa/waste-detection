# ☁️ Setup Google Drive untuk Raw Data

## 🎯 **Tujuan:**
Download `raw_data/` langsung dari Google Drive tanpa perlu download manual ke laptop.

**Keuntungan:**
- ✅ Tidak perlu download manual
- ✅ Hemat storage laptop
- ✅ Bisa akses dari mana saja
- ✅ Backup otomatis
- ✅ Easy sharing dengan tim

---

## 📤 **Step 1: Upload ke Google Drive**

### **Option A: Via Browser (Mudah)**

1. Buka https://drive.google.com
2. Klik **"New"** → **"Folder upload"**
3. Pilih folder `raw_data/` dari laptop
4. Tunggu upload selesai (tergantung ukuran)

### **Option B: Via Google Drive Desktop (Cepat)**

1. Install Google Drive Desktop
2. Drag & drop folder `raw_data/` ke Google Drive folder
3. Tunggu sync selesai

---

## 🔗 **Step 2: Share Folder**

1. Right click folder `raw_data` di Google Drive
2. Klik **"Share"**
3. Klik **"Change to anyone with the link"**
4. Set permission: **"Viewer"** (read-only)
5. Klik **"Copy link"**
6. Save link ini!

**Example link:**
```
https://drive.google.com/drive/folders/1ABC123xyz456...
```

---

## 📥 **Step 3: Download dari Google Drive**

### **Install gdown:**
```bash
pip install gdown
```

### **Method 1: Interactive Script**
```bash
python scripts/download_from_gdrive.py
```

Lalu:
1. Ketik `y` untuk download
2. Paste Google Drive folder URL
3. Enter output directory (default: `raw_data`)
4. Tunggu download selesai

### **Method 2: Direct Command**
```bash
# Download entire folder
gdown --folder "YOUR_GOOGLE_DRIVE_FOLDER_URL" -O raw_data

# Example:
gdown --folder "https://drive.google.com/drive/folders/1ABC123xyz..." -O raw_data
```

### **Method 3: Python Script**
```python
import gdown

# Your Google Drive folder URL
folder_url = "https://drive.google.com/drive/folders/1ABC123xyz..."

# Download
gdown.download_folder(url=folder_url, output='raw_data', quiet=False)
```

---

## 🔧 **Troubleshooting:**

### **Error: "Permission denied"**
**Cause:** Folder tidak di-share atau permission salah

**Solution:**
1. Check folder sharing settings
2. Make sure: "Anyone with the link can view"
3. Try copy link lagi

### **Error: "Too many files"**
**Cause:** Google Drive rate limit

**Solution:**
1. Tunggu 1-2 jam
2. Atau download per subfolder:
   ```bash
   gdown --folder "URL_BERSIH" -O raw_data/bersih
   gdown --folder "URL_TUMPUKAN_RINGAN" -O raw_data/tumpukan_ringan
   gdown --folder "URL_TUMPUKAN_PARAH" -O raw_data/tumpukan_parah
   ```

### **Error: "gdown not found"**
**Cause:** gdown belum ter-install

**Solution:**
```bash
pip install gdown
# atau
pip install --upgrade gdown
```

---

## 📊 **Struktur Folder di Google Drive:**

```
My Drive/
└── raw_data/
    ├── bersih/
    │   ├── img001.jpg
    │   ├── img002.jpg
    │   └── ...
    ├── tumpukan_ringan/
    │   ├── img001.jpg
    │   └── ...
    └── tumpukan_parah/
        ├── img001.jpg
        └── ...
```

**Share link untuk:**
- Entire `raw_data/` folder → Download semua
- Individual subfolders → Download per kategori

---

## 🚀 **Workflow Training dengan Google Drive:**

### **1. Collect Data**
```bash
# Collect new images
python scripts/data_collector.py
```

### **2. Upload to Google Drive**
- Drag & drop ke Google Drive
- Atau sync via Google Drive Desktop

### **3. Download on Another Machine**
```bash
# On training machine (laptop/colab)
python scripts/download_from_gdrive.py
```

### **4. Prepare Dataset**
```bash
python scripts/prepare_dataset.py
```

### **5. Train Model**
```bash
python src/train.py
```

---

## 💡 **Tips:**

### **For Large Datasets:**
1. **Compress before upload:**
   ```bash
   # Zip folder
   zip -r raw_data.zip raw_data/
   
   # Upload zip to Google Drive
   # Download and extract
   gdown "FILE_ID" -O raw_data.zip
   unzip raw_data.zip
   ```

2. **Use Google Colab:**
   - Mount Google Drive directly
   - No download needed!
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   
   # Access files
   raw_data_path = '/content/drive/MyDrive/raw_data'
   ```

### **For Team Collaboration:**
1. Share folder dengan team
2. Everyone can download dengan same link
3. Update data → everyone re-download

### **For Backup:**
1. Keep original di Google Drive
2. Download only when needed
3. Delete local copy after training
4. Re-download next time

---

## 📚 **Alternative: Google Colab**

Jika mau training di cloud (gratis GPU!):

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Set path
import os
os.chdir('/content/drive/MyDrive/waste-detection')

# Run training
!python src/train.py
```

**Keuntungan:**
- ✅ Free GPU (faster training)
- ✅ No download needed
- ✅ Direct access to Google Drive
- ✅ Save model back to Drive

---

## 🔗 **Useful Links:**

- **gdown GitHub:** https://github.com/wkentaro/gdown
- **Google Drive:** https://drive.google.com
- **Google Colab:** https://colab.research.google.com

---

## ✅ **Checklist:**

- [ ] Upload `raw_data/` to Google Drive
- [ ] Share folder (Anyone with link can view)
- [ ] Copy folder URL
- [ ] Install gdown: `pip install gdown`
- [ ] Test download: `python scripts/download_from_gdrive.py`
- [ ] Verify files downloaded correctly
- [ ] Ready for training!

---

**Happy training! 🚀**
