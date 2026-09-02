---
name: torusguard-web-validate
description: Execute authorized HTTP probing against local/staging web applications — session capture, transparent audit headers, and secret redaction.
version: 0.9.2
workflow: .torusguard/workflows/web-validate.md
tools: Read, Grep, Glob, Bash, Write
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Web Validate — Bounded HTTP Probing & Session Capture

## Objective
Safely probe live web applications within authorized scope, injecting transparent audit headers, verifying security headers and cookies, redacting sensitive tokens, and recording deterministic replay traces.

---

## Authorization Gate Check
Before dispatching any HTTP request:
1. Verify `.torusguard/config/scope.json` exists and contains target URL.
2. Confirm current timestamp is prior to `expires_at` TTL.
3. Assert target is local or non-production staging.

---

## Safety Gate
All requests pass through `.torusguard/scripts/safety_gate.py`:
- `Auto-Allowed`: Read-only `GET`, `HEAD`, `OPTIONS` on non-sensitive paths.
- `Approval Required`: Requests touching auth, sessions, or parameters.
- `Manual Only`: Any destructive method (`DELETE`, `DROP`) is strictly blocked.

---

## Execution Steps

1. **Gate Check:** Validate scope in `scope.json` and query `safety_gate.py`.
2. **Inject Audit Header:** Attach `X-TorusGuard-AuthID: <auth_id>` to all outbound requests.
3. **Dispatch Bounded Probe:** Send single non-destructive HTTP request.
4. **Validate Security Headers:** Check for CSP, HSTS, X-Content-Type-Options, and CORS configurations.
5. **Audit Cookie Flags:** Verify `HttpOnly`, `Secure`, and `SameSite` on session cookies.
6. **Capture Replay Trace:** Save sanitized trace in `.torusguard/runs/<run_id>/requests.json`.

---

## Credential Redaction
All Bearer tokens, cookies, passwords, and API keys are redacted prior to disk serialization (`Bearer [REDACTED]`).

---

## Safety Constraints
- Max 50 requests per validation session.
- Never test unauthorized domains or third-party APIs.
- Zero state-changing destructive operations.

---

## Output Format
```markdown
🌐 [TorusGuard] Web Validation Completed
- Target: <Host URL> | Endpoints Tested: <Count>
- Header Posture: <CSP/HSTS Status> | Cookies: <Flags Status>
- Replay Trace: `.torusguard/runs/<run_id>/requests.json`
Next: Run `/torusguard exploit-check` to confirm exploitability of candidate flaws.
```
