# 🚀 Deployment Guide

## 🎯 Deployment Options

### Option 1: Railway (RECOMMENDED for FastAPI) ✅
- **Best for:** FastAPI backends
- **Database:** PostgreSQL included
- **Build:** Automatic with Nixpacks
- **Cost:** Free tier available
- **Ease:** Very easy

### Option 2: Render
- **Best for:** Python apps
- **Database:** PostgreSQL included
- **Build:** Automatic
- **Cost:** Free tier available
- **Ease:** Easy

### Option 3: Vercel (NOT RECOMMENDED for FastAPI) ⚠️
- **Best for:** Next.js, Node.js
- **Database:** Need external PostgreSQL
- **Build:** Limited Python support
- **Cost:** Free tier available
- **Ease:** Difficult for FastAPI

---

## 🚂 Deploy to Railway (RECOMMENDED)

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize Railway Project

```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner
railway init
```

### Step 4: Add PostgreSQL Database

```bash
railway add postgresql
```

### Step 5: Deploy

```bash
railway up
```

### Step 6: Get Your URL

```bash
railway domain
```

Your app will be available at: `https://your-app.railway.app`

### Step 7: Configure Environment Variables

Railway automatically sets:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Port number (usually 8000)

---

## 🎨 Deploy to Render

### Step 1: Create Render Account

Go to https://render.com and sign up

### Step 2: Create PostgreSQL Database

1. Go to Dashboard
2. Click "New" → "PostgreSQL"
3. Create database
4. Copy connection string

### Step 3: Create Web Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `PORT`: `8000`

### Step 4: Deploy

Click "Deploy" and wait for build to complete

### Step 5: Get Your URL

Your app will be available at: `https://your-app.onrender.com`

---

## 🌐 Deploy to Vercel (NOT RECOMMENDED)

Vercel has limited support for FastAPI. Only use if necessary.

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login

```bash
vercel login
```

### Step 3: Deploy

```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner
vercel
```

### Step 4: Configure Environment Variables

Go to Vercel Dashboard → Project → Settings → Environment Variables

Add:
- `DATABASE_URL`: Your PostgreSQL connection string (use external service like Neon, Supabase)
- `API_HOST`: `0.0.0.0`
- `API_PORT`: `8000`

### Step 5: Redeploy

```bash
vercel --prod
```

---

## 🐳 Deploy with Docker

### Step 1: Build Docker Image

```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner
docker build -t security-scanner -f backend/Dockerfile .
```

### Step 2: Run Container

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:port/dbname" \
  security-scanner
```

### Step 3: Push to Docker Hub

```bash
docker tag security-scanner yourusername/security-scanner
docker push yourusername/security-scanner
```

---

## 📊 Deployment Comparison

| Platform | FastAPI Support | Database | Build | Free Tier | Ease |
|----------|----------------|----------|-------|-----------|------|
| **Railway** | ✅ Excellent | ✅ PostgreSQL | ✅ Auto | ✅ Yes | ⭐⭐⭐⭐⭐ |
| **Render** | ✅ Good | ✅ PostgreSQL | ✅ Auto | ✅ Yes | ⭐⭐⭐⭐ |
| **Vercel** | ⚠️ Limited | ❌ External | ⚠️ Limited | ✅ Yes | ⭐⭐ |

---

## 🎯 Recommended Deployment

### For FastAPI Backend: **Railway** ✅

**Why Railway?**
- ✅ Best FastAPI support
- ✅ PostgreSQL included
- ✅ Automatic builds
- ✅ Easy deployment
- ✅ Free tier
- ✅ Good for production

---

## 🔧 After Deployment

### 1. Test Your Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Start a scan
curl -X POST "https://your-app.railway.app/api/scan/start?project_name=Test"

# Upload file
curl -X POST "https://your-app.railway.app/api/scan/1/upload" \
  -F "files=@test_samples/vulnerable_app.py"

# Get results
curl https://your-app.railway.app/api/scan/1/vulnerabilities
```

### 2. View API Documentation

Open browser to:
- Swagger UI: `https://your-app.railway.app/docs`
- ReDoc: `https://your-app.railway.app/redoc`

### 3. Monitor Logs

**Railway:**
```bash
railway logs
```

**Render:**
- Go to Dashboard → Your Service → Logs

**Vercel:**
```bash
vercel logs
```

---

## 📝 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `PORT` | Port number | `8000` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | Host to bind | `0.0.0.0` |
| `API_PORT` | Port to use | `8000` |
| `ENVIRONMENT` | Environment | `production` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |

---

## 🔒 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use strong passwords** - For database
3. **Enable HTTPS** - All platforms provide HTTPS
4. **Rate limiting** - Implement API rate limiting
5. **Authentication** - Add JWT authentication
6. **Regular updates** - Keep dependencies updated

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Docker Docs:** https://docs.docker.com

---

## 🎉 Quick Start (Railway)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\security-scanner
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Deploy
railway up

# 6. Get URL
railway domain

# 7. Test
curl https://your-app.railway.app/health
```

---

**Made with 🤖 by Eye - Deployment Guide**