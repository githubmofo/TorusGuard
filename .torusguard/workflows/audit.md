# /torusguard audit — Static Security Code Scan & Clustering

**Command:** `/torusguard audit [target_dir]`  
**Primary Agent:** `auditor` (`.torusguard/agents/auditor.md`)  
**Lifecycle Phase:** Phase 2 (Audit & Cluster)

---

## Objective
Execute deep, rule-based static analysis across the codebase, assign line-shift invariant Stable Fingerprints, cluster findings by underlying root cause, compute 0–100 confidence scores, and package results in an isolated run folder.

---

## Execution Steps

### Step 1: Run Folder Setup
1. Create an isolated run directory: `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/`.
2. Initialize `manifest.json` recording timestamp, git commit hash, and command metadata.

### Step 2: Code Scanning Against Active Rules
1. Load active rule specifications from `.torusguard/rules/active/`.
2. Scan ASTs and source files matching framework patterns:
   - Secret leaks (`TG-SEC-*`)
   - Unsafe SQL concatenation / raw queries (`TG-INPUT-002`)
   - Missing tenant query isolation (`TG-DB-004`)
   - Missing server-side validation / Pydantic boundaries (`TG-INPUT-001`)
   - Insecure session cookies & CORS credentials (`TG-AUTH-004`, `TG-PLATFORM-001`)
   - Client-side database credentials & public admin SDKs (`TG-DB-001`, `TG-DB-003`)

### Step 3: Fingerprinting & Clustering
1. Compute invariant `primaryLocationLineHash` and stable finding IDs.
2. Group related findings by root cause into systemic clusters:
   - `cluster-tenant-isolation`
   - `cluster-auth-barrier`
   - `cluster-raw-sql-sink`
   - `cluster-secret-exposure`

### Step 4: Confidence Scoring (0–100 Rubric)
Evaluate each finding across the 5 rubric dimensions:
- Evidence Quality (AST match = 35)
- Reproduction Success (Deterministic test = 25)
- Independent Confirmations (Multi-file = 15)
- Environmental Clarity (Direct route = 15)
- Manual Review Status (Unreviewed = 0)

### Step 5: Artifact Generation
Write the following artifacts to the run folder:
- `findings.md`: Detailed card-style findings.
- `summary.md`: Executive summary and cluster breakdown.
- `manifest.json`: Status metrics and finding counts.

### Step 6: Present Executive Findings
Output executive posture (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Ready`), metric table, and top prioritized findings.
