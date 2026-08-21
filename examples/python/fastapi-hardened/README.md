# Hardened FastAPI Reference Application

> **Purpose:** Reference implementation demonstrating TorusGuard-compliant security patterns for FastAPI applications.

---

## 🛡️ Applied Security Controls

1. **SSRF Mitigation (`TG-SSRF-001`, `TG-SSRF-002`):** Destination scheme validation, DNS resolution check, and private IP blocklist.
2. **HMAC Webhook Signature Verification (`TG-WEBHOOK-001`):** Verified using raw request bytes and constant-time comparison (`hmac.compare_digest`).
3. **Strict Pydantic Input Schemas (`TG-AUTH-006`):** Explicit fields defined with `extra = "forbid"`.
4. **Scoped Object Authorization (`TG-AUTH-007`):** Enforced ownership lookup boundaries.

See [fixes.md](fixes.md) for details.
