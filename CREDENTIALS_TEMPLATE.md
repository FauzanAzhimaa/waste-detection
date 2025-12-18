# 🔑 Credentials Template

## 📋 **Cloudinary Credentials**

Copy dari Railway Variables:

```
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

---

## 🚀 **Cara Set di Fly.io:**

```powershell
fly secrets set CLOUDINARY_CLOUD_NAME=your_cloud_name
fly secrets set CLOUDINARY_API_KEY=your_api_key
fly secrets set CLOUDINARY_API_SECRET=your_api_secret
```

---

## 📍 **Cara Dapat Credentials dari Railway:**

1. Buka https://railway.app
2. Login
3. Pilih project: `waste-detection`
4. Tab: `Variables`
5. Copy 3 credentials di atas

---

## ✅ **Verifikasi:**

Setelah set secrets, check:

```powershell
fly secrets list
```

Expected output:
```
NAME                      DIGEST          CREATED AT
CLOUDINARY_API_KEY        xxxxx           1m ago
CLOUDINARY_API_SECRET     xxxxx           1m ago
CLOUDINARY_CLOUD_NAME     xxxxx           1m ago
DATABASE_URL              xxxxx           5m ago
```

---

**Note:** DATABASE_URL akan auto-created saat `fly launch`
