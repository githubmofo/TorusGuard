---
name: torusguard-recheck
description: Execute targeted differential AST re-scan against modified files, verify fix closure, and assert zero regressions via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/recheck.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - internal/harden/patch.go
  - .torusguard/scripts/report_sync.py
---

# TorusGuard Recheck — Targeted Differential Audit & Fix Closure

## Objective
Execute differential security re-scans strictly scoped to modified files and adjacent boundaries, verifying that targeted vulnerability patterns have been eliminated and asserting zero security regressions.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard recheck` | Scans modified files, verifies fix closure, and updates run artifacts. |
| **Mode B: AI Chat Slash** | `/torusguard recheck` | Guides interactive differential review and records fix events. |
| **Mode C: Native MCP Tool**| `torusguard_recheck` | Machine-to-machine differential AST re-scan for AI coding agents. |

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run the differential recheck engine from the terminal:
```bash
# Recheck the latest applied run
torusguard recheck

# Recheck a specific project directory
torusguard recheck ./my-project

# Recheck a specific run ID
torusguard recheck --run run-20260910-121618-audit

# Machine-readable JSON output
torusguard recheck --json
```

**Under the Hood:**
- Evaluates applied candidate bundles from `.torusguard/runs/<run_id>/bundles/`.
- Executes single-file targeted differential AST scans via `internal/scanner` and `internal/recheck`.
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
2. **Re-Scan Sinks:** View the target file and verify that the specific rule violation (e.g. `TG-INPUT-003`, `TG-PLATFORM-001`, `TG-NPE-001`) is no longer triggered.
3. **Assert Zero Regressions:** Verify that no new vulnerabilities (like raw concatenation, missing null checks, or unvalidated inputs) were introduced by the fix.
4. **Update Status:** Log outcome in `.torusguard/runs/<run_id>/recheck.md` and transition status in `security_report.md`.
5. **Memory Telemetry:** Record verification event in persistent memory.

### Mode C: Native MCP Tool Execution
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Tool Invocation:** Call `torusguard_recheck` with target workspace:
  ```json
  {
    "target": "."
  }
  ```
- **Programmatic Return:** Receives differential AST re-scan results, baseline comparison, and confirms zero regressions.

---

---

## Recheck Status Transitions
| Outcome | Visual Indicator | Meaning | Required Action |
| :--- | :--- | :--- | :--- |
| **Confirmed Fixed** | `✔ [Confirmed Fixed]` | Sink eliminated, zero regressions | Proceed to Posture Report |
| **Unresolved** | `⚠ [Unresolved]` | Flaw still present in file | Re-harden with alternative pattern |
| **Regressed** | `✖ [Regressed]` | New security flaw introduced | Instant `torusguard rollback` |

---

## Output Card Format
```markdown
### ✅ TorusGuard Differential Recheck Completed
- **Run ID:** `run-20260910-121618-audit`
- **Confirmed Fixed:** 2 vulnerabilities verified closed
- **Regressions:** 0 detected
- **Unresolved:** 0
- **Artifact:** `.torusguard/runs/<run_id>/recheck.md`
- **Next Step:** Run `torusguard report --html` for visual dashboard
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Premature Closure** | Marks finding "Fixed" merely because code was written, without differential AST re-scan. | Must execute `torusguard recheck` or differential scan to verify the AST sink is genuinely absent. |
| **Line-Shift Drift** | Relies on original finding line numbers after patches shifted line offsets. | Use semantic snippet matching or recalculate line numbers from fresh AST scan. |
| **Regression Blindness** | Checks only the original sink and ignores new flaws introduced in surrounding lines (e.g., introducing an unhandled null pointer or SQL concatenation). | Scan entire changed block and adjacent context ($\pm 3$ lines) for zero newly introduced `TG-*` violations. |
| **Bypass Disguise** | Accepts `# nosec`, `// eslint-disable`, or `InsecureSkipVerify` as a valid "fix". | Strictly flag security bypasses as `✖ [Regressed]` under rule `TG-DIFF-001`. |

---

## ✅ Pre-Flight Self-Audit

Before declaring any finding resolved:
- [ ] Did I read the modified file from disk after applying the patch?
- [ ] Did I verify the exact AST sink is absent and unreachable?
- [ ] Did I verify no new vulnerabilities were introduced in surrounding code ($\pm 3$ lines)?
- [ ] Did I verify zero security suppression comments or bypasses (`# nosec`, `verify=False`, etc.) exist?
- [ ] Is the finding status updated in `security_report.md`?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Inspect disk content of modified files to confirm patch application.
BUILD:   Execute differential re-scan against modified files using scanner rules.
CONFIRM: Assert finding transition to Confirmed Fixed and verify zero regressions.
```
