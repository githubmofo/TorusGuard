# Rate Limiting and Abuse Prevention

## Scope

Protect public and expensive endpoints against brute force, enumeration, spam, denial of service, OTP abuse, and resource exhaustion.

## Threat Model

- Brute force on login and password reset
- OTP flooding and SMS/email cost abuse
- Contact form spam
- API scraping and DoS via high request volume
- Resource exhaustion via large payloads or uploads

## Endpoints That Must Be Reviewed

```
/login, /signup, /logout
/forgot-password, /reset-password
/verify-otp, /send-otp
/contact, /feedback, /search
/api/*, AI/LLM endpoints
File upload endpoints
Payment, coupon, webhook endpoints
```

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| Login endpoint with no rate limit | High |
| Password reset with no per-email limit | High |
| OTP send with no per-identifier limit | High |
| Public POST with no body size limit | Medium |
| In-memory rate limiter as sole protection in distributed prod | Medium |
| Frontend-only throttling with no server limit | High |
| Missing 429 response on limit exceeded | Low |

## Required Rules

- Per-IP limits for public endpoints
- Per-account or per-identifier limits for login, OTP, and password reset
- Body-size limits on JSON endpoints
- Upload-size limits
- Return HTTP **429 Too Many Requests** when limits exceeded
- Include `Retry-After` header when practical
- Backoff or temporary lockout for repeated failed auth
- Shared rate-limit store (Redis) in distributed production — not in-memory only

## Suggested Initial Defaults

| Endpoint type | Suggested limit |
|---------------|-----------------|
| Login | 5 attempts per IP per 15 min + account-level backoff |
| Password reset | 3 requests per email per hour |
| OTP send | 3 requests per phone/email per 15 min |
| Contact form | 5 requests per IP per hour |
| General public API | 60 requests per IP per minute |
| Search | 30 requests per IP per minute |
| File upload | 10 uploads per IP per hour + size limits |
| AI endpoint | Cost-based limit per user and per IP |

Defaults are configurable — adjust for traffic profiles.

## Implementation Examples

### Express with express-rate-limit

```javascript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many login attempts. Try again later.' },
});

app.post('/api/login', loginLimiter, loginHandler);
```

### Per-email reset limiter (Redis example)

```javascript
async function checkResetLimit(email) {
  const key = `reset:${email}`;
  const count = await redis.incr(key);
  if (count === 1) await redis.expire(key, 3600);
  if (count > 3) throw new RateLimitError('Too many reset requests');
}
```

### Body size limits

```javascript
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));
```

## Hard Bans

- Never rely only on frontend throttling
- Never leave login, reset, OTP, or contact endpoints unlimited in production

## Verification Checklist

- [ ] All public write endpoints have appropriate rate limits
- [ ] Auth and reset flows have per-account protections
- [ ] Rate-limit response is 429
- [ ] Body and upload size limits configured
- [ ] Production distributed deployments use shared limit store

## False-Positive Guidance

- Internal admin endpoints behind VPN — may use different limits; document in SECURITY.md
- Webhook endpoints — rate limit by IP + signature verification, not generic public limits
- GraphQL — apply query complexity limits in addition to request rate limits

## Remediation Steps

1. Identify unprotected public endpoints
2. Add appropriate limiter middleware
3. Configure body/upload size limits
4. Use Redis or equivalent for multi-instance deployments
