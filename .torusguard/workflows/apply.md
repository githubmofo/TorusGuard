---
description: Governed patch application with pre-apply rollback snapshots and Human Gate authorization.
tools: Read, Grep, Glob, Bash, Edit, Write, run_command
version: 2.0.0
agent: remediator
lifecycle-phase: Phase 5 (Patch Application)
required-skills:
  - torusguard-apply
scripts-binding:
  - internal/apply/apply.go
  - cmd/torusguard/main.go
---

# /torusguard apply — Governed Patch Application & Rollback Snapshot

$ARGUMENTS

---

## Objective
Safely apply approved remediation bundles to disk source files, creating an automated byte-for-byte pre-apply backup snapshot (`.bak`) in `.torusguard/snapshots/<run_id>/`, asserting syntax validity, and distilling passing patterns into Golden Fix Recipes.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard apply candidate.patch [--yes]` | Shell execution of patch applier with snapshot creation. |
| **Mode B: AI Chat Slash** | `/torusguard apply` | Guided conversational application with explicit Human Gate approval. |
| **Mode C: Native MCP Tool** | Autonomous Agent Flow | Formulates patch with `torusguard_harden`, awaits Human Gate, invokes CLI. |

---

## Mandatory Pre-Flight Context Inspection

Inspect bundle validity and file safety before modifying disk code:
1. **Bundle Verification:** Assert `candidate.patch` or semantic `patch.json` exists.
2. **Pre-Apply Snapshot:** Save a byte-for-byte backup copy (`.torusguard/snapshots/<run_id>/<rel_path>.bak`) prior to editing.
3. **Uncommitted Changes:** Check git status; ensure target file has clean baseline.
4. **Ponytail Check:** Re-verify that patch additions $\le 35$ and deletions $\le 25$.
5. **Human Gate:** Confirm operator approval before committing edits to disk.

---

## Living Report Invariant
- Applied patches create pre-apply `.bak` snapshots in `.torusguard/snapshots/<run_id>/`.
- Finding statuses transition in `security_report.md` to `APPLIED 🔵`.
- Instant rollback available via `torusguard rollback`.

---

## Execution Steps

1. **Load Remediation Bundle:** Read `candidate.patch` or `patch.json`.
2. **Obtain Human Gate:** Confirm user approval to modify target source file.
3. **Create Rollback Backup:** Capture `.bak` in `.torusguard/snapshots/<run_id>/`.
4. **Apply Surgical Edit:** Run `torusguard apply <patch> --yes` or apply semantic reflection.
5. **Assert Syntax & Integrity:** Check that modified file compiles cleanly (`go test ./...`, syntax lint).
6. **Recommend Recheck:** Run `torusguard recheck` or `/torusguard recheck`.

---

## Output Card Format

```markdown
### 🚀 TorusGuard Patch Applied Successfully
- **Target File:** `src/path/to/file`
- **Backup Snapshot:** `.torusguard/snapshots/<run_id>/<file>.bak`
- **Rollback Command:** `torusguard rollback`
- **Next Step:** Run `/torusguard recheck` to verify closure
```

---

## Next Steps

1. Run `/torusguard recheck` or `torusguard recheck` to verify closure and zero regressions.
2. If unexpected behavior occurs, run `torusguard rollback`.
