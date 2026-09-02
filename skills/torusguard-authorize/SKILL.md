---
name: torusguard-authorize
description: Register and validate runtime target authorization boundaries — scope boundaries, ownership proofs, TTL expiration, and Safety Gate enforcement.
version: 0.9.2
workflow: .torusguard/workflows/authorize.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Authorize — Legal Scope & Safety Gate Registration

## Objective
Define and validate legal runtime authorization boundaries, verify target ownership, enforce maximum rate limits, and persist a cryptographically auditable `.torusguard/config/scope.json`.

---

## Execution Steps

1. **Capture Scope Parameters:** Collect target host URL, allowed path prefixes, forbidden prefixes, and session TTL.
2. **Validate Environment:** Assert target is local (`localhost`, `127.0.0.1`) or staging (`*.staging.*`). Block production targets without explicit override.
3. **Verify Host Ownership:** Confirm ownership token or local process socket binding.
4. **Invoke Safety Gate:**
   ```bash
   python .torusguard/scripts/safety_gate.py check --url <target_url>
   ```
5. **Write Scope Record:** Persist authorized targets, rate limits, and expiration timestamp into `.torusguard/config/scope.json`.
6. **Validate Schema:** Confirm `scope.json` adheres to `auth-boundary.schema.json`.

---

## Safety Constraints
- Never authorize wildcard hosts (`*`) or third-party domains.
- State-changing destructive actions (`DELETE`, bulk drops) are disabled by default.
- Set strict TTL (default 4 hours, maximum 24 hours).

---

## Output Format
```markdown
🔒 [TorusGuard] Target Scope Authorized
- Target Host: <Host URL> | Environment: <Local / Staging>
- Allowed Paths: <Prefixes> | Rate Limit: <Max Req/sec>
- Expiration TTL: <Timestamp>
- Scope File: `.torusguard/config/scope.json`
Next: Run `/torusguard web-validate` to begin safe runtime probing.
```
