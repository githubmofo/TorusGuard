---
name: torusguard-harden
description: Package surgical remediation bundles conforming to the Ponytail Protocol (<= 35 additions, <= 25 deletions).
version: 1.0.0
workflow: .torusguard/workflows/harden.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/diff_guard.py
---

# TorusGuard Harden — Governed Remediation & Bundle Packaging

## Objective
Formulate minimal, surgical code fixes bound by the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions), packaging unified diffs into auditable 4-artifact remediation bundles ready for review.

---

## The Ponytail Protocol
- **Limits:** Additions $\le 35$, Deletions $\le 25$ lines per bundle.
- **Invariants:** Zero full-file rewrites; preserve public APIs and tests.
- **Overflow:** Partition into sequential sub-bundles.

---

## Bundle Directory Structure
```
.torusguard/runs/<run_id>/remediation/<finding_id>/
├── patch.diff       # Standard unified diff with line numbers
├── plan.md          # Rationale and root-cause breakdown
├── verification.md  # Test instructions proving fix works
└── rollback.md      # Command or steps to revert patch
```

---

## Execution Steps

1. **Evaluate Findings:** First, review the active run's `findings.md`. If the user has already run the CLI `npx torusguard harden` and it formulated `0` patches (or skipped complex findings), it is **YOUR RESPONSIBILITY** as the AI Agent to manually remediate the remaining findings.
2. **Read AST Context:** View target file surrounding lines (±15) using `view_file` to deeply understand the vulnerability.
3. **Formulate Minimal Fix:** Actively rewrite the code to fix the vulnerability (e.g. parameterize SQL, add tenant filters, use safe DOM APIs). Do NOT wait for the CLI to do it. You must generate the fix. Consult `.torusguard/memory/context.json` for verified idioms.
4. **Validate Line Churn:** Assert additions $\le 35$ and deletions $\le 25$ via `diff_guard.py`. If it's too complex, partition into sequential sub-bundles.
5. **Package Bundle Manually:** Write 4 artifacts (`patch.diff`, `plan.md`, `verification.md`, `rollback.md`) into `.torusguard/runs/<run_id>/remediation/<finding_id>/`.
6. **Flag Sensitive Paths:** Mark changes touching auth or billing with `Requires Sensitive-Path Sign-Off`.

---

## Safety Constraints
- Dry-run only; do NOT apply modifications directly to source code during harden. Only write to the `patch.diff` artifact.
- Keep surrounding formatting and comments intact.
- Never touch files outside the targeted vulnerable sink.

---

## Output Format
```markdown
🛠️ [TorusGuard] Remediation Bundle Packaged (AI Assisted)
- Finding Target: <Finding ID> | File: <Path>
- Line Churn: +<Additions> / -<Deletions> (Ponytail: PASS)
- Sensitive Path: <Yes/No>
- Bundle Path: `.torusguard/runs/<run_id>/remediation/<finding_id>/`

> [!NOTE]
> This patch was formulated manually by the TorusGuard AI Agent because it required architectural changes beyond the CLI's automated templates.

Next: Run `/torusguard apply` to review diff and apply with rollback backup.
```
