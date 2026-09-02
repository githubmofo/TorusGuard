---
description: Governed patch application with pre-apply rollback snapshots and Human Gate authorization.
tools: Read, Grep, Glob, Bash, Edit, Write
version: 0.9.2
agent: remediator
lifecycle-phase: Phase 5 (Patch Application)
required-skills:
  - torusguard-apply
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# /torusguard apply — Governed Patch Application & Rollback Snapshot

$ARGUMENTS

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Mandatory Pre-Flight Context Inspection

Before applying any code patch to disk, you MUST inspect:

1. **Remediation Bundle Integrity** → Confirm that `patch.diff` and `metadata.json` exist under `.torusguard/runs/<run-id>/patches/<bundle-id>/`.
2. **Current Disk State Check** → Check if the target source file has uncommitted changes or was modified since the bundle was packaged.
3. **Pre-Apply Snapshot Capture** → Ensure a byte-for-byte backup of the target file is saved to `pre_apply/` BEFORE touching the file.
4. **Human Gate Authorization** → Present the exact diff to the operator. Obtain explicit approval before modifying source code.

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## When to Use /torusguard apply

| Use `/torusguard apply` when... | Use something else when... |
| :--- | :--- |
| Writing an approved remediation bundle to disk | Generating the patch diff → `/torusguard harden` |
| Applying surgical security fixes safely | Re-scanning after applying → `/torusguard recheck` |
| Requiring rollback snapshot preservation | Auditing vulnerabilities → `/torusguard audit` |
| Staging governed code changes | Full pipeline → `/torusguard full` |

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Execution Steps (Fixed Order)

### Phase 1 — Load & Validate Remediation Bundle
1. Read `.torusguard/runs/<run-id>/patches/<bundle-id>/metadata.json`.
2. Verify target file path and line churn metrics ($\le 35$ additions, $\le 25$ deletions).
3. Read `patch.diff`.

### Phase 2 — Human Gate Authorization
Display the diff preview to the operator:
```markdown
⚠️ HUMAN GATE APPROVAL REQUIRED
Target File: [path/to/file.py]
Bundle:      [bundle-TG-DB-004]
Lines:       +4 / -2

Apply this patch to disk? (Y = Approve | N = Cancel | R = Revise)
```
Wait for operator input. If rejected (`N`), abort cleanly without disk modification.

### Phase 3 — Pre-Apply Rollback Snapshot Capture
Before writing any change, save an exact copy of the active disk file:
```bash
python -c "import shutil, os; os.makedirs('.torusguard/runs/<run-id>/patches/<bundle-id>/pre_apply', exist_ok=True); shutil.copyfile('<target_file>', '.torusguard/runs/<run-id>/patches/<bundle-id>/pre_apply/<filename>.bak')"
```

### Phase 4 — Surgical Code Modification
Apply the patch using surgical code replacement tools (`replace_file_content` or `git apply`):
- Do not reformat surrounding code.
- Maintain existing indentation and style conventions.
- Immediately re-read the file to confirm clean application.

### Phase 5 — Record Audit State
Update `metadata.json` in the bundle directory with `applied: true`, timestamp, and git commit SHA.

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Failure Recovery & Cascade Rules

```
Operator rejects (N):   ABORT — Record 'Rejected by Human Gate' and leave disk untouched
Patch conflict:         HALT — Target file has drifted. Restore from pre_apply/ snapshot
Syntax / Import error:  ROLLBACK — Restore original file from pre_apply/ snapshot immediately
Rollback procedure:     Copy pre_apply/<file>.bak over target file; confirm clean git diff
```

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Hallucination Guard

```
❌ Never apply a patch without explicit Human Gate approval
❌ Never apply a patch without first archiving a pre_apply/ snapshot
❌ Never modify any file other than the exact target specified in metadata.json
❌ Never leave a project in a broken or uncompilable syntax state
```

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Patch Applied Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bundle ID:          [bundle-TG-DB-004-django-tenant-idor]
Target File:        [apps/invoices/views.py]
Status:             ✅ APPLIED TO DISK
Pre-Apply Snapshot: .torusguard/runs/<run-id>/patches/bundle-TG-DB-004/pre_apply/views.py.bak
Line Churn:         +4 additions / -2 deletions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard recheck` to verify fix integrity and detect regressions.
```

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Patch applied successfully | → `/torusguard recheck` to verify closure |
| Patch caused unexpected failure | → Roll back using snapshot, then `/torusguard harden` |
| Apply next queued bundle | → `/torusguard apply <next-bundle-id>` |
