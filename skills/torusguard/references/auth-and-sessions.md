# Authentication, Sessions, and Authorization

## When to load

Load during `/torusguard check auth`, login/signup/reset implementation, or resource route reviews.

## Linked rules

- [TG-AUTH-001](../../rules/TG-AUTH-001-weak-password-storage.md) — Weak Password Storage (Critical)
- [TG-AUTH-002](../../rules/TG-AUTH-002-client-only-authorization.md) — Client-Only Authorization (High)
- [TG-AUTH-003](../../rules/TG-AUTH-003-missing-object-authorization.md) — IDOR/BOLA (High)
- [TG-AUTH-004](../../rules/TG-AUTH-004-insecure-session-cookie.md) — Insecure Session Cookie (High)
- [TG-AUTH-005](../../rules/TG-AUTH-005-unsafe-password-reset.md) — Unsafe Password Reset (High)

## Hard bans

- No plaintext, MD5, or SHA1 password storage
- No authorization enforced only in frontend routing
- No trust in client-supplied user IDs or roles
- No session cookies missing httpOnly/Secure/SameSite in production
- No predictable or reusable password reset tokens

## Safe defaults

- Argon2id or bcrypt (cost ≥ 12) for passwords
- httpOnly, Secure, SameSite cookies for browser sessions
- Server-side role and ownership checks on every sensitive route
- Neutral login/reset responses (no account enumeration)
- CSRF protection for cookie-authenticated state changes
- Reset tokens: random, single-use, expiring

## IDOR test procedure

For each route with a resource ID (`/api/users/:id`, `/api/orders/:orderId`):

> Can User A change the ID and access User B's resource?

If yes → fails TG-AUTH-003.

## Audit checklist

- [ ] Strong password hashing (TG-AUTH-001)
- [ ] Server enforces authZ (TG-AUTH-002)
- [ ] Object ownership verified (TG-AUTH-003)
- [ ] Secure cookie flags (TG-AUTH-004)
- [ ] Safe reset flow + rate limits (TG-AUTH-005)

## Manual review

- Organization/tenant-scoped authorization
- Privilege escalation via mass assignment
- Session fixation and logout invalidation

## Related rules

TG-RATE-001, TG-SEC-004, TG-INPUT-001
