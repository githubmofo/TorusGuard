---
name: torusguard-audit
description: Execute deep static security code audit — AST scanning, stable fingerprinting, root-cause clustering, and 0–100 confidence scoring against active TG-* rules.
version: 0.9.2
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Audit — Static Code Analysis & Finding Clustering

## Objective
Execute thorough, rule-based static analysis across the codebase, assign line-shift invariant Stable Finding Fingerprints, group findings by underlying root cause, compute objective 0–100 confidence scores, and persist structured findings into an isolated run folder.

---

## Execution Steps

### Step 1: Run Directory Setup
Create a dedicated run folder under `.torusguard/runs/` using `python .torusguard/scripts/run_manager.py --action init --type audit` or convention `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/`.
Initialize `manifest.json` recording timestamp, git commit, project stack, and command options.

### Step 2: Load Active Rules & Context
Read active rules from `.torusguard/rules/active/`. If empty, prompt user to run `/torusguard init`.
Read project config from `.torusguard/config/torusguard.json` to obtain severity thresholds.

### Step 3: Source Code Scanning Against Active Rules
Scan project files matching framework patterns:
- **Secret & Credential Leaks (`TG-SEC-*`)**:
  - Hardcoded API keys, JWT secrets, Stripe secret keys (`sk_live_...`), private keys (`-----BEGIN PRIVATE KEY-----`).
- **SQL & Query Injection (`TG-INPUT-002`, `TG-DB-*`)**:
  - String formatting or raw concatenation into SQL queries:
    - Python: `cursor.execute(f"SELECT ... WHERE id = {id}")` or `db.execute(text(f"..."))`.
    - Node: `db.query(\`SELECT ... WHERE id = ${id}\`)` or `prisma.$queryRawUnsafe(...)`.
- **Tenant Isolation Gaps (`TG-DB-004`)**:
  - Database queries missing tenant ID filters in multi-tenant models:
    - `Invoice.objects.all()` or `Invoice.objects.get(id=id)` without tenant scope.
- **Input Validation Deficits (`TG-INPUT-001`)**:
  - Endpoints accepting arbitrary request dictionaries without schema boundaries:
    - FastAPI endpoint with raw `Request` body without Pydantic model.
    - Express route reading `req.body` directly without Zod parsing.
- **Session & Cookie Security (`TG-AUTH-004`, `TG-PLATFORM-001`)**:
  - Missing `HttpOnly`, `SameSite=Lax/Strict`, or `Secure` flags on auth cookies; overly permissive CORS `Access-Control-Allow-Origin: *` with credentials.
- **Client-Side Secret Exposure (`TG-DB-001`, `TG-CLIENT-*`)**:
  - Service role keys or database admin clients imported in frontend components.

### Step 4: Line-Shift Invariant Fingerprinting
For each finding, compute:
1. `rule_id`: Matching rule ID (e.g., `TG-INPUT-002`).
2. `file_path`: Relative file path from repo root.
3. `primaryLocationLineHash`: SHA-256 hash of the normalized 3 surrounding lines of AST context.
4. `finding_id`: Unique identifier formatted as `TG-<RULE_ID>-<SLUG>`.

### Step 5: Root-Cause Clustering
Cluster related findings sharing an underlying architectural cause:
- `cluster-tenant-isolation`: Missing tenant scoping across database query layer.
- `cluster-raw-sql-sink`: Unescaped input flowing into database execute functions.
- `cluster-auth-barrier`: Unprotected route groups or missing authentication middleware.
- `cluster-secret-exposure`: Leaked environment variables or hardcoded constants.

### Step 6: 0–100 Confidence Scoring
Score each finding across the 5 rubric dimensions detailed below.

### Step 7: Write Artifacts
Persist all generated data in `.torusguard/runs/<run-id>/`:
- `findings.md`: Complete card-style presentation of each finding.
- `summary.md`: Executive summary with posture badges and metric breakdown.
- `manifest.json`: Run status, finding counts, and cluster mapping.

---

## Confidence Scoring Rubric (5-Factor 0–100)

| Factor | Max Pts | Criteria & Evaluation |
| :--- | :---: | :--- |
| **1. Evidence Quality** | **35** | • **35 pts**: Exact AST source match demonstrating complete untrusted data flow into sink.<br>• **20 pts**: Regex or pattern heuristic match with confirmed code presence.<br>• **10 pts**: Indirect indicator (e.g., outdated dependency or suspicious import). |
| **2. Reproduction Success** | **25** | • **25 pts**: Deterministic unit test or runtime trace reproduces the vulnerability.<br>• **15 pts**: Partial reproduction or simulated code path confirmed.<br>• **0 pts**: Purely static hypothesis with no reproduction attempt. |
| **3. Independent Confirmations** | **15** | • **15 pts**: Flaw pattern corroborated across 3 or more distinct source files.<br>• **10 pts**: Flaw pattern corroborated across 2 distinct files.<br>• **5 pts**: Single isolated occurrence in the codebase. |
| **4. Environmental Clarity** | **15** | • **15 pts**: Direct, clearly mapped framework route with explicit configuration.<br>• **8 pts**: Minor middleware or proxy ambiguity; deployment context partially clear.<br>• **0 pts**: Highly complex dynamic routing, custom lambdas, or unknown gateway filters. |
| **5. Manual Review Status** | **10** | • **10 pts**: Human security engineer has explicitly reviewed and verified finding.<br>• **5 pts**: Agent consensus / secondary review completed.<br>• **0 pts**: Automated first-pass check only. |

**Classification Bands:**
- **`90–100` (`Confirmed`)**: Indisputable proof with code citation or deterministic trace.
- **`70–89` (`High Confidence`)**: Strong direct indicators; prioritized remediation.
- **`50–69` (`Medium Confidence`)**: Probable flaw; runtime confirmation recommended.
- **`< 50` (`Needs Review`)**: Architectural ambiguity or potential delegated control.

---

## Finding Card Format
```markdown
### [TG-DB-004] Missing Tenant Isolation in /invoices/
- **Severity**: High | **Confidence**: 90/100 (Confirmed)
- **File**: `apps/invoices/views.py:42`
- **Cluster**: `cluster-tenant-isolation`
- **Fingerprint**: `sha256:7f3b...`
- **Vulnerability**: Direct query on `Invoice.objects.get(id=id)` without tenant filter.
- **Evidence**: AST demonstrates route parameter `id` flows directly into unscoped ORM query.
- **Remediation Plan**: Scope query using `Invoice.objects.filter(tenant=request.user.tenant, id=id)`.
```

---

## Safety Constraints
- Strictly read-only; no code files are modified during an audit.
- Exclude build directories (`dist/`, `build/`, `.venv/`, `node_modules/`).
- Redact secrets before saving to `findings.md`.

---

## Output Format
```markdown
🛡️ [TorusGuard] Static Code Audit Completed
- Run ID: run-YYYYMMDD-HHMMSS-audit
- Files Scanned: <Count>
- Total Findings: <Count> (<Critical> Critical · <High> High · <Med> Med)
- Systemic Clusters: <Count> Clusters Identified
- Posture: 🔴 ACTION REQUIRED (or 🟡 WARNINGS / 🟢 SECURE)

Next Step: Run `/torusguard harden` to formulate surgical remediation bundles.
```
