---
description: Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.
tools: Read, Grep, Glob, Bash
version: 0.9.2
agent: reviewer
lifecycle-phase: System / Diagnostics
required-skills:
  - torusguard-status
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# /torusguard status — Workspace Security Posture & Diagnostic Overview

$ARGUMENTS

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, and run history.

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace state and configuration records prior to status display:
1. **Config State (`.torusguard/config/torusguard.json`):** Confirm workspace initialization and read detected stack.
2. **Active Rules Directory (`.torusguard/rules/active/`):** Count active rule files.
3. **Run Folder Ledger (`.torusguard/runs/`):** Check run history and locate latest `manifest.json`.
4. **Scope Record (`.torusguard/config/scope.json`):** Check whether runtime authorization TTL is active or expired.
5. **Read-Only Invariant:** Ensure command performs zero file modifications or disk mutations.

---

## When to Use /torusguard status

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Checking workspace configuration and active security posture | Run `/torusguard status` |
| Reviewing recent audit runs and finding counts | Run `/torusguard status` |
| Checking active legal scope authorization TTL | Run `/torusguard status` |
| Initializing workspace for the first time | Run `/torusguard init` |
| Executing full security scan | Run `/torusguard audit` |

---

## Execution Steps

1. **Read Configuration:** Load `.torusguard/config/torusguard.json`; extract stack, version, and enabled rule count.
2. **Enumerate Active Rules:** Count rule files physically present in `.torusguard/rules/active/`.
3. **Inspect Run History:**
   ```bash
   python .torusguard/scripts/run_manager.py list
   ```
4. **Evaluate Scope Expiry:** Parse `.torusguard/config/scope.json`; report if TTL is valid or expired.
5. **Print Status Overview:** Render complete workspace diagnostic overview card.

---

## Failure Recovery

- **Uninitialized Workspace:** If config is missing, prompt user to execute `/torusguard init`.
- **Zero Runs Found:** Display clean status card noting no historical audit runs exist yet.
- **Corrupt Config File:** Report parsing error and recommend re-running `/torusguard init`.
- **Halt Trigger:** Abort command if read access to `.torusguard/` is denied.

---

## Hallucination Guard

- ❌ Never display fabricated finding counts not substantiated by run manifests.
- ❌ Never execute modifying shell commands or edit source code during status inspection.
- ✅ Always report factual file counts from `.torusguard/rules/active/` and `.torusguard/runs/`.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Workspace Status
- **Version:** v0.9.2
- **Framework Detected:** [Stack or None]
- **Active Rules:** [Count] rules active in `.torusguard/rules/active/`
- **Total Runs:** [Count] historical runs recorded
- **Latest Run:** `run-YYYYMMDD-HHMMSS` ([Findings Count] findings)
- **Scope Status:** [Authorized (TTL Active) / Expired / Unconfigured]
- **Health Posture:** [GOOD / ACTION NEEDED]
```

---

## Next Steps

1. Run `/torusguard audit` to scan codebase for security vulnerabilities.
2. Run `/torusguard authorize` to configure or refresh live target scope.
