---
description: Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: reviewer
lifecycle-phase: Phase 6 (Targeted Recheck & Verification)
required-skills:
  - torusguard-recheck
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# /torusguard recheck — Targeted Differential Recheck & Regression Audit

$ARGUMENTS

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state transitions.

---

## Mandatory Pre-Flight Context Inspection

Inspect applied patch history and target file scope before re-checking:
1. **Applied Patch Record:** Verify `apply-log.json` or modified file list exists in the active run.
2. **Scope Limitation:** Restrict differential scan strictly to modified files to conserve token budget.
3. **Rollback Availability:** Confirm `.bak` snapshot exists in `pre_apply/` in case regression is detected.
4. **4-State Transition Engine:** Prepare to transition findings to `Fixed`, `Partially Fixed`, `Not Fixed`, or `Regression`.
5. **Fresh Syntax Validation:** Ensure no compiler or syntax errors exist before re-evaluating rules.
6. **AST Consistency:** Ensure imported dependencies on modified lines resolve correctly.

---

## When to Use /torusguard recheck

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Immediately after applying a remediation patch | Run `/torusguard recheck` |
| Verifying that a specific finding is eliminated | Run `/torusguard recheck` |
| Checking whether a patch introduced new security flaws | Run `/torusguard recheck` |
| Whole repository baseline audit | Run `/torusguard audit` |
| Generating final signed release report | Run `/torusguard report` |

---

## Execution Steps

1. **Identify Modified Files:** Extract list of altered files from latest apply step.
2. **Execute Differential AST Scan:** Re-run active security rules exclusively against modified files.
3. **Evaluate Finding Status:**
   - If original vulnerable AST pattern is absent and no new sink appears: transition to `Fixed`.
   - If new security rule triggers on altered lines: classify as `Regression`.
4. **Update Finding State:** Record verified resolution status into `findings.json`.
5. **Emit Recheck Report:** Write `recheck-report.md` into the active run folder.

---

## Failure Recovery

- **Finding Still Present (`Not Fixed`):** Review patch diff; the remediation did not neutralize the AST sink.
- **New Vulnerability Detected (`Regression`):** Alert operator; prompt to revert from `.bak` snapshot.
- **File Not Found:** Verify file path matches git repository layout.
- **Halt Trigger:** Abort if diff shows changes outside approved patch scope.

---

## Hallucination Guard

- ❌ Never mark a finding as `Fixed` without re-scanning the actual AST of the patched file.
- ❌ Never ignore new warnings introduced in modified lines.
- ✅ Always provide before/after line comparisons confirming sink removal.

---

## Output Card Format

```markdown
### ✅ TorusGuard Differential Recheck
- **Files Re-scanned:** [List of modified files]
- **Target Finding:** `TG-XXX-HASH`
- **Result:** [FIXED / REGRESSION / PARTIAL]
- **Regressions Introduced:** 0
- **Report:** `.torusguard/runs/<run_id>/recheck-report.md`
- **Status:** VERIFIED — ready for `/torusguard report`
```

---

## Next Steps

1. Run `/torusguard report` to generate executive summary and export OASIS SARIF v2.1.0 data.
2. Commit the verified patch to version control.
