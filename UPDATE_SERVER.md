# 🔄 Update Server dengan Perubahan Terbaru

## Masalah
Perubahan pada `templates/campus_map.html` tidak muncul di browser karena:
1. Server belum memuat template terbaru
2. Browser masih menggunakan cache lama

## ✅ Solusi: Update Server

### 1️⃣ Commit dan Push Perubahan (dari laptop)
```bash
git add templates/campus_map.html
git commit -m "Complete grouped marker implementation with showLocationDetailGroup"
git push origin main
```

### 2️⃣ Update Server (SSH ke server)
```bash
# Masuk ke direktori project
cd ~/waste-detection

# Pull perubahan terbaru
git fetch origin
git reset --hard origin/main

# Restart service
sudo systemctl restart waste-detection

# Cek status
sudo systemctl status waste-detection
```

### 3️⃣ Clear Browser Cache
- **Chrome/Edge**: `Ctrl + Shift + R` atau `Ctrl + F5`
- **Firefox**: `Ctrl + Shift + R`
- Atau buka DevTools (F12) → Network tab → centang "Disable cache"

## 🎯 Fitur Baru yang Sudah Diimplementasi

### ✅ Backend (app.py)
- `_get_map_data_from_json()` mengembalikan **SEMUA deteksi** (bukan hanya latest)
- Filter lokasi invalid (skip "Lokasi tidak diketahui", "Unknown", atau kosong)

### ✅ Frontend (campus_map.html)
- **Grouping by location**: Deteksi dengan lokasi sama dikelompokkan
- **Count badge**: Menampilkan jumlah deteksi di pojok marker (jika > 1)
- **Modal profesional**: `showLocationDetailGroup()` menampilkan semua deteksi dalam modal
- **Animasi smooth**: fadeIn dan slideUp untuk UX yang lebih baik
- **Scrollable**: Modal bisa di-scroll jika banyak deteksi
- **Color-coded**: Setiap status punya warna berbeda (hijau/kuning/merah)

## 📊 Cara Kerja

1. **API `/api/map-data`** mengembalikan semua deteksi (tidak filter per lokasi)
2. **Frontend** mengelompokkan deteksi berdasarkan lokasi
3. **Marker** menampilkan deteksi terbaru + badge jumlah total
4. **Klik marker** → Modal muncul dengan **semua riwayat deteksi** di lokasi tersebut

## 🔍 Verifikasi

Setelah update, cek:
1. ✅ Marker dengan lokasi sama menampilkan badge angka
2. ✅ Klik marker membuka modal dengan semua deteksi
3. ✅ Modal menampilkan riwayat lengkap dengan timestamp
4. ✅ Tidak ada deteksi yang hilang/tertimpa

## 🐛 Troubleshooting

### Perubahan masih tidak muncul?
```bash
# Cek commit terakhir di server
cd ~/waste-detection
git log -1

# Pastikan commit hash sama dengan laptop
# Jika berbeda, ulangi git pull
```

### Service tidak restart?
```bash
# Force restart
sudo systemctl stop waste-detection
sudo systemctl start waste-detection

# Cek log
sudo journalctl -u waste-detection -f
```

### Browser masih cache lama?
1. Buka Incognito/Private window
2. Atau clear all browser data (Ctrl + Shift + Delete)
3. Atau tambahkan `?v=2` di URL: `https://waste-detection.online/map?v=2`

---

**Status**: ✅ Implementasi lengkap, tinggal update server dan clear cache
