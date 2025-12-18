# 🚀 Deploy ke Render.com - 100% GRATIS!

## ✅ **KENAPA RENDER?**

### **Keuntungan:**
- ✅ **100% GRATIS** - Tidak perlu kartu kredit!
- ✅ **750 jam/bulan** - Cukup untuk 24/7
- ✅ **No size limit** - TensorFlow & model OK
- ✅ **Persistent storage** - Uploads tersimpan
- ✅ **Auto-deploy** - Connect GitHub, auto update
- ✅ **SSL gratis** - HTTPS otomatis

### **Kekurangan (minor):**
- ⚠️ Sleep after 15 min idle
- ⚠️ Cold start 30-60s saat wake up
- ⚠️ Setelah wake up, cepat lagi!

---

## 📋 **LANGKAH DEPLOY (5 MENIT!)**

### **1. Persiapan GitHub**

```bash
# Init git (jika belum)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Create repo di GitHub
# Lalu push
git remote add origin https://github.com/USERNAME/waste-detection-unjani.git
git branch -M main
git push -u origin main
```

### **2. Deploy ke Render**

1. **Buka** https://render.com
2. **Sign up** dengan GitHub (gratis, no credit card!)
3. **New +** → **Web Service**
4. **Connect repository** → Pilih repo Anda
5. **Configure:**
   - Name: `waste-detection-unjani`
   - Region: `Singapore` (terdekat)
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Plan: **Free** ✅
6. **Advanced:**
   - Add Disk:
     - Name: `uploads`
     - Mount Path: `/app/uploads`
     - Size: 1GB
7. **Create Web Service**

**SELESAI!** Render akan auto-build dan deploy.

---

## ⏱️ **PROSES DEPLOY**

```
1. Building... (5-10 menit pertama kali)
   - Install dependencies
   - Download TensorFlow
   - Load model

2. Deploying... (1-2 menit)
   - Start server
   - Health check

3. Live! 🎉
   - URL: https://waste-detection-unjani.onrender.com
```

---

## 🔧 **ENVIRONMENT VARIABLES**

Setelah deploy, tambahkan (optional):

1. Buka dashboard Render
2. Pilih service Anda
3. **Environment** tab
4. Add:
   - `PYTHON_VERSION` = `3.9.18`
   - `TF_CPP_MIN_LOG_LEVEL` = `2`

---

## 🌐 **CUSTOM DOMAIN (Optional)**

Jika punya domain:

1. **Environment** → **Custom Domain**
2. Add domain: `waste-detection.yourdomain.com`
3. Update DNS:
   - Type: `CNAME`
   - Name: `waste-detection`
   - Value: `waste-detection-unjani.onrender.com`

---

## 💤 **MENGATASI SLEEP MODE**

### **Opsi 1: Biarkan Sleep (Recommended untuk Demo)**
- Gratis selamanya
- Cold start 30-60s (acceptable untuk demo)
- Hemat resources

### **Opsi 2: Keep Awake dengan UptimeRobot**

1. **Daftar** https://uptimerobot.com (gratis!)
2. **Add Monitor:**
   - Type: `HTTP(s)`
   - URL: `https://waste-detection-unjani.onrender.com`
   - Interval: `5 minutes`
3. **Save**

UptimeRobot akan ping setiap 5 menit → server tidak sleep!

### **Opsi 3: Upgrade ke Paid ($7/month)**
- No sleep
- Faster
- More resources

---

## 📊 **MONITORING**

### **Render Dashboard:**
- Logs: Real-time logs
- Metrics: CPU, Memory, Bandwidth
- Events: Deploy history

### **Check Status:**
```bash
curl https://waste-detection-unjani.onrender.com
```

---

## 🐛 **TROUBLESHOOTING**

### **Build Failed:**
```bash
# Cek requirements.txt
# Pastikan semua dependencies ada
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### **Deploy Failed:**
```bash
# Cek logs di Render dashboard
# Biasanya karena:
# - Port salah (harus 8080)
# - Dependencies kurang
# - Model tidak ada
```

### **Slow Cold Start:**
```bash
# Normal untuk free tier
# Solusi:
# 1. Gunakan UptimeRobot
# 2. Atau upgrade ke paid
# 3. Atau terima 30-60s cold start
```

---

## 🎯 **TIPS & TRICKS**

### **1. Auto-Deploy dari GitHub**
Setiap push ke GitHub → auto deploy!

```bash
git add .
git commit -m "Update feature"
git push
# Render auto-deploy!
```

### **2. Rollback**
Jika deploy error:
1. Dashboard → **Events**
2. Pilih deploy sebelumnya
3. **Rollback**

### **3. Logs Real-time**
```bash
# Di dashboard Render
# Klik "Logs" → Real-time logs
```

### **4. Health Check**
Render auto health check:
- URL: `/`
- Interval: 30s
- Timeout: 30s

---

## 💰 **BIAYA**

### **Free Tier:**
```
✅ 750 jam/bulan (gratis selamanya!)
✅ 512MB RAM
✅ 1GB storage
✅ Unlimited bandwidth
✅ SSL gratis
✅ Auto-deploy

Total: $0/bulan 🎉
```

### **Paid Tier ($7/month):**
```
✅ No sleep
✅ 2GB RAM
✅ 10GB storage
✅ Faster
✅ Priority support

Total: $7/bulan
```

---

## 🎓 **KESIMPULAN**

### **Render.com adalah pilihan TERBAIK untuk:**
- ✅ Demo/Presentasi
- ✅ Portfolio
- ✅ Testing
- ✅ Low-traffic apps
- ✅ **100% GRATIS!**

### **Tidak cocok untuk:**
- ❌ High-traffic production (butuh paid)
- ❌ Real-time apps (karena cold start)
- ❌ Apps yang butuh always-on

---

## 🚀 **READY TO DEPLOY?**

1. Push ke GitHub
2. Connect ke Render
3. Deploy!
4. **SELESAI!** 🎉

**URL Anda:** https://waste-detection-unjani.onrender.com

---

## 📞 **BUTUH BANTUAN?**

Jika ada error saat deploy, screenshot error-nya dan tanya saya! 😊

**Happy Deploying!** 🚀
