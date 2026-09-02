---
name: torusguard-authorize
description: Authorize target host and path boundaries for safe runtime probing and exploitability verification.
version: 0.9.2
workflow: .torusguard/workflows/authorize.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/safety_gate.py
---

# TorusGuard Authorize — Scope Governance & Safety Gate

## Objective
Establish an auditable, legally bounded authorization scope before executing any runtime HTTP probing or exploitability verification. Ensures testing is restricted to staging/local environments with verified ownership and strict path allowlists.

---

## Execution Steps

### Step 1: Collect Scope Parameters
Capture the mandatory authorization parameters:
- `target_host`: Target URL (e.g., `http://127.0.0.1:8000`, `http://localhost:3000`). Must include scheme and port.
- `allowed_prefixes`: Array of path prefixes permitted for probing (e.g., `["/api/v1/", "/auth/"]`).
- `forbidden_paths`: Explicitly blocked paths (e.g., `["/admin/delete", "/payments/charge"]`).
- `allowed_methods`: HTTP verbs permitted (Default: `["GET", "HEAD", "OPTIONS"]`; write verbs require explicit approval).
- `rate_limit_per_second`: Maximum request throughput (Default: `5 req/s`).
- `ttl_hours`: Authorization validity duration (Default: `4 hours`, maximum `24 hours`).

### Step 2: Safety Boundary Validation
Verify parameters against strict safety constraints:
1. Target must NOT match public third-party services (AWS, Stripe, Twilio, Google APIs).
2. Target must resolve to localhost, private IP (`10.*`, `172.16-31.*`, `192.168.*`), or a designated staging domain.
3. Validate parameters conform to `.torusguard/schemas/authorization.schema.json`.

### Step 3: Run Safety Gate Validator
Execute the safety gate validator:
```bash
python .torusguard/scripts/safety_gate.py --validate-scope .torusguard/config/scope.json
```

### Step 4: Write Scope File
Write `.torusguard/config/scope.json`:
```json
{
  "target_host": "http://127.0.0.1:8000",
  "allowed_prefixes": ["/api/v1/", "/auth/"],
  "forbidden_paths": ["/admin/delete", "/system/reboot"],
  "allowed_methods": ["GET", "HEAD", "POST"],
  "rate_limit_per_second": 5,
  "ttl_expiration": "2026-09-02T18:00:00Z",
  "allow_destructive": false,
  "authorized_by": "developer"
}
```

### Step 5: Archive Authorization Record
Write `.torusguard/runs/<active-run>/authorization.md` capturing the signed scope record for auditability.

---

## Safety Constraints
- **Zero Wildcard Hosts**: Never permit `*` as the target host.
- **Production Protection**: Strictly reject production domains without multi-party confirmation.
- **TTL Enforcement**: Authorization expires automatically; runtime tools must refuse expired scopes.
- **Destructive Method Guard**: `DELETE`, `DROP`, and bulk-update actions are strictly prohibited under automated testing.

---

## Output Format
```markdown
🛡️ [TorusGuard] Runtime Scope Authorized & Locked
- Target Host: <target_host>
- Allowed Prefixes: <allowed_prefixes>
- Forbidden Paths: <forbidden_paths>
- Allowed Verbs: <allowed_methods>
- Rate Cap: <rate_limit_per_second> req/s
- TTL Expiration: <ttl_expiration>
- Scope File: .torusguard/config/scope.json

Status: 🟢 AUTHORIZED FOR BOUNDED RUNTIME VERIFICATION
Next Step: Run `/torusguard web-validate` or `/torusguard exploit-check`.
```
