# 🗄️ Setup PostgreSQL Database di Railway

## Step 1: Add PostgreSQL Service

### Via Railway Dashboard:
1. Buka: https://railway.app
2. Login dan buka project: **waste-detection**
3. Klik tombol **"New"** (kanan atas)
4. Pilih **"Database"** → **"Add PostgreSQL"**
5. Railway akan create database otomatis
6. Tunggu 1-2 menit sampai status "Active"

### Get Database URL:
1. Klik PostgreSQL service yang baru dibuat
2. Klik tab **"Variables"**
3. Copy value dari **DATABASE_URL**
4. Format: `postgresql://user:password@host:port/database`

### Add to Main Service:
1. Klik service **waste-detection** (bukan PostgreSQL)
2. Klik tab **"Variables"**
3. Klik **"New Variable"**
4. Name: `DATABASE_URL`
5. Value: Paste DATABASE_URL dari PostgreSQL service
6. Klik **"Add"**

---

## Step 2: Setup Cloudinary

### Sign Up:
1. Buka: https://cloudinary.com/users/register/free
2. Sign up dengan email
3. Verify email
4. Login ke dashboard

### Get Credentials:
1. Di dashboard, lihat bagian **"Account Details"**
2. Copy:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### Add to Railway:
1. Kembali ke Railway dashboard
2. Klik service **waste-detection**
3. Klik tab **"Variables"**
4. Add 3 variables:
   - `CLOUDINARY_CLOUD_NAME` = your_cloud_name
   - `CLOUDINARY_API_KEY` = your_api_key
   - `CLOUDINARY_API_SECRET` = your_api_secret

---

## ✅ Checklist:

- [ ] PostgreSQL service created di Railway
- [ ] DATABASE_URL copied
- [ ] DATABASE_URL added to waste-detection service
- [ ] Cloudinary account created
- [ ] Cloudinary credentials copied
- [ ] Cloudinary variables added to Railway

---

Setelah selesai, lanjut ke Step 3 (Update Code)
