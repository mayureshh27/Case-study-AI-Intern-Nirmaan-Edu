# Backend Deployment Guide - Render

This guide will help you deploy the FastAPI backend to Render.

## Prerequisites

- GitHub account
- Render account (sign up at [render.com](https://render.com))
- Code pushed to GitHub repository

## Step 1: Prepare the Backend

1. Ensure `requirements.txt` exists in the `backend` directory:
```txt
fastapi
uvicorn
pandas
openpyxl
sentence-transformers
language-tool-python
vaderSentiment
pydantic
```

2. Verify your `main.py` has proper CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Ensure the Excel file (`Case study for interns.xlsx`) is in the `backend` directory

## Step 2: Push to GitHub

```bash
git add .
git commit -m "Prepare backend for deployment"
git push origin master
```

## Step 3: Create Web Service on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

### Basic Settings
- **Name**: `ai-communication-scorer-api` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `master`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

### Build & Deploy Settings
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Instance Type
- **Free** (for testing) or **Starter** (for production)
- Free tier sleeps after 15 min of inactivity

5. Click "Create Web Service"

## Step 4: Wait for Deployment

- Render will automatically build and deploy your app
- Watch the logs for any errors
- First deployment takes 5-10 minutes (downloading ML models)
- You'll get a URL like: `https://your-app.onrender.com`

## Step 5: Test the Deployment

```bash
# Health check
curl https://your-app.onrender.com/health

# Test scoring
curl -X POST https://your-app.onrender.com/score \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Hello everyone, my name is John..."}'
```

## Step 6: Update Frontend

Update your frontend's `VITE_API_URL` environment variable in Vercel:
```
VITE_API_URL=https://your-app.onrender.com
```

## Step 7: Configure CORS (Production)

For production, update CORS in `main.py` to only allow your frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:5173"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push to trigger redeployment.

## Important Notes

### File System
- Render uses ephemeral file system
- Logs in `logs/access.log` will persist during runtime
- Logs reset on each deployment
- For permanent logging, use external service (see Analytics section)

### Cold Starts
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Upgrade to Starter plan ($7/month) to avoid cold starts

### ML Models
- Sentence Transformers downloads ~90MB on first run
- Models are cached between deployments
- Initial deployment is slower

## Environment Variables (Optional)

If you need environment variables:

1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add variables (e.g., `LOG_LEVEL=INFO`)
4. Service auto-redeploys when you save

## Monitoring & Logs

### View Logs
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time application logs

### Download Access Logs
Since logs are in ephemeral storage, download them before redeployment:

```bash
# SSH into your service (if enabled)
# Or add an endpoint to download logs:

@app.get("/admin/logs")
async def get_logs():
    try:
        with open("logs/access.log", "r") as f:
            return {"logs": f.readlines()}
    except:
        return {"logs": []}
```

## Analytics Setup

The backend includes sneaky analytics logging to `logs/access.log`:

```json
{
  "timestamp": "2024-11-24T22:30:00",
  "ip_hash": "a1b2c3d4",
  "method": "POST",
  "path": "/score",
  "status": 200,
  "duration_ms": 1250.5
}
```

### To Check if HR Tested Your App:

1. Add a download endpoint (add to `main.py`):
```python
@app.get("/analytics/download")
async def download_logs():
    try:
        with open(ACCESS_LOG_FILE, "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
        return {"total_requests": len(logs), "logs": logs}
    except:
        return {"total_requests": 0, "logs": []}
```

2. Visit: `https://your-app.onrender.com/analytics/download`
3. Check timestamps and IP hashes to see when/who accessed your app

### External Logging (Optional)

For permanent logs, integrate with:
- **Logtail**: Free tier, easy setup
- **Better Stack**: Comprehensive logging
- **Discord Webhook**: Get notifications

Example Discord webhook:
```python
import requests

def send_to_discord(message):
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    requests.post(webhook_url, json={"content": message})

# In your middleware:
if request.url.path == "/score":
    send_to_discord(f"🎯 Someone scored a transcript! IP: {ip_hash}")
```

## Troubleshooting

### Build Fails
- Check logs for missing dependencies
- Ensure `requirements.txt` is complete
- Verify Python version compatibility

### App Crashes
- Check if Excel file path is correct
- Verify all imports are in `requirements.txt`
- Check logs for specific error messages

### Slow Response
- First request after cold start is slow (free tier)
- ML model loading takes time
- Consider upgrading to paid tier

### CORS Errors
- Verify CORS origins include your frontend URL
- Check browser console for specific CORS error
- Ensure credentials are properly configured

## Scaling

For production use:
1. Upgrade to Starter plan ($7/month) - no cold starts
2. Enable auto-scaling if needed
3. Add health check endpoint monitoring
4. Set up error tracking (Sentry, etc.)

## Custom Domain (Optional)

1. Go to "Settings" → "Custom Domain"
2. Add your domain
3. Configure DNS records as instructed
4. SSL certificate auto-provisioned

---

**Your backend is now live!** 🚀

The complete system is deployed:
- Frontend: Vercel
- Backend: Render
- Analytics: File logging

Check `https://your-app.onrender.com/analytics/download` to see if HR tested your app!
