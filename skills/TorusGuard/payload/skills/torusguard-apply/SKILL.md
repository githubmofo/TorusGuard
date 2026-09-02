---
name: torusguard-apply
description: Apply governed remediation patch to disk with pre-apply rollback snapshots and Human Gate authorization.
version: 0.9.2
workflow: .torusguard/workflows/apply.md
tools: Read, Grep, Glob, Bash, Edit, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Apply — Governed Patch Application & Rollback Snapshot

## Objective
Apply a reviewed remediation bundle to disk with mandatory Human Gate approval, preserving a byte-for-byte pre-apply rollback snapshot before any source file is modified.

---

## Execution Steps

### Step 1: Bundle Validation
1. Read `.torusguard/runs/<run-id>/patches/<bundle-id>/metadata.json`.
2. Confirm target file exists on disk and has not changed since bundle formulation.
3. Validate patch line churn is within Ponytail Protocol bounds ($\le 35$ add, $\le 25$ del).

### Step 2: Human Gate Authorization
Display diff preview to operator and request explicit approval:
```markdown
⚠️ HUMAN GATE: Approve patch application to disk?
Target: <target_file> (+<add> / -<del>)
Y = Approve and Write | N = Abort | R = Revise
```
If not approved, abort immediately leaving files untouched.

### Step 3: Capture Pre-Apply Snapshot
Before modifying the source file, archive an exact backup copy:
```bash
python -c "import shutil, os; dst = '.torusguard/runs/<run-id>/patches/<bundle-id>/pre_apply/<file_basename>.bak'; os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile('<target_file>', dst)"
```

### Step 4: Apply Surgical Modification
Apply the diff surgically using file replacement tools or `git apply`:
- Only replace the exact lines specified in the bundle.
- Preserve file indentation, whitespace, and formatting conventions.
- Immediately re-read the file to confirm clean application.

### Step 5: Update Audit State
Record `applied: true`, timestamp, and git commit SHA in `metadata.json`.

---

## Governance & Safety Rules
- **Mandatory Human Gate**: No code is written to disk without explicit operator approval.
- **Rollback Guarantee**: Every patch MUST have a verified `pre_apply/<file>.bak` snapshot before disk modification.
- **Instant Rollback on Failure**: If syntax errors or test regressions occur post-apply, restore the snapshot immediately:
  ```bash
  python -c "import shutil; shutil.copyfile('.torusguard/runs/<run-id>/patches/<bundle-id>/pre_apply/<file_basename>.bak', '<target_file>')"
  ```
- **Single-File Scope**: Each apply operation modifies exactly one target file.

---

## Output Format
```markdown
🛡️ [TorusGuard] Patch Applied to Disk
- Bundle ID: <bundle-id>
- Target File: <target_file>
- Pre-Apply Backup: .torusguard/runs/<run-id>/patches/<bundle-id>/pre_apply/<filename>.bak
- Line Churn: +<additions> / -<deletions>
- Application Status: ✅ SUCCESSFUL

Next Step: Run `/torusguard recheck` to verify fix integrity and detect regressions.
```
