# 🚀 Setup Railway - SEKARANG!

## ❌ **Masalah: Bad Gateway**

**Penyebab:** PostgreSQL dan Cloudinary belum di-setup, tapi code sudah expect credentials.

**Solusi:** Setup credentials ATAU disable database temporarily.

---

## ✅ **Option A: Setup Database (Recommended)**

### **1. Setup PostgreSQL (5 menit)**

#### **Di Railway Dashboard:**
1. Buka: https://railway.app
2. Login → Buka project **waste-detection**
3. Klik **"New"** (kanan atas)
4. Pilih **"Database"** → **"Add PostgreSQL"**
5. Tunggu status "Active" (1-2 menit)

#### **Copy DATABASE_URL:**
1. Klik PostgreSQL service yang baru dibuat
2. Tab **"Variables"**
3. Copy value **DATABASE_URL**
   ```
   postgresql://postgres:password@host:5432/railway
   ```

#### **Add to Main Service:**
1. Klik service **waste-detection** (main app, bukan PostgreSQL)
2. Tab **"Variables"**
3. Klik **"New Variable"**
4. Name: `DATABASE_URL`
5. Value: Paste DATABASE_URL tadi
6. Klik **"Add"**

### **2. Setup Cloudinary (5 menit)**

#### **Sign Up Cloudinary:**
1. Buka: https://cloudinary.com/users/register/free
2. Sign up dengan email (atau Google)
3. Verify email dan login

#### **Get Credentials:**
1. Di dashboard Cloudinary
2. Lihat **"Account Details"** (kiri bawah atau Product Environment Credentials)
3. Copy 3 values:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

#### **Add to Railway:**
1. Kembali ke Railway dashboard
2. Klik service **waste-detection**
3. Tab **"Variables"**
4. Add 3 variables (klik "New Variable" untuk masing-masing):

```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

### **3. Redeploy**

Railway akan auto-redeploy setelah add variables.

Atau manual:
```bash
railway up --detach
```

Tunggu 3-5 menit, lalu test website.

---

## ✅ **Option B: Disable Database Temporarily (Quick Fix)**

Jika mau test app dulu tanpa database:

### **1. Set Fallback Mode**

Di Railway Variables, add:
```
USE_DATABASE = false
```

### **2. Redeploy**
```bash
railway up --detach
```

**Catatan:** Dengan ini:
- ✅ App akan jalan
- ❌ Data akan hilang setelah restart
- ❌ Gambar akan hilang setelah restart

---

## 🎯 **Recommendation:**

**Setup database sekarang** (Option A) - hanya 10 menit total, tapi solve masalah permanent.

---

## ✅ **Checklist:**

### **PostgreSQL:**
- [ ] PostgreSQL service created
- [ ] DATABASE_URL copied
- [ ] DATABASE_URL added to waste-detection service

### **Cloudinary:**
- [ ] Cloudinary account created
- [ ] Cloud Name, API Key, API Secret copied
- [ ] 3 variables added to Railway

### **Deploy:**
- [ ] Railway auto-redeploy (or manual: `railway up --detach`)
- [ ] Wait 3-5 minutes
- [ ] Test website

---

## 🧪 **Test:**

Setelah setup:
1. Buka: https://waste-detection-production-4613.up.railway.app
2. Should load without error
3. Upload gambar
4. Check if works

---

**Mulai dari Step 1 sekarang!** 🚀
