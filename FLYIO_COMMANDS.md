# ⚡ Fly.io Commands - Quick Reference

## 🚀 **Deployment Commands**

### **Initial Setup:**
```powershell
# Install Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
fly auth login

# Launch app
fly launch

# Set secrets
fly secrets set CLOUDINARY_CLOUD_NAME=xxx
fly secrets set CLOUDINARY_API_KEY=xxx
fly secrets set CLOUDINARY_API_SECRET=xxx

# Deploy
fly deploy

# Open app
fly open
```

---

## 📊 **Monitoring Commands**

```powershell
# Check status
fly status

# View logs (live)
fly logs

# View logs (last 100 lines)
fly logs -n 100

# View metrics
fly metrics

# Open dashboard
fly dashboard
```

---

## 🔧 **Management Commands**

```powershell
# Restart app
fly apps restart waste-detection-unjani

# Redeploy
fly deploy

# Deploy without cache
fly deploy --no-cache

# Scale memory
fly scale memory 512

# Scale CPU (paid)
fly scale vm shared-cpu-2x
```

---

## 🗄️ **Database Commands**

```powershell
# Create PostgreSQL
fly postgres create --name waste-detection-unjani-db --region sin

# Attach database
fly postgres attach waste-detection-unjani-db

# List databases
fly postgres db list -a waste-detection-unjani-db

# Connect to database
fly postgres connect -a waste-detection-unjani-db

# Restart database
fly postgres restart -a waste-detection-unjani-db

# Backup database
fly postgres backup create -a waste-detection-unjani-db

# List backups
fly postgres backup list -a waste-detection-unjani-db
```

---

## 🔑 **Secrets Commands**

```powershell
# List secrets
fly secrets list

# Set secret
fly secrets set KEY=value

# Set multiple secrets
fly secrets set KEY1=value1 KEY2=value2

# Unset secret
fly secrets unset KEY

# Import from file
fly secrets import < secrets.txt
```

---

## 🐛 **Debugging Commands**

```powershell
# SSH to container
fly ssh console

# Run command in container
fly ssh console -C "ls -la"

# Check app info
fly info

# Check releases
fly releases

# Rollback to previous release
fly releases rollback <version>

# Check health
fly checks list
```

---

## 📦 **App Management**

```powershell
# List apps
fly apps list

# Destroy app (careful!)
fly apps destroy waste-detection-unjani

# Suspend app
fly apps suspend waste-detection-unjani

# Resume app
fly apps resume waste-detection-unjani

# Rename app
fly apps rename waste-detection-unjani new-name
```

---

## 🌍 **Region & Scaling**

```powershell
# List regions
fly platform regions

# List VM sizes
fly platform vm-sizes

# Scale to multiple regions
fly scale count 2 --region sin,hkg

# Scale memory
fly scale memory 512

# Scale CPU
fly scale vm shared-cpu-2x
```

---

## 🔐 **Authentication**

```powershell
# Login
fly auth login

# Logout
fly auth logout

# Check who's logged in
fly auth whoami

# Get auth token
fly auth token
```

---

## 📝 **Configuration**

```powershell
# Validate fly.toml
fly config validate

# Show current config
fly config show

# Save config
fly config save
```

---

## 🧪 **Testing & Development**

```powershell
# Open app in browser
fly open

# Open dashboard
fly dashboard

# Proxy to app
fly proxy 8080:8080

# SSH console
fly ssh console

# Run command
fly ssh console -C "python --version"
```

---

## 📊 **Monitoring & Logs**

```powershell
# Live logs
fly logs

# Last N lines
fly logs -n 100

# Filter by instance
fly logs --instance <instance-id>

# Metrics
fly metrics

# Status
fly status

# Health checks
fly checks list
```

---

## 🔄 **Deployment & Releases**

```powershell
# Deploy
fly deploy

# Deploy without cache
fly deploy --no-cache

# Deploy specific Dockerfile
fly deploy --dockerfile Dockerfile.prod

# List releases
fly releases

# Rollback
fly releases rollback <version>

# Show release info
fly releases show <version>
```

---

## 💾 **Volumes (Optional)**

```powershell
# Create volume
fly volumes create data --size 1

# List volumes
fly volumes list

# Delete volume
fly volumes delete <volume-id>

# Extend volume
fly volumes extend <volume-id> --size 2
```

---

## 🆘 **Emergency Commands**

```powershell
# Restart everything
fly apps restart waste-detection-unjani
fly postgres restart -a waste-detection-unjani-db

# Check everything
fly status
fly logs
fly postgres db list -a waste-detection-unjani-db
fly secrets list

# Rollback if broken
fly releases
fly releases rollback <previous-version>

# SSH to debug
fly ssh console
```

---

## 📚 **Help Commands**

```powershell
# General help
fly help

# Command help
fly deploy --help

# Version
fly version

# Check for updates
fly version update
```

---

## 🎯 **Most Used Commands**

```powershell
# Daily use
fly logs          # Check logs
fly status        # Check status
fly deploy        # Deploy changes
fly open          # Open app

# Weekly use
fly metrics       # Check metrics
fly dashboard     # Open dashboard
fly postgres backup create -a waste-detection-unjani-db  # Backup

# When issues
fly apps restart waste-detection-unjani  # Restart
fly logs -n 200   # Check more logs
fly ssh console   # Debug
```

---

## 💡 **Pro Tips**

### **Alias untuk PowerShell:**
```powershell
# Add to $PROFILE
Set-Alias fl fly
function flog { fly logs }
function fstat { fly status }
function fdep { fly deploy }
function fopen { fly open }
```

### **Watch logs:**
```powershell
# Keep logs open
fly logs
```

### **Quick restart:**
```powershell
fly apps restart waste-detection-unjani && fly logs
```

### **Deploy and watch:**
```powershell
fly deploy && fly logs
```

---

## 🔗 **Useful Links**

- **Docs:** https://fly.io/docs
- **Dashboard:** https://fly.io/dashboard
- **Community:** https://community.fly.io
- **Status:** https://status.fly.io

---

**Bookmark this file for quick reference! 📌**
