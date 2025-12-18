# 🚀 Deploy ke Fly.io - Panduan Lengkap

## 📋 **Persiapan**

### **Yang Dibutuhkan:**
1. ✅ Akun Fly.io (gratis)
2. ✅ Kartu kredit (tidak akan dicharge untuk free tier)
3. ✅ PowerShell/Terminal
4. ✅ Code sudah siap (sudah ada!)

---

## 🔧 **STEP 1: Install Fly CLI**

### **Windows (PowerShell):**
```powershell
# Buka PowerShell sebagai Administrator
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### **Verifikasi instalasi:**
```powershell
fly version
```

**Expected output:**
```
flyctl v0.x.x windows/amd64
```

---

## 🔐 **STEP 2: Login ke Fly.io**

```powershell
fly auth login
```

**Apa yang terjadi:**
1. Browser akan terbuka
2. Login/signup dengan GitHub atau email
3. Masukkan kartu kredit (tidak akan dicharge)
4. Kembali ke terminal

**Verifikasi login:**
```powershell
fly auth whoami
```

---

## 🎯 **STEP 3: Aktifkan Database di app.py**

Sebelum deploy, kita perlu aktifkan database:

```powershell
# Edit app.py - uncomment baris 19-27
```

**Ubah dari:**
```python
USE_DATABASE = False
print("⚠️ Database temporarily disabled for testing")

# try:
#     from database import DatabaseManager
#     from cloudinary_helper import CloudinaryManager
#     USE_DATABASE = True
```

**Menjadi:**
```python
USE_DATABASE = True

try:
    from database import DatabaseManager
    from cloudinary_helper import CloudinaryManager
    print("✓ Database and Cloudinary modules loaded")
```

**Simpan file!**

---

## 🚀 **STEP 4: Launch App**

```powershell
# Di folder project
fly launch
```

**Pertanyaan yang akan muncul:**

1. **Choose an app name:**
   ```
   waste-detection-unjani
   ```
   (atau biarkan kosong untuk auto-generate)

2. **Choose a region:**
   ```
   sin (Singapore)
   ```
   Pilih Singapore karena paling dekat dengan Indonesia

3. **Would you like to set up a PostgreSQL database?**
   ```
   Yes
   ```

4. **Select configuration:**
   ```
   Development - Single node, 1x shared CPU, 256MB RAM, 1GB disk
   ```
   (Gratis!)

5. **Would you like to deploy now?**
   ```
   No
   ```
   (Kita setup secrets dulu)

**Output:**
```
✓ Created app 'waste-detection-unjani' in organization 'personal'
✓ Created Postgres cluster waste-detection-unjani-db
✓ Database attached to app
```

---

## 🔑 **STEP 5: Set Cloudinary Secrets**

```powershell
# Set Cloudinary credentials
fly secrets set CLOUDINARY_CLOUD_NAME=your_cloud_name
fly secrets set CLOUDINARY_API_KEY=your_api_key
fly secrets set CLOUDINARY_API_SECRET=your_api_secret
```

**Ganti dengan credentials Cloudinary kamu!**

**Cek secrets:**
```powershell
fly secrets list
```

**Expected output:**
```
NAME                      DIGEST          CREATED AT
CLOUDINARY_API_KEY        xxxxx           1m ago
CLOUDINARY_API_SECRET     xxxxx           1m ago
CLOUDINARY_CLOUD_NAME     xxxxx           1m ago
DATABASE_URL              xxxxx           5m ago (auto-created)
```

---

## 🚢 **STEP 6: Deploy!**

```powershell
fly deploy
```

**Apa yang terjadi:**
1. Build Docker image (~5 menit)
2. Upload ke Fly.io
3. Start app
4. Run health checks

**Expected output:**
```
==> Building image
...
==> Pushing image to fly
...
==> Deploying
...
✓ Deployment successful!

Visit your app at: https://waste-detection-unjani.fly.dev
```

---

## ✅ **STEP 7: Verifikasi Deployment**

### **1. Check status:**
```powershell
fly status
```

**Expected output:**
```
App
  Name     = waste-detection-unjani
  Status   = running
  Hostname = waste-detection-unjani.fly.dev
  
Machines
  ID       STATE   REGION  HEALTH
  xxxxx    started sin     passing
