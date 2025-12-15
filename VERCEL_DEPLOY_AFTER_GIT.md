# Vercel Deployment - After GitHub Upload

## Once Files Are on GitHub

### Step 1: Go to Vercel
1. Open: https://vercel.com/number2111111s-projects
2. Make sure you're logged in

### Step 2: Import from GitHub
1. Click **"Add New Project"**
2. Click **"Import Git Repository"**
3. Find and select **"SSRT"** repository
4. Click **"Import"**

### Step 3: Configure (Vercel Auto-Detects)
- **Framework Preset:** Other (or Static)
- **Root Directory:** `.` (leave as is)
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- Click **"Deploy"**

### Step 4: Wait for Deployment
- Takes 1-2 minutes
- You'll get a URL like: `ssrt-deployment-xxxxx.vercel.app`

### Step 5: Set Environment Variables (CRITICAL!)
1. Go to project → **Settings** → **Environment Variables**
2. Add these (from your `F:\SQUARE_PAY_API.json`):

```
SQUARE_APPLICATION_ID = (your application_id)
SQUARE_ACCESS_TOKEN = (your access_token)
SQUARE_LOCATION_ID = (your location_id)
SQUARE_ENVIRONMENT = sandbox (or production)
SALE_PRICE = 29.99
REGULAR_PRICE = 49.00
SALE_LIMIT = 500
CURRENT_SUBSCRIBERS = 0
SALE_ACTIVE = true
```

3. For each variable, check all environments (Production, Preview, Development)
4. Click **"Save"**

### Step 6: Redeploy
1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**

### Step 7: Test
- Visit your site URL
- Test payment system
- Test "Try for Free" button

---

## Your Site Will Be Live!

URL will be: `ssrt-deployment-xxxxx.vercel.app`

You can also add a custom domain later in Settings.

