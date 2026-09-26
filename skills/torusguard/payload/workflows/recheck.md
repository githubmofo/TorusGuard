---
description: Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: reviewer
lifecycle-phase: Phase 6 (Targeted Recheck & Verification)
required-skills:
  - torusguard-recheck
scripts-binding:
  - internal/recheck/recheck.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard recheck — Targeted Differential Recheck & Regression Audit

$ARGUMENTS

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions across modified files.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard recheck` | Terminal execution of differential AST scanner. |
| **Mode B: AI Chat Slash** | `/torusguard recheck` | Conversational differential review and regression verification. |
| **Mode C: Native MCP Tool** | `torusguard_recheck` | Agent tool call with `{"target": "."}` returning diff assertions. |

---

## Mandatory Pre-Flight Context Inspection

Inspect applied patch history and target file scope before re-checking:
1. **Applied Patch Record:** Inspect git status or diff for modified files.
2. **Scope Limitation:** Restrict differential scan strictly to modified files to conserve token budget.
3. **Rollback Availability:** Confirm `.bak` snapshot exists in `.torusguard/snapshots/` in case regression is detected.
4. **4-State Transition Engine:** Prepare to transition findings to `Fixed`, `Partially Fixed`, `Not Fixed`, or `Regression`.
5. **Fresh Syntax Validation:** Ensure no compiler or syntax errors exist before re-evaluating rules.

---

## Living Report Invariant
- Verified fix closures transition findings in `security_report.md` to `RESOLVED 🟢`.
- Regressions transition findings to `REGRESSED ❌`.

---

## Execution Steps

1. **Trigger Recheck:**
   - **Mode A (CLI):** Run `torusguard recheck`.
   - **Mode B (Chat):** Review modified files and re-scan AST sinks.
   - **Mode C (MCP):** Call `torusguard_recheck`.
2. **Evaluate Finding Status:**
   - If original vulnerable pattern is absent and no new sink appears: transition to `✔ [Confirmed Fixed]`.
   - If new security rule triggers on altered lines: classify as `✖ [Regressed]`.
3. **Update Finding State:** Update `security_report.md`.
4. **Recommend Posture Report:** Advise running `torusguard report --html`.

---

## Output Card Format

```markdown
### ✅ TorusGuard Differential Recheck
- **Files Re-scanned:** [List of modified files]
- **Target Finding:** `TG-XXX-HASH`
- **Result:** [FIXED / REGRESSION / PARTIAL]
- **Regressions Introduced:** 0
- **Status:** VERIFIED — ready for `/torusguard report`
```

---

## Next Steps

1. Run `/torusguard report` to generate executive summary and export OASIS SARIF v2.1.0 data.
2. Commit the verified patch to version control.
