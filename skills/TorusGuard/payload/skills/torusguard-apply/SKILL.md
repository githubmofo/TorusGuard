---
name: torusguard-apply
description: Apply governed remediation patches to disk with pre-apply rollback snapshots and Human Gate validation.
version: 0.9.2
workflow: .torusguard/workflows/apply.md
tools: Read, Grep, Glob, Bash, Edit, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Apply — Governed Patch Application & Rollback Snapshot

## Objective
Safely apply approved remediation bundles to disk source files, capturing a byte-for-byte pre-apply backup snapshot and asserting syntax validity post-patch.

---

## Execution Steps

1. **Load Bundle:** Read `patch.diff` and metadata from `.torusguard/runs/<run_id>/remediation/<finding_id>/`.
2. **Pre-Apply Snapshot:** Save exact backup to `.torusguard/runs/<run_id>/pre_apply/<filename>.bak`.
3. **Obtain Human Gate:** Confirm user approval for proposed diff.
4. **Apply Patch:** Execute surgical modification using `replace_file_content` or `patch`.
5. **Assert Integrity:** Verify modified file compiles cleanly without syntax errors.
6. **Record Ledger:** Log timestamp, file path, and post-patch SHA-256 in `apply-log.json`.

---

## Governance & Safety Rules
- Hard limit: additions $\le 35$, deletions $\le 25$ lines.
- Always create a rollback snapshot before modifying disk code.
- If compile or syntax error occurs, instantly restore from `.bak`.
- Require explicit operator confirmation before writing changes.

---

## Output Format
```markdown
🚀 [TorusGuard] Patch Applied Successfully
- Finding Target: <Finding ID> | File: <Path>
- Churn: +<Additions> / -<Deletions>
- Rollback Backup: `.torusguard/runs/<run_id>/pre_apply/<file>.bak`
- Compile Check: PASSED
Next: Run `/torusguard recheck` to verify vulnerability is closed.
```
