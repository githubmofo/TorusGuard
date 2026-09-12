---
name: torusguard-harden
description: Package surgical remediation bundles conforming to the Ponytail Protocol (<= 35 additions, <= 25 deletions) via CLI or AI Agent.
version: 1.3.5
workflow: .torusguard/workflows/harden.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/harden_runner.py
  - .torusguard/scripts/diff_guard.py
  - .torusguard/scripts/term_ui.py
---

# TorusGuard Harden — Governed Remediation & Bundle Packaging

## Objective
Formulate minimal, surgical code fixes bound by the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions), packaging unified diffs into auditable remediation bundles ready for review.

---

## Two Execution Modes

### Mode A: Automated CLI Execution (Recommended First Step)
Run the autonomous remediation engine via the terminal:
```bash
# Harden latest audit run
npx torusguard harden

# Harden specific project directory
npx torusguard harden ./my-project

# Harden specific run ID
npx torusguard harden --run run-20260910-121618-audit

# Machine-readable JSON output
npx torusguard harden --json
```
**Under the Hood:** Executes `python .torusguard/scripts/harden_runner.py`.
- Discovers findings in `.torusguard/runs/<run_id>/findings.json`.
- Matches findings against canonical AST patch templates (`TG-SEC-*`, `TG-INPUT-*`, `TG-DB-*`, `TG-PLATFORM-*`, `TG-AUTH-*`, `TG-DIFF-*`).
- Validates that every candidate patch strictly satisfies Ponytail bounds ($\le 35$ additions, $\le 25$ deletions).
- Packages candidate bundles into `.torusguard/runs/<run_id>/bundles/<bundle_id>/` containing `patch.diff`, `minimal_patch_plan.md`, and `metadata.json`.
- Emits run-level summary `remediation.md`.
- Renders pixel-perfect 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Remediation
When findings require complex architectural changes, or when the automated CLI cannot formulate a template match:
1. **Locate Target Finding:** Inspect `.torusguard/runs/<run_id>/findings.md` or `findings.json`.
2. **Inspect AST Context:** Read surrounding lines ($\pm 15$) of the vulnerable sink using `view_file`.
3. **Formulate Minimal Fix:** Craft a surgical code modification:
   - Parameterize SQL queries (replace concatenation with `?` or `$1` or `%s`).
   - Add tenant isolation (`where: { tenantId }`, `organization_id=...`).
   - Replace unsafe HTML injection (`dangerouslySetInnerHTML`, `.innerHTML = ...`) with safe text rendering (`textContent`, React elements).
   - Sanitize path traversal using `path.basename()` or `os.path.basename()`.
   - Constrain wildcard CORS headers to verified origin environment variables.
   - Restore TLS verification flags (`verify=True`, `rejectUnauthorized: true`).
4. **Validate Ponytail Bounds:** Count additions ($\le 35$) and deletions ($\le 25$). Never perform full-file rewrites.
5. **Package Bundle Artifacts:** Write bundle under `.torusguard/runs/<run_id>/bundles/<bundle_id>/`:
   - `patch.diff`: Standard unified diff.
   - `minimal_patch_plan.md`: Context, rationale, and diff preview.
   - `metadata.json`: Bundle metadata.
6. **Report to Operator:** Present proposed diff card and recommend running `/torusguard apply` or `npx torusguard apply`.

---

## Remediation Bundle Structure
```
.torusguard/runs/<run_id>/
├── remediation.md                         # Run-level catalog of formulated candidate patches
└── bundles/
    └── bnd-<rule_id>-<line>-<hash>/
        ├── patch.diff                    # Unified diff preview
        ├── minimal_patch_plan.md         # Detailed explanation, rationale, and churn stats
        └── metadata.json                 # Machine-readable bundle metadata
```

---

## Non-Negotiable Invariants
- **Ponytail Limit:** Strict upper bound of $\le 35$ additions and $\le 25$ deletions per bundle.
- **Dry-Run Rule:** Never modify target source code during `harden`. All edits must be reviewed before application in Phase 5 (`apply`).
- **No Unrelated Churn:** Do not reformat unrelated code, reorder imports, or change styles.
- **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `[AllowAnonymous]`, or `csrf().disable()`.

---

## Output Card Format
```markdown
### 🛠️ TorusGuard Remediation Bundle Formulated
- **Target Finding:** `[TG-SEC-001]` at `server/index.js:9`
- **Ponytail Churn:** +1 / -1 (Compliant <= 35 add, <= 25 del)
- **Strategy:** Migrated hardcoded JWT secret to environment variable process.env.JWT_SECRET
- **Bundle Directory:** `.torusguard/runs/<run_id>/bundles/bnd-tg-sec-001-9-a8310c/`
- **Next Step:** Run `npx torusguard apply` or `/torusguard apply` to review and apply
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.
