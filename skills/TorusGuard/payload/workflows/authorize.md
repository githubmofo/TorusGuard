---
description: Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: reviewer
lifecycle-phase: Phase 1 (Authorization Gate)
required-skills:
  - torusguard-authorize
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# /torusguard authorize — Legal Scope & Safety Gate

$ARGUMENTS

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement.

---

## Mandatory Pre-Flight Context Inspection

Inspect authorization parameters and environment safety before executing:
1. **Config Record (`.torusguard/config/torusguard.json`):** Assert repository is initialized.
2. **Current Scope (`.torusguard/config/scope.json`):** Inspect active allowed targets, paths, and TTL expiry.
3. **Environment Classification:** Assert target is local or staging (`localhost`, `127.0.0.1`, `*.local`, `*.staging.*`). Production targets require explicit approval.
4. **Destructive Guard:** Ensure state-changing operations (`DELETE`, bulk drops) remain blocked by default.
5. **Ownership Proof:** Verify target ownership token or local process binding.
6. **TTL Window:** Ensure authorization window does not exceed 24 hours.

---

## When to Use /torusguard authorize

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Preparing for live HTTP probes or API validation | Run `/torusguard authorize` |
| Updating allowed hosts, path prefixes, or rate limits | Run `/torusguard authorize` |
| Static-only security audit | Skip authorize; run `/torusguard audit` |
| Checking active legal scope status | Run `/torusguard status` |
| Expired authorization window | Re-run `/torusguard authorize` |

---

## Execution Steps

1. **Capture Scope Parameters:** Collect target URL, allowed paths, forbidden prefixes, and max request budget.
2. **Validate Host Ownership:** Verify target is local or matches authorized test domains.
3. **Invoke Safety Gate:**
   ```bash
   python .torusguard/scripts/safety_gate.py check --url <target_url>
   ```
4. **Write Scope File (`.torusguard/config/scope.json`):** Save authorized targets, valid TTL timestamp, and request rate caps.
5. **Confirm Scope Binding:** Verify `.torusguard/config/scope.json` parses as valid JSON against schema.

---

## Failure Recovery

- **Unreachable Host:** Verify local server is running on the specified port.
- **Production Target Warning:** If target resolves to an external production host, halt and request operator override.
- **Malformed JSON:** Re-initialize `scope.json` from `.torusguard/schemas/auth-boundary.schema.json`.
- **Halt Trigger:** Abort immediately if user provides wildcard target (`*`) or third-party domain.

---

## Hallucination Guard

- ❌ Never proceed with runtime probing without an explicit, valid `.torusguard/config/scope.json`.
- ❌ Never authorize destructive HTTP methods (`DELETE`, `DROP`) under default non-destructive policy.
- ✅ Always validate targets through `.torusguard/scripts/safety_gate.py`.

---

## Output Card Format

```markdown
### 🔒 TorusGuard Authorization Gate
- **Target URL:** [Target Host or URL]
- **Environment:** [Localhost / Staging / Container]
- **Allowed Paths:** [Path prefixes or all authorized]
- **Rate Limit:** [Max requests / concurrency limit]
- **Scope File:** `.torusguard/config/scope.json`
- **Status:** AUTHORIZED — ready for `/torusguard web-validate`
```

---

## Next Steps

1. Run `/torusguard audit` to scan codebase for AST security vulnerabilities.
2. Run `/torusguard web-validate` to begin safe, authorized endpoint validation.
