---
description: Evidence sufficiency verification, live disk line match audit, and finding score refinement.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: validator
lifecycle-phase: Phase 3a (Evidence Verification)
required-skills:
  - torusguard-verify
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
---

# /torusguard verify — Evidence Verification & Score Refinement

$ARGUMENTS

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Mandatory Pre-Flight Context Inspection

Before auditing finding evidence, you MUST inspect:

1. **Latest Run Artifacts (`.torusguard/runs/`)** → Identify the most recent audit run directory.
2. **Finding Manifest Integrity** → Confirm `findings.md` or `findings.json` is present in the target run folder.
3. **Current Disk State Synchronization** → Check whether source files cited in findings have been altered on disk since the audit ran.
4. **Scoring Model Calibration** → Ensure `finding_scorer.py` evaluates all 5 rubric dimensions without arbitrary score padding.

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## When to Use /torusguard verify

| Use `/torusguard verify` when... | Use something else when... |
| :--- | :--- |
| Auditing whether static findings are valid | No audit has been run yet → `/torusguard audit` |
| Upgrading Medium confidence finding to Confirmed | Running live HTTP requests against server → `/torusguard web-validate` |
| Verifying evidence before generating patches | Formulating unified diff patches → `/torusguard harden` |
| Investigating potential false positives | Re-scanning after code changes → `/torusguard recheck` |

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Execution Steps (Fixed Order)

### Phase 1 — Locate Target Findings
1. Parse findings from the active run folder: `.torusguard/runs/<latest-run>/findings.md`.
2. For each finding, extract cited file path, line number range, and AST snippet.

### Phase 2 — Live Disk State Cross-Check
1. Read the target file directly from disk using exact file path.
2. Compare lines around the cited line number against the stored `primaryLocationLineHash`.
3. If code has shifted, locate new line offset via AST pattern matching; if code was removed or altered, mark as `Stale / Requires Re-scan`.

### Phase 3 — 5-Factor Evidence Sufficiency Audit
Evaluate each finding across the 5 verifiable factors:
1. **Evidence Quality (Max 35)**:
   - Direct AST match with source citation = 35 pts.
   - Text regex match without AST parsing = 20 pts.
   - Indirect heuristic indicator = 10 pts.
2. **Reproduction Success (Max 25)**:
   - Deterministic test / repro script exists = 25 pts.
   - Trace logs or stack dump present = 15 pts.
   - Purely static inference = 0 pts.
3. **Independent Confirmations (Max 15)**:
   - Confirmed in 3+ independent callers/files = 15 pts.
   - Confirmed in 2 files = 10 pts.
   - Single isolated file = 5 pts.
4. **Environmental Clarity (Max 15)**:
   - Direct routable endpoint with visible controller = 15 pts.
   - Minor middleware indirection = 8 pts.
   - Ambiguous or unreachable dead code = 0 pts.
5. **Manual Review Status (Max 10)**:
   - Verified by security engineer = 10 pts.
   - Secondary agent consensus = 5 pts.
   - Unreviewed = 0 pts.

### Phase 4 — Recalculate Scores & Update Findings
Run `finding_scorer.py` to record adjusted confidence score:
```bash
python .torusguard/scripts/finding_scorer.py --evidence AST_MATCH --repro TEST_REPRO --independent MULTI_FILE --clarity DIRECT_ROUTE
```
Update confidence bands in `.torusguard/runs/<latest-run>/findings.md`.

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Failure Recovery & Cascade Rules

```
Run folder not found:  HALT — Instruct user to run /torusguard audit first
File deleted on disk:  Mark finding as INVALIDATED (File No Longer Exists)
Evidence insufficient: Downgrade confidence to 'Needs Review' (<50); flag for manual audit
Score calculation err: Fall back to static baseline score and log error
```

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Hallucination Guard

```
❌ Never mark a finding as 'Confirmed' if the cited file content cannot be read from disk
❌ Never give points for 'Reproduction Success' without an actual test or trace log
❌ Never silently discard a finding without recording the invalidation reason
```

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Evidence Verification & Confidence Audit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run ID:               [run-YYYYMMDD-HHMMSS-audit]
Findings Verified:    [Count, e.g., 6 findings audited]
Score Adjustments:    [e.g., 2 Confirmed, 3 High Confidence, 1 Needs Review]
Disk State Parity:    100% Invariant Hashes Matched on Disk
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confidence Classification:
- TG-DB-004: 90/100 (Confirmed - Exact AST + Deterministic Route)
- TG-INPUT-002: 85/100 (High Confidence - Parameterized Alternative Available)
- TG-AUTH-003: 45/100 (Needs Review - Delegated to Upstream Proxy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard harden` to formulate patches for Confirmed findings.
```

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| High confidence findings confirmed | → `/torusguard harden` to create remediation |
| Ambiguous endpoints need runtime proof | → `/torusguard exploit-check` |
| Code modified during review | → `/torusguard recheck` |
