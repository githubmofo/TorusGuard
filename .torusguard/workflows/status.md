# /torusguard status — Project Security Posture & Run History

**Command:** `/torusguard status`  
**Primary Agent:** *System*  
**Lifecycle Phase:** Monitoring & Status

---

## Objective
Inspect the workspace state, display the active configuration, summarize recent run history, list activated security rules, and report the current project security posture.

---

## Execution Steps

### Step 1: Inspect Workspace Configuration
1. Read `.torusguard/config/torusguard.json`.
2. Confirm active severity thresholds, patch boundaries, and runtime settings.

### Step 2: Enumerate Run History
1. Scan `.torusguard/runs/` for past run folders.
2. For each run, read `manifest.json` to extract:
   - Timestamp and command type.
   - Total finding count.
   - Status counts (Confirmed, Remediated, Rechecked Fixed).

### Step 3: Count Active Rules
1. Inspect `.torusguard/rules/active/`.
2. Count activated rule definitions and group by rule category (AUTH, INPUT, SEC, DB, PLATFORM, etc.).

### Step 4: Display Posture Summary
Output formatted status overview:
```markdown
🛡️ TorusGuard Status Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Workspace Version: v0.8.0
- Active Rules: <Count> rules active in .torusguard/rules/active/
- Total Runs Completed: <Run Count>
- Latest Run: run-<timestamp> (<Command>)
- Posture Indicator: 🟢 Ready / 🔴 Action Required

Recent Execution History:
| Run ID | Command | Total Findings | Confirmed Fixed | Date |
| :--- | :--- | :---: | :---: | :--- |
| run-20260902-120000 | audit | 4 | 0 | 2026-09-02 |
| run-20260902-121500 | apply | 4 | 4 | 2026-09-02 |
```
