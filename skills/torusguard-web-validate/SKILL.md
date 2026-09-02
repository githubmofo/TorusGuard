---
name: torusguard-web-validate
description: Execute authorized, bounded HTTP probes and session navigation with secret redaction and replay trace capture.
version: 0.9.2
workflow: .torusguard/workflows/web-validate.md
tools: Read, Grep, Glob, Bash, Write
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Web Validate — Bounded HTTP Probing & Session Capture

## Objective
Execute bounded, authorized HTTP requests against staging/local web endpoints to verify route responses, analyze security headers, audit cookie flags, and capture sanitized reproduction traces without causing denial-of-service or data corruption.

---

## Authorization Gate Check
Before dispatching any HTTP request:
1. Load `.torusguard/config/scope.json`.
2. Confirm `target_host` matches the requested endpoint.
3. Confirm `ttl_expiration` is in the future.
4. Confirm requested path matches an allowed prefix in `allowed_prefixes`.
*If any check fails, HALT immediately with a scope boundary error.*

---

## Safety Gate & Action Classification
Run `safety_gate.py` to classify proposed actions:
```bash
python .torusguard/scripts/safety_gate.py --method GET --path /api/v1/users --action check
```
- **Auto-Allowed**: Non-sensitive `GET`, `HEAD`, `OPTIONS` requests within authorized scope.
- **Approval Required**: Sensitive paths (`/auth/login`, `/settings`) or state-changing `POST` verbs.
- **Manual Only / Blocked**: Destructive operations (`DELETE`, `DROP`), payment endpoints, or forbidden paths.

---

## Execution Steps

### Step 1: Pre-Flight Safety Verification
Verify authorization scope and safety gate classification.

### Step 2: Prepare Request with Audit Headers
Inject mandatory audit headers into outbound requests:
- `X-TorusGuard-Scan: v0.9.2`
- `X-TorusGuard-RunId: <run-id>`

### Step 3: Dispatch Bounded Request
Send HTTP request adhering to strict limits:
- Max timeout: `5000ms`.
- Max redirect depth: `3`.
- Rate limiting: strictly cap requests to `rate_limit_per_second` (default 5 req/s).

### Step 4: Redact Credentials & Secrets
Scrub all captured requests and responses:
- Bearer tokens masked: `Bearer [REDACTED_JWT_sha256:<hash-prefix>]`
- Cookies masked: `session_id=[REDACTED_COOKIE]`
- Passwords and secret keys masked: `[REDACTED_SECRET]`

### Step 5: Save Run Artifacts
Write results to active run folder:
- `requests.json` and `responses.json`: Serialized, redacted HTTP interaction logs.
- `replay.json`: Deterministic curl command for manual reproduction.
- `web-validation.md`: Security analysis of status codes, headers (HSTS, CSP, X-Frame-Options), and cookie flags.

---

## Credential Redaction Protocol
```
Authorization: Bearer <jwt>   → Authorization: Bearer [REDACTED_JWT_sha256:abcd...]
Set-Cookie: session=<token>   → Set-Cookie: session=[REDACTED_COOKIE]
"password": "secret"          → "password": "[REDACTED_SECRET]"
"api_key": "sk_live_..."      → "api_key": "[REDACTED_KEY_sha256:ef01...]"
```

---

## Safety Constraints
- Only interact with hosts and paths explicitly listed in `.torusguard/config/scope.json`.
- Never execute automated `DELETE`, `PUT`, or bulk write operations.
- Never write unredacted credentials, tokens, or personal data to disk or console output.
- Cap request throughput strictly at 5 requests/sec.

---

## Output Format
```markdown
🛡️ [TorusGuard] Web Validation Completed
- Target Endpoint: <target_url>
- Response Code: <status_code>
- Security Headers: HSTS: <✅/❌> | CSP: <✅/❌> | X-Frame-Options: <✅/❌>
- Cookie Flags: HttpOnly: <✅/❌> | Secure: <✅/❌> | SameSite: <✅/❌>
- Credential Redaction: 100% Verified
- Replay Trace: .torusguard/runs/<run-id>/replay.json

Next Step: Run `/torusguard exploit-check` for deep vulnerability confirmation.
```
