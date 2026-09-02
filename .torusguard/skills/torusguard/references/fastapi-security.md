# TorusGuard Skill Reference: FastAPI Security

> **Loaded When:** Project uses `fastapi` dependencies or imports.

---

## 🛡️ Key Inspection Areas & Rules

### 1. Route Authorization & Dependencies
* `TG-AUTH-001` / `TG-AUTH-003`: Verify protected routes include security dependencies (`Depends(get_current_user)`).
* `TG-AUTH-007`: In route handlers taking numeric/UUID path parameters (e.g. `profile_id`, `invoice_id`), verify that database queries filter by the authenticated user's ID.

### 2. Request Models & Mass Assignment
* `TG-AUTH-006`: Check that endpoints accept structured Pydantic `BaseModel` classes rather than raw `dict`, `Body(...)`, or unpacking `**payload` directly into ORM entities.

### 3. Outbound Requests & SSRF
* `TG-SSRF-001`: Inspect endpoints that fetch external URLs via `httpx` or `requests`. Verify scheme validation and private IP address filtering.

### 4. Webhook Integrity
* `TG-WEBHOOK-001`: In webhook endpoints, verify HMAC signature validation using `await request.body()` (raw bytes) before JSON parsing.
