---
name: torusguard-status
description: Diagnostic read-only inspection of active workspace security posture, configuration, active rules, and run history.
version: 0.9.2
workflow: .torusguard/workflows/status.md
tools: Read, Grep, Glob, Bash
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Status — Workspace Posture & Diagnostic Overview

## Objective
Provide a quick, strictly read-only inspection of the current workspace security posture, active framework-tailored rules, authorization scope state, and historical run ledger without modifying any files or settings.

---

## Execution Steps

### Step 1: Read Project Configuration
Open `.torusguard/config/torusguard.json`:
- Read project name, version, and detected framework.
- If file is missing, inform operator that the workspace has not yet been initialized.

### Step 2: Audit Active Rules on Disk
Inspect `.torusguard/rules/active/`:
- Count active rule specification files.
- Group active rules by family (`TG-SEC`, `TG-INPUT`, `TG-AUTH`, `TG-DB`, `TG-RATE`, `TG-CLIENT`, `TG-PLATFORM`).

### Step 3: Check Runtime Scope State
Open `.torusguard/config/scope.json`:
- Check if target host and paths are defined.
- Compare `ttl_expiration` with current UTC time to determine if authorization is `Active`, `Expired`, or `Unconfigured`.

### Step 4: Inspect Run Ledger History
Scan `.torusguard/runs/`:
- Count total recorded runs.
- Locate the most recent run folder.
- Read `manifest.json` from the latest run to extract:
  - Last scan timestamp.
  - Finding counts (total, open, fixed).
  - Executive posture classification.

### Step 5: Format Diagnostic Summary Card
Present the consolidated status card to the operator.

---

## Safety Constraints
- **Strictly Read-Only**: Never create, edit, or delete any files during a status check.
- Never report stale or cached run metrics if the runs folder is empty.
- Do not trigger network traffic or probe endpoints.

---

## Output Format
```markdown
🛡️ [TorusGuard] Workspace Security Posture Overview
- Version: 0.9.2
- Detected Stack: <Framework> (<Language>) · <ORM>
- Active Rules: <Count> tailored rules active in .torusguard/rules/active/
- Runtime Scope: <Active until YYYY-MM-DD HH:MM | Expired | Unconfigured>
- Run History: <Count> runs logged in .torusguard/runs/

Latest Run (<run-id>):
- Last Scanned: <Timestamp>
- Posture: <🟢 SECURE | 🔴 ACTION REQUIRED | 🟡 WARNINGS>
- Findings: <Open> Open · <Fixed> Fixed

Next Step: Run `/torusguard audit` to start a new scan.
```
