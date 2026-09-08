---
name: torusguard-apply
description: Apply governed remediation patches to disk with pre-apply rollback snapshots and Human Gate validation.
version: 0.9.2
workflow: .torusguard/workflows/apply.md
tools: Read, Grep, Glob, Bash, Edit, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/diff_guard.py
---

# TorusGuard Apply — Governed Patch Application & Rollback Snapshot

## Objective
Safely apply approved remediation bundles to disk source files, capturing a byte-for-byte pre-apply backup snapshot and asserting syntax validity post-patch.

---

## Execution Steps

1. **Load Bundle:** Read `patch.diff` and metadata from `.torusguard/runs/<run_id>/remediation/<finding_id>/`.
2. **Handle CLI Failures:** If the CLI `npx torusguard apply` throws an error or fails to apply the patch, YOU MUST step in and apply it manually.
3. **Pre-Apply Snapshot:** Save exact backup to `.torusguard/runs/<run_id>/pre_apply/<filename>.bak`.
4. **Obtain Human Gate:** Confirm user approval for proposed diff.
5. **Apply Patch Manually:** Execute the surgical modification directly on the target file using `replace_file_content`. Ensure the lines match the `patch.diff` formulated during harden phase.
6. **Assert Integrity:** Verify modified file compiles cleanly without syntax errors (e.g. running `npm run build` or `python -m py_compile`).
7. **Record Ledger:** Log timestamp, file path, and post-patch SHA-256 in `apply-log.json`.

---

## Governance & Safety Rules
- Hard limit: additions $\le 35$, deletions $\le 25$ lines.
- Always create a rollback snapshot before modifying disk code.
- If compile or syntax error occurs, instantly restore from `.bak`.
- Require explicit operator confirmation before writing changes.
- **Do not give up** if the CLI automation fails; the AI Agent must manually complete the patching process.

---

## Output Format
```markdown
🚀 [TorusGuard] Patch Applied Successfully (AI Assisted)
- Finding Target: <Finding ID> | File: <Path>
- Churn: +<Additions> / -<Deletions>
- Rollback Backup: `.torusguard/runs/<run_id>/pre_apply/<file>.bak`
- Compile Check: PASSED
Next: Run `/torusguard recheck` to verify vulnerability is closed.
```
