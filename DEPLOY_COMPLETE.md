# 🚀 Deploy Lengkap: Render + UptimeRobot (100% GRATIS!)

## ✨ **HASIL AKHIR**

Setelah setup ini, Anda akan punya:
- ✅ **Website live 24/7** - Always-on, no sleep!
- ✅ **100% GRATIS** - Tidak perlu kartu kredit!
- ✅ **Auto-deploy** - Push GitHub = auto update
- ✅ **HTTPS gratis** - SSL otomatis
- ✅ **No cold start** - Selalu cepat!

**URL:** `https://waste-detection-unjani.onrender.com`

---

## 📋 **LANGKAH 1: PUSH KE GITHUB (5 MENIT)**

### **1.1. Init Git**

```bash
# Di folder project
git init
```

### **1.2. Add Files**

```bash
# Add semua file
git add .

# Commit
git commit -m "Initial commit - Waste Detection System"
```

### **1.3. Create GitHub Repository**

1. Buka https://github.com
2. Klik **New repository** (tombol hijau)
3. Repository name: `waste-detection-unjani`
4. Description: `AI Waste Detection System - Kampus 1 UNJANI Yogyakarta`
5. Public atau Private (terserah)
6. **JANGAN** centang "Initialize with README"
7. Klik **Create repository**

### **1.4. Push ke GitHub**

```bash
# Ganti USERNAME dengan username GitHub Anda
git remote add origin https://github.com/USERNAME/waste-detection-unjani.git
git branch -M main
git push -u origin main
```

**✅ SELESAI!** Repo sudah di GitHub.

---

## 🌐 **LANGKAH 2: DEPLOY KE RENDER (10 MENIT)**

### **2.1. Sign Up Render**

1. Buka https://render.com
2. Klik **Get Started for Free**
3. **Sign up with GitHub** (recommended!)
4. Authorize Render untuk akses GitHub
5. **Tidak perlu kartu kredit!** ✅

### **2.2. Create Web Service**

1. Dashboard Render → Klik **New +**
2. Pilih **Web Service**
3. **Connect a repository:**
   - Jika tidak muncul, klik **Configure account**
   - Pilih **All repositories** atau pilih `waste-detection-unjani`
   - Save
4. Pilih repository: `waste-detection-unjani`
5. Klik **Connect**

### **2.3. Configure Service**

**Basic Settings:**
```
Name: waste-detection-unjani
Region: Singapore (terdekat dengan Indonesia)
Branch: main
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

**Instance Type:**
```
Plan: Free ✅ (pilih yang gratis!)
```

### **2.4. Advanced Settings**

Klik **Advanced** → **Add Disk**:
```
Name: uploads
Mount Path: /app/uploads
Size: 1 GB
```

Klik **Add Environment Variable** (optional):
```
Key: TF_CPP_MIN_LOG_LEVEL
Value: 2
```

### **2.5. Deploy!**

1. Klik **Create Web Service**
2. Tunggu build (10-15 menit pertama kali)
3. Lihat logs real-time
4. Tunggu sampai status: **Live** ✅

**URL Anda:** `https://waste-detection-unjani.onrender.com`

---

## ⏰ **LANGKAH 3: SETUP UPTIMEROBOT (5 MENIT)**

### **3.1. Sign Up UptimeRobot**

1. Buka https://uptimerobot.com
2. Klik **Register for FREE**
3. Isi form:
   - Email: email Anda
   - Password: buat password
4. Verify email
5. Login

### **3.2. Add Monitor**

1. Dashboard → Klik **+ Add New Monitor**
2. **Monitor Type:** `HTTP(s)`
3. **Friendly Name:** `Waste Detection UNJANI`
4. **URL:** `https://waste-detection-unjani.onrender.com`
5. **Monitoring Interval:** `5 minutes` (gratis!)
6. **Monitor Timeout:** `30 seconds`
7. **Alert Contacts:** (optional, untuk notif jika down)
8. Klik **Create Monitor**

**✅ SELESAI!** UptimeRobot akan ping setiap 5 menit.

### **3.3. Verify**

Tunggu 5 menit, lalu cek:
- Status: **Up** (hijau) ✅
- Response Time: ~1-2 detik
- Uptime: 100%

---

## 🎉 **SELESAI! WEBSITE LIVE 24/7!**

### **Cek Website:**

1. Buka: `https://waste-detection-unjani.onrender.com`
2. Upload gambar
3. Lihat hasil deteksi
4. Cek peta kampus: `/map`
5. Cek history: `/history`

**Semuanya GRATIS & Always-On!** 🎉

---

## 🔄 **AUTO-DEPLOY WORKFLOW**

Setelah setup, workflow Anda:

