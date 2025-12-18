# 🚀 Deploy ke Railway - TANPA Kartu Kredit!

## ✨ **KENAPA RAILWAY?**

- ✅ **$5 credit gratis** - Tanpa kartu kredit!
- ✅ **No sleep mode** - Always fast, no cold start!
- ✅ **~500 jam gratis** (~20 hari 24/7)
- ✅ **Setup super mudah** (5 menit!)
- ✅ **Auto-deploy** dari GitHub

---

## 🚀 **DEPLOY (5 MENIT!)**

### **1. Install Railway CLI**

```bash
npm install -g @railway/cli
```

### **2. Login Railway**

```bash
railway login
```

Browser akan terbuka:
- Sign up dengan GitHub (gratis!)
- Authorize Railway
- Kembali ke terminal

### **3. Link ke Project**

```bash
# Di folder project
railway init
```

Pilih:
- Create new project? **Yes**
- Project name: `waste-detection-unjani`

### **4. Deploy!**

```bash
railway up
```

Railway akan:
- Upload code
- Detect Python
- Install dependencies
- Build & deploy
- Generate URL

### **5. Add Environment Variable**

```bash
railway variables set PORT=8080
```

### **6. Buka Website**

```bash
railway open
```

**SELESAI!** Website live! 🎉

---

## 🌐 **ATAU: Deploy via GitHub (Lebih Mudah!)**

### **1. Buka Railway Dashboard**

https://railway.app

### **2. New Project**

- Klik **New Project**
- Pilih **Deploy from GitHub repo**
- Pilih `waste-detection`
- Klik **Deploy**

### **3. Configure**

Railway auto-detect Python!

Add environment variable:
- Key: `PORT`
- Value: `8080`

### **4. Deploy!**

Railway auto-deploy! Tunggu 5-10 menit.

**URL:** `https://waste-detection-unjani.up.railway.app`

---

## 💰 **BIAYA**

```
$5 credit gratis/bulan
~500 jam server
= ~20 hari 24/7
= ~2 bulan jika pakai 8 jam/hari

GRATIS untuk demo/presentasi!
```

---

## ⚠️ **KNOWN ISSUES & SOLUTIONS**

### 1. Heatmap Tidak Muncul
**Penyebab:** Memory limit 512MB di Railway free tier

**Solusi:**
- ✅ Sudah ada auto-resize gambar max 800px
- ✅ Error handling: prediksi tetap ditampilkan
- ✅ Gunakan gambar <3MB untuk hasil terbaik
- 📖 Lihat: `TROUBLESHOOTING_HEATMAP.md`

### 2. Timeout Kadang Terjadi
**Penyebab:** Shared resources di Railway

**Solusi:**
- ✅ Timeout sudah 120 detik
- ✅ Retry jika gagal
- ✅ Gunakan gambar lebih kecil

### 3. File Upload Hilang Setelah Restart
**Penyebab:** Ephemeral filesystem

**Solusi:**
- ✅ Normal behavior di Railway free tier
- ✅ Upload ulang jika perlu
- ✅ History tetap tersimpan di `detection_logs.json`

---

## 📊 **MONITORING**

### Check Logs:
```bash
railway logs
```

### Check Memory Usage:
Railway Dashboard → Metrics → Memory

**Normal:** 200-400MB
**High:** 400-500MB (heatmap mungkin gagal)

---

## 🎯 **KESIMPULAN**

Railway **LEBIH MUDAH** dari Render:
- ✅ No credit card
- ✅ No sleep mode
- ✅ Faster setup
- ✅ Always fast

**Perfect untuk project ini!** 🚀

**Catatan:** Heatmap kadang gagal karena memory limit, tapi prediksi tetap akurat!
