# 📝 Changelog - Sistem Deteksi Sampah

## [Update 17 Desember 2025 - 22:20 WIB]

### ✅ **Perbaikan Timezone**
- **Masalah:** Waktu di riwayat menampilkan UTC (tidak sesuai dengan waktu lokal Indonesia)
- **Solusi:** Semua timestamp sekarang menggunakan **WIB (UTC+7)**
- **Perubahan:**
  - Timestamp di `detection_logs.json` sekarang dalam WIB
  - Format tampilan: `DD/MM/YYYY HH:MM:SS WIB`
  - Ditampilkan di halaman hasil deteksi dan riwayat

### ✅ **Perbaikan Heatmap Generation**
- **Masalah:** Heatmap tidak muncul di Railway karena memory limit
- **Solusi:**
  - Auto-resize gambar max 800px untuk menghemat memory
  - Memory-efficient processing dengan float32
  - Graceful error handling jika heatmap gagal
  - Prediksi tetap ditampilkan meski heatmap gagal
- **Optimizations:**
  - Layer selection yang lebih optimal
  - Better error messages dan logging
  - Cache busting untuk mencegah cache gambar lama

### ✅ **Informasi Penyimpanan Data**
- **Ditambahkan:** Info box di halaman riwayat
- **Menjelaskan:**
  - Semua data tersimpan di `detection_logs.json`
  - Data akan hilang setelah Railway restart (ephemeral filesystem)
  - Solusi: Export CSV secara berkala atau gunakan database eksternal

### 📊 **Status Fitur**

#### ✅ **Yang Berfungsi:**
1. Upload gambar atau capture dari kamera
2. Deteksi AI dengan 3 kategori (Bersih, Tumpukan Ringan, Tumpukan Parah)
3. Heatmap visualization (kadang gagal di Railway karena memory)
4. Location tracking (manual input atau GPS dari EXIF)
5. Detection history dengan filter dan search
6. Campus map visualization
7. Export to CSV
8. Responsive design untuk mobile
9. **Timezone WIB yang benar**

#### ⚠️ **Known Limitations:**
1. **Memory Limit:** Railway free tier = 512MB
   - Heatmap kadang gagal untuk gambar besar
   - Solusi: Gunakan gambar <3MB
2. **Ephemeral Filesystem:** 
   - File upload dan logs hilang setelah restart
   - Solusi: Export CSV atau upgrade ke database
3. **Model Accuracy:** ~40% karena data training terbatas
   - Perlu 300+ gambar per kategori untuk accuracy lebih baik

---

## [Update Sebelumnya]

### [16 Desember 2025]
- Deploy ke Railway berhasil
- Gunicorn untuk production server
- Timeout 120 detik untuk Railway

### [15 Desember 2025]
- Camera capture feature
- Campus map dengan real-time data
- Responsive design untuk mobile
- History page dengan stats

### [Awal Desember 2025]
- Initial Flask application
- MobileNetV2 model training
- Grad-CAM heatmap visualization
- OOP architecture

---

## 🚀 **Deployment Info**

**URL:** https://waste-detection-production-4613.up.railway.app

**Platform:** Railway.app
**Plan:** Free tier ($5 credit/month)
**Memory:** 512MB
**Storage:** Ephemeral

**Deploy Command:**
```bash
railway up --detach
```

**Check Logs:**
```bash
railway logs
```

---

## 📖 **Dokumentasi**

- `README.md` - Overview dan cara penggunaan
- `DEPLOY_RAILWAY.md` - Panduan deploy ke Railway
- `TROUBLESHOOTING_HEATMAP.md` - Troubleshooting heatmap issues
- `DEPLOY_NGROK.md` - Alternatif deploy dengan Ngrok (backup)
- `PANDUAN_CEPAT.md` - Quick start guide
- `CARA_TARUH_DATA.md` - Cara menambah data training

---

## 🔮 **Future Improvements**

### High Priority:
1. **Database Integration** (PostgreSQL/MongoDB)
   - Persistent storage untuk logs
   - Tidak hilang setelah restart
2. **Improve Model Accuracy**
   - Collect 300+ images per category
   - Retrain model
   - Target: 85%+ accuracy

### Medium Priority:
3. **Cloud Storage** (AWS S3/Cloudinary)
   - Persistent image storage
   - CDN untuk loading lebih cepat
4. **User Authentication**
   - Login system
   - Role-based access (admin, user)
5. **Notification System**
   - Email/WhatsApp alert untuk tumpukan parah
   - Real-time notifications

### Low Priority:
6. **Analytics Dashboard**
   - Grafik trend kebersihan
   - Heatmap lokasi bermasalah
7. **Mobile App**
   - Native Android/iOS app
   - Push notifications
8. **API Documentation**
   - Swagger/OpenAPI docs
   - Public API untuk integrasi

---

## 🐛 **Bug Reports**

Jika menemukan bug, catat:
1. Waktu kejadian (WIB)
2. Screenshot error
3. Langkah untuk reproduce
4. Browser/device yang digunakan

---

## 👥 **Contributors**

- Fauzan Azhima - Developer
- Kampus 1 UNJANI Yogyakarta - Client

---

## 📄 **License**

Proprietary - Kampus 1 Universitas Jenderal Achmad Yani Yogyakarta
