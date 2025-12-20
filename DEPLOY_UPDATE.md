# Deploy Update ke Server Production

## ⚠️ IMPORTANT: Clear Old Data

**Data lama masih menggunakan Grad-CAM heatmap!**

Sebelum atau setelah deploy, hapus data lama:

```bash
# SSH ke server
ssh user@your-server-ip

# Navigate ke project
cd /path/to/waste-detection

# Backup old data (optional)
cp detection_logs.json detection_logs_backup_$(date +%Y%m%d).json

# Delete old data
rm detection_logs.json

# Restart service
sudo systemctl restart waste-detection
```

**Catatan:** Ini akan menghapus semua history deteksi lama. Jika ingin keep history, skip langkah ini (tapi data lama akan tetap tampil dengan Grad-CAM).

---

## Perubahan yang Sudah Di-push

✅ **Commit terakhir:** `0d2b2d4`

### Fitur Baru:
1. ✅ Multiple image upload (unlimited)
2. ✅ Batch processing dengan progress bar
3. ✅ Summary statistics (total, per kategori, total objek)
4. ✅ Detail lengkap per gambar (visualisasi, probabilitas, rekomendasi)
5. ✅ YOLO-based density heatmap (mengganti Grad-CAM)
6. ✅ Improved classification logic dengan spatial clustering
7. ✅ Priority fix (LOW/MEDIUM/HIGH sesuai klasifikasi)

### Bug Fixes:
1. ✅ Hapus warning box yang tidak relevan
2. ✅ Fix priority yang selalu HIGH
3. ✅ Fix save log setelah YOLO override
4. ✅ Fix styling result box di multiple upload

---

## Cara Deploy ke Server

### Option 1: SSH Manual (Recommended)

```bash
# 1. SSH ke server
ssh user@your-server-ip
# atau jika pakai Tailscale
ssh user@100.x.x.x

# 2. Navigate ke project directory
cd /path/to/waste-detection

# 3. Backup & delete old data (IMPORTANT!)
cp detection_logs.json detection_logs_backup_$(date +%Y%m%d).json
rm detection_logs.json

# 4. Pull latest changes
git pull origin main

# 5. Restart service
sudo systemctl restart waste-detection

# 6. Check status
sudo systemctl status waste-detection

# 7. Check logs (optional)
sudo journalctl -u waste-detection -f
```

### Option 2: Automated Script

Buat file `deploy.sh` di server:

```bash
#!/bin/bash
echo "🚀 Deploying waste-detection updates..."

cd /path/to/waste-detection

# Backup current state
echo "📦 Creating backup..."
git stash

# Backup and clear old data
echo "🗑️ Clearing old data (Grad-CAM)..."
if [ -f "detection_logs.json" ]; then
    cp detection_logs.json detection_logs_backup_$(date +%Y%m%d).json
    rm detection_logs.json
    echo "✅ Old data cleared and backed up"
fi

# Pull latest
echo "⬇️ Pulling latest changes..."
git pull origin main

# Check if pull successful
if [ $? -eq 0 ]; then
    echo "✅ Pull successful"
    
    # Restart service
    echo "🔄 Restarting service..."
    sudo systemctl restart waste-detection
    
    # Wait for service to start
    sleep 3
    
    # Check status
    if systemctl is-active --quiet waste-detection; then
        echo "✅ Service running successfully!"
        echo "🌐 Access: https://waste-detection.online"
        echo "📊 Old data cleared - history will be empty"
    else
        echo "❌ Service failed to start!"
        echo "📋 Check logs: sudo journalctl -u waste-detection -n 50"
        exit 1
    fi
else
    echo "❌ Pull failed!"
    git stash pop
    exit 1
fi

echo "🎉 Deployment complete!"
```

Jalankan:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Verification Checklist

Setelah deploy, verify fitur-fitur berikut:

### 1. Multiple Upload
- [ ] Bisa pilih multiple files
- [ ] Progress bar muncul
- [ ] Summary statistics benar
- [ ] Setiap gambar tampil dengan detail lengkap

### 2. YOLO Detection
- [ ] Bounding boxes muncul
- [ ] Object count akurat
- [ ] Density heatmap konsisten dengan detection

