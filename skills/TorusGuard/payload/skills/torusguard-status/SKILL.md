---
name: torusguard-status
description: Display current TorusGuard security posture, active configuration, rules catalog, and run history via CLI or AI Agent.
version: 1.3.5
workflow: .torusguard/workflows/status.md
tools: Read, Grep, Glob, run_command, Write
scripts-binding:
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/term_ui.py
---

# TorusGuard Status — Workspace Security Posture & Diagnostic Overview

## Objective
Provide an instant diagnostic summary of the repository's security state, active framework rules, historical run results, and runtime scope validity.

---

## Two Execution Modes

### Mode A: Automated CLI Execution
Run the diagnostic overview from your terminal:
```bash
# Display 75-column status cards
npx torusguard status

# Check status of specific project directory
npx torusguard status ./examples/vulnerable-react-express

# Output machine-readable JSON
npx torusguard status --json
```
**Under the Hood:**
- Evaluates `.torusguard/config/torusguard.json` for initialized status and detected stack.
- Enumerates active rules in `.torusguard/rules/active/` (or canonical 74 rules).
- Scans `.torusguard/runs/` for run history, finding counts, and verified fixes.
- Inspects `.torusguard/config/scope.json` for authorized runtime validation targets.
- Displays mathematically aligned 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Status Check
When checking workspace status in AI chat:
1. **Verify Workspace Setup:** Check if `.torusguard/` exists on disk.
2. **Inspect Active Config:** Read `.torusguard/config/torusguard.json` for detected stack, framework, and rules.
3. **Inspect Latest Run:** Find the latest run directory under `.torusguard/runs/` and read `manifest.json`.
4. **Inspect Memory Engine:** Check `.torusguard/memory/patterns.json` for captured Golden Fix Recipes.
5. **Render Diagnostic Card:** Present an overview of posture, stack, and recommended next steps.

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Workspace Status Overview
- **Version:** v1.3.3 | **Stack:** Node.js / React / Express
- **Active Rules:** 74 canonical security rules enabled
- **Historical Runs:** 3 runs recorded
- **Golden Recipes:** 4 distilled into persistent memory
- **Overall Posture:** SECURE (All targeted vulnerabilities verified closed)
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.
