# Hardened Django Reference Application

> **Purpose:** Reference implementation demonstrating TorusGuard-compliant security patterns for Django web applications.

---

## 🛡️ Applied Security Controls

1. **Environment-driven Secrets (`TG-SEC-001`):** `SECRET_KEY` is loaded strictly from environment variables.
2. **Production-safe Settings (`TG-PLATFORM-001`, `TG-PLATFORM-003`):** `DEBUG = False`, explicit `ALLOWED_HOSTS`, and cookie security flags (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`).
3. **Ownership-scoped Lookups (`TG-AUTH-007`):** Object views filter lookups by `request.user` to prevent IDOR vulnerabilities.
4. **Explicit ModelForm Whitelist (`TG-AUTH-006`):** Forms define strict `fields = [...]` lists to prevent mass assignment.
5. **Cache Isolation (`TG-CACHE-001`):** Sensitive user views are decorated with `@never_cache`.

See [fixes.md](fixes.md) for the exact line-by-line remediation matrix.
