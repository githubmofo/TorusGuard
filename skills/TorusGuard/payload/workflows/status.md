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
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Mandatory Pre-Flight Context Inspection

Before displaying workspace security status, you MUST inspect:

1. **Workspace Configuration (`.torusguard/config/torusguard.json`)** → Confirm if the project is initialized, check detected stack, and read active rules list.
2. **Active Rules Directory (`.torusguard/rules/active/`)** → Count physically active tailored rules on disk.
3. **Run Folder Ledger (`.torusguard/runs/`)** → Inspect existing run folders and read the most recent run's `manifest.json`.
4. **Scope Authorization State (`.torusguard/config/scope.json`)** → Check if runtime authorization is configured and whether TTL is active or expired.

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## When to Use /torusguard status

| Use `/torusguard status` when... | Use something else when... |
| :--- | :--- |
| Checking workspace configuration and posture | Initializing for the first time → `/torusguard init` |
| Viewing recent audit run history | Scanning codebase for vulnerabilities → `/torusguard audit` |
| Checking active rule families and scope TTL | Formulating code fixes → `/torusguard harden` |
| Diagnostic read-only inspection | Full pipeline execution → `/torusguard full` |

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Execution Steps (Fixed Order)

### Phase 1 — Read Active Configuration
Inspect `.torusguard/config/torusguard.json`:
- Project Name and Version (e.g., `0.9.2`).
- Detected Stack (Language, Framework, ORM, Build Tool).
- Active Rules count and listing.

### Phase 2 — Inspect Active Rules on Disk
Count files inside `.torusguard/rules/active/`:
- Cross-reference active rules with `.torusguard/rules/README.md` catalog.
- Verify that standard rule families (`TG-SEC-*`, `TG-INPUT-*`, `TG-AUTH-*`, `TG-DB-*`) are properly symlinked or defined.

### Phase 3 — Check Runtime Scope & Authorization
Read `.torusguard/config/scope.json`:
- Check `target_host`, `allowed_prefixes`, and `ttl_expiration`.
- Determine whether runtime testing is currently `Active`, `Expired`, or `Unconfigured`.

### Phase 4 — Inspect Run History Ledger
List directories in `.torusguard/runs/`:
- Find most recent run directory.
- Read `manifest.json` from the latest run to extract:
  - Last Scan Timestamp.
  - Findings Count (Total, Open, Fixed).
  - Last Posture (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Secure`).

### Phase 5 — Output Read-Only Diagnostic Summary
Format and display the diagnostic overview card. Strictly read-only; no files are modified.

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Failure Recovery & Cascade Rules

```
Not initialized:     Inform operator: 'Workspace not yet initialized. Run /torusguard init.'
Corrupted config:    Warn operator and offer to refresh configuration via /torusguard init
No runs recorded:    Display 'No previous runs found. Run /torusguard audit to start.'
Scope expired:       Flag as 'Scope Expired (Re-authorize via /torusguard authorize)'
```

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Hallucination Guard

```
❌ Never invent scan counts or fake timestamps when no runs exist
❌ Never modify any files on disk during a status check (strictly read-only)
❌ Never claim rules are active if .torusguard/rules/active/ is empty
```

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Workspace Security Posture Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TorusGuard Version: 0.9.2
Detected Stack:     [Framework] ([Language]) · [ORM]
Active Rules:       [Count] tailored rules active in .torusguard/rules/active/
Runtime Scope:      [Active until YYYY-MM-DD HH:MM | Expired | Unconfigured]
Total Runs Logged:  [Count] runs in .torusguard/runs/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Latest Run Overview:
- Run ID:           [run-YYYYMMDD-HHMMSS-audit]
- Last Scanned:     [Timestamp / Date]
- Posture:          [🟢 Secure / 🔴 Action Required / 🟡 Warnings]
- Open Findings:    [Count]
- Fixed Findings:   [Count]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard audit` to start a new scan.
```

---

## Objective
Read-only diagnostic overview of workspace security posture, active configuration, rules catalog, and run history.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Workspace clean and ready | → `/torusguard audit` to scan code |
| Scope expired or needed | → `/torusguard authorize` |
| Open findings remain | → `/torusguard harden` to formulate patches |
