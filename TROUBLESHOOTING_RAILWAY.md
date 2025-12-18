# 🔧 Troubleshooting Railway Deployment

## ❌ Error: "free(): invalid pointer"

### **Penyebab:**
TensorFlow memory management issue saat load model di Railway environment.

### **Solusi yang Sudah Diterapkan:**

#### 1. **Load Model dengan compile=False**
```python
self.model = tf.keras.models.load_model(str(self.model_path), compile=False)
```
Ini mencegah TensorFlow compile metrics yang bisa cause memory issue.

#### 2. **Manual Compile**
```python
self.model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```
Compile manual setelah load untuk kontrol lebih baik.

#### 3. **Garbage Collection**
```python
import gc
gc.collect()
```
Clear memory sebelum load model.

#### 4. **Environment Variables**
```python
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
```
Suppress warnings dan disable oneDNN yang bisa cause issues.

---

## ⏳ **Tunggu Build Selesai**

Setelah deploy:
1. Tunggu 2-3 menit
2. Refresh browser
3. Check Railway logs: `railway logs`

**Look for:**
```
✓ Model loaded from /app/models/waste_mobilenet.h5
✓ Database connected and tables created
✓ Cloudinary configured
* Running on http://0.0.0.0:8080
```

---

## 🧪 **Test Deployment:**

### **1. Check Website**
```
https://waste-detection-production-4613.up.railway.app
```

**Expected:**
- ✅ Website loads (no error page)
- ✅ Upload form visible
- ✅ Can select/capture image

### **2. Upload Test**
1. Upload small image (<1MB)
2. Wait for result
3. Check if:
   - ✅ Prediction shows
   - ✅ Image displays
   - ✅ Heatmap displays (or error message)

### **3. Check Logs**
```bash
railway logs
```

**Look for errors:**
- ❌ `free(): invalid pointer` → Still has memory issue
- ❌ `Database/Cloudinary not available` → Credentials issue
- ❌ `ModuleNotFoundError` → Dependencies issue

---

## 🔄 **If Still Failing:**

### **Option 1: Restart Railway Service**
1. Go to Railway dashboard
2. Click service → Settings
3. Click "Restart"
4. Wait 2-3 minutes

### **Option 2: Check Memory Usage**
Railway free tier: 512MB limit

If app uses >512MB:
- Model loading: ~300MB
- TensorFlow: ~150MB
- App: ~50MB
- **Total: ~500MB** (close to limit!)

**Solution:**
- Disable heatmap temporarily
- Use smaller model
- Upgrade Railway plan

### **Option 3: Fallback to JSON Storage**

If database/cloudinary causing issues, app will automatically fallback:

```python
USE_DATABASE = False  # Automatic fallback
```

This means:
- ✅ App still works
- ❌ Data will be lost on restart
- ❌ Images will be lost on restart

---

## 📊 **Check Railway Dashboard:**

### **Metrics to Monitor:**
1. **Memory Usage**: Should be <500MB
2. **CPU Usage**: Should be <80%
3. **Build Time**: Should be <5 minutes
4. **Deploy Status**: Should be "Active"

### **Variables to Check:**
```
DATABASE_URL = postgresql://...
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
PORT = 8080 (optional, auto-detected)
```

---

## 🆘 **Still Not Working?**

### **Collect Debug Info:**

1. **Railway Logs:**
```bash
railway logs > railway_logs.txt
```

2. **Browser Console:**
- Open browser (F12)
- Go to Console tab
- Screenshot any errors

3. **Network Tab:**
- F12 → Network tab
- Try upload
- Check failed requests
- Screenshot

4. **Railway Dashboard:**
- Screenshot Metrics
- Screenshot Variables (blur sensitive data)
- Screenshot Deploy logs

### **Send to Support:**
- Railway logs
- Browser console errors
- Screenshots
- Description of what you tried

---

## ✅ **Success Indicators:**

When everything works:

```bash
# Railway logs should show:
✓ Database and Cloudinary modules loaded
✓ Database connected and tables created
✓ Cloudinary configured: your_cloud_name
✓ Model loaded from /app/models/waste_mobilenet.h5
📁 Temp folder: /app/temp
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
INFO:werkzeug: * Running on http://10.x.x.x:8080
```

```bash
# Website should:
✅ Load without errors
✅ Show upload form
✅ Accept image uploads
✅ Show predictions
✅ Show images (from Cloudinary)
✅ Show history (from PostgreSQL)
```

```bash
# After restart:
✅ History still has data
✅ Images still accessible
✅ No data loss
```

---

## 🎯 **Expected Timeline:**

- **Deploy**: 2-3 minutes
- **First load**: 10-15 seconds (model loading)
- **Subsequent loads**: 1-2 seconds
- **Upload + Predict**: 5-10 seconds
- **With heatmap**: 10-20 seconds

---

## 💡 **Tips:**

1. **Be Patient**: First deploy takes time
2. **Check Logs**: Always check logs for errors
3. **Test Small**: Start with small images
4. **Monitor Memory**: Watch Railway metrics
5. **Backup Data**: Export CSV regularly

---

**Good luck! 🚀**
