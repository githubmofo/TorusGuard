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
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Mandatory Pre-Flight Context Inspection

Before registering runtime authorization boundaries, you MUST inspect:

1. **Active Project Config (`.torusguard/config/torusguard.json`)** → Confirm the project was initialized.
2. **Current Scope Record (`.torusguard/config/scope.json`)** → Inspect existing targets, allowed paths, and TTL expiration timestamps.
3. **Target Environment Sanity** → Verify that target URLs are non-production staging, localhost, or ephemeral containers (`localhost`, `127.0.0.1`, `*.staging.*`, `*.test`).
4. **Destructive Method Guard** → Ensure state-changing operations (`DELETE`, `PUT`, bulk mutations) require explicit `allow_destructive: true` flags.

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## When to Use /torusguard authorize

| Use `/torusguard authorize` when... | Use something else when... |
| :--- | :--- |
| Preparing to run live API / HTTP checks | Performing static-only analysis → `/torusguard audit` |
| Authorizing new staging host or port | Viewing current authorization → `/torusguard status` |
| Updating allowed path prefixes or rate limits | Generating remediation patch → `/torusguard harden` |
| Setting an expiration TTL on live testing | Running full pipeline → `/torusguard full` |

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Execution Steps (Fixed Order)

### Phase 1 — Prompt & Capture Authorization Parameters
Capture the mandatory legal scope parameters:
- **Target URL / Host**: e.g., `http://127.0.0.1:8000` or `https://staging.internal.net`
- **Allowed Path Prefixes**: e.g., `["/api/v1/", "/auth/", "/users/"]`
- **Forbidden Paths**: e.g., `["/admin/delete", "/system/reboot", "/payments/capture"]`
- **Allowed HTTP Methods**: Default to `["GET", "HEAD", "OPTIONS"]`. Require explicit approval for `["POST", "PUT"]`.
- **Max Requests Per Second**: Default to `5 req/sec` to prevent DoS.
- **Authorization Expiration (TTL)**: Default to `4 hours`.

### Phase 2 — Target Ownership & Environment Validation
1. Verify target host does not belong to third-party providers (AWS, Stripe, Google, Twilio APIs).
2. Validate against `.torusguard/schemas/authorization.schema.json`.
3. Check for staging/development markers (`localhost`, `.local`, `staging`, test headers).

### Phase 3 — Safety Gate Configuration & Scope Persistence
1. Run the safety gate script to validate parameters:
   ```bash
   python .torusguard/scripts/safety_gate.py --validate-scope .torusguard/config/scope.json
   ```
2. Write authorized parameters to `.torusguard/config/scope.json`.
3. Archive signed authorization record into current run folder:
   - Path: `.torusguard/runs/<active-run>/authorization.md`

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Failure Recovery & Cascade Rules

```
Target URL invalid:       HALT — Prompt user for RFC-compliant URL (scheme + host + port)
Third-party domain:       HALT — Refuse unauthorized target with legal boundary warning
TTL expired:              HALT — Require operator re-authorization via /torusguard authorize
Schema validation error:  HALT — Print exact JSON schema discrepancy and reject
```

**Hard limit: Zero bypasses.** Runtime tools (`web-validate`, `exploit-check`) will strictly refuse to execute if `scope.json` is invalid, expired, or absent.

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Hallucination Guard

```
❌ Never fabricate an authorization record without explicit operator input
❌ Never permit wildcard (*) allowed_hosts on public domain names
❌ Never authorize DELETE or DROP commands under automated execution
❌ Never set TTL greater than 24 hours without human confirmation
```

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Runtime Scope Authorized & Locked
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target Host:        [e.g., http://localhost:8000]
Allowed Prefixes:   [/api/v1/, /auth/]
Forbidden Paths:    [/admin/delete, /billing/charge]
Allowed Methods:    [GET, HEAD, POST]
Rate Cap:           [5 req/sec (burst: 10)]
TTL Expiration:     [Timestamp, 4 hours from now]
Scope File:         .torusguard/config/scope.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: 🟢 AUTHORIZED FOR BOUNDED RUNTIME VERIFICATION
Next Step: Run `/torusguard web-validate` or `/torusguard exploit-check`.
```

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Scope locked and verified | → `/torusguard web-validate` to probe endpoints |
| Specific vulnerability found | → `/torusguard exploit-check` to confirm exploitability |
| Static analysis needed first | → `/torusguard audit` |
