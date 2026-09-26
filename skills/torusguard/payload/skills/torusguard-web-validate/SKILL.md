---
name: torusguard-web-validate
description: Execute authorized HTTP probing against local/staging web applications — session capture, transparent audit headers, and secret redaction.
version: 2.0.0
workflow: .torusguard/workflows/web-validate.md
tools: Read, Grep, Glob, Bash, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Web Validate — Bounded HTTP Probing & Session Capture

## Objective
Safely probe live web applications within authorized scope, injecting transparent audit headers, verifying security headers and cookies, redacting sensitive tokens, and recording deterministic replay traces.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard web-validate` | Dispatches bounded HTTP probes with transparent audit headers and redaction. |
| **Mode B: AI Chat Slash** | `/torusguard web-validate` | Interactive verification of endpoints, security headers, and cookie flags. |
| **Mode C: Native MCP Tool**| — | Safe runtime execution guarded by scope.json boundaries. |

---

## Authorization Gate Check
Before dispatching any HTTP request:
1. Verify `.torusguard/config/scope.json` exists and contains target URL.
2. Confirm current timestamp is prior to `expires_at` TTL.
3. Assert target is local or non-production staging.
4. **SSRF Boundary Enforcement:** Resolve target IP and assert it does not target cloud metadata endpoints (`169.254.169.254`) or unintended internal subnets (`127.0.0.1` unless explicitly authorized as local dev).

---

## Safety Gate
All requests pass through safety boundary checks:
- `Auto-Allowed`: Read-only `GET`, `HEAD`, `OPTIONS` on non-sensitive paths.
- `Approval Required`: Requests touching auth, sessions, or parameters.
- `Manual Only`: Any destructive method (`DELETE`, `DROP`) is strictly blocked.

---

## Execution Steps

1. **Gate Check:** Validate scope in `scope.json`.
2. **Execute Probe:**
   ```bash
   torusguard web-validate --target http://localhost:3000
   ```
3. **Inject Audit Header:** Attach `X-TorusGuard-AuthID: <auth_id>` to all outbound requests.
4. **Validate Security Headers:** Check for CSP, HSTS, X-Content-Type-Options, and CORS configurations.
5. **Audit Cookie Flags:** Verify `HttpOnly`, `Secure`, and `SameSite` on session cookies.
6. **Capture Replay Trace:** Save sanitized trace in `.torusguard/runs/<run_id>/requests.json`.

---

## Credential Redaction
All Bearer tokens, cookies, passwords, and API keys are redacted prior to disk serialization (`Bearer [REDACTED]`).

---

## Living Report Ground Truth
- Always inspect `security_report.md` at workspace root before acting.
- Update finding statuses after completion to eliminate hallucination.

## Safety Constraints
- Max 50 requests per validation session.
- Never test unauthorized domains or third-party APIs.
- Zero state-changing destructive operations.

---

## Output Format
```markdown
🌐 [TorusGuard] Web Validation Completed (AI Assisted)
- Target: <Host URL> | Endpoints Tested: <Count>
- Header Posture: <CSP/HSTS Status> | Cookies: <Flags Status>
- Replay Trace: `.torusguard/runs/<run_id>/requests.json`
Next: Run `/torusguard exploit-check` to confirm exploitability of candidate flaws.
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Scope Bypass Probing** | Sends HTTP requests to arbitrary endpoints without validating `.torusguard/config/scope.json`. | Check `scope.json` and verify TTL before every outbound probe. |
| **Token Exposure in Traces** | Writes unredacted `Authorization: Bearer <secret>` or session cookies to `requests.json`. | Redact all credentials to `[REDACTED]` before saving traces to disk. |
| **SSRF Blindness** | Follows redirects or probes endpoints pointing to AWS/GCP metadata (`169.254.169.254`). | Block private IP ranges and metadata addresses under invariant 9. |
| **Unbounded Flooding** | Launches high-concurrency request loops or stress tests against local dev server. | Enforce rate limiting and cap session probes to maximum 50 requests. |

---

## ✅ Pre-Flight Self-Audit

Before dispatching web probes:
- [ ] Is the target URL verified inside `scope.json` and within valid TTL?
- [ ] Are transparent audit headers (`X-TorusGuard-AuthID`) attached?
- [ ] Are destructive operations (`DELETE`, drops) blocked?
- [ ] Are sensitive tokens and cookies redacted from trace logs?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Check scope.json validity, TTL, and SSRF boundaries for the target URL.
BUILD:   Construct bounded HTTP request with X-TorusGuard-AuthID audit header.
CONFIRM: Redact sensitive tokens and save sanitized trace into requests.json.
```
