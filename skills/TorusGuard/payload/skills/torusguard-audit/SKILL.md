---
name: torusguard-audit
description: Static security AST scanning, stable fingerprinting, root-cause clustering, and 0–100 confidence scoring.
version: 0.9.2
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Audit — Static Code Analysis & Finding Clustering

## Objective
Execute static analysis across ASTs, generate line-shift invariant fingerprints, group findings into root causes, compute 0–100 confidence scores, and persist findings to `.torusguard/runs/`.

---

## Execution Steps

1. **Setup Run Directory:** Initialize `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/` via `run_manager.py`.
2. **Load Active Rules:** Load rules from `.torusguard/rules/active/` and thresholds from `torusguard.json`.
3. **AST Scan Sinks:** Match files against active rules:
   - `TG-SEC-*`: Leaked API keys, secrets.
   - `TG-INPUT-*`: Unescaped SQL or unvalidated payloads.
   - `TG-DB-*`: Unscoped queries omitting tenant filters (`Model.get(id=id)`).
   - `TG-AUTH-*`: Missing `HttpOnly`/`Secure` flags; open CORS.
   - `TG-CLIENT-*`: Admin credentials in client bundles.
4. **Stable Fingerprinting:** Compute SHA-256 hash of normalized 3 surrounding AST lines.
5. **Root-Cause Clustering:** Group findings by root cause (`cluster-tenant-isolation`, `cluster-raw-sql-sink`).
6. **Confidence Scoring:** Calculate 0–100 score across 5-factor rubric via `finding_scorer.py`.
7. **Write Run Artifacts:** Persist `findings.md`, `findings.json`, and `summary.md`.

---

## Confidence Scoring Rubric
- **1. Evidence (35):** AST flow (35), regex match (20), indirect (10).
- **2. Reproduction (25):** Deterministic test (25), simulated (15), hypothesis (0).
- **3. Corroboration (15):** >=3 files (15), 2 files (10), single (5).
- **4. Environment (15):** Explicit route (15), minor ambiguity (8), unknown (0).
- **5. Review Status (10):** Human verified (10), agent consensus (5), auto (0).
- **Bands:** 90–100 (`Confirmed`), 70–89 (`High`), 50–69 (`Medium`), <50 (`Review`).

---

## Finding Card Format
```markdown
### [TG-DB-004] Missing Tenant Scoping in /invoices/
- **Severity**: High | **Confidence**: 90/100 (Confirmed)
- **File**: `views.py:42` | **Cluster**: `cluster-tenant-isolation`
- **Evidence**: Unscoped query leaks records.
- **Remediation**: Scope by `tenant=request.user.tenant`.
```

---

## Safety Constraints
- Read-only execution; zero code modifications.
- Exclude build folders (`node_modules/`, `.venv/`, `dist/`).
- Redact secrets before saving to `findings.md`.

---

## Output Format
```markdown
🛡️ [TorusGuard] Static Code Audit Completed
- Run ID: run-YYYYMMDD-HHMMSS-audit | Files: <Count> | Findings: <Count>
- Clusters: <Count> identified | Posture: ACTION REQUIRED
Next: Run `/torusguard harden` to formulate surgical fixes.
```
