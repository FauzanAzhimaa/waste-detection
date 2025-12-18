# 🔧 Solusi Persistent Storage untuk Railway

## ❌ **Masalah Saat Ini**

### 1. Ephemeral Filesystem
- Railway free tier menggunakan ephemeral filesystem
- Setiap restart, semua file hilang:
  - `detection_logs.json` → History hilang
  - `uploads/*.jpg` → Gambar hilang
  - `uploads/heatmaps/*.jpg` → Heatmap hilang

### 2. Railway Restart Otomatis
Railway restart container ketika:
- Deploy baru
- Memory limit exceeded
- Inactivity (sleep mode - tapi Railway tidak sleep)
- Platform maintenance

---

## ✅ **Solusi 1: PostgreSQL Database (RECOMMENDED)**

### Kenapa PostgreSQL?
- ✅ **Gratis** di Railway (500MB storage)
- ✅ **Persistent** - data tidak hilang
- ✅ **Fast** - query lebih cepat dari JSON
- ✅ **Scalable** - bisa handle ribuan records

### Setup PostgreSQL di Railway:

#### 1. Add PostgreSQL Service
```bash
# Di Railway dashboard
1. Buka project: waste-detection
2. Klik "New" → "Database" → "Add PostgreSQL"
3. Railway akan create database otomatis
4. Copy DATABASE_URL dari Variables tab
```

#### 2. Install Dependencies
Tambah ke `requirements.txt`:
```
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
```

#### 3. Update Code
Ganti `detection_logs.json` dengan PostgreSQL table.

**Keuntungan:**
- History tidak hilang setelah restart
- Bisa query by date, location, category
- Export CSV lebih cepat
- Bisa add user authentication nanti

**Kekurangan:**
- Gambar tetap hilang (butuh cloud storage)

---

## ✅ **Solusi 2: Cloud Storage untuk Gambar (OPTIONAL)**

### Cloudinary (Recommended)
- ✅ **Gratis**: 25GB storage, 25GB bandwidth/month
- ✅ **CDN**: Loading cepat
- ✅ **Image optimization**: Auto-resize, compress

### Setup Cloudinary:

#### 1. Sign Up
```
https://cloudinary.com/users/register/free
```

#### 2. Install SDK
```bash
pip install cloudinary
```

#### 3. Update Code
Upload gambar ke Cloudinary instead of local filesystem.

**Keuntungan:**
- Gambar tidak hilang
- Loading lebih cepat (CDN)
- Auto-optimization

**Kekurangan:**
- Perlu setup tambahan
- Limit 25GB/month

---

## ✅ **Solusi 3: Hybrid (BEST)**

### Kombinasi PostgreSQL + Cloudinary

**Database (PostgreSQL):**
- Detection logs
- Metadata (timestamp, location, prediction)
- Cloudinary URLs

**Cloud Storage (Cloudinary):**
- Original images
- Heatmap images

**Workflow:**
1. User upload gambar
2. Upload ke Cloudinary → dapat URL
3. AI prediction
4. Save log + URL ke PostgreSQL
5. Display dari Cloudinary URL

**Keuntungan:**
- ✅ Tidak ada data hilang
- ✅ Fast loading
- ✅ Scalable
- ✅ 100% persistent

---

## 🚀 **Quick Fix Sementara (Tanpa Database)**

Jika tidak mau setup database sekarang, gunakan workaround ini:

### 1. Disable Heatmap (Hemat Memory)
Heatmap butuh banyak memory dan sering gagal di Railway.

Edit `app.py`:
```python
# Generate heatmap
heatmap_filename = None
heatmap_error = "Heatmap disabled to save memory"
# Comment out heatmap generation
```

### 2. Accept Data Loss
- Data history akan hilang setelah restart
- User harus export CSV secara berkala
- Tambahkan warning di UI

### 3. Reduce Restart Frequency
- Optimize memory usage
- Avoid memory leaks
- Use smaller images

---

## 📊 **Comparison**

| Solution | Cost | Setup Time | Persistence | Performance |
|----------|------|------------|-------------|-------------|
| Current (JSON) | Free | 0 min | ❌ No | ⭐⭐ |
| PostgreSQL | Free | 30 min | ✅ Yes | ⭐⭐⭐⭐ |
| Cloudinary | Free | 20 min | ✅ Yes | ⭐⭐⭐⭐⭐ |
| Hybrid | Free | 60 min | ✅ Yes | ⭐⭐⭐⭐⭐ |

---

## 🎯 **Rekomendasi**

### Untuk Demo/Presentasi (Sekarang):
**Quick Fix** - Disable heatmap, accept data loss
- Setup: 5 menit
- Cukup untuk demo
- Export CSV sebelum presentasi

### Untuk Production (Nanti):
**Hybrid Solution** - PostgreSQL + Cloudinary
- Setup: 1 jam
- Data persistent
- Professional solution

---

## 🔨 **Mau Saya Implementasikan Yang Mana?**

**Option A: Quick Fix (5 menit)**
- Disable heatmap
- Add warning about data loss
- Deploy sekarang

**Option B: PostgreSQL Only (30 menit)**
- Setup database
- Migrate logs to PostgreSQL
- History persistent (gambar tetap hilang)

**Option C: Full Solution (1 jam)**
- PostgreSQL + Cloudinary
- Everything persistent
- Production-ready

Pilih mana? Atau mau tetap pakai yang sekarang dan accept data loss?
