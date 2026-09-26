---
name: torusguard-authorize
description: Register and validate runtime target authorization boundaries — scope boundaries, ownership proofs, TTL expiration, and Safety Gate enforcement.
version: 2.0.0
workflow: .torusguard/workflows/authorize.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Authorize — Legal Scope & Safety Gate Registration

## Objective
Define and validate legal runtime authorization boundaries, verify target ownership, enforce maximum rate limits, and persist a cryptographically auditable `.torusguard/config/scope.json`.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard authorize` | Interactive boundary setup, generates cryptographically signed scope tokens. |
| **Mode B: AI Chat Slash** | `/torusguard authorize` | Conversational parameter collection, validates host ownership and environment. |
| **Mode C: Native MCP Tool**| — | Administrative gatekeeper ensuring strict safety boundaries before probes. |

---

## Execution Steps

1. **Capture Scope Parameters:** Collect target host URL, allowed path prefixes, forbidden prefixes, and session TTL.
2. **Validate Environment:** Assert target is local (`localhost`, `127.0.0.1`) or staging (`*.staging.*`). Block production targets without explicit cryptographic override.
3. **Verify Host Ownership:** Confirm ownership token or local process socket binding.
4. **Invoke Safety Gate:**
   ```bash
   torusguard authorize --url <target_url>
   ```
5. **Write Scope Record:** Persist authorized targets, rate limits, and expiration timestamp into `.torusguard/config/scope.json`.
6. **Validate Schema:** Confirm `scope.json` adheres to `auth-boundary.schema.json`.

---

## Living Report Ground Truth
- Always inspect `security_report.md` at workspace root before acting.
- Update finding statuses after completion to eliminate hallucination.

## Safety Constraints
- Never authorize wildcard hosts (`*`) or third-party domains.
- State-changing destructive actions (`DELETE`, bulk drops) are disabled by default.
- Set strict TTL (default 4 hours, maximum 24 hours).
- Fail-Closed Cryptography: Authorization token generation must panic on entropy failure. No hardcoded fallback tokens are permitted.

---

## Output Format
```markdown
🔒 [TorusGuard] Target Scope Authorized (AI Assisted)
- Target Host: <Host URL> | Environment: <Local / Staging>
- Allowed Paths: <Prefixes> | Rate Limit: <Max Req/sec>
- Expiration TTL: <Timestamp>
- Scope File: `.torusguard/config/scope.json`
Next: Run `/torusguard web-validate` to begin safe runtime probing.
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Wildcard Scope Authorization** | Accepts `*` or wide domain patterns like `*.com`, enabling unbounded network probes. | Strictly enforce exact domain/port matching (`http://localhost:3000`, `https://staging.internal`). |
| **Infinite TTL** | Omits `expires_at` or sets multi-year expiration timestamps. | Enforce TTL bound of maximum 24 hours (default 4 hours) to prevent lingering test permissions. |
| **Production Probe Authorization** | Authorizes live production domains without ownership challenge or manual user confirmation. | Reject production domains unless explicit cryptographic ownership challenge succeeds. |
| **Destructive Method Inclusion** | Allows `DELETE`, `PUT /bulk`, or `DROP` routes in `allowed_paths`. | Blacklist state-altering destructive paths; confine runtime validation to safe, non-destructive probes. |

---

## ✅ Pre-Flight Self-Audit

Before authorizing any runtime scope:
- [ ] Is the target host local (`localhost`, `127.0.0.1`) or an authorized staging environment?
- [ ] Are wildcards (`*`) strictly rejected?
- [ ] Is the TTL strictly bounded (≤24 hours)?
- [ ] Are destructive routes and SQL operations explicitly forbidden?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Check target URL, environment, and ownership proof against safety boundaries.
BUILD:   Construct scope.json record with explicit allowed paths and TTL bounds.
CONFIRM: Validate JSON against auth-boundary.schema.json and persist to .torusguard/config/scope.json.
```
