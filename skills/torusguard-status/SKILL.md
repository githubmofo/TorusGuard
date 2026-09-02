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
2. **Enumerate Active Rules:** Count rule files physically present in `.torusguard/rules/active/`.
3. **Inspect Run History:** List historical run folders in `.torusguard/runs/` via `run_manager.py`.
4. **Check Authorization Scope:** Check `.torusguard/config/scope.json` for active targets and TTL expiration.
5. **Render Diagnostic Overview:** Output formatted status card.

---

## Safety Constraints
- Read-only execution; zero file modifications.
- Handle uninitialized workspaces gracefully with advice to run `/torusguard init`.

---

## Output Format
```markdown
🛡️ [TorusGuard] Workspace Status Overview
- Version: v0.9.2 | Stack: <Detected Framework>
- Active Rules: <Count> rules active in `.torusguard/rules/active/`
- Historical Runs: <Count> runs recorded
- Scope: <Authorized (TTL Active) / Expired / Unconfigured>
- Posture: <SECURE / ACTION REQUIRED>
```
