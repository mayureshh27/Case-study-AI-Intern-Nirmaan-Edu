# Quick Setup & Verification Guide

## Prerequisites Check

- ✅ Node.js 18+ and pnpm installed
- ✅ Python 3.11+ installed
- ✅ uv installed

## Setup Steps

### 1. Backend Setup

```bash
cd backend

# Create .env file (optional)
cp .env.example .env

# Install dependencies (already done with uv)
uv sync

# Start backend
uv run uvicorn main:app --reload --port 8000
```

Backend should be running at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Create .env file for local development
cp .env.example .env

# The .env file should contain:
# VITE_API_URL=http://localhost:8000

# Install dependencies
pnpm install

# Start frontend
pnpm dev
```

Frontend should be running at: `http://localhost:5173`

## Verification

### Test Backend

Open browser and visit:
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Analytics: `http://localhost:8000/analytics/download`

### Test Frontend-Backend Communication

1. Visit `http://localhost:5173`
2. Paste this sample transcript:
   ```
   Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. I am 13 years old. I live with my family.
   ```
3. Click "Analyze Transcript"
4. You should see scores appear

### Check CORS

If you see CORS errors in browser console:
1. Verify backend is running on port 8000
2. Check frontend .env has correct `VITE_API_URL`
3. Restart both servers

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
No environment variables required for basic operation.

## Common Issues

### Issue: "Failed to fetch" error
**Solution**: 
- Ensure backend is running
- Check `VITE_API_URL` in frontend/.env
- Verify no firewall blocking port 8000

### Issue: CORS error
**Solution**:
- Backend CORS is configured to allow all origins
- Restart backend server
- Clear browser cache

### Issue: Analytics not working
**Solution**:
- Check `backend/logs/access.log` exists
- Folder is created automatically on first request

## Production Deployment

### Frontend (Vercel)
Set environment variable:
```
VITE_API_URL=https://your-backend.onrender.com
```

### Backend (Render)
No environment variables needed.
CORS will automatically allow your Vercel domain.

## Quick Test Commands

```bash
# Test backend health
curl http://localhost:8000/health

# Test scoring
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Hello everyone, my name is John."}'

# Check analytics
curl http://localhost:8000/analytics/download
```

## Success Criteria

✅ Backend returns 200 on /health
✅ Frontend loads without errors
✅ Can submit transcript and get scores
✅ Analytics endpoint returns data
✅ No CORS errors in browser console

---

**Everything working?** You're ready to deploy! 🚀
