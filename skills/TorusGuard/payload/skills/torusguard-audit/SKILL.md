---
name: torusguard-audit
description: Static AST scanning, memory pattern boosting, and 0–100 confidence scoring.
version: 1.0.0
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Audit — Static Code Analysis & Memory Scanning

## Objective
Execute static AST analysis, query memory context, compute 0–100 confidence scores with memory boosts, and record findings to runs and memory.

---

## Execution Steps

1. **Run Setup:** Initialize `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/` via `run_manager.py`.
2. **Context & Rules:** Load `.torusguard/memory/context.json` for patterns and false positives. Load rules from `.torusguard/rules/active/`.
3. **AST Scan Sinks:** Match files against active rules:
   - `TG-SEC-*`: Secrets and API keys.
   - `TG-INPUT-*`: SQL injection, unvalidated input.
   - `TG-DB-*`: Unscoped tenant queries (`Model.get(id=id)`).
   - `TG-AUTH-*`: Insecure cookies, open CORS.
   - `TG-CLIENT-*`: Client bundle secret leaks.
4. **Stable Fingerprinting:** Compute SHA-256 hash of surrounding AST context.
5. **Root-Cause Clustering:** Group findings by causal sink (`cluster-tenant-isolation`).
6. **Scoring:** Calculate 0–100 score via `finding_scorer.py` (applies memory boost/suppression).
7. **Write Artifacts:** Save `findings.json` and sync findings to memory engine.

---

## Confidence Scoring Rubric
- **1. Evidence (35):** AST flow (35), regex sink (20), heuristic (10).
- **2. Reproduction (25):** Automated test (25), simulated (15), hypothesis (0).
- **3. Corroboration (15):** >=3 files (15), 2 files (10), single (5).
- **4. Environment (15):** Explicit route (15), ambiguous (8), unknown (0).
- **5. Review Status (10):** Human confirmed (10), agent verified (5), auto (0).
- **Memory Modifier:** False positive (-30), regression (+15), recurring (+10).
- **Bands:** 90–100 (`Confirmed`), 70–89 (`High`), 50–69 (`Medium`), <50 (`Review`).

---

## Finding Card Format
```markdown
### [TG-DB-004] Missing Tenant Scoping in /invoices/
- **Severity**: High | **Confidence**: 90/100 (Confirmed) | **Memory Boost**: +10
- **File**: `views.py:42` | **Cluster**: `cluster-tenant-isolation`
- **Remediation**: Apply `.filter(tenant=request.user.tenant)`.
```

---

## Safety Constraints
- Read-only analysis; zero code modifications during audit.
- Exclude build directories (`node_modules/`, `.venv/`, `dist/`).
- Redact secrets before saving to `findings.md`.

---

## Output Format
```markdown
🛡️ [TorusGuard] Static Code Audit Completed
- Run ID: run-YYYYMMDD-HHMMSS-audit | Files: <Count> | Findings: <Count>
- Clusters: <Count> identified | Memory Patterns Applied: <Count>
Next: Run `/torusguard harden` to formulate surgical fixes.
```
