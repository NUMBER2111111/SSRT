# SSRT Payment System Setup Guide

## Current Status: SANDBOX TEST MODE

The payment system is currently in **sandbox test mode** which allows you to test the full payment flow without real Square credentials.

## Step 1: Sandbox Testing (Current)

The system will work in test mode automatically. You can:
- Test the payment flow UI
- See how the paywall works
- Verify email tracking
- Test subscriber counting

**Test Mode Features:**
- No real Square credentials needed
- Payments are simulated (no actual charges)
- All functionality works for testing

## Step 2: Get Square Sandbox Credentials

1. Go to: https://developer.squareup.com/apps
2. Sign in or create a Square Developer account
3. Create a new application
4. Get your **Application ID** (starts with `sandbox-sq0idb-`)
5. Generate a **Sandbox Access Token** (starts with `sandbox-sq0atb-`)
6. Get your **Sandbox Location ID** from the Locations section

## Step 3: Update Configuration File

Edit `F:\SQUARE_PAY_API.json`:

```json
{
  "square_api": {
    "application_id": "sandbox-sq0idb-YOUR_ACTUAL_ID",
    "access_token": "sandbox-sq0atb-YOUR_ACTUAL_TOKEN",
    "location_id": "sandbox-location-YOUR_ACTUAL_LOCATION",
    "environment": "sandbox",
    "api_version": "2024-01-18"
  },
  "payment_config": {
    "currency": "USD",
    "sale_price": 29.99,
    "regular_price": 49.00,
    "sale_limit": 500,
    "current_subscribers": 0,
    "sale_active": true
  }
}
```

## Step 4: Test in Sandbox

1. Restart the API server: `node api/server.js`
2. Test payment flow on the website
3. Use Square test cards:
   - Success: `4111 1111 1111 1111`
   - Decline: `4000 0000 0000 0002`
   - CVV: Any 3 digits
   - Expiry: Any future date

## Step 5: Production Setup

When ready for production:

1. Switch to production in Square Dashboard
2. Get production credentials:
   - Production Application ID
   - Production Access Token
   - Production Location ID
3. Update `F:\SQUARE_PAY_API.json`:
   - Replace all sandbox values with production values
   - Set `"environment": "production"`
4. Test with small real transaction first
5. Monitor Square Dashboard for transactions

## Security Notes

- **NEVER** commit `SQUARE_PAY_API.json` to version control
- Store production credentials securely
- Use environment variables in production (recommended)
- Rotate access tokens regularly
- Monitor for unauthorized access

## Troubleshooting

**Error: "Payment system initialization failed"**
- Check if `F:\SQUARE_PAY_API.json` exists
- Verify file has valid JSON
- Check server logs for specific errors

**Error: "Square configuration incomplete"**
- Ensure all three values are set (application_id, access_token, location_id)
- Remove placeholder values

**Test Mode Active**
- This is normal if credentials aren't set
- System will simulate payments for testing
- Update config file to use real Square credentials

## Support

For payment issues: support@acutrione.com

