# 🔥 Troubleshooting Heatmap

## Masalah: Heatmap Tidak Muncul

### Penyebab Umum:

#### 1. **Memory Limit di Railway (512MB)**
Railway free tier memiliki memory limit 512MB. Grad-CAM membutuhkan memory ekstra untuk:
- Load model
- Process image
- Compute gradients
- Generate heatmap overlay

**Solusi:**
- Gambar otomatis di-resize max 800px untuk menghemat memory
- Jika tetap gagal, coba gambar yang lebih kecil (<1MB)

#### 2. **Ephemeral Filesystem**
Railway menggunakan ephemeral filesystem - file yang di-upload tidak persisten setelah restart.

**Solusi:**
- Heatmap di-generate on-the-fly setiap request
- Jika server restart, file lama akan hilang
- Upload ulang gambar untuk analisis baru

#### 3. **Timeout (120 detik)**
Proses Grad-CAM bisa memakan waktu 30-60 detik untuk gambar besar.

**Solusi:**
- Timeout sudah di-set 120 detik
- Gunakan gambar dengan ukuran wajar (<5MB)

---

## Fitur Error Handling Baru

### ✅ Automatic Fallback
Jika heatmap gagal di-generate:
- Prediksi tetap ditampilkan (prediksi tidak terpengaruh)
- Gambar original tetap ditampilkan
- Error message ditampilkan di tempat heatmap
- User tetap bisa melihat hasil analisis

### ✅ Cache Busting
Gambar menggunakan timestamp parameter untuk mencegah cache:
```
/uploads/image.jpg?t=1234567890
```

### ✅ Image Fallback
Jika gambar gagal load, akan muncul placeholder SVG.

---

## Testing Lokal

### Test Heatmap Generation:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run app
python app.py

# Buka browser
http://localhost:8080

# Upload gambar dan cek console log
```

### Check Console Output:
```
🔥 Starting Grad-CAM generation...
✓ Original image size: (1920, 1080)
✓ Resized to: (800, 450) (memory optimization)
✓ Using layer: Conv_1
✓ Heatmap computed, shape: (7, 7)
✓ Heatmap generated successfully
✓ Heatmap saved: heatmap_20251217_211530_image.jpg
```

---

## Monitoring di Railway

### Check Logs:
```bash
railway logs
```

Look for:
- `✓ Heatmap generated successfully` - Success
- `❌ Memory error during Grad-CAM` - Memory issue
- `❌ Grad-CAM error` - Other error

### Memory Usage:
Railway dashboard menampilkan memory usage real-time.
- Normal: 200-400MB
- High: 400-500MB (risk of failure)
- Critical: >500MB (akan crash)

---

## Optimizations Applied

1. **Image Size Limit**: Max 800px dimension
2. **Memory-Efficient Processing**: Using float32 instead of float64
3. **Layer Selection**: Optimized to find best conv layer
4. **Error Handling**: Graceful degradation if heatmap fails
5. **Timeout**: 120 seconds for Railway

---

## Alternatif Jika Heatmap Tetap Gagal

### Option 1: Disable Heatmap
Edit `app.py`, comment out heatmap generation:
```python
# Generate heatmap
heatmap_filename = None
heatmap_error = "Heatmap disabled"
# try:
#     overlay = self.model_handler.generate_gradcam(...)
# except Exception as e:
#     ...
```

### Option 2: Upgrade Railway Plan
- Hobby Plan: $5/month
- Memory: 8GB (16x lebih besar)
- No timeout issues

### Option 3: Deploy ke Platform Lain
- Google Cloud Run: 2GB memory free tier
- AWS Lambda: 3GB memory (dengan container)
- Heroku: 512MB (sama seperti Railway)

---

## FAQ

**Q: Apakah prediksi tetap akurat jika heatmap gagal?**
A: Ya! Heatmap hanya visualisasi. Prediksi AI tetap 100% akurat.

**Q: Kenapa heatmap kadang berhasil, kadang gagal?**
A: Tergantung ukuran gambar dan memory usage saat itu. Railway shared resources.

**Q: Apakah bisa disable heatmap untuk mempercepat?**
A: Ya, tapi heatmap berguna untuk memahami fokus AI. Lebih baik optimize ukuran gambar.

**Q: Berapa ukuran gambar ideal?**
A: 1-3MB, resolusi 1920x1080 atau lebih kecil. Akan otomatis di-resize ke max 800px.
