# /torusguard authorize — Legal Scope & Target Ownership Gate

**Command:** `/torusguard authorize [target_url]`  
**Primary Agent:** `reviewer` (`.torusguard/agents/reviewer.md`)  
**Lifecycle Phase:** Phase 0 (Legal & Scope Gate)

---

## Objective
Establish clear, non-negotiable target ownership, scope limits, permitted path prefixes, and time-to-live (TTL) boundaries before any live runtime validation is permitted.

---

## Execution Steps

### Step 1: Clarifying Intent & Target Ownership
Prompt the operator to confirm:
1. **Target Identification:**
   - Hostname or IP of the running application (e.g., `http://localhost:8000`).
2. **Authority Confirmation:**
   - Confirm explicit target ownership or written penetration testing authorization.
3. **Scope Type:**
   - `source_code_only` (No live probes permitted).
   - `source_and_runtime` (Bounded HTTP/browser probes enabled).
4. **Permitted Endpoints:**
   - Allowed path prefixes (e.g., `/api/*`, `/auth/*`).
   - Forbidden / excluded paths (e.g., `/admin/delete*`, `/system/shutdown*`).
5. **Authorization Duration:**
   - Valid window in hours (default: 24h).

### Step 2: Write Scope File
Serialize the confirmed boundaries into `.torusguard/config/scope.json`:
```json
{
  "authorization": {
    "target": "http://localhost:8000",
    "owner_confirmed": true,
    "scope_type": "source_and_runtime",
    "allowed_hosts": ["localhost", "127.0.0.1"],
    "allowed_paths": ["/api/*", "/auth/*"],
    "excluded_paths": ["/admin/delete*"],
    "duration_hours": 24,
    "authorized_at": "<ISO-TIMESTAMP>",
    "authorized_by": "<USER_ID>"
  }
}
```

### Step 3: Authorization Record Artifact
Write `authorization.md` in the active run folder using `.torusguard/templates/authorization.template.md`.

### Step 4: Summary Output
```markdown
🔒 [TorusGuard] Authorization Scope Established
- Target: <Target URL>
- Owner Confirmed: YES
- Allowed Paths: /api/*, /auth/*
- Excluded Paths: /admin/delete*
- Valid Until: <Expiry Timestamp>

Runtime commands (`/torusguard web-validate`, `/torusguard exploit-check`) are now authorized.
```
