---
description: Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: reviewer
lifecycle-phase: System / Diagnostics
required-skills:
  - torusguard-status
scripts-binding:
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
  - internal/workspace/workspace.go
---

# /torusguard status — Workspace Security Posture & Diagnostic Overview

$ARGUMENTS

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, and run history across 74 canonical security rules and 18 families.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard status [--json]` | Terminal execution of 75-column diagnostic cards. |
| **Mode B: AI Chat Slash** | `/torusguard status` | Conversational diagnostic inspection of active config and ledger. |
| **Mode C: Native MCP Tool** | `torusguard_status` | Agent tool call with `{"target": "."}` returning posture JSON/string. |

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace state and configuration records prior to status display:
1. **Config State (`.torusguard/config/torusguard.json`):** Confirm workspace initialization and read detected stack.
2. **Active Rules Directory (`.torusguard/rules/active/`):** Count active rule files (74 canonical rules).
3. **Living Report (`security_report.md`):** Read current open vs resolved findings.
4. **Read-Only Invariant:** Ensure command performs zero file modifications or disk mutations.

---

## Living Report Invariant
- Reads current health score and status breakdown directly from `security_report.md`.
- Displays 18 rule families and 74 rules in standardized 75-column terminal cards.

---

## Execution Steps

1. **Trigger Status Check:**
   - **Mode A (CLI):** Run `torusguard status`.
   - **Mode B (Chat):** Read `torusguard.json` and `security_report.md`.
   - **Mode C (MCP):** Call `torusguard_status`.
2. **Evaluate Posture:** Report detected stack, active invariants, and living findings ledger.
3. **Recommend Next Actions:** Direct user to audit or remediation as needed.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Workspace Status
- **Version:** v2.0.0
- **Framework Detected:** [Stack]
- **Active Rules:** 74 canonical rules active across 18 families
- **Living Report:** `security_report.md`
- **Health Posture:** [OPTIMAL DEFENSE / ACTION NEEDED]
```

---

## Next Steps

1. Run `/torusguard audit` to scan codebase for security vulnerabilities.
2. Run `/torusguard report --html` to view interactive dashboard.
