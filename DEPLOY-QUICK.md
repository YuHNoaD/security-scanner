# 🚀 Quick Deploy to Railway

## One-Click Deploy

### Option 1: PowerShell Script (Windows)

```powershell
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner
.\deploy-railway.ps1
```

### Option 2: Manual Steps

```bash
# 1. Login to Railway
railway login

# 2. Navigate to project
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner

# 3. Initialize Railway
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Deploy
railway up

# 6. Get URL
railway domain
```

## 🧪 Test Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# API Documentation
# Open: https://your-app.railway.app/docs
```

## 📊 What Gets Deployed

- ✅ FastAPI backend
- ✅ PostgreSQL database
- ✅ All vulnerability analyzers
- ✅ REST API with 8 endpoints
- ✅ Automatic HTTPS

## 🌐 Your App URL

After deployment, Railway will provide:
- App URL: `https://your-app.railway.app`
- API Docs: `https://your-app.railway.app/docs`
- Health: `https://your-app.railway.app/health`

## 💡 Notes

- Railway provides free PostgreSQL database
- Automatic HTTPS is included
- Builds are automatic with Nixpacks
- Logs available in Railway dashboard

---

**Made with 🤖 by Eye**