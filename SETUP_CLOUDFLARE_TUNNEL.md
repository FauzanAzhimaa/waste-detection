# ☁️ Setup Cloudflare Tunnel - Solusi Hybrid

## Arsitektur Hybrid
```
┌─────────────────────────────────────────────────────────┐
│                    Linux Server                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Waste Detection App (Port 8080)          │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                               │
│         ┌────────────────┴────────────────┐             │
│         ↓                                  ↓             │
│  ┌─────────────┐                  ┌──────────────┐     │
│  │  Tailscale  │                  │  Cloudflare  │     │
│  │   Private   │                  │    Tunnel    │     │
│  └─────────────┘                  └──────────────┘     │
└─────────────────────────────────────────────────────────┘
         ↓                                  ↓
    ┌─────────┐                      ┌──────────┐
    │   You   │                      │  Public  │
    │ (Dev)   │                      │  Users   │
    └─────────┘                      └──────────┘
  100.x.x.x:8080              waste-detection.com
```

**Keuntungan:**
- ✅ **Tailscale Private:** Akses cepat untuk development (private)
- ✅ **Cloudflare Tunnel:** Akses public untuk demo/production
- ✅ **Satu app, dua cara akses**
- ✅ **Fleksibel:** Bisa matikan public access kapan saja

---

## Persiapan

### 1. Domain (Pilih Salah Satu)

**Opsi A: Pakai Domain Sendiri (Jika Punya)**
- Domain dari Niagahoster, Rumahweb, dll
- Pindahkan nameserver ke Cloudflare (gratis)

**Opsi B: Domain Gratis dari Freenom**
- Daftar di: https://www.freenom.com
- Pilih domain: `.tk`, `.ml`, `.ga`, `.cf`, `.gq`
- Gratis 1 tahun (bisa renew)

**Opsi C: Subdomain Gratis dari Cloudflare Pages**
- Format: `your-project.pages.dev`
- Tidak perlu domain sendiri

**Untuk panduan ini, saya asumsikan kamu pakai domain sendiri atau Freenom.**

### 2. Akun Cloudflare
- Daftar gratis di: https://dash.cloudflare.com/sign-up
- Verifikasi email

---

## Langkah 1: Setup Domain di Cloudflare

### 1.1 Tambah Domain ke Cloudflare

1. Login ke Cloudflare Dashboard
2. Klik **"Add a Site"**
3. Masukkan domain kamu (misal: `wastedetection.tk`)
4. Pilih plan **"Free"**
5. Klik **"Continue"**

### 1.2 Update Nameserver

Cloudflare akan kasih 2 nameserver, contoh:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

**Update di registrar domain:**
- Jika pakai Freenom: Dashboard → Manage Domain → Management Tools → Nameservers
- Jika pakai Niagahoster/Rumahweb: Client Area → Domain → Nameservers

Tunggu 5-30 menit untuk propagasi DNS.

### 1.3 Verifikasi Domain Aktif

Di Cloudflare Dashboard, tunggu sampai status berubah jadi **"Active"**.

---

## Langkah 2: Install Cloudflared di Server

### 2.1 SSH ke Server
```bash
ssh user@100.x.x.x  # Via Tailscale
```

### 2.2 Download dan Install Cloudflared

**Untuk Ubuntu/Debian:**
```bash
# Download
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify
cloudflared --version
```

**Untuk CentOS/RHEL:**
```bash
# Download
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm

# Install
sudo rpm -i cloudflared-linux-amd64.rpm

# Verify
cloudflared --version
```

---

## Langkah 3: Authenticate Cloudflared

### 3.1 Login ke Cloudflare
```bash
cloudflared tunnel login
```

Ini akan buka browser dan minta kamu login ke Cloudflare. Setelah login, pilih domain yang mau dipakai.

File certificate akan disimpan di: `~/.cloudflared/cert.pem`

---

## Langkah 4: Create Tunnel

### 4.1 Create Tunnel
```bash
cloudflared tunnel create waste-detection
```

Output:
```
Tunnel credentials written to /home/user/.cloudflared/TUNNEL_ID.json
Created tunnel waste-detection with id TUNNEL_ID
```

**Simpan TUNNEL_ID** (akan dipakai nanti).

### 4.2 List Tunnels (Verify)
```bash
cloudflared tunnel list
```

