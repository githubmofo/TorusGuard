# /torusguard apply — Surgical Governed Patch Application

**Command:** `/torusguard apply [bundle_id]`  
**Primary Agent:** `remediator` (`.torusguard/agents/remediator.md`)  
**Lifecycle Phase:** Phase 5 (Patch Application)

---

## Objective
Apply a validated, bounded remediation patch cleanly to the target source file, preserving existing error handling and authorization logic, and creating pre-apply rollback backups.

---

## Execution Steps

### Step 1: Bundle Selection & Pre-Flight Review
1. Load candidate bundle from `.torusguard/runs/<latest>/bundles/<bundle_id>/`.
2. Inspect `candidate.patch` and verify:
   - Additions $\le 35$ lines.
   - Deletions $\le 25$ lines.
   - Target files currently exist and match expected pre-patch content.
3. Display the unified diff to the developer for explicit confirmation.

### Step 2: Create Rollback Backup
Save original file snapshots into `.torusguard/runs/<latest>/patches/backup-<timestamp>/`.

### Step 3: Surgical Patch Application
1. Apply changes surgically to the target lines.
2. Avoid whole-file overwrites.
3. Ensure formatting and indentation match the surrounding file conventions.

### Step 4: Verification & Handoff
1. Verify syntax of modified files (e.g. `python -m py_compile <file>`).
2. Record applied patch details into `manifest.json`.
3. Output result:
   ```markdown
   ✅ [TorusGuard] Patch Applied Successfully!
   - Bundle: <bundle_id>
   - Files Modified: <list of files>
   - Lines Changed: +<additions> / -<deletions>
   - Backup Saved: .torusguard/runs/<run-id>/patches/
   
   Next Step: Run `/torusguard recheck` to verify the fix and check for regressions.
   ```
