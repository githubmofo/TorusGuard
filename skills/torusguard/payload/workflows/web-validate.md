---
description: Authorized HTTP probing, token redaction, transparent audit header injection, and replay trace capture.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: validator
lifecycle-phase: Phase 3b (Runtime Web Validation)
required-skills:
  - torusguard-web-validate
scripts-binding:
  - internal/validate/validate.go
  - cmd/torusguard/main.go
---

# /torusguard web-validate — Bounded HTTP Probing & Session Capture

$ARGUMENTS

---

## Objective
Authorized HTTP probing, token redaction, transparent audit header injection, and replay capture against local/staging web applications.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard web-validate [--url <url>]` | Terminal execution of bounded HTTP validator. |
| **Mode B: AI Chat Slash** | `/torusguard web-validate` | Interactive verification of endpoints and security headers. |
| **Mode C: Native MCP Tool** | Scope Guarded Probing | Safe runtime probing guarded by `scope.json` and SSRF boundaries. |

---

## Mandatory Pre-Flight Context Inspection

Inspect authorization parameters and safety limits before sending HTTP requests:
1. **Active Scope (`.torusguard/config/scope.json`):** Assert target host and path are authorized with valid TTL.
2. **SSRF Boundary Enforcement:** Assert target does not resolve to private cloud metadata (`169.254.169.254`).
3. **Sensitive Route Guard:** Ensure destructive endpoints (`DELETE`, account drops) are never called automatically.
4. **Token Redaction Pipeline:** Ensure bearer tokens and session cookies are masked (`Bearer [REDACTED]`).
5. **Request Budget:** Enforce maximum cap of 50 requests per validation session.

---

## Execution Steps

1. **Trigger Web Validation:**
   - **Mode A (CLI):** Run `torusguard web-validate --url http://localhost:3000`.
   - **Mode B (Chat):** Send non-destructive probe and inspect response headers.
2. **Audit Security Headers:** Check CSP, HSTS, X-Content-Type-Options, and CORS headers.
3. **Audit Cookie Flags:** Verify `HttpOnly`, `Secure`, and `SameSite` on session cookies.
4. **Sanitize Traces:** Redact all secrets and save sanitized replay trace.

---

## Output Card Format

```markdown
### 🌐 TorusGuard Web Validation
- **Target Host:** [Host URL]
- **Endpoints Probed:** [Count] routes tested
- **Security Headers:** [CSP / HSTS / CORS status]
- **Cookie Security:** [HttpOnly / Secure / SameSite status]
- **Status:** COMPLETED — non-destructive probe finished
```

---

## Next Steps

1. Run `/torusguard exploit-check` to confirm if reachable flaws constitute verified exploits.
2. Run `/torusguard harden` to build surgical remediation diffs.
