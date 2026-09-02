---
description: Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: validator
lifecycle-phase: Phase 3b (Runtime Web Validation)
required-skills:
  - torusguard-web-validate
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# /torusguard web-validate — Bounded HTTP Probing & Session Capture

$ARGUMENTS

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Mandatory Pre-Flight Context Inspection

Before dispatching any live network requests, you MUST inspect:

1. **Authorization Scope Record (`.torusguard/config/scope.json`)** → Confirm that target URL and paths are explicitly authorized and TTL has not expired.
2. **Safety Gate Classification** → Check proposed HTTP methods and paths against `safety_gate.py` policies (`Auto-Allowed`, `Approval Required`, or `Manual Only`).
3. **Sensitive Path Restrictions** → Verify that administrative actions, password resets, or account deletions are NOT executed automatically.
4. **Token Redaction Pipeline** → Ensure all cookies, Bearer tokens, and auth headers will be redacted before saving to disk.

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## When to Use /torusguard web-validate

| Use `/torusguard web-validate` when... | Use something else when... |
| :--- | :--- |
| Checking live route accessibility and headers | Pure source code scan → `/torusguard audit` |
| Verifying cookie flags (HttpOnly, Secure, SameSite) | Checking exploit payloads → `/torusguard exploit-check` |
| Validating CORS headers and authentication barriers | Authorizing new scope → `/torusguard authorize` |
| Capturing deterministic HTTP replay traces | Patching code → `/torusguard harden` |

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Execution Steps (Fixed Order)

### Phase 1 — Verify Legal Authorization
Read `.torusguard/config/scope.json` and confirm:
- `target_host` matches the requested endpoint.
- `ttl_expiration` is in the future.
- Path matches an authorized prefix in `allowed_prefixes`.
If invalid or expired, HALT and instruct operator to run `/torusguard authorize`.

### Phase 2 — Safety Gate Pre-Flight Filter
Run `safety_gate.py` on the proposed action:
```bash
python .torusguard/scripts/safety_gate.py --method GET --path /api/v1/users --action check
```
- **Auto-Allowed**: Non-sensitive `GET`, `HEAD`, `OPTIONS` within authorized prefix. Proceed.
- **Approval Required**: Sensitive endpoints (`/auth/login`, `/settings`). Ask operator for confirmation before sending.
- **Manual Only / Blocked**: Destructive verbs (`DELETE`, `DROP`) or forbidden paths (`/admin/delete`). Block immediately.

### Phase 3 — Dispatched Bounded Request Execution
1. Inject mandatory TorusGuard audit headers:
   - `X-TorusGuard-Scan: v0.9.2`
   - `X-TorusGuard-RunId: <active-run-id>`
2. Execute bounded HTTP probe with safety constraints:
   - Timeout: `5000ms` max per request.
   - Max redirects: `3`.
   - Max payload response size: `256KB`.

### Phase 4 — Secret & Credential Redaction
Sanitize raw request and response data:
- Bearer tokens replaced with `Bearer [REDACTED_JWT_sha256:abcd...]`
- Cookies scrubbed or hashed.
- Passwords and secret keys masked with `[REDACTED_SECRET]`.

### Phase 5 — Record Artifacts & Replay Trace
Save outputs into current run folder:
- `requests.json` and `responses.json` (redacted request/response pairs).
- `replay.json` (deterministic curl command for reproduction).
- `web-validation.md` (summary of response codes, header security posture, and findings).

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Failure Recovery & Cascade Rules

```
Target unreachable (599): Record 'Unreachable Target' in web-validation.md; do not crash
Safety gate rejection:    Log 'Blocked by Safety Policy'; continue with remaining routes
Rate limit triggered:    Pause 5 seconds, back off request rate by 50%, and retry once
Secret redaction failure: HALT IMMEDIATELY — Never write unredacted credentials to disk
```

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Hallucination Guard

```
❌ Never issue HTTP requests outside the exact hosts defined in scope.json
❌ Never bypass the safety_gate.py check under any circumstance
❌ Never log raw authorization headers or passwords to disk or terminal
❌ Never flood endpoints beyond the rate limit defined in scope.json
```

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Web Validation Probe Completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target Endpoint:    [http://localhost:8000/api/v1/users]
Response Code:      [200 OK / 401 Unauthorized / 403 Forbidden]
Security Headers:   Strict-Transport-Security: ✅ | Content-Type-Options: ✅
Cookie Attributes:  HttpOnly: ⚠️ Missing | SameSite: Strict ✅
Redaction Status:   100% Auth Headers & Cookies Redacted
Replay Artifact:    .torusguard/runs/<run-id>/replay.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Findings:
- Cookie 'session_id' lacks HttpOnly flag (Exposes cookie to XSS read)
- Missing X-Frame-Options on /login (Clickjacking risk)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard harden` to remediate identified cookie configurations.
```

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Security header or cookie flaw found | → `/torusguard harden` |
| Deep exploit confirmation needed | → `/torusguard exploit-check` |
| Scope expired | → `/torusguard authorize` |