```bash
# 1. Edit code di local
# 2. Test di localhost

# 3. Commit & push
git add .
git commit -m "Update feature X"
git push

# 4. Render auto-detect & deploy!
# 5. Tunggu 2-3 menit
# 6. Live di production! ✅
```

**Tidak perlu login Render lagi!**

---

## 📊 **MONITORING**

### **Render Dashboard:**
- **Logs:** Real-time logs
- **Metrics:** CPU, Memory, Bandwidth
- **Events:** Deploy history
- **Settings:** Environment variables

### **UptimeRobot Dashboard:**
- **Uptime:** Persentase uptime
- **Response Time:** Grafik response time
- **Logs:** History ping
- **Alerts:** Email jika down

---

## 🐛 **TROUBLESHOOTING**

### **Build Failed di Render:**

**Cek logs:**
1. Dashboard Render → Pilih service
2. Klik **Logs**
3. Lihat error message

**Common issues:**
```bash
# Error: requirements.txt not found
# Fix: Pastikan file ada di root folder

# Error: Module not found
# Fix: Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push

# Error: Port binding
# Fix: Sudah OK, app.py sudah pakai PORT dari env
```

### **Website Down di UptimeRobot:**

**Cek:**
1. Buka Render dashboard
2. Cek status service: Running?
3. Cek logs: Ada error?
4. Restart service jika perlu

### **Slow Response:**

**Normal untuk:**
- First request after deploy (loading model)
- Large image upload
- Complex prediction

**Jika terlalu lambat:**
- Cek Render metrics (CPU, Memory)
- Optimize code
- Atau upgrade ke paid tier

---

## 💰 **BIAYA**

### **Total Biaya Bulanan:**

```
Render Free Tier:     $0
UptimeRobot Free:     $0
GitHub:               $0
Domain (optional):    $0-12/tahun
─────────────────────────
TOTAL:                $0/bulan 🎉
```

**100% GRATIS SELAMANYA!**

---

## 🎯 **TIPS & TRICKS**

### **1. Custom Domain (Optional)**

Jika punya domain:

**Di Render:**
1. Settings → Custom Domain
2. Add: `waste-detection.yourdomain.com`

**Di DNS Provider:**
```
Type: CNAME
Name: waste-detection
Value: waste-detection-unjani.onrender.com
TTL: 3600
```

### **2. Environment Variables**

Untuk config sensitif:

**Di Render:**
1. Settings → Environment
2. Add variable
3. Redeploy

**Di code:**
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### **3. Rollback Deploy**

Jika deploy error:

1. Dashboard → Events
2. Pilih deploy sebelumnya
3. Klik **Rollback**

### **4. View Logs Real-time**

```bash
# Di Render dashboard
# Klik "Logs" → Auto-refresh
```

### **5. Health Check Endpoint**

Render auto health check ke `/`

Atau buat custom:
```python
@app.route('/health')
def health():
    return {'status': 'ok'}, 200
```

---

## 📈 **SCALING (Jika Perlu)**

### **Jika Traffic Tinggi:**

**Opsi 1: Upgrade Render ($7/month)**
- 2GB RAM
- Faster CPU
- No sleep
- Priority support

**Opsi 2: Add CDN (Cloudflare - Gratis!)**
- Cache static files
- DDoS protection
- Faster global access

**Opsi 3: Optimize Code**
- Compress images
- Cache predictions
- Lazy load model

---

## 🎓 **KESIMPULAN**

### **Apa yang Anda Dapat:**

✅ **Website live 24/7** - Always-on
✅ **100% GRATIS** - No credit card
✅ **Auto-deploy** - Push = live
✅ **HTTPS** - SSL gratis
✅ **Monitoring** - UptimeRobot
✅ **Scalable** - Bisa upgrade kapan saja

### **Perfect untuk:**

- ✅ Demo/Presentasi
- ✅ Portfolio
- ✅ Tugas kuliah
- ✅ Prototype
- ✅ Low-medium traffic apps

---

## 📞 **BUTUH BANTUAN?**

### **Jika Ada Error:**

1. Screenshot error
2. Copy logs dari Render
3. Tanya saya!

### **Jika Ingin Custom:**

- Custom domain
- Database integration
- API endpoints
- Authentication
- Dan lainnya

**Saya siap bantu!** 😊

---

## 🚀 **READY TO DEPLOY?**

**Checklist:**
- [ ] Push ke GitHub
- [ ] Deploy ke Render
- [ ] Setup UptimeRobot
- [ ] Test website
- [ ] Share URL!

**Let's go!** 🎉

---

**Happy Deploying!** 🚀

**URL Anda:** `https://waste-detection-unjani.onrender.com`
