# 🚀 Deploy to Render

## ⚠️ Fix for Build Errors

If you encounter **pydantic-core build errors** during deployment:

### ✅ **Already Fixed in This Project:**
- Updated to **pydantic 2.10.0** with pre-built wheels
- Updated to **pydantic-core 2.27.1** (specific version with wheels)
- Added **runtime.txt** with Python 3.11.9
- Added **PIP_NO_CACHE_DIR=1** to avoid cache issues

### 🔧 **Manual Fix (if still needed):**
If you still get build errors, try these alternatives:

1. **Use different pydantic versions:**
   ```
   pydantic==2.9.0
   pydantic-core==2.23.2
   ```

2. **Or use pydantic v1 (less recommended):**
   ```
   pydantic==1.10.15
   ```

3. **Add Rust compiler (advanced):**
   In Render dashboard → Environment → Build Command:
   ```
   apt-get update && apt-get install -y rustc cargo && pip install -r requirements.txt
   ```

## Quick Deploy Steps

### 1. Commit Changes
```bash
git add .
git commit -m "Fix Render deployment: update pydantic versions and add runtime.txt"
git push origin main
```

### 2. Connect to Render
1. Go to [render.com](https://render.com)
2. Sign up/Login with your account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### 3. Configure Service
- **Name**: `solar-system-api` (or your choice)
- **Runtime**: `Python 3`
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT`

### 4. Environment Variables
- `PYTHON_VERSION`: `3.11.9`
- `PIP_NO_CACHE_DIR`: `1` (optional, helps with cache issues)

### 5. Deploy
Click "Create Web Service" and wait for deployment to complete.

## Alternative: Manual Deploy

If you prefer manual setup:

1. **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
2. **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Testing Your Deployment

After deployment, your API will be available at:
- **API Base**: `https://your-service-name.onrender.com`
- **API Docs**: `https://your-service-name.onrender.com/docs`
- **Health Check**: `https://your-service-name.onrender.com/health`

## Troubleshooting

- **Port Issues**: Render automatically provides `$PORT` environment variable
- **Timeout**: Free tier has 15-minute timeout for requests
- **Memory**: Free tier has 512MB RAM limit
- **Build Errors**: Check the fixes above for pydantic-core issues

## Cost
- **Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: Available if you need more resources