# Hardened Flask Reference Application

> **Purpose:** Reference implementation demonstrating TorusGuard-compliant security patterns for Flask applications.

---

## 🛡️ Applied Security Controls

1. **Environment-Based Secret Key (`TG-SEC-001`):** `SECRET_KEY` loaded from environment variables with mandatory production validation.
2. **Ownership-Scoped Document Lookups (`TG-AUTH-007`):** Enforces ownership check against authenticated session context.
3. **Safe File Uploads (`TG-INPUT-004`):** Uses `secure_filename()` and extension allowlisting.
4. **CSRF Protection (`TG-CSRF-001`):** Global CSRF protection enabled via `flask_wtf.CSRFProtect`.

See [fixes.md](fixes.md) for remediation details.
