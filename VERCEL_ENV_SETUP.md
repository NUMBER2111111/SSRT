# Vercel Environment Variables Setup - ssrt-opal

## Current Status
✅ Code deployed: commit f2343cc is live  
✅ API endpoint exists: `/api/payment/create-link`  
✅ Frontend button ready: "Buy SSRT ($5)"  
❌ Environment variables: **MISSING** (needs to be added)

---

## Step 1: Add Environment Variables (Vercel Dashboard)

**Navigate to:**
```
https://vercel.com/number2111111s-projects/ssrt-opal/settings/environment-variables
```

**Or manually:**
- Vercel Dashboard → ssrt-opal → Settings → Environment Variables

---

### Add Variable 1: SQUARE_ACCESS_TOKEN

1. Click **"Add New"** button
2. **Name:** `SQUARE_ACCESS_TOKEN`
3. **Value:** (paste your Square Production access token)
4. **Environment:** Select **Production** only (uncheck Preview/Development)
5. Click **Save**

---

### Add Variable 2: SQUARE_LOCATION_ID

1. Click **"Add New"** button again
2. **Name:** `SQUARE_LOCATION_ID`
3. **Value:** (paste your Square Location ID)
4. **Environment:** Select **Production** only (uncheck Preview/Development)
5. Click **Save**

---

## Step 2: Redeploy Latest Deployment

**Navigate to:**
```
https://vercel.com/number2111111s-projects/ssrt-opal/deployments
```

**Or manually:**
- Vercel Dashboard → ssrt-opal → Deployments

1. Find the latest deployment (should show commit f2343cc)
2. Click the **⋯** (three dots) menu
3. Click **"Redeploy"**
4. Wait for status to show **"Ready"** (usually 1-2 minutes)

---

## Step 3: Verify API Endpoint

**Run this PowerShell command:**
```powershell
.\verify-square-api.ps1
```

**Or run directly:**
```powershell
Invoke-WebRequest `
  -Uri "https://ssrt-opal.vercel.app/api/payment/create-link" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"amount":500,"currency":"USD","name":"SSRT"}' |
Select-Object StatusCode, @{Name='Response';Expression={$_.Content}}
```

**Expected Result:**
- StatusCode: `200`
- Response contains: `"url":"https://square.link/..."`

---

## Step 4: Test Frontend Button

1. Open: `https://ssrt-opal.vercel.app` (use incognito if needed)
2. Click **"Buy SSRT ($5)"** button
3. Should redirect to Square checkout page

---

## Troubleshooting

### If API returns 500 error:
- Check env vars are set for **Production** (not just Preview)
- Verify token is **Production** token (not Sandbox)
- Verify Location ID matches your Square account
- **Redeploy** after adding/changing env vars

### If homepage shows old content:
- Hard refresh: `Ctrl+Shift+R`
- Or open in incognito window
- Check deployment is **Ready** and from commit f2343cc

### If button doesn't redirect:
- Open browser DevTools → Network tab
- Click button
- Check POST to `/api/payment/create-link`
- Paste the response JSON here for debugging

---

## Success Criteria

✅ API returns 200 with Square link  
✅ Button redirects to Square checkout  
✅ Payment can be completed on Square's page  
✅ Transaction appears in Square Dashboard

---

**Once these are set, you're live and collecting payments.**

