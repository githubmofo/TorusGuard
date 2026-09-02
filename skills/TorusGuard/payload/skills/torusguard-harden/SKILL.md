---
name: torusguard-harden
description: Package surgical remediation bundles conforming to the Ponytail Protocol (<= 35 additions, <= 25 deletions).
version: 0.9.2
workflow: .torusguard/workflows/harden.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Harden — Governed Remediation & Bundle Packaging

## Objective
Formulate minimal, surgical code fixes for confirmed vulnerabilities strictly bound by the Ponytail Protocol line churn constraints ($\le 35$ additions, $\le 25$ deletions), packaging unified diffs into auditable 4-artifact remediation bundles ready for human review.

---

## The Ponytail Protocol (Governed Patch Limits)

To prevent code bloat, architectural drift, and accidental regressions, TorusGuard enforces hard line churn limits:

```
┌────────────────────────────────────────────────────────┐
│               PONYTAIL PROTOCOL BOUNDS                 │
├────────────────────────────────────────────────────────┤
│ • Additions: <= 35 lines per bundle                    │
│ • Deletions: <= 25 lines per bundle                    │
│ • Zero full-file rewrites                              │
│ • Preserve all existing auth checks & error handling   │
│ • Preserve existing public API contracts               │
└────────────────────────────────────────────────────────┘
```

If a proposed fix exceeds these limits:
- Partition the fix into sequential sub-bundles (Bundle A, Bundle B), OR
- Escalate the finding as `Requires Manual Architectural Refactor`.

---

## Execution Steps

### Step 1: Select Target Finding
Identify target finding from `.torusguard/runs/<latest-run>/findings.md`:
- Prioritize `Confirmed` and `High Confidence` findings.
- Isolate the exact vulnerable function or code block.

### Step 2: Formulate Surgical Unified Diff
Generate a minimal patch addressing the root cause:
- **SQL Injection**: Replace string concatenation with bound parameters (`?` or `:param`).
- **Tenant Isolation**: Append `.filter(tenant=request.user.tenant)` or equivalent scoping clause.
- **Input Validation**: Insert schema parser (`UserCreateSchema.model_validate(data)` or Zod schema).
- **Cookie Security**: Add `httponly=True, secure=True, samesite="Lax"` flags.

### Step 3: Validate Line Churn
Calculate diff line counts:
- Verify additions $\le 35$ and deletions $\le 25$.
- Confirm surrounding code remains unformatted and unchanged.

### Step 4: Package Remediation Bundle
Create bundle folder under active run: `.torusguard/runs/<run-id>/patches/<bundle-id>/` containing:
1. `patch.diff`: Unified diff compatible with `git apply`.
2. `metadata.json`: Bundle ID, targeted finding IDs, line counts, and author role.
3. `explanation.md`: Root-cause analysis, fix justification, and risk assessment.
4. `pre_apply/`: Empty directory reserved for rollback snapshot capture during apply.

### Step 5: Prepare Human Gate Preview
Present diff and explanation to the operator for review.

---

## Bundle Directory Structure
```
.torusguard/runs/<run-id>/patches/<bundle-id>/
├── patch.diff          # Unified diff
├── metadata.json       # Bundle metadata and churn metrics
├── explanation.md      # Technical justification
└── pre_apply/          # Staging for pre-apply rollback backup
```

---

## Safety Constraints
- **Zero Disk Writes to Project Code**: Never modify source code during the harden phase (writing is strictly reserved for `/torusguard apply`).
- **Strict Churn Caps**: Reject any bundle exceeding Ponytail Protocol bounds.
- **Preserve Error Handling**: Never remove existing try/catch blocks, error loggers, or input sanitizers.

---

## Output Format
```markdown
🛡️ [TorusGuard] Remediation Bundle Formulated
- Bundle ID: <bundle-id>
- Target File: <file_path>
- Targeted Finding: <finding_id>
- Ponytail Bounds: +<additions> lines (limit: 35) ✅ | -<deletions> lines (limit: 25) ✅
- Sensitive Path: <Yes/No>
- Bundle Path: .torusguard/runs/<run-id>/patches/<bundle-id>/

Next Step: Run `/torusguard apply <bundle-id>` to review and write patch to disk.
```
