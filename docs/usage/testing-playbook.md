# TorusGuard Testing Playbook & Safe Verification Guide

This playbook provides a practical guide for reproducing TorusGuard's validation workflow on your own web applications, staging environments, and educational security labs (such as OWASP Juice Shop).

---

## ⚠️ Fundamental Operating Rules

Before initiating any audit, review these hard constraints:
1. **Authorized Targets Only:** Run runtime probes exclusively against applications you own, locally hosted test containers, or staging environments where you have written permission.
2. **Non-Destructive Testing:** Never supply destructive payloads, excessive rate-fuzzing requests, or data deletion commands.
3. **Guidance, Not Offensive AI:** TorusGuard is an automated guidance and governed remediation assistant—**not** an autonomous offensive penetration testing agent. It verifies candidate weaknesses through passive/bounded queries and formulates surgical code patches.

---

## 🧪 Safe External Testing Lab Setup (Juice Shop + Local Fixtures)

### 1. Lab Preconditions & Environment Setup
We recommend testing against two classes of targets:
- **Internal Educational Fixtures:** Built-in Python reference apps under `examples/python/` (Django, DRF, FastAPI, Flask, SQLAlchemy).
- **External Local Lab Instance:** An intentionally vulnerable web application like **OWASP Juice Shop** running locally via Docker:
  ```bash
  docker run --rm -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
  ```

### 2. Step-by-Step Verification Workflow

#### Step 0: Autonomous Workspace Initialization
Initialize `.torusguard/` in your project root:
```bash
# Terminal CLI
npx torusguard init

# AI Agent Chat
/torusguard init
```
- **Output:** Auto-detects polyglot stack across 16+ languages and 30+ frameworks, activates tailored security rules across 74 rules in 18 families, and configures `.torusguard/config/torusguard.json`.

#### Step 1: Static Code Audit & Living Report Synchronization
Scan repository source files and configuration manifests:
```bash
# Terminal CLI
npx torusguard audit

# AI Agent Chat
/torusguard audit
```
- **Output:** Discovers framework stack, evaluates 74 AST rules, computes line-shift invariant fingerprints, groups findings into systemic root-cause clusters, and synchronizes `security_report.md` at workspace root.
- **Artifacts:** `security_report.md`, `.torusguard/runs/<run-id>/findings.json`, `.torusguard/runs/<run-id>/manifest.json`.

#### Step 2: Governed Remediation Planning
Generate minimal, self-contained remediation bundles for identified issues:
```bash
# Terminal CLI
npx torusguard harden

# AI Agent Chat
/torusguard harden
```
- **Output:** Produces surgical candidate patch bundles adhering to the **Ponytail Protocol** ($\le 35$ additions, $\le 25$ deletions per bundle) with minimal patch plans.

#### Step 3: Surgical Patch Application & Targeted Recheck
Apply bounded fixes using the Human Gate and verify:
```bash
# Terminal CLI
npx torusguard apply [--yes]
npx torusguard recheck

# AI Agent Chat
/torusguard apply
/torusguard recheck
```
- **Output:** Automatically saves pre-apply snapshots to `.torusguard/snapshots/<run_id>/`, applies minimal patches, and differentially re-audits modified files. Transitions findings in `security_report.md` from `APPLIED 🔵` to `RESOLVED 🟢` (or `REGRESSED ❌`). Automatically distills Golden Fix Recipes into `.torusguard/memory/patterns.json`.

#### Step 4: Authorized Runtime Validation (`verify`, `web-validate`, `exploit-check`)
For authorized local or staging instances, validate exploitability in runtime:

1. **Establish Legal Scope (`/torusguard authorize`):**
   Initialize target authorization manifest:
   ```json
   {
     "target_hosts": ["localhost:3000", "127.0.0.1:3000"],
     "allowed_path_prefixes": ["/rest/", "/api/"],
     "forbidden_paths": ["/admin/delete", "/system/reset"],
     "max_requests": 50,
     "valid_from": "2026-09-01T00:00:00Z",
     "valid_until": "2026-09-02T00:00:00Z"
   }
   ```
   Emits `authorization.md` and `scope.json`. Probing fails if this step is omitted.

2. **Crawl & Inspect Web Endpoints (`/torusguard web-validate`):**
   Navigates in-scope routes, validates session cookie flags (`HttpOnly`, `SameSite`), injects transparent audit headers (`X-TorusGuard-AuthID`), and records sanitized requests and responses to `requests.json` and `responses.json`.

3. **Confirm Bounded Exploitability (`/torusguard exploit-check`):**
   Dispatches bounded, single-step verification probes for selected vulnerability classes:
   - **Auth Bypass / IDOR:** Asserts whether protected resources are exposed without valid credentials.
   - **Header Injection:** Checks if untrusted role headers (`X-User-Role`) are reflected into privileged states.
   - **Path Traversal:** Tests for safe directory containment using benign sentinel markers.
   - **Debug Exposure:** Detects active tracebacks or exposed configuration endpoints.

4. **Verify Deterministic Replay (`/torusguard replay`):**
   Replays the recorded trace from `replay.json` to verify that findings reproduce consistently across runs.

---

## 📊 Interpreting Runtime Validation Statuses

Every evaluated runtime probe produces one of five honest classifications:

| Status | Meaning | Action Required |
|---|---|---|
| 🔴 **`Runtime Confirmed`** | Bounded probe indisputably triggered the flaw (e.g., sensitive marker reflected). | Immediate priority remediation. |
| 🟠 **`Runtime Likely`** | Observed HTTP 200/success response without complete canary payload reflection. | Apply remediation bundle and re-test. |
| 🟡 **`Needs Manual Review`** | Ambiguous response (e.g., HTTP 500 error) or complex architectural boundary. | Investigate service logs and out-of-band proxy logic. |
| 🟢 **`Not Reproducible in Scope`** | Access actively blocked by gateway, 401/403 barrier, or input sanitization. | Retain defense-in-depth static fix; no active exploit found. |
| ⚪ **`Blocked by Controls`** | Action halted by safety gate policy (e.g., destructive path or state mutation). | Perform offline static analysis or request human approval. |

---

## 📝 Recording Lab Results

After completing a verification run, document outcomes using the standard run report:
```markdown
# Lab Verification Summary: [Target Name]
- **Target URL:** http://localhost:3000
- **Scope ID:** AUTH-LAB-01 (Valid: 2026-09-01)
- **Static Findings Identified:** 4
- **Runtime Probes Dispatched:** 4
  - Runtime Confirmed: 2 (IDOR, Missing Auth)
  - Not Reproducible: 1 (Guarded by WAF)
  - Blocked by Controls: 1 (Sensitive Delete Route)
- **Remediation Status:** 2 Patches Applied, 2 Confirmed Fixed on Recheck
```
All raw evidence, session cookies, and replay traces are stored in `runs/<run-id>/` for full auditability.
