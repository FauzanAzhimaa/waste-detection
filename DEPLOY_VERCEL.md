# 🚀 Deploy ke Vercel - Panduan Lengkap

## ⚠️ **PERINGATAN PENTING**

### **Vercel TIDAK IDEAL untuk project ini karena:**
1. ❌ TensorFlow + Model = ~600MB (Vercel limit: 250MB)
2. ❌ Cold start sangat lambat (10-30 detik)
3. ❌ File upload tidak persistent (serverless)
4. ❌ Timeout 10 detik (prediksi bisa lebih lama)

### **REKOMENDASI ALTERNATIF:**
- ✅ **Railway.app** - Unlimited size, Docker support
- ✅ **Render.com** - Free tier, persistent storage
- ✅ **Google Cloud Run** - Auto-scaling, pay as you go
- ✅ **Heroku** - Classic, reliable

---

## 📋 **JIKA TETAP INGIN VERCEL**

### **Persiapan:**

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login ke Vercel**
```bash
vercel login
```

3. **Buat akun di vercel.com** (jika belum punya)

---

### **Langkah Deploy:**

#### **1. Bersihkan Project**
```bash
# Hapus file besar yang tidak perlu
rm -rf .venv
rm -rf raw_data
rm -rf raw_data_backup_small
rm -rf uploads/*.jpeg
rm -rf uploads/*.jpg
```

#### **2. Cek Ukuran Model**
```bash
# Model harus < 50MB untuk Vercel
ls -lh models/waste_mobilenet.h5
```

Jika > 50MB, compress model atau gunakan platform lain!

#### **3. Deploy**
```bash
vercel
```

Ikuti prompt:
- Set up and deploy? **Y**
- Which scope? Pilih akun Anda
- Link to existing project? **N**
- Project name? **waste-detection-unjani**
- Directory? **.** (current)
- Override settings? **N**

#### **4. Deploy Production**
```bash
vercel --prod
```

---

## 🔧 **Konfigurasi yang Sudah Dibuat**

### **1. vercel.json**
- Konfigurasi build dan routing
- Max lambda size: 250MB
- Python version: 3.9

### **2. api/index.py**
- Entry point untuk Vercel serverless
- Import app dari app.py

### **3. .vercelignore**
- Ignore file besar (data, uploads)
- Keep only essential files

### **4. requirements-vercel.txt**
- Lightweight dependencies
- tensorflow-cpu (lebih kecil dari tensorflow)

---

## ⚙️ **Environment Variables di Vercel**

Setelah deploy, set environment variables:

1. Buka dashboard Vercel
2. Pilih project
3. Settings → Environment Variables
4. Tambahkan:
   - `PYTHON_VERSION` = `3.9`
   - `TF_CPP_MIN_LOG_LEVEL` = `2`

---

## 🐛 **Troubleshooting**

### **Error: Lambda size exceeded**
**Solusi:**
- Gunakan tensorflow-cpu (bukan tensorflow)
- Compress model dengan quantization
- Atau gunakan platform lain (Railway/Render)

### **Error: Timeout**
**Solusi:**
- Vercel timeout 10s untuk free tier
- Upgrade ke Pro ($20/month) untuk 60s timeout
- Atau gunakan platform lain

### **Error: File upload tidak tersimpan**
**Solusi:**
- Vercel serverless tidak persistent
- Gunakan cloud storage (AWS S3, Cloudinary)
- Atau gunakan platform dengan persistent storage

---

## 🎯 **REKOMENDASI: Deploy ke Railway.app**

Railway lebih cocok untuk project ini:

### **Keuntungan:**
- ✅ Unlimited size
- ✅ Docker support
- ✅ Persistent storage
- ✅ No timeout limit
- ✅ Free $5/month credit

### **Cara Deploy ke Railway:**

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login**
```bash
railway login
```

3. **Init Project**
```bash
railway init
```

4. **Deploy**
```bash
railway up
```

5. **Buka URL**
```bash
railway open
```

---

## 📊 **Perbandingan Platform**

| Platform | Size Limit | Timeout | Storage | Price |
|----------|-----------|---------|---------|-------|
| Vercel | 250MB | 10s (free) | ❌ | Free/$20 |
| Railway | ∞ | ∞ | ✅ | $5 credit |
| Render | ∞ | ∞ | ✅ | Free |
| Heroku | ∞ | 30s | ✅ | $7/month |

---

## 💡 **Kesimpulan**

**Untuk project ini, saya SANGAT REKOMENDASIKAN:**
1. **Railway.app** (paling mudah, unlimited)
2. **Render.com** (free tier bagus)
3. **Google Cloud Run** (scalable)

**Vercel hanya cocok jika:**
- Model < 50MB
- Prediksi < 10 detik
- Tidak perlu file upload persistent

---

## 📞 **Butuh Bantuan Deploy?**

Jika Anda ingin saya bantu setup untuk Railway/Render/Heroku, beritahu saya!

Saya bisa buatkan:
- Dockerfile
- railway.toml
- render.yaml
- Procfile (Heroku)

**Pilih platform mana yang Anda inginkan?** 🚀
