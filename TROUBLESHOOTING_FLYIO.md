# 🐛 Troubleshooting Fly.io

## 🔍 **Common Issues & Solutions**

---

## 1️⃣ **Installation Issues**

### **Error: "fly: command not found"**

**Penyebab:** Fly CLI belum ter-install atau PATH belum ter-update

**Solusi:**
```powershell
# Restart PowerShell
# Atau install ulang
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Verify
fly version
```

---

## 2️⃣ **Authentication Issues**

### **Error: "not logged in"**

**Solusi:**
```powershell
fly auth login
```

### **Error: "credit card required"**

**Penyebab:** Fly.io memerlukan kartu kredit untuk free tier

**Solusi:**
1. Buka https://fly.io/dashboard
2. Settings → Billing
3. Add credit card
4. Tidak akan dicharge untuk free tier!

---

## 3️⃣ **Launch Issues**

### **Error: "app name already taken"**

**Solusi:**
```powershell
# Gunakan nama lain
fly launch --name waste-detection-unjani-2

# Atau biarkan auto-generate
fly launch
```

### **Error: "region not available"**

**Solusi:**
```powershell
# Pilih region lain
# Recommended untuk Indonesia:
# - sin (Singapore)
# - hkg (Hong Kong)
# - nrt (Tokyo)
```

---

## 4️⃣ **Database Issues**

### **Error: "failed to create postgres cluster"**

**Solusi:**
```powershell
# Create manual
fly postgres create --name waste-detection-unjani-db --region sin

# Attach to app
fly postgres attach waste-detection-unjani-db
```

### **Error: "database connection failed"**

**Check database status:**
```powershell
fly postgres db list -a waste-detection-unjani-db
```

**Restart database:**
```powershell
fly postgres restart -a waste-detection-unjani-db
```

**Check connection string:**
```powershell
fly secrets list
# Look for DATABASE_URL
```

---

## 5️⃣ **Secrets Issues**

### **Error: "secret not found"**

**List secrets:**
```powershell
fly secrets list
```

**Set missing secrets:**
```powershell
fly secrets set CLOUDINARY_CLOUD_NAME=xxx
fly secrets set CLOUDINARY_API_KEY=xxx
fly secrets set CLOUDINARY_API_SECRET=xxx
```

### **Error: "invalid secret value"**

**Penyebab:** Special characters di secret value

**Solusi:**
```powershell
# Use quotes
fly secrets set CLOUDINARY_API_SECRET="your-secret-with-special-chars"
```

---

## 6️⃣ **Build Issues**

### **Error: "failed to fetch an image"**

**Solusi:**
```powershell
# Clear cache
fly deploy --no-cache
```

### **Error: "dockerfile not found"**

**Check Dockerfile exists:**
```powershell
dir Dockerfile
```

**Solusi:**
```powershell
# Make sure you're in project root
cd path\to\waste-detection
fly deploy
```

### **Error: "build timeout"**

**Solusi:**
```powershell
# Increase timeout di fly.toml
# Edit: grace_period = "60s"
fly deploy
```

---

## 7️⃣ **Deployment Issues**

### **Error: "health checks failing"**

**Check logs:**
```powershell
fly logs
```

**Common causes:**
1. Model file tidak ada
2. Database connection error
3. Port mismatch

**Solusi:**
```powershell
# Check model exists
fly ssh console
ls -la models/

# Check port di fly.toml
# internal_port = 8080

# Check app.py
# port = int(os.environ.get('PORT', 8080))
```

### **Error: "deployment failed"**

**Check status:**
```powershell
fly status
```

**Check logs:**
```powershell
fly logs
```

**Redeploy:**
```powershell
fly deploy
```

---

## 8️⃣ **Runtime Issues**

### **Error: "Application failed to respond"**

**Check logs:**
```powershell
fly logs
```

**Common causes:**
1. Model loading error
2. Database connection error
3. Out of memory

**Solusi:**
```powershell
# Restart app
fly apps restart waste-detection-unjani

# Scale memory
fly scale memory 512

# Check logs
fly logs
```