```

### **2. Check logs:**
```powershell
fly logs
```

**Look for:**
```
✓ Database and Cloudinary modules loaded
✓ Database connected and tables created
✓ Cloudinary configured: your_cloud_name
✓ Model loaded successfully
```

### **3. Open app:**
```powershell
fly open
```

Browser akan membuka: `https://waste-detection-unjani.fly.dev`

---

## 🧪 **STEP 8: Test App**

### **Test 1: Upload gambar**
1. Buka app di browser
2. Upload gambar sampah
3. Lihat hasil prediksi
4. Check heatmap muncul

### **Test 2: Check history**
1. Klik "Riwayat Deteksi"
2. Data harus muncul
3. Gambar dari Cloudinary harus muncul

### **Test 3: Test persistence**
```powershell
# Restart app
fly apps restart waste-detection-unjani

# Tunggu 30 detik
# Buka history lagi - data harus masih ada!
```

---

## 🔧 **Commands Berguna**

### **Monitoring:**
```powershell
# Live logs
fly logs

# Status
fly status

# SSH ke container
fly ssh console

# Check database
fly postgres connect -a waste-detection-unjani-db
```

### **Management:**
```powershell
# Restart app
fly apps restart waste-detection-unjani

# Scale memory (jika perlu)
fly scale memory 512

# Deploy ulang
fly deploy

# Rollback
fly releases
fly releases rollback <version>
```

### **Database:**
```powershell
# Connect to database
fly postgres connect -a waste-detection-unjani-db

# Backup database
fly postgres backup create -a waste-detection-unjani-db

# List backups
fly postgres backup list -a waste-detection-unjani-db
```

---

## 🐛 **Troubleshooting**

### **Error: "failed to fetch an image"**
**Solusi:**
```powershell
# Clear build cache
fly deploy --no-cache
```

### **Error: "health checks failing"**
**Solusi:**
```powershell
# Check logs
fly logs

# Increase timeout di fly.toml
# Edit: grace_period = "60s"
fly deploy
```

### **Error: "database connection failed"**
**Solusi:**
```powershell
# Check database status
fly postgres db list -a waste-detection-unjani-db

# Restart database
fly postgres restart -a waste-detection-unjani-db
```

### **Error: "out of memory"**
**Solusi:**
```powershell
# Scale to 512MB (masih gratis)
fly scale memory 512
```

---

## 💰 **Free Tier Limits**

**Fly.io Free Tier:**
- ✅ 3 shared-cpu VMs (256MB each)
- ✅ 3GB PostgreSQL storage
- ✅ 160GB bandwidth/month
- ✅ Gratis selamanya!

**Cloudinary Free Tier:**
- ✅ 25GB storage
- ✅ 25GB bandwidth/month
- ✅ Gratis selamanya!

**Total: Gratis untuk production app! 🎉**

---

## 📊 **Monitoring Usage**

### **Fly.io Dashboard:**
```powershell
fly dashboard
```

### **Check metrics:**
```powershell
fly metrics
```

### **Cloudinary Dashboard:**
https://cloudinary.com/console

---

## 🔄 **Update App (Future)**

Jika ada perubahan code:

```powershell
# 1. Edit code
# 2. Deploy
fly deploy

# 3. Check logs
fly logs

# 4. Test
fly open
```

---

## 🎯 **Checklist Deployment**

- [ ] Fly CLI installed
- [ ] Login ke Fly.io
- [ ] Uncomment database di app.py
- [ ] `fly launch` berhasil
- [ ] PostgreSQL created
- [ ] Cloudinary secrets set
- [ ] `fly deploy` berhasil
- [ ] App bisa diakses
- [ ] Upload gambar berhasil
- [ ] Heatmap muncul
- [ ] History muncul
- [ ] Data persistent setelah restart

---

## 🆘 **Butuh Bantuan?**

### **Check logs:**
```powershell
fly logs
```

### **Check status:**
```powershell
fly status
```

### **SSH ke container:**
```powershell
fly ssh console
```

### **Kirim ke saya:**
1. Screenshot error
2. Output dari `fly logs`
3. Output dari `fly status`

---

## 🎉 **Selesai!**

App kamu sekarang:
- ✅ Running di Fly.io (gratis!)
- ✅ PostgreSQL database (persistent)
- ✅ Cloudinary storage (persistent)
- ✅ Auto-scaling
- ✅ HTTPS enabled
- ✅ Production-ready!

**URL:** `https://waste-detection-unjani.fly.dev`

**Good luck! 🚀**
