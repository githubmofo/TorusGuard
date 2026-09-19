# Platform and HTTP Hardening

## When to load

Load during `/TorusGuard check platform`, deployment prep, or `/TorusGuard verify`.

## Linked rules

- [TG-PLATFORM-001](../../rules/TG-PLATFORM-001-wildcard-cors-with-credentials.md) — Wildcard CORS + Credentials (High)
- [TG-PLATFORM-002](../../rules/TG-PLATFORM-002-missing-security-headers.md) — Missing Security Headers (Medium)
- [TG-PLATFORM-003](../../rules/TG-PLATFORM-003-production-stack-trace-exposure.md) — Stack Trace Exposure (Medium)
- [TG-PLATFORM-004](../../rules/TG-PLATFORM-004-missing-request-size-limits.md) — Missing Request Size Limits (Medium)

## Hard bans

- No `Access-Control-Allow-Origin: *` with credentials
- No production stack traces or raw DB errors to clients
- No debug mode in production
- No missing body limits on public JSON endpoints
- No executable uploads in public web directories

## Safe defaults

- CORS explicit allowlist
- Helmet or equivalent: CSP, `X-Content-Type-Options`, HSTS (production), `Referrer-Policy`, clickjacking protection
- Generic user-facing errors; detailed logs server-side with request ID
- HTTPS enforced in production
- `express.json({ limit: '100kb' })` or appropriate caps
- Dependency audit before deploy

## Audit checklist

- [ ] CORS allowlist (TG-PLATFORM-001)
- [ ] Security headers configured (TG-PLATFORM-002)
- [ ] Errors sanitized (TG-PLATFORM-003)
- [ ] Request/upload limits set (TG-PLATFORM-004)

## Framework notes

- **Express** — Helmet + central error handler
- **Next.js** — headers in `next.config` or middleware
- **Reverse proxy** — TLS termination, HSTS, rate limits

## Manual review

- CSP compatibility with actual script/style sources
- Infrastructure firewall and WAF rules
- Backup and monitoring configuration

## Related rules

TG-RATE-003, TG-SEC-004, TG-CLIENT-001

## Framework guide

[Express Security](../../guides/express-security.md)
