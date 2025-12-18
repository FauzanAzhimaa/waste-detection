# ✅ Fly.io Deployment Checklist

## 📋 **Pre-Deployment**

- [ ] Punya akun Fly.io
- [ ] Punya kartu kredit (tidak akan dicharge)
- [ ] PowerShell/Terminal ready
- [ ] Copy Cloudinary credentials dari Railway

---

## 🔧 **Installation**

- [ ] Install Fly CLI
  ```powershell
  powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
  ```
- [ ] Verify installation
  ```powershell
  fly version
  ```

---

## 🔐 **Authentication**

- [ ] Login ke Fly.io
  ```powershell
  fly auth login
  ```
- [ ] Browser terbuka
- [ ] Login/signup berhasil
- [ ] Kartu kredit ditambahkan
- [ ] Verify login
  ```powershell
  fly auth whoami
  ```

---

## 🚀 **Launch App**

- [ ] Run launch command
  ```powershell
  fly launch
  ```
- [ ] App name: `waste-detection-unjani` (atau auto)
- [ ] Region: `sin` (Singapore)
- [ ] PostgreSQL: `Yes`
- [ ] Config: `Development` (gratis)
- [ ] Deploy now: `No`
- [ ] Verify app created
  ```powershell
  fly status
  ```

---

## 🔑 **Set Secrets**

- [ ] Set CLOUDINARY_CLOUD_NAME
  ```powershell
  fly secrets set CLOUDINARY_CLOUD_NAME=xxx
  ```
- [ ] Set CLOUDINARY_API_KEY
  ```powershell
  fly secrets set CLOUDINARY_API_KEY=xxx
  ```
- [ ] Set CLOUDINARY_API_SECRET
  ```powershell
  fly secrets set CLOUDINARY_API_SECRET=xxx
  ```
- [ ] Verify secrets
  ```powershell
  fly secrets list
  ```

---

## 🚢 **Deploy**

- [ ] Run deploy
  ```powershell
  fly deploy
  ```
- [ ] Build berhasil (tunggu ~5 menit)
- [ ] Upload berhasil
- [ ] Deployment berhasil
- [ ] Health checks passing

---

## ✅ **Verification**

- [ ] Check status
  ```powershell
  fly status
  ```
- [ ] Status: `running`
- [ ] Health: `passing`
- [ ] Check logs
  ```powershell
  fly logs
  ```
- [ ] Look for:
  - `✓ Database and Cloudinary modules loaded`
  - `✓ Database connected`
  - `✓ Cloudinary configured`
  - `✓ Model loaded successfully`

---

## 🧪 **Testing**

- [ ] Open app
  ```powershell
  fly open
  ```
- [ ] Website loading
- [ ] Upload gambar berhasil
- [ ] Prediksi muncul
- [ ] Heatmap muncul
- [ ] Check history
- [ ] Data muncul di history
- [ ] Gambar dari Cloudinary muncul

---

## 🔄 **Persistence Test**

- [ ] Upload beberapa gambar
- [ ] Check history - data ada
- [ ] Restart app
  ```powershell
  fly apps restart waste-detection-unjani
  ```
- [ ] Tunggu 30 detik
- [ ] Check history lagi
- [ ] **Data masih ada!** ✅

---

## 📊 **Monitoring**

- [ ] Setup monitoring
  ```powershell
  fly dashboard
  ```
- [ ] Check metrics
  ```powershell
  fly metrics
  ```
- [ ] Bookmark URL app
- [ ] Bookmark Fly.io dashboard

---

## 🎉 **Post-Deployment**

- [ ] Share URL dengan tim/dosen
- [ ] Test dari device lain
- [ ] Test dari network lain
- [ ] Document URL di README
- [ ] Backup credentials
- [ ] Setup monitoring alerts (optional)

---

## 📝 **Documentation**

- [ ] Update README dengan URL baru
- [ ] Document deployment process
- [ ] Share credentials dengan tim (secure)
- [ ] Create user guide

---

## 🆘 **Troubleshooting**

Jika ada masalah:

- [ ] Check logs: `fly logs`
- [ ] Check status: `fly status`
- [ ] Check database: `fly postgres db list -a waste-detection-unjani-db`
- [ ] Restart: `fly apps restart waste-detection-unjani`
- [ ] Redeploy: `fly deploy`
- [ ] Contact support atau tanya saya

---

## ✅ **Success Criteria**

Deployment berhasil jika:

- ✅ App accessible via HTTPS
- ✅ Upload gambar berhasil
- ✅ Prediksi akurat
- ✅ Heatmap muncul
- ✅ History muncul
- ✅ Data persistent setelah restart
- ✅ Gambar persistent via Cloudinary
- ✅ No errors di logs
- ✅ Health checks passing

---

## 🎯 **Next Steps**

Setelah deployment berhasil:

1. Monitor usage (Fly.io + Cloudinary dashboard)
2. Collect user feedback
3. Improve model (optional)
4. Add more features (optional)
5. Scale if needed (optional)

---

**Semua checklist ✅? Congratulations! 🎉**

Your app is now production-ready and running on Fly.io!

**URL:** `https://waste-detection-unjani.fly.dev`
