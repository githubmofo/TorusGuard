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

Inspect finding records and evidence integrity before verification:
1. **Latest Run Records (`.torusguard/runs/`):** Locate most recent audit run directory.
2. **Finding Files:** Confirm `findings.md` or `findings.json` exists in the target run folder.
3. **Live File Drift:** Assert cited source files have not been edited or relocated on disk.
4. **Scoring Model Calibration:** Ensure `finding_scorer.py` evaluates all 5 rubric dimensions.
5. **Role Boundary:** Enforce validator role; do not apply code modifications during verification.

---

## When to Use /torusguard verify

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Auditing whether static findings are valid code flaws | Run `/torusguard verify` |
| Upgrading Medium confidence finding to Confirmed | Run `/torusguard verify` |
| No audit run executed yet | Run `/torusguard audit` first |
| Running live network requests against endpoints | Run `/torusguard web-validate` |
| Generating patch after verification | Run `/torusguard harden` |

---

## Execution Steps

1. **Locate Target Findings:** Load active findings from latest run directory.
2. **Live Disk Line Match:** Read current code at cited line ranges; verify AST snippet matches.
3. **Audit Evidence Sufficiency:** Assess whether taint path is unbroken and caller context is exposed.
4. **Refine Confidence Scores:**
   ```bash
   python .torusguard/scripts/finding_scorer.py --run <run_dir> --verify
   ```
5. **Classify Status:** Assign verified state (`Confirmed`, `Plausible`, or `False Positive / Disputed`).
6. **Emit Verification Ledger:** Write `verified-evidence.md` into the active run folder.

---

## Failure Recovery

- **Missing Run Folder:** Run `/torusguard audit` first to produce a valid run baseline.
- **Line Drift Detected:** Flag line mismatch; scan nearby lines (±25) for relocated AST sink.
- **Malformed Finding JSON:** Repair JSON structure using finding schema before scoring.
- **Halt Trigger:** Abort if cited files are completely deleted from disk.

---

## Hallucination Guard

- ❌ Never confirm a finding if the cited sink has already been sanitized by middleware.
- ❌ Never bump confidence score without documenting unbroken taint source-to-sink flow.
- ✅ Always anchor line matches to live disk reads using `view_file`.

---

## Output Card Format

```markdown
### 🧪 TorusGuard Evidence Verification
- **Run ID:** `run-YYYYMMDD-HHMMSS-audit`
- **Findings Evaluated:** [Count] findings
- **Confirmed Real:** [Count] verified flaws
- **Downgraded / False Positives:** [Count] filtered out
- **Refined Mean Score:** [Score]/100
- **Ledger:** `.torusguard/runs/<run_id>/verified-evidence.md`
```

---

## Next Steps

1. Run `/torusguard web-validate` if live endpoint probing is required.
2. Run `/torusguard harden` to build surgical patch bundles for verified flaws.
