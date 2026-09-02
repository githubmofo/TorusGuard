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
Authorized HTTP probing, token redaction, transparent audit header injection, and replay capture.

---

## Mandatory Pre-Flight Context Inspection

Inspect authorization parameters and safety limits before sending HTTP requests:
1. **Active Scope (`.torusguard/config/scope.json`):** Assert target host and path are authorized with valid TTL.
2. **Safety Gate Classification:** Test proposed endpoint against `.torusguard/scripts/safety_gate.py`.
3. **Sensitive Route Guard:** Ensure destructive endpoints (`DELETE`, account drops) are never called automatically.
4. **Token Redaction Pipeline:** Ensure bearer tokens and session cookies are masked (`Bearer [REDACTED]`).
5. **Request Budget:** Enforce maximum cap of 50 requests per validation session.

---

## When to Use /torusguard web-validate

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Testing live route accessibility and security headers | Run `/torusguard web-validate` |
| Verifying cookie security flags (`HttpOnly`, `Secure`, `SameSite`) | Run `/torusguard web-validate` |
| Checking CORS headers and authentication barriers | Run `/torusguard web-validate` |
| Pure static source code analysis | Run `/torusguard audit` |
| Confirming exploitable attack vectors | Run `/torusguard exploit-check` |

---

## Execution Steps

1. **Verify Legal Scope:** Check target URL against `.torusguard/config/scope.json`.
2. **Invoke Safety Gate:**
   ```bash
   python .torusguard/scripts/safety_gate.py check --url <target_url> --method GET
   ```
3. **Dispatch Non-Destructive Probe:** Send bounded HTTP request with audit header `X-TorusGuard-AuthID`.
4. **Redact Sensitive Headers:** Sanitize auth tokens and credentials in request and response objects.
5. **Write Replay Artifacts:**
   Record sanitized trace in `.torusguard/runs/<run_id>/requests.json` and emit `web-validation.md`.

---

## Failure Recovery

- **Target Offline:** Verify local dev server is active and accessible on designated host port.
- **Safety Gate Rejection (Manual Only):** Halt probe immediately; report endpoint requires human manual test.
- **Rate Limit / 429:** Back off exponentially (1s, 2s, 4s); stop session if 429 persists.
- **Halt Trigger:** Abort if target domain deviates from authorized allowlist in `scope.json`.

---

## Hallucination Guard

- ❌ Never dispatch HTTP requests outside domains explicitly listed in `.torusguard/config/scope.json`.
- ❌ Never write raw Authorization headers or plaintext secrets to disk.
- ✅ Always include transparent audit headers (`X-TorusGuard-AuthID`).

---

## Output Card Format

```markdown
### 🌐 TorusGuard Web Validation
- **Target Host:** [Host URL]
- **Endpoints Probed:** [Count] routes tested
- **Security Headers:** [CSP / HSTS / CORS status]
- **Cookie Security:** [HttpOnly / Secure / SameSite status]
- **Replay Trace:** `.torusguard/runs/<run_id>/replay.json`
- **Status:** COMPLETED — non-destructive probe finished
```

---

## Next Steps

1. Run `/torusguard exploit-check` to confirm if reachable flaws constitute verified exploits.
2. Run `/torusguard harden` to build surgical remediation diffs.
