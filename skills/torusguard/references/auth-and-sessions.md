# Authentication, Sessions, and Authorization

## Scope

Make authentication and authorization server-enforced and resistant to session and object-access failures (including IDOR).

## Threat Model

- Credential stuffing and brute force on login
- Session hijacking via insecure cookies or localStorage
- IDOR: accessing another user's resources by changing IDs
- Account enumeration via error messages
- Weak password hashing

## Detection Patterns

| Pattern | Severity |
|---------|----------|
| Plaintext password storage or comparison | Critical |
| MD5 or SHA1 password hashing | Critical |
| Role checks only in frontend routing | Critical |
| Trust in client-provided user ID | Critical |
| Missing auth middleware on sensitive routes | Critical |
| Missing ownership check on resource routes | Critical |
| JWT in localStorage without documented tradeoff | High |
| Session cookie missing httpOnly, Secure, or SameSite | High |
| Predictable password reset tokens | High |
| Login errors revealing "user not found" vs "wrong password" | Medium |

## Hard Bans

- No plaintext passwords
- No MD5 or SHA1 password hashes
- No role checks only in frontend routing
- No trust in user IDs passed by the client
- No predictable password reset tokens
- No authentication tokens in localStorage by default without documented threat tradeoffs
- No session cookie missing httpOnly, Secure, or appropriate SameSite
- No endpoint returning another user's data solely because its ID appears in the URL

## Required Safe Defaults

### Password hashing

```javascript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;
const hash = await bcrypt.hash(password, SALT_ROUNDS);
const valid = await bcrypt.compare(password, storedHash);
// Prefer Argon2id where available
```

### Secure cookies

```javascript
res.cookie('session', token, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'lax', // or 'strict' for sensitive apps
  maxAge: 24 * 60 * 60 * 1000,
  path: '/',
});
```

### Authorization middleware

```javascript
async function requireOwnership(req, res, next) {
  const resource = await db.query('SELECT user_id FROM posts WHERE id = $1', [req.params.id]);
  if (!resource.rows[0] || resource.rows[0].user_id !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
}
```

### Neutral login responses

```javascript
// Prevent account enumeration
if (!user || !(await bcrypt.compare(password, user.password_hash))) {
  return res.status(401).json({ error: 'Invalid email or password' });
}
```

### Password reset tokens

- Cryptographically random (32+ bytes)
- Expire within 15–60 minutes
- Single-use: invalidate after successful reset

## IDOR Test Requirement

For each sensitive route, ask:

> Can User A change the resource ID in this request and access User B's resource?

If yes, the route **fails** the audit.

Test routes like:

- `GET /api/users/:id`
- `PUT /api/posts/:id`
- `DELETE /api/orders/:id`

## CSRF Protection

When using cookie-based auth:

- Use CSRF tokens for state-changing requests, or
- SameSite=Strict/Lax cookies + verify Origin/Referer headers

## Verification Checklist

- [ ] All sensitive API endpoints authenticate users
- [ ] Each sensitive endpoint checks role, ownership, or org membership
- [ ] Passwords use Argon2id or bcrypt
- [ ] Reset tokens expire and are one-time use
- [ ] Session cookies use secure flags in production
- [ ] Login/reset responses do not enumerate accounts
- [ ] IDOR test passed for all resource routes

## False-Positive Guidance

- Public read endpoints intentionally unauthenticated (e.g., blog posts) — document in SECURITY.md
- JWT in Authorization header (not cookie) — CSRF less relevant; ensure XSS protection
- OAuth flows handled by provider — verify callback state parameter

## Remediation Steps

1. Add auth middleware to protected routes
2. Add ownership/role checks per resource
3. Upgrade password hashing
4. Fix cookie flags
5. Neutralize enumeration-prone error messages
