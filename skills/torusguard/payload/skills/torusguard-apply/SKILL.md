---
name: torusguard-apply
description: Apply governed remediation patches to disk with pre-apply rollback snapshots and Human Gate validation via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/apply.md
tools: Read, Grep, Glob, Write, replace_file_content, run_command
scripts-binding:
  - internal/apply/apply.go
  - internal/apply/snapshot.go
  - internal/apply/rollback.go
  - cmd/torusguard/main.go
---

# TorusGuard Apply — Governed Patch Application & Rollback Snapshot

## Objective
Safely apply approved remediation bundles to disk source files, creating an automated byte-for-byte pre-apply backup snapshot (`.bak`) in `.torusguard/snapshots/<run_id>/`, asserting syntax validity, and distilling passing patterns into Golden Fix Recipes.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution (Interactive or Non-Interactive)
Run the governed patch applier from your terminal:
```bash
# Non-interactive automated application of unified diff or semantic patch
torusguard apply candidate.patch --yes
# or
torusguard apply patch.json --yes

# Emergency rollback from pre-apply snapshot
torusguard rollback
```
**Under the Hood:** Executes compiled Go apply engine (`internal/apply`).
1. Supports both unified diff files (`git apply`) and Semantic Reflection JSON patches (`harden.ReflectAndVerify`).
2. Creates byte-for-byte snapshot in `.torusguard/snapshots/<run_id>/<rel_path>.bak`.
3. Performs line-aware replacement without corrupting concurrent modifications.
4. Distills the applied fix into a **Golden Fix Recipe** registered in persistent memory.
5. Displays pixel-perfect 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Application
When applying patches directly within an AI chat session:
1. **Human Gate Confirmation:** Present the semantic patch or unified diff to the operator and request explicit approval before editing code.
2. **Pre-Apply Snapshot:** Ensure target file backup is created at `.torusguard/snapshots/<run_id>/<rel_path>.bak`.
3. **Deterministic Reflection Execution:** Leverage Go CLI `torusguard apply <patch.json> --yes` or `replace_file_content` with exact verbatim strings.
4. **Syntax & Integrity Check:** Verify that the patched file compiles and runs clean (`go test ./...`, `npm test`, or syntax linter). If syntax fails, immediately restore from `.bak`.
5. **Memory Registration:** Update persistent memory events in `.torusguard/memory/events.json` with event `fix_applied`.
6. **Recommend Recheck:** Advise running `/torusguard recheck` or `torusguard recheck` to verify closure.

### Mode C: Native MCP Tool Integration
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Remediation Validation:** First validate the patch via `torusguard_harden`.
- **Governed Application:** Autonomous tools respect the **Human Gate Invariant**; agents invoke terminal command `torusguard apply candidate.patch --yes` upon receiving explicit user confirmation.
- **Rollback Safety:** If any test fails, run `torusguard rollback` to restore pre-apply `.bak` snapshots instantly.

---

## Rollback Guarantee
If an applied patch introduces unexpected runtime behavior or breaks tests:
```bash
# Instant one-command rollback of the latest applied run:
torusguard rollback
```
All affected files are restored byte-for-byte from `.torusguard/snapshots/<run_id>/`.

---

## Output Card Format
```markdown
### 🚀 TorusGuard Patch Applied Successfully
- **Target File:** `server/index.js:9`
- **Rule ID:** `TG-SEC-001` (Hardcoded JWT secret)
- **Ponytail Churn:** +1 / -1
- **Engine:** Line-Level Reflection Match (Alibaba OpenCodeReview Hybrid Pipeline)
- **Rollback Snapshot:** `.torusguard/snapshots/<run_id>/server/index.js.bak`
- **Golden Recipe:** Distilled into persistent memory
- **Next Step:** Run `torusguard recheck` or `/torusguard recheck` to verify closure
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Skipping Pre-Apply Snapshot** | Modifies files on disk before creating a `.bak` backup in `.torusguard/snapshots/`. | Always capture a byte-for-byte snapshot before writing any modified content. |
| **Bypassing Human Gate** | Applies changes to disk without presenting the diff preview to the operator. | Require explicit confirmation or `--yes` flag before altering source code. |
| **Blind Unified Diff Rejection** | Uses standard `git apply` which fails on CRLF/LF line-ending differences or offset drift. | Use the Line-Level Reflection Module (`SemanticPatch`) with exact substring replacement. |
| **Leaving Broken Build Unchecked** | Leaves file modified even if project tests or compilation fails after patch. | Run immediate integrity checks; trigger `torusguard rollback` if regression is introduced. |

---

## ✅ Pre-Flight Self-Audit

Before modifying code on disk, verify:
- [ ] Did the operator provide explicit approval for this specific change?
- [ ] Has a pre-apply `.bak` backup been saved in `.torusguard/snapshots/<run_id>/`?
- [ ] Does the edit strictly touch only the vulnerable lines without unrelated changes?
- [ ] Did I verify line matches using the Line-Level Reflection Module?
- [ ] Is there an instant rollback path ready if tests fail?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Confirm operator approval and verify target file snapshot is captured on disk.
BUILD:  Apply surgical replacement via torusguard apply or exact replace_file_content.
CONFIRM: Run project test suite; execute torusguard recheck to mark finding Confirmed Fixed.
```