---

## Langkah 5: Configure Tunnel

### 5.1 Create Config File
```bash
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

### 5.2 Paste Configuration

**Ganti:**
- `YOUR_TUNNEL_ID` dengan tunnel ID dari step 4.1
- `YOUR_USERNAME` dengan username server kamu
- `wastedetection.tk` dengan domain kamu

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /home/YOUR_USERNAME/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  # Route untuk domain utama
  - hostname: wastedetection.tk
    service: http://localhost:8080
  
  # Route untuk subdomain (opsional)
  - hostname: app.wastedetection.tk
    service: http://localhost:8080
  
  # Catch-all rule (harus ada di akhir)
  - service: http_status:404
```

Save: `Ctrl+O`, Enter, `Ctrl+X`

---

## Langkah 6: Route DNS

### 6.1 Route Domain ke Tunnel

**Untuk domain utama:**
```bash
cloudflared tunnel route dns waste-detection wastedetection.tk
```

**Untuk subdomain (opsional):**
```bash
cloudflared tunnel route dns waste-detection app.wastedetection.tk
```

Output:
```
Created CNAME record for wastedetection.tk
```

### 6.2 Verify DNS di Cloudflare Dashboard

1. Buka Cloudflare Dashboard
2. Pilih domain kamu
3. Klik **"DNS"** → **"Records"**
4. Lihat CNAME record baru:
   - Type: `CNAME`
   - Name: `wastedetection.tk` atau `app`
   - Target: `TUNNEL_ID.cfargotunnel.com`
   - Proxy status: **Proxied** (orange cloud)

---

## Langkah 7: Run Tunnel (Test)

### 7.1 Test Run Manual
```bash
cloudflared tunnel run waste-detection
```

Output yang diharapkan:
```
INF Starting tunnel tunnelID=YOUR_TUNNEL_ID
INF Connection registered connIndex=0
INF Connection registered connIndex=1
```

### 7.2 Test Akses dari Browser

Buka browser dan akses:
```
https://wastedetection.tk
atau
https://app.wastedetection.tk
```

Jika muncul aplikasi waste detection, berarti **berhasil**! 🎉

Tekan `Ctrl+C` untuk stop tunnel.

---

## Langkah 8: Setup Systemd Service (Auto Start)

Agar tunnel jalan otomatis saat server restart.

### 8.1 Install Cloudflared Service
```bash
sudo cloudflared service install
```

### 8.2 Enable dan Start Service
```bash
# Enable auto-start
sudo systemctl enable cloudflared

# Start service
sudo systemctl start cloudflared

# Check status
sudo systemctl status cloudflared
```

Output yang diharapkan:
```
● cloudflared.service - cloudflared
   Loaded: loaded
   Active: active (running)
```

### 8.3 Check Logs
```bash
# Real-time logs
sudo journalctl -u cloudflared -f

# Last 50 lines
sudo journalctl -u cloudflared -n 50
```

---

## Langkah 9: Verify Setup Hybrid

Sekarang kamu punya **2 cara akses**:

### Akses 1: Via Tailscale (Private - Development)
```
http://100.x.x.x:8080
```
- Hanya kamu yang bisa akses
- Tidak perlu internet
- Lebih cepat (direct connection)

### Akses 2: Via Cloudflare Tunnel (Public - Demo/Production)
```
https://wastedetection.tk
```
- Siapa saja bisa akses
- HTTPS otomatis
- DDoS protection
- Professional URL

---

## Management Commands

### Cloudflare Tunnel

**Start:**
```bash
sudo systemctl start cloudflared
```

**Stop:**
```bash
sudo systemctl stop cloudflared
```

**Restart:**
```bash
sudo systemctl restart cloudflared
```

**Status:**
```bash
sudo systemctl status cloudflared
```

**Logs:**
```bash
sudo journalctl -u cloudflared -f
```

**List Tunnels:**
```bash
cloudflared tunnel list
```

**Delete Tunnel:**
```bash
cloudflared tunnel delete waste-detection
```

---

## Cloudflare Dashboard Features

### 1. Analytics
- Dashboard → Domain → Analytics
- Lihat traffic, requests, bandwidth

### 2. Access Control (Opsional)
Tambah password protection:

1. Dashboard → Zero Trust → Access → Applications
2. Add an application
3. Set policy (email whitelist, password, dll)

### 3. Caching
- Dashboard → Domain → Caching
- Set cache rules untuk static files

### 4. Firewall Rules
- Dashboard → Domain → Security → WAF
- Block countries, IPs, dll

---

## Troubleshooting

### Tunnel Tidak Connect

**Cek service status:**
```bash
sudo systemctl status cloudflared
```

**Cek logs:**
```bash
sudo journalctl -u cloudflared -n 100
```

**Restart tunnel:**
```bash
sudo systemctl restart cloudflared
```

### Domain Tidak Resolve

**Cek DNS propagation:**
```bash
nslookup wastedetection.tk
```

Atau online: https://dnschecker.org

**Tunggu 5-30 menit** untuk DNS propagation.

### Certificate Error

**Re-authenticate:**
```bash
cloudflared tunnel login
```

### Port 8080 Tidak Bisa Diakses

**Cek app running:**
```bash
sudo systemctl status waste-detection
```

**Cek port:**
```bash
sudo netstat -tlnp | grep 8080
```

---

## Security Best Practices

### 1. Firewall
Karena pakai Cloudflare Tunnel, **tidak perlu buka port 8080** ke internet:

```bash
# Pastikan port 8080 hanya listen di localhost
# Di app.py sudah set host='0.0.0.0', tapi bisa ganti ke '127.0.0.1' untuk lebih aman
```

### 2. Rate Limiting
Set di Cloudflare Dashboard → Security → Rate Limiting

### 3. SSL/TLS Mode
Dashboard → SSL/TLS → Overview → Set to **"Full (strict)"**

### 4. Bot Protection
Dashboard → Security → Bots → Enable

---

## Update Domain (Jika Ganti Domain)

### 1. Update Config
```bash
nano ~/.cloudflared/config.yml
```

Ganti hostname ke domain baru.

### 2. Route DNS Baru
```bash
cloudflared tunnel route dns waste-detection newdomain.com
```

### 3. Restart Tunnel
```bash
sudo systemctl restart cloudflared
```

---

## Monitoring

### Check Tunnel Status
```bash
cloudflared tunnel info waste-detection
```

### Check Connections
```bash
sudo journalctl -u cloudflared -f | grep "Connection registered"
```

### Cloudflare Dashboard
- Real-time analytics
- Traffic graphs
- Security events

---

## Backup Configuration

### Backup Tunnel Credentials
```bash
# Backup credentials
cp ~/.cloudflared/*.json ~/backup_cloudflared_$(date +%Y%m%d).json

# Backup config
cp ~/.cloudflared/config.yml ~/backup_config_$(date +%Y%m%d).yml
```

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Cloudflare Tunnel | **FREE** | Unlimited bandwidth |
| Cloudflare DNS | **FREE** | Unlimited queries |
| SSL Certificate | **FREE** | Auto-renew |
| DDoS Protection | **FREE** | Basic protection |
| Domain (Freenom) | **FREE** | 1 year, renewable |
| Domain (Paid) | ~$10/year | Optional |

**Total: $0 - $10/year** (tergantung domain)

---

## URLs Akhir

Setelah setup selesai, aplikasi bisa diakses via:

### Development (Private):
```
http://100.x.x.x:8080
```

### Production (Public):
```
https://wastedetection.tk
https://app.wastedetection.tk
```

### Share ke Dosen/Teman:
Cukup kasih link:
```
https://wastedetection.tk
```

Tidak perlu install apapun, langsung bisa akses!

---

## Kesimpulan

✅ **Setup Hybrid Selesai!**

**Untuk Development:**
- Akses via Tailscale: `http://100.x.x.x:8080`
- Private, cepat, aman

**Untuk Demo/Production:**
- Akses via Cloudflare: `https://wastedetection.tk`
- Public, HTTPS, professional

**Keuntungan:**
- ✅ Fleksibel (2 cara akses)
- ✅ Aman (private untuk dev, public untuk demo)
- ✅ Professional (custom domain)
- ✅ Gratis selamanya
- ✅ 24/7 online

---

**Generated:** 19 Desember 2025  
**Setup:** Cloudflare Tunnel + Tailscale Hybrid  
**Status:** Production Ready 🚀
