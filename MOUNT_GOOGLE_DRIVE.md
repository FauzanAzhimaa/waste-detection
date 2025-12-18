# 🔗 Mount Google Drive - Akses Langsung Tanpa Download

## 🎯 **Tujuan:**
Akses `raw_data/` dari Google Drive **tanpa download** - seperti folder lokal biasa.

---

## ✅ **Option 1: Google Drive Desktop (Windows/Mac)**

### **Cara Kerja:**
Google Drive Desktop mount Google Drive sebagai drive lokal (seperti USB drive).

### **Setup:**

#### **1. Install Google Drive Desktop**
- Download: https://www.google.com/drive/download/
- Install dan login dengan Google account

#### **2. Configure Sync Mode**

**Stream Mode (Recommended):**
- File **tidak** download ke laptop
- Akses langsung dari cloud
- Hemat storage
- Butuh internet

**Mirror Mode:**
- File di-sync ke laptop
- Bisa akses offline
- Pakai storage laptop

**Cara setting:**
1. Klik icon Google Drive di taskbar/menu bar
2. Settings → Preferences
3. Pilih "Stream files" atau "Mirror files"

#### **3. Access di Code**

**Windows:**
```python
# Google Drive akan muncul sebagai drive G: (atau huruf lain)
raw_data_path = "G:/My Drive/raw_data"

# Atau
import os
drive_letter = "G:"  # Check di File Explorer
raw_data_path = os.path.join(drive_letter, "My Drive", "raw_data")
```

**Mac:**
```python
import os
username = os.getenv('USER')
email = "youremail@gmail.com"  # Your Google email

raw_data_path = f"/Users/{username}/Library/CloudStorage/GoogleDrive-{email}/My Drive/raw_data"

# Atau shortcut
raw_data_path = "~/Google Drive/My Drive/raw_data"
```

#### **4. Update Training Script**

Edit `scripts/prepare_dataset.py`:
```python
# Before
RAW_DATA_DIR = Path('raw_data')

# After (Windows)
RAW_DATA_DIR = Path('G:/My Drive/raw_data')

# After (Mac)
RAW_DATA_DIR = Path('~/Google Drive/My Drive/raw_data').expanduser()
```

#### **5. Train Model**
```bash
python scripts/prepare_dataset.py
python src/train.py
```

**Data dibaca langsung dari Google Drive!** ✅

---

## ✅ **Option 2: Google Colab (Cloud Training)**

### **Cara Kerja:**
Training di cloud dengan GPU gratis, akses Google Drive langsung.

### **Setup:**

#### **1. Upload Project ke Google Drive**
```
My Drive/
└── waste-detection/
    ├── raw_data/
    ├── scripts/
    ├── src/
    ├── models/
    └── requirements.txt
```

#### **2. Open Google Colab**
- Buka: https://colab.research.google.com
- File → Open notebook
- Upload → `notebooks/train_on_colab.ipynb`

#### **3. Enable GPU**
- Runtime → Change runtime type
- Hardware accelerator: **GPU**
- Save

#### **4. Run Cells**
```python
# Cell 1: Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Cell 2: Change directory
import os
os.chdir('/content/drive/MyDrive/waste-detection')

# Cell 3: Train
!python src/train.py
```

**Training dengan GPU, akses Drive langsung!** ✅

---

## 📊 **Comparison:**

| Method | Storage | Speed | Internet | GPU | Setup |
|--------|---------|-------|----------|-----|-------|
| **Google Drive Desktop** | Stream: 0GB<br>Mirror: Full | Fast | Required | No | Easy |
| **Google Colab** | 0GB | Very Fast | Required | Yes (Free!) | Medium |
| **Local Download** | Full | Fastest | Not required | Depends | Easy |

---

## 💡 **Recommendations:**

### **For Development (Laptop):**
✅ **Google Drive Desktop - Stream Mode**
- No storage used
- Access like local folder
- Auto sync

### **For Training (Heavy):**
✅ **Google Colab**
- Free GPU (10x faster!)
- No laptop resources used
- Direct Drive access

### **For Production (Railway):**
❌ **Don't use Google Drive**
- Use Cloudinary for images
- Use PostgreSQL for data
- Already implemented! ✅

---

## 🔧 **Troubleshooting:**

### **Google Drive Desktop not showing**
1. Check if Google Drive Desktop is running
2. Check drive letter in File Explorer (Windows)
3. Restart Google Drive Desktop

### **Permission denied**
1. Check folder permissions in Google Drive
2. Make sure you're logged in
3. Try re-mount

### **Slow access**
1. Check internet connection
2. Use Mirror mode instead of Stream
3. Or download specific folders only

---

## 📝 **Example: Training with Mounted Drive**

### **Windows:**
```python
# prepare_dataset.py
from pathlib import Path

# Mount point
GOOGLE_DRIVE = Path('G:/My Drive')
RAW_DATA_DIR = GOOGLE_DRIVE / 'waste-detection' / 'raw_data'
OUTPUT_DIR = GOOGLE_DRIVE / 'waste-detection' / 'data'

# Rest of code stays the same
# Data will be read from Google Drive directly!
```

### **Mac:**
```python
# prepare_dataset.py
from pathlib import Path
import os

# Mount point
username = os.getenv('USER')
GOOGLE_DRIVE = Path(f'/Users/{username}/Google Drive/My Drive')
RAW_DATA_DIR = GOOGLE_DRIVE / 'waste-detection' / 'raw_data'
OUTPUT_DIR = GOOGLE_DRIVE / 'waste-detection' / 'data'

# Rest of code stays the same
```

### **Google Colab:**
```python
# Already mounted at /content/drive/MyDrive
RAW_DATA_DIR = Path('/content/drive/MyDrive/waste-detection/raw_data')
OUTPUT_DIR = Path('/content/drive/MyDrive/waste-detection/data')
```

---

## ✅ **Benefits:**

### **No Download Needed:**
```
Before: Upload to Drive → Download to laptop → Train
After:  Upload to Drive → Train directly
```

### **Save Storage:**
```
Before: 2GB on Drive + 2GB on laptop = 4GB total
After:  2GB on Drive only = 2GB total
```

### **Auto Sync:**
```
Update on Drive → Instantly available on laptop
Add new images → No re-download needed
```

### **Team Collaboration:**
```
Team member adds data → Everyone sees it instantly
No need to share files manually
```

---

## 🚀 **Quick Start:**

### **Windows:**
1. Install Google Drive Desktop
2. Login
3. Wait for sync
4. Check drive letter (usually G:)
5. Update code: `RAW_DATA_DIR = Path('G:/My Drive/raw_data')`
6. Train: `python src/train.py`

### **Mac:**
1. Install Google Drive Desktop
2. Login
3. Wait for sync
4. Update code: `RAW_DATA_DIR = Path('~/Google Drive/My Drive/raw_data').expanduser()`
5. Train: `python src/train.py`

### **Google Colab:**
1. Upload project to Google Drive
2. Open `notebooks/train_on_colab.ipynb`
3. Run all cells
4. Done!

---

## 📚 **Resources:**

- **Google Drive Desktop:** https://www.google.com/drive/download/
- **Google Colab:** https://colab.research.google.com
- **Colab Notebook:** `notebooks/train_on_colab.ipynb`

---

**Sekarang kamu bisa akses raw_data langsung dari Google Drive tanpa download!** 🎉
