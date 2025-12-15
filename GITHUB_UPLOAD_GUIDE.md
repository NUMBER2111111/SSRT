# Upload SSRT to GitHub - Step by Step

## ✅ SAFETY CHECK COMPLETE
- ✅ No secrets in code (only sandbox test values)
- ✅ .gitignore updated to protect secrets
- ✅ SQUARE_PAY_API.json will NOT be uploaded

---

## Method 1: GitHub Web Interface (EASIEST - No Git Install)

### Step 1: Go to Your Repository
1. Open: https://github.com/NUMBER2111111/SSRT
2. You should see the repository page

### Step 2: Upload Files
1. Click **"Add file"** button (top right, near "Code")
2. Click **"Upload files"**
3. Drag your entire `F:\ssrt-deployment` folder OR:
   - Click "choose your files"
   - Select all files from `F:\ssrt-deployment` (except node_modules, .vercel, etc.)

### Step 3: Commit
1. Scroll down to "Commit changes"
2. Commit message: "Initial SSRT deployment site"
3. Click **"Commit changes"**

---

## Method 2: Install Git (For Future Updates)

### Download Git:
1. Go to: https://git-scm.com/download/win
2. Download and install Git for Windows
3. Restart PowerShell

### Then Run:
```powershell
cd F:\ssrt-deployment
git init
git add .
git commit -m "Initial SSRT deployment"
git branch -M main
git remote add origin https://github.com/NUMBER2111111/SSRT.git
git push -u origin main
```

---

## Step 4: Enable GitHub Pages

1. Go to your repo: https://github.com/NUMBER2111111/SSRT
2. Click **"Settings"** (top menu)
3. Scroll to **"Pages"** (left sidebar)
4. Under "Source":
   - Select: **"Deploy from a branch"**
   - Branch: **"main"**
   - Folder: **"/ (root)"**
5. Click **"Save"**
6. Your site will be at: `https://NUMBER2111111.github.io/SSRT/`

---

## Step 5: Connect to Vercel

1. Go to: https://vercel.com/number2111111s-projects
2. Click **"Add New Project"**
3. Click **"Import Git Repository"**
4. Select **"SSRT"** repository
5. Click **"Import"**
6. Vercel will auto-detect `vercel.json`
7. Click **"Deploy"**

---

## Files to Upload

✅ **Upload these:**
- index.html
- engineering.html
- api/server.js
- package.json
- vercel.json
- manifest.json
- sw.js
- .gitignore
- README.md
- All folders (ios/, android/, etc.)

❌ **DO NOT upload:**
- node_modules/ (already in .gitignore)
- .vercel/ (already in .gitignore)
- SQUARE_PAY_API.json (already in .gitignore)
- *.log files

---

## After Upload: Set Environment Variables in Vercel

1. Go to Vercel project settings
2. Add environment variables (from F:\SQUARE_PAY_API.json)
3. Redeploy

---

## Ready to Upload!

Use Method 1 (GitHub web interface) - it's the easiest!

