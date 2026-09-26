---
name: torusguard-status
description: Display current TorusGuard security posture, active configuration, rules catalog, and run history via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/status.md
tools: Read, Grep, Glob, run_command, Write
scripts-binding:
  - internal/scanner/scanner.go
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Status — Workspace Security Posture & Diagnostic Overview

## Objective
Provide an instant diagnostic summary of the repository's security state, active framework rules, historical run results, and runtime scope validity.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard status` | Emits 75-column diagnostic cards with stack, posture, and active rules. |
| **Mode B: AI Chat Slash** | `/torusguard status` | Parses workspace posture, reviews latest run manifest and open findings. |
| **Mode C: Native MCP Tool**| `torusguard_status` | Returns structured diagnostic payload directly to AI coding agents. |

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run the diagnostic overview from your terminal:
```bash
# Display 75-column status cards
torusguard status

# Check status of specific project directory
torusguard status ./examples/vulnerable-react-express

# Output machine-readable JSON
torusguard status --json
```

**Under the Hood:**
- Evaluates `.torusguard/config/torusguard.json` for initialized status and detected stack.
- Enumerates active rules in `.torusguard/rules/active/` (or canonical 74 rules across 18 families).
- Scans `.torusguard/runs/` for run history, finding counts, and verified fixes.
- Inspects `.torusguard/config/scope.json` for authorized runtime validation targets.
- Displays mathematically aligned 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Status Check
When checking workspace status in AI chat:
1. **Verify Workspace Setup:** Check if `.torusguard/` exists on disk.
2. **Inspect Active Config:** Read `.torusguard/config/torusguard.json` for detected stack, framework, and rules.
3. **Inspect Latest Run:** Find the latest run directory under `.torusguard/runs/` and read `manifest.json`.
4. **Inspect Living Ledger:** Inspect `security_report.md` for current open/fixed finding counts.
5. **Inspect Memory Engine:** Check `.torusguard/memory/patterns.json` for captured Golden Fix Recipes.
6. **Render Diagnostic Card:** Present an overview of posture, stack, and recommended next steps.

### Mode C: Native MCP Tool Execution
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Tool Invocation:** Call `torusguard_status` with target directory:
  ```json
  {
    "target": "."
  }
  ```
- **Programmatic Return:** Receives formatted diagnostic status string detailing detected stack, engine version, and active protection state.

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Workspace Status Overview
- **Version:** v2.0.0 | **Stack:** Node.js / React / Express
- **Active Rules:** 74 canonical security rules enabled
- **Historical Runs:** 3 runs recorded
- **Golden Recipes:** 4 distilled into persistent memory
- **Overall Posture:** SECURE (All targeted vulnerabilities verified closed)
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Hallucinated Posture** | Reports repository is "100% secure" without reading `security_report.md` or `.torusguard/config/torusguard.json`. | Read actual disk artifacts (`security_report.md`, `manifest.json`) before reporting status. |
| **Phantom Run Counts** | Fabricates arbitrary run IDs or counts instead of checking `.torusguard/runs/`. | Enumerate `.torusguard/runs/` directories or use `torusguard status` CLI/MCP output. |
| **Stack Guessing** | Assumes project stack without inspecting package manifests (`go.mod`, `package.json`, `Cargo.toml`). | Verify detected stack from `torusguard.json` or root dependency files. |
| **Stale Cache Reliance** | Reports previous conversation status after new files or patches were applied. | Perform fresh inspection of workspace status on each invocation. |

---

## ✅ Pre-Flight Self-Audit

Before emitting a status report:
- [ ] Did I verify the existence and content of `.torusguard/config/torusguard.json`?
- [ ] Did I check `security_report.md` for active finding counts?
- [ ] Did I verify if `.torusguard/runs/` contains historical run data?
- [ ] Are all reported counts and stack frameworks backed by active disk state?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Check disk for .torusguard/ directory and read configuration files.
BUILD:   Aggregate stack information, active rules, and latest run findings.
CONFIRM: Emit standardized 75-column diagnostic summary card with recommended next steps.
```
