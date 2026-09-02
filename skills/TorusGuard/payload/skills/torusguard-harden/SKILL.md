---
name: torusguard-harden
description: Package surgical remediation bundles conforming to the Ponytail Protocol (<= 35 additions, <= 25 deletions).
version: 0.9.2
workflow: .torusguard/workflows/harden.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/run_manager.py
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

1. **Select Finding:** Choose prioritized verified flaw from active run's `findings.md`.
2. **Read AST Context:** View target file surrounding lines (±15) using `view_file`.
3. **Formulate Minimal Fix:** Parameterize SQL, add tenant filters, insert validation schemas.
4. **Validate Line Churn:** Assert additions $\le 35$ and deletions $\le 25$.
5. **Package Bundle:** Write 4 artifacts (`patch.diff`, `plan.md`, `verification.md`, `rollback.md`).
6. **Flag Sensitive Paths:** Mark changes touching auth or billing with `Requires Sensitive-Path Sign-Off`.

---

## Safety Constraints
- Dry-run only; do NOT apply modifications to source code during harden.
- Keep surrounding formatting and comments intact.
- Never touch files outside the targeted vulnerable sink.

---

## Output Format
```markdown
🛠️ [TorusGuard] Remediation Bundle Packaged
- Finding Target: <Finding ID> | File: <Path>
- Line Churn: +<Additions> / -<Deletions> (Ponytail: PASS)
- Sensitive Path: <Yes/No>
- Bundle Path: `.torusguard/runs/<run_id>/remediation/<finding_id>/`
Next: Run `/torusguard apply` to review diff and apply with rollback backup.
```
