---
description: Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: auditor
lifecycle-phase: Phase 2 (Static Audit & Clustering)
required-skills:
  - torusguard-audit
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# /torusguard audit — Static Security Code Scan & Clustering

$ARGUMENTS

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Mandatory Pre-Flight Context Inspection

Before launching a full static codebase audit, you MUST inspect:

1. **Workspace Health & Init Status (`.torusguard/config/torusguard.json`)** → Confirm project initialization. If missing, run `/torusguard init` first.
2. **Active Rules Directory (`.torusguard/rules/active/`)** → Ensure tailored rule definitions exist for the target framework.
3. **Repository Cleanliness & Exclusions** → Verify that virtual environments (`.venv/`, `env/`), build artifacts (`dist/`, `build/`, `.next/`), and dependencies (`node_modules/`, `vendor/`) are excluded from AST parsing.
4. **Isolated Run Directory Allocation** → Generate a unique run directory `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/` to prevent cross-run pollution.

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## When to Use /torusguard audit

| Use `/torusguard audit` when... | Use something else when... |
| :--- | :--- |
| First scan of a repository or feature branch | Project not yet initialized → `/torusguard init` |
| Before submitting code for pull request review | Checking live API runtime exploitability → `/torusguard exploit-check` |
| Auditing architectural patterns & security flaws | Generating surgical remediation diffs → `/torusguard harden` |
| Systemic clustering across multiple files | Verifying existing patches → `/torusguard recheck` |

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Execution Steps (Fixed Order)

### Phase 1 — Initialize Run Folder
Create a new timestamped run folder via `run_manager.py`:
```bash
python .torusguard/scripts/run_manager.py --action init --type audit
```
Output: `.torusguard/runs/run-<run-id>/` initialized with `manifest.json`.

### Phase 2 — AST & Pattern Scanning Against Active Rules
Scan codebase against all active rules in `.torusguard/rules/active/`:
- **Secrets & Credentials (`TG-SEC-*`)**: Hardcoded API keys, JWT tokens, AWS secrets, connection strings.
- **Injection Flaws (`TG-INPUT-*`)**: Unsanitized raw SQL (`cursor.execute(f"...")`), command injections, template injection.
- **Tenant & Scoping Flaws (`TG-DB-004`)**: Unscoped queries (`Model.objects.all()`, `db.query(User).filter_by(id=id)` without tenant filter).
- **Authentication & Sessions (`TG-AUTH-*`)**: Missing `@login_required`, weak password hashing, missing cookie `HttpOnly`/`SameSite`.
- **API Boundaries (`TG-INPUT-001`)**: Unvalidated request payloads, missing Pydantic schemas, unchecked body inputs.

### Phase 3 — Invariant Fingerprinting & Identity Preservation
For each finding, compute:
- **`finding_id`**: Deterministic format `TG-<RULE_ID>-<SLUG>`.
- **`primaryLocationLineHash`**: SHA-256 hash of surrounding 3 lines of AST context, ensuring invariance across minor line shifts.

### Phase 4 — Systemic Root-Cause Clustering
Group individual findings sharing an underlying root cause into clusters:
- `cluster-tenant-isolation`: Multiple endpoints missing tenant context.
- `cluster-raw-sql-sink`: Repeated string interpolation in data layer.
- `cluster-unvalidated-boundary`: Multiple endpoints accepting raw dictionaries without schemas.

### Phase 5 — Objective 0–100 Confidence Scoring
Calculate confidence using `finding_scorer.py`:
```bash
python .torusguard/scripts/finding_scorer.py --evidence AST_MATCH --repro TEST_REPRO --independent MULTI_FILE --clarity DIRECT_ROUTE
```
- Score $\ge 90$: **Confirmed**
- Score $70–89$: **High Confidence**
- Score $50–69$: **Medium Confidence**
- Score $< 50$: **Needs Review**

### Phase 6 — Persist Run Artifacts
Write findings to `.torusguard/runs/<run-id>/`:
- `findings.md`: Complete finding cards with file/line citations and diff context.
- `summary.md`: Cluster distribution, severity breakdown, and executive posture.
- `manifest.json`: Final finding counts and metadata.

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Failure Recovery & Cascade Rules

```
No rules active:     HALT — Run /torusguard init to detect framework and activate rules
Parser failure:      Skip problematic single file with warning; continue scanning remaining files
Timeout (>3 min):    Partition scan into subdirectories (src/, app/, lib/) and report progress
Critical flaw found: Mark run as 🔴 Action Required; prioritize cluster remediation
```

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Hallucination Guard

```
❌ Never report a finding without an exact file path and line number citation
❌ Never guess line numbers — compute them directly from active disk state
❌ Never fabricate a finding from memory; every finding must map to an active rule
❌ Never skip root-cause clustering when 2+ findings share an architectural source
```

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Static Code Audit Completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run ID:             [run-YYYYMMDD-HHMMSS-audit]
Files Scanned:      [Count, e.g., 84 files]
Total Findings:     [Count] ([Critical] Critical · [High] High · [Med] Med)
Systemic Clusters:  [Count, e.g., 2 Clusters Identified]
Executive Posture:  🔴 ACTION REQUIRED (or 🟡 WARNINGS / 🟢 SECURE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top Prioritized Findings:
1. [TG-DB-004] Missing Tenant Isolation in /invoices/ (Confidence: 90/100 - Confirmed)
2. [TG-INPUT-002] Unsafe SQL Query String in /search/ (Confidence: 85/100 - High)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard harden` to formulate surgical remediation bundles.
```

---

## Objective
Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| High-confidence findings detected | → `/torusguard harden` to formulate patches |
| Ambiguous findings require runtime proof | → `/torusguard exploit-check` |
| Evidence review needed first | → `/torusguard verify` |
| View detailed report | Inspect `.torusguard/runs/<run-id>/findings.md` |
