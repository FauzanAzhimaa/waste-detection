# 🐧 Deploy ke Server Linux dengan Tailscale

## Keuntungan Solusi Ini
- ✅ 24/7 online tanpa laptop menyala
- ✅ Tidak ada batasan memory (pakai resource server sendiri)
- ✅ 100% gratis (server sendiri)
- ✅ Akses via Tailscale dari mana saja
- ✅ Semua fitur jalan (detection + heatmap)
- ✅ Lebih cepat dari cloud free tier

---

## Persiapan

### 1. Informasi yang Dibutuhkan
- IP Tailscale server (misal: `100.x.x.x`)
- SSH access ke server
- Server specs minimal:
  - RAM: 2GB+ (recommended 4GB)
  - Storage: 5GB free space
  - OS: Ubuntu 20.04+ / Debian 11+ / CentOS 8+

### 2. Cek Koneksi Tailscale
```bash
# Dari laptop Windows, test SSH via Tailscale
ssh user@100.x.x.x
```

---

## Langkah 1: Setup Server Linux

### 1.1 Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Install Python 3.9+
```bash
# Cek versi Python
python3 --version

# Jika < 3.9, install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y
```

### 1.3 Install Dependencies System
```bash
# Install library untuk OpenCV dan TensorFlow
sudo apt install -y \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git
```

---

## Langkah 2: Upload Project ke Server

### Opsi A: Via Git (Recommended)
```bash
# Di server
cd ~
git clone https://github.com/FauzanAzhimaa/waste-detection.git
cd waste-detection
```

### Opsi B: Via SCP (Jika tidak pakai Git)
```bash
# Dari laptop Windows (PowerShell)
# Compress project dulu
tar -czf waste-detection.tar.gz -C "D:\Semester 5\Kecerdasan Buatan\Project Deteksi Tumpukan Sampah" .

# Upload ke server
scp waste-detection.tar.gz user@100.x.x.x:~/

# Di server, extract
cd ~
tar -xzf waste-detection.tar.gz
mv "Project Deteksi Tumpukan Sampah" waste-detection
cd waste-detection
```

---

## Langkah 3: Setup Python Environment

### 3.1 Create Virtual Environment
```bash
cd ~/waste-detection
python3 -m venv venv
source venv/bin/activate
```

### 3.2 Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Catatan:** Install TensorFlow di Linux bisa lama (5-10 menit), sabar ya!

---

## Langkah 4: Test Run

### 4.1 Test Manual
```bash
# Pastikan masih di venv
source venv/bin/activate

# Run app
python app.py
```

Output yang diharapkan:
```
📦 Loading model from models/waste_mobilenet.h5...
✓ Model loaded successfully (CPU mode)
📁 Temp folder: temp
💾 Storage: JSON file (fallback)
🚀 Sistem Deteksi Sampah - Kampus 1 UNJANI Yogyakarta
====================================
📍 Server: http://localhost:8080
```

### 4.2 Test Akses dari Laptop
Buka browser di laptop Windows:
```
http://100.x.x.x:8080
```
(Ganti `100.x.x.x` dengan IP Tailscale server kamu)

Jika bisa akses, berarti berhasil! Tekan `Ctrl+C` untuk stop.

---

## Langkah 5: Setup Systemd Service (Auto Start)

Agar app jalan otomatis saat server restart dan jalan di background.

### 5.1 Create Service File
```bash
sudo nano /etc/systemd/system/waste-detection.service
```

### 5.2 Paste Config Ini
```ini
[Unit]
Description=Waste Detection System - Kampus 1 UNJANI Yogyakarta
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/waste-detection
Environment="PATH=/home/YOUR_USERNAME/waste-detection/venv/bin"
ExecStart=/home/YOUR_USERNAME/waste-detection/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**PENTING:** Ganti `YOUR_USERNAME` dengan username server kamu!

### 5.3 Enable dan Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start
sudo systemctl enable waste-detection

# Start service
sudo systemctl start waste-detection

# Cek status
sudo systemctl status waste-detection
```

Output yang diharapkan:
```
● waste-detection.service - Waste Detection System
   Loaded: loaded
   Active: active (running)
```

### 5.4 Cek Logs
```bash
# Lihat logs real-time
sudo journalctl -u waste-detection -f

# Lihat logs terakhir
sudo journalctl -u waste-detection -n 50
```

---

## Langkah 6: Setup Firewall (Opsional)

Jika server pakai firewall:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 8080/tcp
sudo ufw reload

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

---

