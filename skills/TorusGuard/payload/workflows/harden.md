---
description: Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: remediator
lifecycle-phase: Phase 4 (Remediation Formulation)
required-skills:
  - torusguard-harden
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# /torusguard harden — Governed Remediation & Bundle Packaging

$ARGUMENTS

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<=35 add, <=25 del).

---

## Mandatory Pre-Flight Context Inspection

Inspect finding targets and patch constraints before generating diffs:
1. **Target Finding (`findings.md`):** Identify prioritized verified findings.
2. **Ponytail Protocol:** Enforce hard limit ($\le 35$ additions, $\le 25$ deletions). Ban rewrites.
3. **Sensitive Path Review:** Flag changes touching `auth/` or `settings.py` for human sign-off.
4. **Behavior Preservation:** Ensure patch addresses flaw without breaking public APIs.
5. **Dry-Run Rule:** Do NOT apply changes to disk during harden; emit bundle for review.
6. **Backup Readiness:** Ensure rollback procedures are prepared before staging patch.

---

## When to Use /torusguard harden

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Formulating minimal patches for verified findings | Run `/torusguard harden` |
| Packaging a 4-artifact remediation bundle for review | Run `/torusguard harden` |
| Writing and applying changes to code files | Run `/torusguard apply` |
| Differentially re-scanning code after patch application | Run `/torusguard recheck` |
| Discovering new vulnerabilities | Run `/torusguard audit` |

---

## Execution Steps

1. **Select Target Finding:** Choose verified flaw from active run directory.
2. **Examine Live Code Context:** Read surrounding lines (±15) of vulnerable sink.
3. **Draft Unified Diff:** Formulate minimal fix adhering to Ponytail Protocol limits.
4. **Package 4-Artifact Bundle:**
   - `patch.diff`: Unified diff with line numbers.
   - `plan.md`: Step-by-step remediation rationale.
   - `verification.md`: Instructions to verify fix.
   - `rollback.md`: Revert commands on regression.
5. **Write Bundle:** Save to `.torusguard/runs/<run_id>/remediation/<finding_id>/`.

---

## Failure Recovery

- **Line Churn Exceeded (>35 add or >25 del):** Decompose patch into smaller sequential sub-fixes.
- **Sensitive Path Conflict:** Mark bundle with `Requires Sensitive-Path Sign-Off` in `plan.md`.
- **Finding Not Found:** Ensure finding ID exists in active `findings.md`.
- **Halt Trigger:** Abort if target source file cannot be read from disk.

---

## Hallucination Guard

- ❌ Never generate full-file replacements or unconstrained cosmetic code refactoring.
- ❌ Never modify imports, variables, or functions unrelated to the vulnerability.
- ✅ Always calculate addition and deletion line counts before emitting `patch.diff`.

---

## Output Card Format

```markdown
### 🛠️ TorusGuard Remediation Bundle
- **Finding Target:** `TG-XXX-HASH` ([Vulnerability Name])
- **File Affected:** `src/path/to/file.py`
- **Line Churn:** +[Additions] / -[Deletions] (Ponytail: PASS)
- **Sensitive Path:** [Yes (Sign-Off Needed) / No (Standard)]
- **Bundle Path:** `.torusguard/runs/<run_id>/remediation/<finding_id>/`
- **Status:** READY FOR REVIEW — run `/torusguard apply` to execute
```

---

## Next Steps

1. Review proposed diff in `.torusguard/runs/<run_id>/remediation/<finding_id>/patch.diff`.
2. Run `/torusguard apply` to execute the governed patch with automatic rollback backup.
