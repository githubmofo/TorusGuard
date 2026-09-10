---
name: torusguard-apply
description: Apply governed remediation patches to disk with pre-apply rollback snapshots and Human Gate validation via CLI or AI Agent.
version: 1.3.4
workflow: .torusguard/workflows/apply.md
tools: Read, Grep, Glob, Write, replace_file_content, run_command
scripts-binding:
  - .torusguard/scripts/apply_runner.py
  - .torusguard/scripts/term_ui.py
  - .torusguard/scripts/memory_engine.py
---

# TorusGuard Apply — Governed Patch Application & Rollback Snapshot

## Objective
Safely apply approved remediation bundles to disk source files, creating an automated byte-for-byte pre-apply backup snapshot (`.bak`) in `.torusguard/snapshots/<run_id>/`, asserting syntax validity, and distilling passing patterns into Golden Fix Recipes.

---

## Two Execution Modes

### Mode A: Automated CLI Execution (Interactive or Non-Interactive)
Run the governed patch applier from your terminal:
```bash
# Interactive Human Gate review (prompts for each patch: [y]es / [n]o / [a]ll / [q]uit)
npx torusguard apply

# Non-interactive automated application
npx torusguard apply --yes

# Apply patches from a specific run ID
npx torusguard apply --run run-20260910-121618-audit --yes

# Emergency rollback from pre-apply snapshot
npx torusguard rollback
# or
npx torusguard apply --rollback
```
**Under the Hood:** Executes `python .torusguard/scripts/apply_runner.py`.
1. Reads candidate bundles from `.torusguard/runs/<run_id>/bundles/`.
2. Creates `.bak` snapshot in `.torusguard/snapshots/<run_id>/<rel_path>.bak`.
3. Performs line-aware replacement without corrupting concurrent modifications.
4. Distills the applied fix into a **Golden Fix Recipe** registered in `.torusguard/memory/patterns.json`.
5. Emits `diff_summary.md` and `apply_plan.md` in the run directory.
6. Displays pixel-perfect 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Application
When applying patches directly within an AI chat session:
1. **Human Gate Confirmation:** Present the unified diff to the operator and request explicit approval before editing code.
2. **Pre-Apply Snapshot:** Ensure target file backup is created at `.torusguard/snapshots/<run_id>/<rel_path>.bak`.
3. **Execute Surgical Edit:** Use `replace_file_content` to apply only the approved lines. Strictly adhere to the formulated Ponytail diff.
4. **Syntax & Integrity Check:** Verify that the patched file is syntactically valid (e.g. `node --check <file>` or `python -m py_compile <file>`). If syntax fails, immediately restore from `.bak`.
5. **Memory Registration:** Update persistent memory events in `.torusguard/memory/events.json` with event `fix_applied`.
6. **Recommend Recheck:** Advise running `/torusguard recheck` or `npx torusguard recheck` to verify closure.

---

## Rollback Guarantee
If an applied patch introduces unexpected runtime behavior or breaks tests:
```bash
# Instant one-command rollback of the latest applied run:
npx torusguard rollback

# Or rollback a specific run:
npx torusguard rollback --run run-20260910-121618-audit
```
All affected files are restored byte-for-byte from `.torusguard/snapshots/<run_id>/`.

---

## Output Card Format
```markdown
### 🚀 TorusGuard Patch Applied Successfully
- **Target File:** `server/index.js:9`
- **Rule ID:** `TG-SEC-001` (Hardcoded JWT secret)
- **Ponytail Churn:** +1 / -1
- **Rollback Snapshot:** `.torusguard/snapshots/<run_id>/server/index.js.bak`
- **Golden Recipe:** Distilled into persistent memory
- **Next Step:** Run `npx torusguard recheck` or `/torusguard recheck` to verify closure
```
