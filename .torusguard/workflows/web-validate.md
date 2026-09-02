# /torusguard web-validate — Authorized HTTP/API Runtime Probing

**Command:** `/torusguard web-validate [target_url]`  
**Primary Agent:** `validator` (`.torusguard/agents/validator.md`)  
**Lifecycle Phase:** Phase 3 (Runtime Validation)

---

## Objective
Dispatch safe, authorized HTTP requests against the live target to capture network evidence, check route reachability, verify headers, inspect session cookie handling, and record request/response traces with automatic token redaction.

---

## Execution Steps

### Step 1: Pre-Flight Scope & Safety Check
1. Read `.torusguard/config/scope.json`.
2. Confirm:
   - Target URL matches an allowed host in `allowed_hosts`.
   - Endpoint path matches an allowed prefix in `allowed_paths`.
   - Endpoint path is NOT in `excluded_paths`.
   - `owner_confirmed` is `true`.
3. If scope check fails, halt with an explicit authorization error.

### Step 2: Safety Gate Classification
Before firing each prospective probe:
- GET / HEAD / OPTIONS $\rightarrow$ `Auto-Allowed`.
- POST with non-destructive canary $\rightarrow$ `Approval Required` (request developer confirmation).
- Destructive methods (DELETE, mass update) $\rightarrow$ `Manual Only` (blocked).

### Step 3: Probe Execution & Trace Capture
1. Add audit tracking headers: `X-TorusGuard-AuthID: <AUTH-ID>`.
2. Execute HTTP probe with configured timeout (default 10s).
3. Capture HTTP status code, headers, and response body preview.
4. **Token Redaction:** Automatically sanitize any `Authorization: Bearer ...`, `Set-Cookie: ...`, `api_key=...`, or password fields into `[REDACTED]`.

### Step 4: Ledger Persistence
Save captured traces to the active run folder:
- `requests.json` & `responses.json`: Full redacted HTTP transaction logs.
- `web-validation.md`: Human-readable summary of executed probes and outcomes.
- `session-notes.md`: Observed cookie flags (`HttpOnly`, `Secure`, `SameSite`).

### Step 5: Output Summary
```markdown
🌐 [TorusGuard] Web Validation Complete
- Target: <Target URL>
- Probes Dispatched: <Count>
- Reachable Endpoints: <Reachable Count>
- Redacted Secrets: <Redacted Count>
- Evidence Log: .torusguard/runs/<run-id>/web-validation.md

Next Step: Run `/torusguard exploit-check` to confirm practical exploitability.
```
