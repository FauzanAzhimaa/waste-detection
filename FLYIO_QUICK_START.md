# ⚡ Fly.io Quick Start - 10 Menit Deploy!

## 🎯 **Langkah Cepat:**

### **1. Install Fly CLI (2 menit)**
```powershell
# Buka PowerShell sebagai Administrator
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Verifikasi
fly version
```

### **2. Login (1 menit)**
```powershell
fly auth login
```
- Browser akan terbuka
- Login dengan GitHub/email
- Masukkan kartu kredit (tidak dicharge!)

### **3. Launch App (3 menit)**
```powershell
fly launch
```

**Jawab pertanyaan:**
- App name: `waste-detection-unjani` (atau kosong)
- Region: `sin` (Singapore)
- PostgreSQL: `Yes` → `Development` (gratis)
- Deploy now: `No`

### **4. Set Cloudinary Secrets (1 menit)**
```powershell
fly secrets set CLOUDINARY_CLOUD_NAME=your_cloud_name
fly secrets set CLOUDINARY_API_KEY=your_api_key
fly secrets set CLOUDINARY_API_SECRET=your_api_secret
```

**Ganti dengan credentials kamu dari Railway!**

### **5. Deploy! (5 menit)**
```powershell
fly deploy
```

Tunggu build selesai...

### **6. Test (1 menit)**
```powershell
fly open
```

Upload gambar → Check hasil → Check history!

---

## ✅ **Selesai!**

App kamu sekarang running di:
`https://waste-detection-unjani.fly.dev`

**Features:**
- ✅ PostgreSQL (persistent data)
- ✅ Cloudinary (persistent images)
- ✅ Auto-scaling
- ✅ HTTPS
- ✅ Gratis selamanya!

---

## 🔧 **Commands Penting:**

```powershell
# Logs
fly logs

# Status
fly status

# Restart
fly apps restart waste-detection-unjani

# Deploy ulang
fly deploy

# Open app
fly open
```

---

## 🐛 **Troubleshooting:**

### **Error saat deploy:**
```powershell
fly logs
```

### **Database error:**
```powershell
fly postgres db list -a waste-detection-unjani-db
```

### **Out of memory:**
```powershell
fly scale memory 512
```

---

## 📚 **Dokumentasi Lengkap:**

Lihat `DEPLOY_FLYIO.md` untuk panduan detail!

---

**Good luck! 🚀**