### 3. Classification
- [ ] 0 objek → Bersih (LOW priority)
- [ ] 1-8 objek scattered → Tumpukan Ringan (MEDIUM priority)
- [ ] Objek piled/many → Tumpukan Parah (HIGH priority)

### 4. Visualisasi
- [ ] 3 gambar muncul (Original, Heatmap, YOLO)
- [ ] Styling result box benar (colored background)
- [ ] Probabilitas berbeda per gambar

### 5. History & Map
- [ ] Data baru tersimpan dengan priority yang benar
- [ ] Heatmap menggunakan YOLO density (bukan Grad-CAM)
- [ ] No warning boxes

---

## Troubleshooting

### Issue 1: Service Gagal Start

```bash
# Check error logs
sudo journalctl -u waste-detection -n 100

# Common issues:
# - Port 8080 already in use
# - Python dependencies missing
# - Model file not found
```

**Fix:**
```bash
# Kill existing process
sudo pkill -f "python app.py"

# Reinstall dependencies (if needed)
cd /path/to/waste-detection
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl restart waste-detection
```

### Issue 2: YOLO Model Not Found

```bash
# Check if model exists
ls -lh models/waste_yolo_best.pt

# If not found, pull again
git pull origin main

# Or download manually
wget https://github.com/FauzanAzhimaa/waste-detection/raw/main/models/waste_yolo_best.pt -O models/waste_yolo_best.pt
```

### Issue 3: Old Data Still Showing

```bash
# Clear old logs (optional - will delete history!)
rm detection_logs.json

# Restart service
sudo systemctl restart waste-detection
```

### Issue 4: Cloudflare Tunnel Issues

```bash
# Check tunnel status
sudo systemctl status cloudflared

# Restart tunnel
sudo systemctl restart cloudflared

# Check tunnel logs
sudo journalctl -u cloudflared -f
```

---

## Rollback (Jika Ada Masalah)

```bash
# 1. SSH ke server
ssh user@your-server

# 2. Navigate to project
cd /path/to/waste-detection

# 3. Check commit history
git log --oneline -10

# 4. Rollback to previous commit (before multiple upload)
git checkout ef908b0  # Commit sebelum multiple upload

# 5. Restart service
sudo systemctl restart waste-detection

# 6. Verify
curl http://localhost:8080
```

---

## Performance Notes

### Multiple Upload Performance:
- **Sequential processing**: Gambar diproses satu per satu
- **Estimated time**: ~3-5 detik per gambar
- **Recommendation**: Max 10 gambar per batch untuk UX yang baik

### Server Resources:
- **CPU**: YOLO detection CPU-intensive
- **Memory**: ~500MB per process
- **Disk**: Temp files cleaned after upload to cloud

### Optimization Tips:
1. Pastikan Cloudinary configured untuk auto-cleanup temp files
2. Monitor disk space: `df -h`
3. Monitor memory: `free -h`
4. Set up log rotation untuk journald

---

## Post-Deployment

### 1. Announce to Users
```
🎉 Update Sistem Deteksi Sampah!

Fitur Baru:
✨ Upload multiple gambar sekaligus (unlimited!)
📊 Summary statistics untuk batch analysis
🎯 YOLO detection lebih akurat
🔥 Density heatmap yang konsisten
⚡ Priority yang benar (LOW/MEDIUM/HIGH)

Akses: https://waste-detection.online
```

### 2. Monitor Logs
```bash
# Real-time monitoring
sudo journalctl -u waste-detection -f

# Check for errors
sudo journalctl -u waste-detection | grep ERROR

# Check YOLO detection
sudo journalctl -u waste-detection | grep "YOLO"
```

### 3. Backup
```bash
# Backup detection logs (if using JSON)
cp detection_logs.json detection_logs_backup_$(date +%Y%m%d).json

# Backup database (if using PostgreSQL)
pg_dump waste_detection > backup_$(date +%Y%m%d).sql
```

---

## Contact

Jika ada masalah saat deployment, check:
1. Server logs: `sudo journalctl -u waste-detection -n 100`
2. Application logs: Check console output
3. Network: `curl http://localhost:8080`
4. Cloudflare: Check tunnel status

---

## Summary

**Total Changes:** 10+ commits
**New Features:** 7
**Bug Fixes:** 4
**Files Modified:** 3 (app.py, templates/index.html, templates/history.html)

**Ready to deploy!** 🚀