### **Error: "Out of memory"**

**Solusi:**
```powershell
# Scale to 512MB (masih gratis)
fly scale memory 512

# Redeploy
fly deploy
```

### **Error: "Database connection timeout"**

**Check database:**
```powershell
fly postgres db list -a waste-detection-unjani-db
```

**Restart database:**
```powershell
fly postgres restart -a waste-detection-unjani-db
```

---

## 9️⃣ **Cloudinary Issues**

### **Error: "Cloudinary upload failed"**

**Check secrets:**
```powershell
fly secrets list
```

**Verify credentials:**
1. Login ke Cloudinary dashboard
2. Check credentials masih valid
3. Update secrets jika perlu

**Test Cloudinary:**
```powershell
fly ssh console
python -c "from cloudinary_helper import CloudinaryManager; cm = CloudinaryManager(); print('OK')"
```

---

## 🔟 **Performance Issues**

### **App lambat/slow**

**Check metrics:**
```powershell
fly metrics
```

**Scale resources:**
```powershell
# Scale memory
fly scale memory 512

# Scale CPU (paid)
fly scale vm shared-cpu-2x
```

### **Cold start lambat**

**Solusi:**
```powershell
# Keep app warm
# Edit fly.toml:
# auto_stop_machines = false
# min_machines_running = 1

fly deploy
```

---

## 🆘 **Emergency Commands**

### **Restart everything:**
```powershell
# Restart app
fly apps restart waste-detection-unjani

# Restart database
fly postgres restart -a waste-detection-unjani-db
```

### **Rollback deployment:**
```powershell
# List releases
fly releases

# Rollback to previous
fly releases rollback <version>
```

### **SSH to container:**
```powershell
fly ssh console
```

### **Check everything:**
```powershell
# Status
fly status

# Logs
fly logs

# Secrets
fly secrets list

# Database
fly postgres db list -a waste-detection-unjani-db

# Metrics
fly metrics
```

---

## 📊 **Debugging Workflow**

### **Step 1: Check Status**
```powershell
fly status
```

### **Step 2: Check Logs**
```powershell
fly logs
```

### **Step 3: Check Database**
```powershell
fly postgres db list -a waste-detection-unjani-db
```

### **Step 4: Check Secrets**
```powershell
fly secrets list
```

### **Step 5: SSH to Container**
```powershell
fly ssh console

# Inside container:
ls -la
python -c "import tensorflow; print(tensorflow.__version__)"
python -c "from database import DatabaseManager; print('DB OK')"
python -c "from cloudinary_helper import CloudinaryManager; print('Cloudinary OK')"
```

---

## 🔍 **Log Analysis**

### **Look for these in logs:**

**✅ Good signs:**
```
✓ Database and Cloudinary modules loaded
✓ Database connected and tables created
✓ Cloudinary configured: your_cloud_name
✓ Model loaded successfully
```

**❌ Bad signs:**
```
❌ Error loading model
❌ Database connection failed
❌ Cloudinary upload failed
free(): invalid pointer
MemoryError
```

---

## 📞 **Get Help**

### **Fly.io Community:**
- Forum: https://community.fly.io
- Discord: https://fly.io/discord

### **Documentation:**
- Docs: https://fly.io/docs
- Postgres: https://fly.io/docs/postgres

### **Contact Me:**
Kirim:
1. Screenshot error
2. Output dari `fly logs`
3. Output dari `fly status`
4. Apa yang sudah dicoba

---

## ✅ **Prevention Tips**

1. **Always check logs after deploy:**
   ```powershell
   fly deploy && fly logs
   ```

2. **Monitor regularly:**
   ```powershell
   fly status
   fly metrics
   ```

3. **Backup database:**
   ```powershell
   fly postgres backup create -a waste-detection-unjani-db
   ```

4. **Test before deploy:**
   - Test locally first
   - Check Dockerfile builds
   - Verify all files exist

5. **Keep secrets safe:**
   - Don't commit secrets
   - Use `.env` for local
   - Use `fly secrets` for production

---

**Still stuck? Tanya saya dengan detail error! 🆘**
