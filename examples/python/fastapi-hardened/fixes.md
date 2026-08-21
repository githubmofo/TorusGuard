# Hardened Fixes Matrix: FastAPI

| Risk | Rule ID | Hardened Implementation |
|---|---|---|
| Unrestricted URL Fetch | `TG-SSRF-001` | Scheme validation and private/loopback IP verification |
| Unverified Webhook | `TG-WEBHOOK-001` | `hmac.compare_digest()` validation on `await request.body()` |
| Mass Assignment Risk | `TG-AUTH-006` | Structured `ProfileUpdateSchema(BaseModel)` with `extra="forbid"` |
