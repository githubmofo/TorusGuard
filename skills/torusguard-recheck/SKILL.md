---
name: torusguard-recheck
description: Execute targeted differential AST re-scan against modified files, verify fix closure, and assert zero regressions.
version: 1.0.0
workflow: .torusguard/workflows/recheck.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Recheck — Targeted Differential Audit & Regression Verification

## Objective
Re-scan only files modified by remediation patches, confirming that targeted vulnerability sinks have been neutralized and verifying that no new security regressions were introduced.

---

## Execution Steps

1. **Identify Modified Files:** Read `apply-log.json` from active run directory.
2. **Execute Differential Scan:** Re-run active `TG-*` rules exclusively against modified files.
3. **Evaluate Finding Status:** Transition finding state according to transition rules below.
4. **Assert Regression-Free:** Ensure no new security warnings triggered on altered lines.
5. **Update State & Memory:** Record status in `findings.json` and sync verified results to memory engine.
6. **Emit Recheck Report:** Save summary in `.torusguard/runs/<run_id>/recheck-report.md`.

---

## State Transition Rules
- **`Fixed`:** Targeted vulnerable AST pattern is absent and no new issues appear on modified lines.
- **`Partially Fixed`:** Vulnerability surface was reduced but sanitization remains incomplete.
- **`Not Fixed`:** Vulnerable AST sink remains present in patched file.
- **`Regression`:** Patch introduced a new security rule violation on modified lines.

---

## Safety Constraints
- Restrict AST scan strictly to modified files and direct callers.
- If regression is detected, halt and recommend immediate rollback via `.bak` snapshot.
- Read-only differential analysis.

---

## Output Format
```markdown
✅ [TorusGuard] Differential Recheck Completed
- Modified Files Scanned: <Count>
- Target Finding: <Finding ID> ──► FIXED
- Regressions Detected: 0
- Report: `.torusguard/runs/<run_id>/recheck-report.md`
Next: Run `/torusguard report` to export final SARIF and release summary.
```
