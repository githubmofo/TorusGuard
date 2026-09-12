---
name: torusguard-recheck
description: Execute targeted differential AST re-scan against modified files, verify fix closure, and assert zero regressions via CLI or AI Agent.
version: 1.3.5
workflow: .torusguard/workflows/recheck.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/recheck_runner.py
  - .torusguard/scripts/audit_runner.py
  - .torusguard/scripts/memory_engine.py
  - .torusguard/scripts/term_ui.py
---

# TorusGuard Recheck — Targeted Differential Audit & Fix Closure

## Objective
Execute differential security re-scans strictly scoped to modified files and adjacent boundaries, verifying that targeted vulnerability patterns have been eliminated and asserting zero security regressions.

---

## Two Execution Modes

### Mode A: Automated CLI Execution
Run the differential recheck engine from the terminal:
```bash
# Recheck the latest applied run
npx torusguard recheck

# Recheck a specific project directory
npx torusguard recheck ./my-project

# Recheck a specific run ID
npx torusguard recheck --run run-20260910-121618-audit

# Machine-readable JSON output
npx torusguard recheck --json
```
**Under the Hood:** Executes `python .torusguard/scripts/recheck_runner.py`.
- Evaluates applied candidate bundles from `.torusguard/runs/<run_id>/bundles/`.
- Executes single-file targeted differential AST scans via `audit_runner.scan_file()`.
- Calculates formal status transitions:
  - `✔ [Confirmed Fixed]`: Vulnerable pattern absent, zero regressions.
  - `✖ [Regressed]`: New security finding introduced by patch.
  - `⚠ [Unresolved]`: Vulnerable sink still present.
- Emits run-level transition artifact: `.torusguard/runs/<run_id>/recheck.md`.
- Synchronizes verification telemetry to `.torusguard/memory/events.json`.
- Displays 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Differential Scan
When evaluating patches directly in AI chat:
1. **Identify Modified Files:** Read `diff_summary.md` or git status for files modified in the active run.
2. **Re-Scan Sinks:** View the target file and verify that the specific rule violation (e.g. `TG-INPUT-003`, `TG-PLATFORM-001`) is no longer triggered.
3. **Assert Zero Regressions:** Verify that no new vulnerabilities (like raw concatenation or unvalidated input) were introduced by the fix.
4. **Update Status:** Log outcome in `.torusguard/runs/<run_id>/recheck.md`.
5. **Memory Telemetry:** Record verification event with `memory_engine.record_event("fix_verified", ...)`.

---

## Recheck Status Transitions
| Outcome | Visual Indicator | Meaning | Required Action |
| :--- | :--- | :--- | :--- |
| **Confirmed Fixed** | `✔ [Confirmed Fixed]` | Sink eliminated, zero regressions | Proceed to Posture Report |
| **Unresolved** | `⚠ [Unresolved]` | Flaw still present in file | Re-harden with alternative pattern |
| **Regressed** | `✖ [Regressed]` | New security flaw introduced | Instant `npx torusguard rollback` |

---

## Output Card Format
```markdown
### ✅ TorusGuard Differential Recheck Completed
- **Run ID:** `run-20260910-121618-audit`
- **Confirmed Fixed:** 2 vulnerabilities verified closed
- **Regressions:** 0 detected
- **Unresolved:** 0
- **Artifact:** `.torusguard/runs/<run_id>/recheck.md`
- **Next Step:** Run `npx torusguard report --html` for visual dashboard
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.
