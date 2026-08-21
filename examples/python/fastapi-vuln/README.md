# Intentionally Vulnerable Example: FastAPI Application
> **WARNING:** This project exists only to test and demonstrate TorusGuard guidance. Do not deploy it, expose it to the internet, reuse its security patterns, or add real credentials. All secrets, users, payment values, and tokens are fake and nonfunctional.

---

## 🎯 Educational Purpose
Demonstrates common FastAPI security vulnerabilities:
1. **`TG-SSRF-001`**: Unvalidated outbound URL fetching via `requests.get(url)`.
2. **`TG-WEBHOOK-001`**: Missing HMAC signature validation on POST `/webhook`.
3. **`TG-AUTH-006`**: Mass assignment vulnerability on POST `/update_profile` taking an unfiltered `dict`.
4. **`TG-AUTH-007`**: Profile lookup by numeric ID without verifying authenticated caller ownership.

See [fixes.md](fixes.md) and [../fastapi-hardened/](../fastapi-hardened/) for the hardened counterpart.
