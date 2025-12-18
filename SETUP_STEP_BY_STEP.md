# 🚀 Setup PostgreSQL + Cloudinary - Step by Step

## ✅ **Yang Sudah Saya Lakukan:**

1. ✅ Update `requirements.txt` - tambah psycopg2, sqlalchemy, cloudinary
2. ✅ Buat `database.py` - PostgreSQL models dan manager
3. ✅ Buat `cloudinary_helper.py` - Cloudinary upload manager
4. ✅ Update `app.py` - integrasi database + cloudinary
5. ✅ Update `templates/index.html` - support Cloudinary URLs

---

## 📋 **Yang Perlu Kamu Lakukan:**

### **Step 1: Setup PostgreSQL di Railway** (5 menit)

1. Buka https://railway.app
2. Login dan buka project **waste-detection**
3. Klik **"New"** (kanan atas) → **"Database"** → **"Add PostgreSQL"**
4. Tunggu sampai status "Active" (1-2 menit)
5. Klik PostgreSQL service → tab **"Variables"**
6. Copy value **DATABASE_URL**
7. Klik service **waste-detection** (main app)
8. Tab **"Variables"** → **"New Variable"**
9. Name: `DATABASE_URL`
10. Value: Paste DATABASE_URL tadi
11. Klik **"Add"**

✅ **PostgreSQL setup selesai!**

---

### **Step 2: Setup Cloudinary** (5 menit)

1. Buka https://cloudinary.com/users/register/free
2. Sign up dengan email (atau Google/GitHub)
3. Verify email dan login
4. Di dashboard, lihat **"Account Details"** (kiri bawah)
5. Copy 3 values:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

6. Kembali ke Railway dashboard
7. Klik service **waste-detection**
8. Tab **"Variables"** → Add 3 variables:

```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

✅ **Cloudinary setup selesai!**

---

### **Step 3: Deploy ke Railway** (5 menit)

Di terminal/command prompt:

```bash
# Deploy update
railway up --detach
```

Tunggu 5-10 menit sampai build selesai.

---

### **Step 4: Test** (2 menit)

1. Buka: https://waste-detection-production-4613.up.railway.app
2. Upload gambar
3. Cek apakah:
   - ✅ Gambar muncul
   - ✅ Heatmap muncul
   - ✅ Data masuk history
4. Refresh page atau restart Railway
5. Cek history lagi - **data harus tetap ada!**

---

## 🎉 **Hasil Akhir:**

Setelah setup selesai:

✅ **History tidak hilang** - tersimpan di PostgreSQL
✅ **Gambar tidak hilang** - tersimpan di Cloudinary
✅ **Heatmap tidak hilang** - tersimpan di Cloudinary
✅ **Loading cepat** - CDN Cloudinary
✅ **100% Gratis** - PostgreSQL + Cloudinary free tier

---

## 🔍 **Cara Cek Apakah Berhasil:**

### Check Database:
```bash
railway logs
```

Look for:
```
✓ Database and Cloudinary modules loaded
✓ Database connected and tables created
✓ Cloudinary configured: your_cloud_name
```

### Check Upload:
Upload gambar, lihat logs:
```
☁️ Uploading image to Cloudinary...
✓ Image uploaded: https://res.cloudinary.com/...
✓ Log saved to database
```

### Check Persistence:
1. Upload gambar
2. Lihat history - ada data
3. Restart Railway (atau tunggu auto-restart)
4. Lihat history lagi - **data masih ada!**

---

## ❌ **Troubleshooting:**

### Error: "DATABASE_URL not found"
- Pastikan sudah add DATABASE_URL di Railway Variables
- Restart deployment

### Error: "Cloudinary credentials not found"
- Pastikan sudah add 3 Cloudinary variables
- Check spelling: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

### Error: "Failed to initialize database"
- Check DATABASE_URL format: `postgresql://user:pass@host:port/db`
- Pastikan PostgreSQL service status "Active"

### Gambar tidak muncul
- Check browser console untuk error
- Pastikan Cloudinary upload berhasil (lihat logs)
- Check Cloudinary dashboard - ada gambar?

---

## 📊 **Monitoring:**

### Railway Dashboard:
- PostgreSQL: Lihat storage usage
- Cloudinary: https://cloudinary.com/console - lihat storage & bandwidth

### Limits (Free Tier):
- **PostgreSQL**: 500MB storage
- **Cloudinary**: 25GB storage, 25GB bandwidth/month

---

## 🆘 **Need Help?**

Jika ada error, kirim:
1. Screenshot error
2. Railway logs: `railway logs`
3. Browser console error (F12)

---

**Ready? Mulai dari Step 1!** 🚀
