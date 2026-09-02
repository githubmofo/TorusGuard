# TorusGuard Security Rule Catalog & Activation System

This directory manages the active and custom security rules enforced by TorusGuard.

---

## 1. Rule Architecture & Taxonomy

TorusGuard security rules follow a canonical identifier pattern: `TG-<CATEGORY>-<NUMBER>`.

| Category Prefix | Domain Area | Focus & Vulnerability Classes |
| :--- | :--- | :--- |
| `TG-AUTH` | Authentication & Authorization | Missing tenant scoping, client-only route guards, session cookie flags, insecure password resets |
| `TG-INPUT` | Input Validation & Injection | SQL injection, unsafe HTML/template rendering, unvalidated file uploads, path traversal |
| `TG-SEC` | Secrets & Configuration | Hardcoded API keys, tracked `.env` files, sensitive logging, exposed cloud credentials |
| `TG-DB` | Database & ORM Security | Frontend direct DB access, admin SDK exposure, missing multi-tenant query isolation |
| `TG-CLIENT` | Frontend & Client Bundles | Public production source maps, sensitive secrets embedded in client build assets |
| `TG-RATE` | Rate Limiting & Resource Abuse | Unlimited auth endpoints, unbounded pagination, excessive resource consumption |
| `TG-PLATFORM` | Platform & Gateway Hardening | Wildcard CORS with credentials, missing security headers, exposed stack traces |
| `TG-SSRF` | Outbound Requests & SSRF | Unvalidated HTTP client destinations, metadata IP access, internal network probing |
| `TG-SUPPLY` | Dependency & Supply Chain | Unpinned dependencies, known CVEs, malicious dependency confusion risks |

---

## 2. Active Rules System (`rules/active/`)

When you run `/torusguard init`, TorusGuard automatically inspects your project stack and activates relevant rules in `rules/active/`.

- **Universal Rules:** Always activated (`TG-SEC-*`, `TG-INPUT-*`, `TG-AUTH-*`).
- **Framework-Specific Rules:**
  - Python / Django: `TG-DB-004`, `TG-RATE-001`, `TG-PLATFORM-*`.
  - Next.js / React: `TG-CLIENT-*`, `TG-PLATFORM-001`, `TG-AUTH-002`.
  - API / Node.js: `TG-INPUT-001`, `TG-SSRF-001`, `TG-RATE-002`.

---

## 3. Creating Custom Rules

You can add custom rules directly into this directory or configure a custom path in `.torusguard/config/torusguard.json`:

```markdown
# TG-CUSTOM-001: Require Organization UUID on All Tenant Queries

**Severity:** High  
**Category:** authentication-authorization  
**Confidence Base:** 80  

### Vulnerability Pattern
Ensure every database query on multi-tenant models filters explicitly by `org_id` or `tenant_id`.

### Unsafe Pattern
```python
# Unsafe: Queries tenant data globally without org predicate
TenantRecord.objects.filter(status="active")
```

### Safe Pattern
```python
# Safe: Scoped to requesting organization
TenantRecord.objects.filter(org_id=request.user.org_id, status="active")
```
```
