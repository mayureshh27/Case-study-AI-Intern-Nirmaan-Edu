# Frontend Deployment Guide - Vercel

This guide will help you deploy the frontend React application to Vercel.

## Prerequisites

- GitHub account
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Code pushed to GitHub repository

## Step 1: Prepare the Frontend

1. Ensure your `package.json` has the correct build script:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  }
}
```

2. Update `vite.config.ts` if needed (current config should work):
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  }
})
```

## Step 2: Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin master
```

## Step 3: Deploy to Vercel

### Option A: Vercel Dashboard (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm build`
   - **Output Directory**: `dist`
   - **Install Command**: `pnpm install`

5. Add Environment Variable:
   - **Name**: `VITE_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.onrender.com`)

6. Click "Deploy"

### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? ai-communication-scorer
# - Directory? ./
# - Override settings? Yes
#   - Build Command: pnpm build
#   - Output Directory: dist
#   - Development Command: pnpm dev
```

## Step 4: Configure Environment Variables

After deployment, add the backend URL:

1. Go to your project dashboard on Vercel
2. Navigate to "Settings" → "Environment Variables"
3. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com`
   - **Environment**: Production, Preview, Development

4. Redeploy to apply changes

## Step 5: Update Frontend Code

Ensure your frontend uses the environment variable:

```typescript
// src/lib/api.ts or wherever you make API calls
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function scoreTranscript(transcript: string) {
  const response = await fetch(`${API_URL}/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transcript })
  });
  return response.json();
}
```

## Step 6: Verify Deployment

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Test the scoring functionality
3. Check browser console for any errors
4. Verify API calls are going to the correct backend URL

## Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (can take up to 48 hours)

## Troubleshooting

### Build Fails

- Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Verify TypeScript has no errors: `pnpm tsc --noEmit`

### API Calls Fail

- Check `VITE_API_URL` environment variable
- Verify backend CORS allows your Vercel domain
- Check browser console for CORS errors

### Environment Variables Not Working

- Ensure variable names start with `VITE_`
- Redeploy after adding environment variables
- Clear cache and hard reload browser

## Continuous Deployment

Vercel automatically deploys on every push to your main branch:
- Push to `master` → Production deployment
- Push to other branches → Preview deployment

## Monitoring

- View deployment logs in Vercel dashboard
- Check Analytics tab for visitor stats
- Monitor performance in Speed Insights

---

**Your frontend is now live!** 🎉

Next: Deploy the backend following [DEPLOYMENT_BACKEND.md](./DEPLOYMENT_BACKEND.md)