## Langkah 7: Akses dari Mana Saja

### Via Tailscale (Recommended)
```
http://100.x.x.x:8080
```

### Via Tailscale Hostname (Jika sudah setup)
```
http://your-server-name.tailnet-xxxx.ts.net:8080
```

### Share ke Dosen/Teman
1. Mereka harus install Tailscale
2. Invite mereka ke Tailnet kamu
3. Mereka bisa akses via IP Tailscale

---

## Management Commands

### Start Service
```bash
sudo systemctl start waste-detection
```

### Stop Service
```bash
sudo systemctl stop waste-detection
```

### Restart Service
```bash
sudo systemctl restart waste-detection
```

### Cek Status
```bash
sudo systemctl status waste-detection
```

### Lihat Logs
```bash
sudo journalctl -u waste-detection -f
```

### Update Code (Jika ada perubahan)
```bash
# Stop service
sudo systemctl stop waste-detection

# Pull latest code
cd ~/waste-detection
git pull

# Restart service
sudo systemctl start waste-detection
```

---

## Troubleshooting

### Port 8080 Sudah Dipakai
Ubah port di `app.py`:
```python
# Line terakhir di app.py
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8081))  # Ganti ke 8081
    waste_app.run(debug=False, host='0.0.0.0', port=port)
```

Atau set environment variable di service file:
```ini
Environment="PORT=8081"
```

### Memory Error
Cek memory server:
```bash
free -h
```

Jika RAM < 2GB, TensorFlow mungkin crash. Solusi:
- Upgrade RAM server
- Atau pakai swap file (lebih lambat)

### Model Tidak Load
Pastikan file model ada:
```bash
ls -lh ~/waste-detection/models/waste_mobilenet.h5
```

### Permission Error
Fix ownership:
```bash
cd ~/waste-detection
sudo chown -R $USER:$USER .
```

---

## Monitoring

### Cek Resource Usage
```bash
# CPU dan Memory
htop

# Atau
top

# Disk usage
df -h
```

### Cek App Logs
```bash
# Real-time
sudo journalctl -u waste-detection -f

# Last 100 lines
sudo journalctl -u waste-detection -n 100
```

---

## Backup & Restore

### Backup Detection Logs
```bash
# Backup JSON logs
cp ~/waste-detection/detection_logs.json ~/backup_logs_$(date +%Y%m%d).json

# Backup temp images (jika ada)
tar -czf ~/backup_temp_$(date +%Y%m%d).tar.gz ~/waste-detection/temp/
```

### Auto Backup (Cron)
```bash
# Edit crontab
crontab -e

# Tambahkan (backup setiap hari jam 2 pagi)
0 2 * * * cp ~/waste-detection/detection_logs.json ~/backup_logs_$(date +\%Y\%m\%d).json
```

---

## Keamanan

### 1. Hanya Akses via Tailscale
Jangan expose port 8080 ke internet public. Hanya akses via Tailscale.

### 2. Update Reguler
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd ~/waste-detection
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 3. Firewall
Pastikan firewall aktif dan hanya allow port yang diperlukan:
```bash
sudo ufw status
```

---

## Performa Tips

### 1. Gunakan Gunicorn (Production)
Untuk performa lebih baik, pakai Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Update service file
ExecStart=/home/YOUR_USERNAME/waste-detection/venv/bin/gunicorn -w 2 -b 0.0.0.0:8080 app:app
```

### 2. Nginx Reverse Proxy (Opsional)
Untuk HTTPS dan caching, bisa tambah Nginx di depan.

---

## URL Akses

Setelah setup selesai, aplikasi bisa diakses:

**Via Tailscale IP:**
```
http://100.x.x.x:8080
```

**Via Tailscale Hostname:**
```
http://your-server.tailnet.ts.net:8080
```

**Untuk Demo:**
- Buka URL di browser
- Upload gambar
- Semua fitur jalan (detection + heatmap)
- 24/7 online!

---

## Kesimpulan

✅ **Setup selesai!** Aplikasi sekarang:
- Jalan 24/7 di server Linux
- Akses via Tailscale dari mana saja
- Auto-start saat server restart
- Semua fitur jalan sempurna
- Tidak perlu laptop menyala

**Untuk tugas kuliah:**
- Share IP Tailscale ke dosen (atau invite ke Tailnet)
- Atau demo langsung via screen share
- Aplikasi selalu online untuk testing

---

**Generated:** 19 Desember 2025  
**Server:** Linux + Tailscale  
**Status:** Production Ready 🚀
