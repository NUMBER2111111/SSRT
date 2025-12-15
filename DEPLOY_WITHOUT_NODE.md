# Deploy SSRT Site WITHOUT Node.js

## ✅ You DON'T Need Node.js Installed!

You can deploy to Vercel **without installing Node.js** using these methods:

---

## 🚀 Method 1: Vercel Web Interface (EASIEST - No Node.js Needed)

### Step 1: Create Vercel Account
1. Go to: https://vercel.com
2. Sign up (free) with GitHub, GitLab, or email

### Step 2: Deploy via Web
1. Click **"Add New Project"**
2. If you have GitHub/GitLab connected:
   - Import your repository
   - Vercel auto-detects settings
   - Click **"Deploy"**
3. If you DON'T have Git:
   - Use **Vercel CLI** (see Method 2 below)
   - OR use **Vercel Drag & Drop** (see Method 3)

---

## 🚀 Method 2: Vercel CLI (One-Time Install)

### Option A: Install Node.js Just for Vercel CLI
1. Download Node.js: https://nodejs.org (LTS version)
2. Install it
3. Run:
   ```bash
   npm install -g vercel
   vercel login
   cd F:\ssrt-deployment
   vercel --prod
   ```
4. **Then you can uninstall Node.js if you want**

### Option B: Use npx (No Install)
If you have any way to run `npx`:
```bash
npx vercel --prod
```

---

## 🚀 Method 3: Vercel Drag & Drop (No Node.js, No Git)

1. Go to: https://vercel.com/dashboard
2. Click **"Add New Project"**
3. Look for **"Deploy without Git"** or **"Import Project"**
4. Drag your `F:\ssrt-deployment` folder
5. Vercel will:
   - Auto-detect `vercel.json`
   - Deploy your site
   - Give you a URL

---

## 🚀 Method 4: GitHub Integration (Recommended)

### If You Have GitHub:
1. Create a GitHub repository
2. Push your `F:\ssrt-deployment` folder to GitHub
3. Connect GitHub to Vercel
4. Vercel auto-deploys on every push
5. **No Node.js needed locally!**

---

## ⚙️ Environment Variables Setup

After deployment, set these in Vercel Dashboard:

1. Go to: **Project Settings → Environment Variables**
2. Add:
   - `SQUARE_APPLICATION_ID` = (from your Square API)
   - `SQUARE_ACCESS_TOKEN` = (from your Square API)
   - `SQUARE_LOCATION_ID` = (from your Square API)
   - `SQUARE_ENVIRONMENT` = `production` (or `sandbox` for testing)

**Note:** Your `F:\SQUARE_PAY_API.json` file should NOT be uploaded. Use environment variables instead.

---

## 📋 What Vercel Needs

Your site is **already configured** with:
- ✅ `vercel.json` - Deployment config
- ✅ `api/server.js` - Backend API
- ✅ `package.json` - Dependencies
- ✅ Static files (HTML, CSS, JS)

Vercel will:
- ✅ Install Node.js on their servers (you don't need it)
- ✅ Run your API automatically
- ✅ Serve your static files
- ✅ Handle HTTPS automatically

---

## 🎯 RECOMMENDED: Method 1 or 4

**Best Option:** Use Vercel Web Interface or GitHub integration
- No Node.js needed
- No command line needed
- Just point and click
- Auto-deploys on updates

---

## 🚨 Important: Square Pay API

Your `api/server.js` reads from `F:\SQUARE_PAY_API.json`

**For Production:**
- Don't upload that file to Vercel
- Use Vercel Environment Variables instead
- Update `api/server.js` to read from environment variables

**Quick Fix for Production:**
```javascript
// In api/server.js, replace:
const configPath = path.join('F:', 'SQUARE_PAY_API.json');

// With:
const config = {
  square_api: {
    application_id: process.env.SQUARE_APPLICATION_ID,
    access_token: process.env.SQUARE_ACCESS_TOKEN,
    location_id: process.env.SQUARE_LOCATION_ID,
    environment: process.env.SQUARE_ENVIRONMENT || 'sandbox'
  }
};
```

---

## ✅ Summary

**You DON'T need Node.js installed!**

**Easiest Way:**
1. Go to vercel.com
2. Sign up
3. Drag & drop your folder OR connect GitHub
4. Deploy!

**That's it!** 🚀

