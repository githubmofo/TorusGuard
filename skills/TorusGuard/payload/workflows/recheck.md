---
description: Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: reviewer
lifecycle-phase: Phase 6 (Targeted Recheck & Verification)
required-skills:
  - torusguard-recheck
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# /torusguard recheck — Targeted Differential Recheck & Regression Audit

$ARGUMENTS

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Mandatory Pre-Flight Context Inspection

Before running a targeted differential recheck, you MUST inspect:

1. **Applied Patches Ledger** → Confirm that a patch was applied during the active or recent run (`patches/<bundle-id>/metadata.json` with `applied: true`).
2. **Modified File Identification** → Identify the exact list of files modified by the applied patches.
3. **AST Scan Scope Restriction** → Restrict the differential scan strictly to modified files and their direct callers to save token budget.
4. **4-State Transition Engine** → Prepare to classify each targeted finding into: `Fixed`, `Partially Fixed`, `Not Fixed`, or `Regression`.

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## When to Use /torusguard recheck

| Use `/torusguard recheck` when... | Use something else when... |
| :--- | :--- |
| Immediately after applying a patch bundle | Before applying changes → `/torusguard apply` |
| Verifying that a specific vulnerability is closed | Scanning whole repo from scratch → `/torusguard audit` |
| Checking for introduced regressions | Exporting final compliance SARIF → `/torusguard report` |
| Auditing fix integrity | Full pipeline execution → `/torusguard full` |

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Execution Steps (Fixed Order)

### Phase 1 — Scope Isolation to Modified Files
1. Read `metadata.json` from the applied remediation bundle.
2. Identify target file(s) modified on disk.
3. Confirm the files exist and contain valid syntax (`python -m py_compile <file>` or `npx tsc --noEmit`).

### Phase 2 — Targeted AST & Heuristic Re-Scan
Re-scan the modified file specifically for the original rule violation:
- Check if vulnerable AST node still exists.
- Verify that safe pattern is properly implemented (e.g., tenant filter exists, query is parameterized, schema validation is active).

### Phase 3 — Neighboring Regression Scan
Scan surrounding 50 lines and direct callers for introduced regressions:
- New syntax errors, broken imports, or missing variable definitions.
- New security rule violations (e.g., unintended bypasses or dropped decorators).

### Phase 4 — 4-State Transition Evaluation
Classify outcome for each targeted finding:
1. **`Confirmed Fixed`**: Original vulnerable AST node eliminated; safe pattern verified; zero regressions.
2. **`Partially Fixed`**: Vulnerability partially mitigated, but edge cases remain (e.g., sanitized for GET but not POST).
3. **`Not Fixed`**: Vulnerable AST node remains intact; patch was ineffective.
4. **`Regression`**: Original flaw or a new flaw was introduced by the code change.

### Phase 5 — Record Recheck Artifacts
Write recheck outcomes to active run folder:
- `recheck.md`: Breakdown of transitions for each finding.
- Update `manifest.json` with closure metrics (`fixed_count`, `remaining_count`).

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Failure Recovery & Cascade Rules

```
Regression detected:      ALERT operator immediately; offer instant rollback to pre_apply/ snapshot
Syntax error in file:     ROLLBACK immediately using pre_apply/<file>.bak snapshot
Finding Still Not Fixed:  Reopen finding; recommend alternative remediation strategy
All findings Fixed:       Mark bundle verified; proceed to /torusguard report
```

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Hallucination Guard

```
❌ Never mark a finding as 'Fixed' without re-reading the active disk file
❌ Never skip the neighboring regression check around the modified lines
❌ Never ignore a regression — escalate immediately to Human Gate with rollback option
```

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Targeted Recheck & Regression Audit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target File:        [apps/invoices/views.py]
Tested Findings:    [1 finding re-scanned]
Outcome:            🟢 CONFIRMED FIXED (0 Regressions Detected)
Syntax Check:       ✅ Clean compilation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Finding Status Transition:
- TG-DB-004-django-tenant-idor:
  Before: 🔴 Confirmed (Score: 90)
  After:  🟢 CONFIRMED FIXED (Tenant query scoping verified)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard report` to export the signed audit report and SARIF log.
```

---

## Objective
Targeted differential AST re-scan, fix closure verification, and regression state machine transitions.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| All targeted findings Fixed | → `/torusguard report` to generate SARIF |
| Regression detected | → Roll back from snapshot or `/torusguard harden` |
| More patches to apply | → `/torusguard apply <next-bundle>` |
