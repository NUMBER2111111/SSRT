# 🚀 VERCEL DEPLOYMENT - STEP BY STEP GUIDE

## What You Need to Do on Vercel Website

---

## STEP 1: Go to Vercel
1. Open your browser
2. Go to: **https://vercel.com**
3. Click **"Sign Up"** (top right)

---

## STEP 2: Create Account
Choose one:
- **Option A:** Sign up with GitHub (if you have GitHub)
- **Option B:** Sign up with Email
- **Option C:** Sign up with Google

**Just pick the easiest one for you!**

---

## STEP 3: Add New Project
1. After logging in, you'll see the Vercel Dashboard
2. Click the big **"Add New Project"** button (or **"New Project"**)

---

## STEP 4: Import Your Project

### Option A: If You Have GitHub/GitLab
1. Click **"Import Git Repository"**
2. Connect your GitHub/GitLab account (if not connected)
3. Select your repository
4. Click **"Import"**
5. **SKIP TO STEP 6**

### Option B: If You DON'T Have Git (EASIEST)
1. Look for **"Deploy without Git"** or **"Import Project"**
2. OR use **Vercel CLI** (see below)

### Option C: Use Vercel CLI (Command Line)
1. Open PowerShell in `F:\ssrt-deployment`
2. Run: `npx vercel` (this will install Vercel CLI temporarily)
3. Follow the prompts:
   - Login to Vercel (it will open browser)
   - Link to existing project? **No**
   - Project name? **ssrt-deployment** (or just press Enter)
   - Directory? **.** (just press Enter)
   - Override settings? **No** (just press Enter)
4. Wait for deployment
5. **DONE!** You'll get a URL like: `ssrt-deployment-xxxxx.vercel.app`

---

## STEP 5: Configure Project (If Using Git)
1. Vercel will auto-detect your `vercel.json`
2. **Framework Preset:** Should be "Other" or "Static"
3. **Root Directory:** Leave as `.` (current directory)
4. **Build Command:** Leave empty (no build needed)
5. **Output Directory:** Leave empty
6. Click **"Deploy"**

---

## STEP 6: Wait for Deployment
- Vercel will:
  - Install dependencies
  - Build your site
  - Deploy it
- Takes about 1-2 minutes
- You'll see progress in real-time

---

## STEP 7: Get Your URL
After deployment completes:
- You'll see: **"Congratulations! Your project has been deployed"**
- Your site URL will be: `ssrt-deployment-xxxxx.vercel.app`
- Click the URL to see your live site!

---

## STEP 8: Set Environment Variables (IMPORTANT!)

### Go to Project Settings:
1. Click on your project name
2. Click **"Settings"** tab (top menu)
3. Click **"Environment Variables"** (left sidebar)

### Add These Variables:
Click **"Add New"** for each one:

1. **Name:** `SQUARE_APPLICATION_ID`
   **Value:** (from your `F:\SQUARE_PAY_API.json` file, copy the `application_id`)

2. **Name:** `SQUARE_ACCESS_TOKEN`
   **Value:** (from your `F:\SQUARE_PAY_API.json` file, copy the `access_token`)

3. **Name:** `SQUARE_LOCATION_ID`
   **Value:** (from your `F:\SQUARE_PAY_API.json` file, copy the `location_id`)

4. **Name:** `SQUARE_ENVIRONMENT`
   **Value:** `sandbox` (for testing) or `production` (for real payments)

5. **Name:** `SALE_PRICE`
   **Value:** `29.99`

6. **Name:** `REGULAR_PRICE`
   **Value:** `49.00`

7. **Name:** `SALE_LIMIT`
   **Value:** `500`

8. **Name:** `CURRENT_SUBSCRIBERS`
   **Value:** `0`

9. **Name:** `SALE_ACTIVE`
   **Value:** `true`

### For Each Variable:
- **Environment:** Select **Production**, **Preview**, and **Development** (check all three)
- Click **"Save"**

---

## STEP 9: Redeploy (After Adding Variables)
1. Go to **"Deployments"** tab
2. Click the **"..."** menu on the latest deployment
3. Click **"Redeploy"**
4. This applies your environment variables

---

## STEP 10: Test Your Site
1. Visit your site URL
2. Test the payment system
3. Test the "Try for Free" button
4. Make sure everything works!

---

## 🎯 QUICK SUMMARY

**What You Do:**
1. ✅ Go to vercel.com
2. ✅ Sign up
3. ✅ Click "Add New Project"
4. ✅ Either:
   - Import from GitHub, OR
   - Use CLI: `npx vercel` in `F:\ssrt-deployment`
5. ✅ Wait for deployment
6. ✅ Add environment variables in Settings
7. ✅ Redeploy
8. ✅ Done!

**Time:** About 5-10 minutes total

---

## 🚨 TROUBLESHOOTING

### "Command not found: vercel"
- Use: `npx vercel` instead (no install needed)

### "Cannot find module"
- Make sure you're in `F:\ssrt-deployment` folder
- Vercel will install dependencies automatically

### Payment system not working
- Check environment variables are set correctly
- Make sure you redeployed after adding variables
- Check `SQUARE_ENVIRONMENT` is set to `sandbox` or `production`

### Need help?
- Vercel has great docs: https://vercel.com/docs
- Or check the deployment logs in Vercel dashboard

---

## ✅ YOU'RE READY!

Just follow these steps on the Vercel website. It's super easy!

