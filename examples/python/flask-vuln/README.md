# Intentionally Vulnerable Example: Flask Application
> **WARNING:** This project exists only to test and demonstrate TorusGuard guidance. Do not deploy it, expose it to the internet, reuse its security patterns, or add real credentials. All secrets, users, payment values, and tokens are fake and nonfunctional.

---

## 🎯 Educational Purpose
Demonstrates common Flask vulnerabilities:
1. **`TG-SEC-001`**: Hardcoded `SECRET_KEY = "insecure_dev_key"`.
2. **`TG-AUTH-007`**: Document lookup by ID without user ownership filtering (IDOR).
3. **`TG-CSRF-001`**: State-changing POST endpoint missing CSRF protection.
4. **`TG-INPUT-004`**: File upload accepting unsanitized client filename directly into filesystem.

See [fixes.md](fixes.md) and [../flask-hardened/](../flask-hardened/) for the hardened counterpart.
