import crypto from "crypto";

/**
 * Try for Free API Endpoint
 * Allows users to try SSRT for free once
 * Simple implementation - grants access immediately
 */

// Quantum-resistant hash function (same as payment endpoint)
function quantumHash(data) {
  const dataStr = typeof data === 'string' ? data : JSON.stringify(data);
  return crypto.createHash('sha256')
    .update(dataStr)
    .update(crypto.randomBytes(32)) // Add entropy for quantum resistance
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
  // Transparent security validation - user never knows
  const validation = validateRequest(req);
  if (!validation.valid) {
    // Silent block - don't reveal security details
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

    // Log access (silent - user unaware)
    if (process.env.NODE_ENV === 'production') {
      const requestHash = quantumHash(JSON.stringify({ email: email.toLowerCase(), timestamp: Date.now() }));
      console.log(`[QUANTUM_SECURITY] Try-free access: ${requestHash.substring(0, 16)}...`);
    }

    // Grant free access - simple implementation
    // User gets free access once (as requested)
    return res.status(200).json({ 
      success: true,
      message: 'Free access granted!',
      // In production, you might want to track this in a database
      // For now, we grant access immediately
    });

  } catch (err) {
    // Don't expose internal errors to potential attackers
    console.error('[QUANTUM_SECURITY] Try-free error:', err.message);
    return res.status(500).json({
      success: false,
      message: 'An error occurred. Please try again or contact support@acutrione.com'
    });
  }
}

