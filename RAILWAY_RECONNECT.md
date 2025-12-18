# 🚂 Cara Reconnect Railway ke GitHub Repo Baru

## Masalah
Railway masih terhubung ke repo GitHub lama yang sudah dihapus, sehingga muncul **Bad Gateway** error.

## Solusi: Reconnect ke Repo Baru

### Langkah 1: Buka Railway Dashboard
1. Login ke Railway: https://railway.app
2. Pilih project: **waste-detection-production-4613**

### Langkah 2: Disconnect Repo Lama
1. Klik tab **Settings** di project
2. Scroll ke bagian **Service**
3. Klik **Disconnect Source** atau **Remove GitHub Connection**

### Langkah 3: Connect Repo Baru
1. Klik **Connect Repo** atau **Add GitHub Repo**
2. Pilih repo: **FauzanAzhimaa/waste-detection**
3. Branch: **main**
4. Root Directory: `/` (default)

### Langkah 4: Trigger Redeploy
1. Setelah connected, Railway akan otomatis deploy
2. Atau klik **Deploy** manual di tab **Deployments**

### Langkah 5: Cek Environment Variables
Pastikan env vars masih ada:
- `DATABASE_URL` (Supabase - DISABLED untuk Railway free)
- `CLOUDINARY_CLOUD_NAME` (DISABLED untuk Railway free)
- `CLOUDINARY_API_KEY` (DISABLED untuk Railway free)
- `CLOUDINARY_API_SECRET` (DISABLED untuk Railway free)

**CATATAN**: Database dan Cloudinary di-disable di Railway karena memory limit 512MB. App akan fallback ke JSON file storage.

### Langkah 6: Monitor Logs
1. Klik tab **Deployments**
2. Pilih deployment terbaru
3. Klik **View Logs**
4. Tunggu sampai muncul: `✓ Model loaded successfully`

### Langkah 7: Test App
Buka URL: https://waste-detection-production-4613.up.railway.app

## Expected Output di Logs
```
📦 Loading model from models/waste_mobilenet.h5...
✓ Model loaded successfully
📁 Temp folder: temp
💾 Storage: JSON file (fallback)
🚀 Sistem Deteksi Sampah - Kampus 1 UNJANI Yogyakarta
```

## Troubleshooting

### Masih Bad Gateway?
- Tunggu 2-3 menit untuk deployment selesai
- Cek logs untuk error
- Pastikan `models/waste_mobilenet.h5` ada di repo

### CUDA Error di Logs?
- Normal! Railway tidak punya GPU
- App sudah disable GPU dengan: `tf.config.set_visible_devices([], 'GPU')`
- Model tetap jalan di CPU

### Memory Error?
- Railway free tier hanya 512MB
- Heatmap generation mungkin gagal (normal)
- Detection tetap jalan, hanya heatmap yang skip

## Status Saat Ini
- ✅ Code sudah dipush ke GitHub repo baru
- ✅ Bug `UPLOAD_FOLDER` sudah diperbaiki
- ✅ 26 file platform berbayar sudah dihapus
- ⏳ Railway perlu reconnect ke repo baru (manual step)

## URL
- GitHub: https://github.com/FauzanAzhimaa/waste-detection
- Railway: https://waste-detection-production-4613.up.railway.app
