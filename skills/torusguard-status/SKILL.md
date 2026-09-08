---
name: torusguard-status
description: Display current TorusGuard security posture, active configuration, rules catalog, and run history.
version: 0.9.2
workflow: .torusguard/workflows/status.md
tools: Read, Grep, Glob
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Status — Workspace Security Posture & Diagnostic Overview

## Objective
Provide an instant diagnostic summary of the repository's security state, active framework rules, historical run results, and runtime scope validity.

---

## Execution Steps

1. **Read Configuration:** Parse `.torusguard/config/torusguard.json` to verify initialization state and detected framework stack.
2. **Handle CLI Failures:** If `npx torusguard status` throws an error, YOU must manually parse the local files (e.g. `torusguard.json`, `scope.json`) to deduce the status instead of just returning the CLI error.
3. **Enumerate Active Rules:** Count rule files physically present in `.torusguard/rules/active/`.
4. **Inspect Run History:** List historical run folders in `.torusguard/runs/` via `run_manager.py`.
5. **Check Authorization Scope:** Check `.torusguard/config/scope.json` for active targets and TTL expiration.
6. **Render Diagnostic Overview:** Output formatted status card.

---

## Safety Constraints
- Read-only execution; zero file modifications.
- Handle uninitialized workspaces gracefully with advice to run `/torusguard init` (or manual AI initialization).

---

## Output Format
```markdown
🛡️ [TorusGuard] Workspace Status Overview (AI Assisted)
- Version: v0.9.2 | Stack: <Detected Framework>
- Active Rules: <Count> rules active in `.torusguard/rules/active/`
- Historical Runs: <Count> runs recorded
- Scope: <Authorized (TTL Active) / Expired / Unconfigured>
- Posture: <SECURE / ACTION REQUIRED>
```
