# 🌐 Deploy dengan Ngrok - Share Localhost ke Internet

## ✨ **KENAPA NGROK?**

- ✅ **Gratis** - Tidak perlu kartu kredit
- ✅ **Instant** - Setup 2 menit
- ✅ **Stable** - Localhost performance
- ✅ **Public URL** - Bisa diakses siapa saja
- ✅ **No file loss** - Semua data persist
- ✅ **Fast** - Tidak ada cold start

---

## 🚀 **SETUP NGROK (5 MENIT)**

### **1. Download Ngrok**

Buka: https://ngrok.com/download

Atau download langsung:
- Windows: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip

### **2. Extract File**

Extract `ngrok.exe` ke folder project atau folder lain yang mudah diakses.

### **3. Sign Up (Gratis)**

1. Buka: https://dashboard.ngrok.com/signup
2. Sign up dengan Google/GitHub (gratis)
3. Copy **Authtoken** dari dashboard

### **4. Setup Authtoken**

Buka terminal/PowerShell di folder ngrok, jalankan:

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

Ganti `YOUR_AUTHTOKEN_HERE` dengan token dari dashboard.

---

## 🎯 **CARA MENGGUNAKAN**

### **Step 1: Jalankan Flask App**

```bash
# Aktifkan virtual environment
.venv\Scripts\activate

# Jalankan aplikasi
python app.py
```

Server akan berjalan di: http://localhost:8080

### **Step 2: Jalankan Ngrok (Terminal Baru)**

Buka terminal/PowerShell **BARU**, jalankan:

```bash
ngrok http 8080
```

### **Step 3: Copy Public URL**

Ngrok akan menampilkan:

```
Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        Asia Pacific (ap)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:8080

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Public URL**: `https://xxxx-xxxx-xxxx.ngrok-free.app`

### **Step 4: Share URL**

Kirim URL tersebut ke siapa saja! Mereka bisa akses aplikasi Anda dari mana saja.

---

## 📱 **FITUR NGROK FREE**

✅ **1 Online Tunnel** - 1 URL aktif
✅ **40 Connections/Minute** - Cukup untuk demo
✅ **HTTPS** - Secure connection
✅ **Random URL** - URL berubah setiap restart
✅ **No Time Limit** - Bisa jalan 24/7 selama PC nyala

---

## 🎨 **TIPS & TRICKS**

### **Custom Subdomain (Paid)**

Ngrok paid ($8/bulan) bisa custom subdomain:
```bash
ngrok http 8080 --subdomain=waste-detection-unjani
```

URL jadi: `https://waste-detection-unjani.ngrok.app`

### **Keep Alive**

Ngrok akan tetap jalan selama:
1. PC/Laptop tidak dimatikan
2. Flask app tetap running
3. Internet tetap connect

### **Monitor Traffic**

Buka: http://localhost:4040

Dashboard untuk lihat:
- Request/Response
- Traffic statistics
- Error logs

---

## 🔧 **TROUBLESHOOTING**

### **Error: "command not found"**

Pastikan ngrok.exe ada di folder yang sama atau tambahkan ke PATH.

### **Error: "authentication failed"**

Jalankan ulang:
```bash
ngrok config add-authtoken YOUR_TOKEN
```

### **URL Berubah Setiap Restart**

Normal untuk free tier. Paid plan bisa fixed URL.

---

## 📊 **PERBANDINGAN**

| Platform | Speed | Stability | Persist | Cost |
|----------|-------|-----------|---------|------|
| **Ngrok** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | FREE |
| Railway | ⭐⭐ | ⭐⭐ | ❌ | FREE |
| Render | ⭐⭐ | ⭐⭐⭐ | ❌ | FREE |

---

## 🎯 **KESIMPULAN**

**Ngrok adalah solusi TERBAIK untuk:**
- Demo/Presentasi
- Testing dengan tim
- Share ke dosen/penguji
- Development yang butuh public URL

**Perfect untuk project ini!** 🚀

---

## 📝 **QUICK START**

```bash
# Terminal 1: Flask App
.venv\Scripts\activate
python app.py

# Terminal 2: Ngrok
ngrok http 8080

# Share URL yang muncul!
```

**SELESAI!** Aplikasi bisa diakses dari mana saja! 🎉
