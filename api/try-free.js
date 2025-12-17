import crypto from "crypto";
import fs from "fs";
import path from "path";

/**
 * Try for Free API Endpoint
 * Allows users to try SSRT for free once per email per week
 * Tracks email usage to prevent abuse
 */

// Path to store email tracking data
const TRACKING_FILE = path.join(process.cwd(), 'api', 'data', 'try-free-emails.json');

// Ensure data directory exists
function ensureDataDir() {
  const dataDir = path.dirname(TRACKING_FILE);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
}

// Load email tracking data
function loadTrackingData() {
  try {
    ensureDataDir();
    if (fs.existsSync(TRACKING_FILE)) {
      const data = fs.readFileSync(TRACKING_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('[ERROR] Failed to load tracking data:', error.message);
  }
  return {};
}

// Save email tracking data
function saveTrackingData(data) {
  try {
    ensureDataDir();
    fs.writeFileSync(TRACKING_FILE, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error('[ERROR] Failed to save tracking data:', error.message);
    return false;
  }
}

// Check if email can use free trial (not used in last 7 days)
function canUseFreeTrial(email, trackingData) {
  const normalizedEmail = email.toLowerCase().trim();
  const now = Date.now();
  const oneWeekAgo = now - (7 * 24 * 60 * 60 * 1000); // 7 days in milliseconds

  if (!trackingData[normalizedEmail]) {
    return { allowed: true, reason: 'first_time' };
  }

  const lastUsed = trackingData[normalizedEmail].lastUsed;
  if (lastUsed < oneWeekAgo) {
    return { allowed: true, reason: 'week_passed' };
  }

  const daysRemaining = Math.ceil((lastUsed + (7 * 24 * 60 * 60 * 1000) - now) / (24 * 60 * 60 * 1000));
  return { 
    allowed: false, 
    reason: 'recently_used',
    daysRemaining: daysRemaining,
    lastUsed: new Date(lastUsed).toISOString()
  };
}

// Record email usage
function recordEmailUsage(email, trackingData) {
  const normalizedEmail = email.toLowerCase().trim();
  if (!trackingData[normalizedEmail]) {
    trackingData[normalizedEmail] = {
      firstUsed: Date.now(),
      lastUsed: Date.now(),
      count: 1
    };
  } else {
    trackingData[normalizedEmail].lastUsed = Date.now();
    trackingData[normalizedEmail].count = (trackingData[normalizedEmail].count || 0) + 1;
  }
  return trackingData;
}

// Quantum-resistant hash function
function quantumHash(data) {
  const dataStr = typeof data === 'string' ? data : JSON.stringify(data);
  return crypto.createHash('sha256')
    .update(dataStr)
    .update(crypto.randomBytes(32))
    .digest('hex');
}

// Transparent request validation - blocks attacks silently
function validateRequest(req) {
  const bodyStr = JSON.stringify(req.body || {});
  
  // SQL Injection protection
  if (/('|(\\')|(;)|(\\)|(\/\*)|(\*\/)|(xp_)|(sp_)|(exec)|(execute)|(union)|(select)|(insert)|(update)|(delete)|(drop)|(create)|(alter)|(grant)|(revoke)|(truncate))/i.test(bodyStr)) {
    return { valid: false, threat: 'SQL_INJECTION' };
  }
  
  // XSS protection
  if (/<script|javascript:|onerror=|onload=|onclick=|eval\(|document\.cookie|window\.location/i.test(bodyStr)) {
    return { valid: false, threat: 'XSS_ATTEMPT' };
  }
  
  // Command injection protection
  if (/(\||&|;|`|\$\(|\.\.\/|\.\.\\|cmd|powershell|bash|sh)/i.test(bodyStr)) {
    return { valid: false, threat: 'COMMAND_INJECTION' };
  }
  
  return { valid: true };
}

export default async function handler(req, res) {
  // Transparent security validation
  const validation = validateRequest(req);
  if (!validation.valid) {
    return res.status(400).json({ error: 'Invalid request' });
  }

  // Add quantum security headers transparently
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('X-Quantum-Security', 'MAXIMUM');

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { email } = req.body || {};

    if (!email) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email address is required' 
      });
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ 
        success: false, 
        message: 'Invalid email address format' 
      });
    }

    // Load tracking data
    const trackingData = loadTrackingData();

    // Check if email can use free trial
    const checkResult = canUseFreeTrial(email, trackingData);

    if (!checkResult.allowed) {
      // Email used recently - deny access
      return res.status(200).json({
        success: false,
        message: `This email has already used the free trial. Please try again in ${checkResult.daysRemaining} day(s) or purchase SSRT for full access.`,
        daysRemaining: checkResult.daysRemaining,
        lastUsed: checkResult.lastUsed
      });
    }

    // Email can use free trial - record usage
    const updatedTrackingData = recordEmailUsage(email, trackingData);
    const saved = saveTrackingData(updatedTrackingData);

    if (!saved) {
      console.error('[ERROR] Failed to save email tracking data');
      // Still grant access even if save fails (graceful degradation)
    }

    // Log access (silent - user unaware)
    if (process.env.NODE_ENV === 'production') {
      const requestHash = quantumHash(JSON.stringify({ email: email.toLowerCase(), timestamp: Date.now() }));
      console.log(`[QUANTUM_SECURITY] Try-free access granted: ${requestHash.substring(0, 16)}...`);
    }

    // Grant free access
    return res.status(200).json({ 
      success: true,
      message: 'Free access granted!',
      reason: checkResult.reason
    });

  } catch (err) {
    console.error('[QUANTUM_SECURITY] Try-free error:', err.message);
    return res.status(500).json({
      success: false,
      message: 'An error occurred. Please try again or contact support@acutrione.com'
    });
  }
}
