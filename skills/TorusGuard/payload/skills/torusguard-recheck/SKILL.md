---
name: torusguard-recheck
description: Execute targeted differential AST re-scan, verify fix integrity, and manage 4-state closure transitions.
version: 0.9.2
workflow: .torusguard/workflows/recheck.md
tools: Read, Grep, Glob, Bash, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Recheck — Targeted Differential Re-Scan & Regression Audit

## Objective
Differentially re-scan modified source files post-patch, verify that the original vulnerability is closed without introducing neighboring regressions, and update finding closure status across 4 formal states.

---

## Execution Steps

### Step 1: Identify Modified Files
Read `metadata.json` from the applied bundle to extract the list of modified source files.

### Step 2: Compile & Syntax Sanity Check
Run a quick compiler or syntax validator:
- Python: `python -m py_compile <modified_file>`
- TypeScript: `npx tsc --noEmit`
If syntax fails, immediately trigger rollback from `pre_apply/` snapshot.

### Step 3: Targeted Differential AST Scan
Re-scan the modified lines for the original finding rule:
- Verify that the vulnerable AST node has been eliminated.
- Verify that safe patterns (parameterized queries, tenant filters, schema boundaries) are active.

### Step 4: Neighboring Regression Check
Scan the 50 lines surrounding the patch and direct callers:
- Verify no existing imports, decorators, or error handlers were dropped.
- Verify no new security rule violations were introduced.

### Step 5: Classify State Transition
Apply the 4-state transition rules detailed below.

### Step 6: Update Run Artifacts
Write `recheck.md` and update `manifest.json` with resolved and remaining finding counts.

---

## State Transition Rules

Each targeted finding transitions into one of 4 formal states:

| Transition State | Definition | Action Required |
| :--- | :--- | :--- |
| **`Confirmed Fixed`** | Vulnerable AST node eliminated, safe pattern verified, zero regressions detected. | Finding marked as closed; proceed to `/torusguard report`. |
| **`Partially Fixed`** | Flaw mitigated on primary path, but secondary code path or method remains exposed. | Refine remediation bundle to cover edge case. |
| **`Not Fixed`** | Vulnerable AST node remains intact; patch did not resolve the flaw. | Discard patch, re-analyze root cause, and re-harden. |
| **`Regression`** | Patch introduced syntax error, broken logic, or a new security vulnerability. | **HALT IMMEDIATELY**: Roll back from `pre_apply/` snapshot. |

---

## Safety Constraints
- Only re-scan files modified by the applied patch to conserve context and execution budget.
- Never mark a finding as `Confirmed Fixed` without re-reading the active disk file.
- Automatically offer instant rollback if any regression is detected.

---

## Output Format
```markdown
🛡️ [TorusGuard] Targeted Recheck Completed
- Target File: <file_path>
- Findings Re-Scanned: <Count>
- Status: 🟢 CONFIRMED FIXED (0 Regressions Detected)
- Syntax Verification: ✅ Clean compilation
- Transition Breakdown:
  - <finding_id>: Confirmed (Score: 90) → 🟢 Confirmed Fixed

Next Step: Run `/torusguard report` to export signed report and SARIF log.
```
