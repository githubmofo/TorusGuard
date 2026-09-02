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
  - .torusguard/scripts/diff_guard.py
---

# /torusguard apply — Governed Patch Application & Rollback Snapshot

$ARGUMENTS

---

## Objective
Governed patch application with pre-apply rollback snapshots and Human Gate authorization.

---

## Mandatory Pre-Flight Context Inspection

Inspect bundle validity and file safety before modifying disk code:
1. **Bundle Verification:** Assert `patch.diff` exists in active run's remediation folder.
2. **Pre-Apply Snapshot:** Save a byte-for-byte backup copy (`.bak` or `pre_apply/`) prior to editing.
3. **Uncommitted Changes:** Check git status; ensure target file has clean baseline.
4. **Ponytail Check:** Re-verify that patch additions $\le 35$ and deletions $\le 25$.
5. **Human Gate:** Confirm operator approval before committing edits to disk.
6. **Workspace Cleanliness:** Verify git working tree has no uncommitted merge conflicts.
7. **Execution Privilege:** Verify write access to targeted file locations.

---

## When to Use /torusguard apply

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Applying an approved remediation patch to disk | Run `/torusguard apply` |
| Generating patch diff without modifying disk | Run `/torusguard harden` |
| Verifying that patch eliminated flaw without regression | Run `/torusguard recheck` |
| Reverting an applied patch | Restore from `.bak` snapshot |
| Checking workspace status | Run `/torusguard status` |

---

## Execution Steps

1. **Load Remediation Bundle:** Read `patch.diff` and metadata from active run directory.
2. **Audit Patch Invariants:** Run `python .torusguard/scripts/diff_guard.py <patch.diff>`.
3. **Create Rollback Backup:** Copy target file to `.torusguard/runs/<run_id>/pre_apply/<filename>.bak`.
4. **Apply Minimal Diff:** Execute precise surgical edit using `replace_file_content` or `patch`.
5. **Assert Syntax & Integrity:** Check that modified file compiles cleanly without syntax errors.
6. **Log Application Ledger:** Record timestamp, original SHA-256, and patched SHA-256 in `apply-log.json`.

---

## Failure Recovery

- **Syntax Error After Patch:** Instantly revert target file from `.bak` backup snapshot.
- **Merge / Context Conflict:** Re-run `/torusguard harden` to regenerate diff against latest disk lines.
- **Missing Backup File:** Do not apply patch if backup copy cannot be written.
- **Halt Trigger:** Abort if git working tree is dirty on conflicting lines.

---

## Hallucination Guard

- ❌ Never apply code changes without creating an exact pre-apply rollback backup first.
- ❌ Never touch files not explicitly listed in the approved `patch.diff`.
- ✅ Always verify syntax compilation immediately after modifying source files.

---

## Output Card Format

```markdown
### 🚀 TorusGuard Patch Application
- **Finding Addressed:** `TG-XXX-HASH`
- **File Patched:** `src/path/to/file.py`
- **Rollback Backup:** `.torusguard/runs/<run_id>/pre_apply/<file>.bak`
- **Churn Applied:** +[Additions] / -[Deletions] lines
- **Syntax Check:** PASSED (clean compile)
- **Status:** APPLIED — run `/torusguard recheck` to verify fix
```

---

## Next Steps

1. Run `/torusguard recheck` to perform differential audit on the modified file.
2. Run test suites to verify that business logic and regressions remain intact.
