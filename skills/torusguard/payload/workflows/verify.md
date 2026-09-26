---
description: Evidence sufficiency verification, live disk line match audit, and finding score refinement.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: validator
lifecycle-phase: Phase 3a (Evidence Verification)
required-skills:
  - torusguard-verify
scripts-binding:
  - internal/validate/validate.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard verify — Evidence Verification & Score Refinement

$ARGUMENTS

---

## Objective
Evidence sufficiency verification, live disk line match audit, and finding score refinement.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard verify` | Terminal audit of living security report and evidence presence. |
| **Mode B: AI Chat Slash** | `/torusguard verify` | Live code line inspection, taint flow audit, and false-positive filtering. |
| **Mode C: Native MCP Tool** | `torusguard_verify` | Agent tool call with `{"target": "."}` returning line audit proofs. |

---

## Mandatory Pre-Flight Context Inspection

Inspect finding records and evidence integrity before verification:
1. **Living Report (`security_report.md`):** Confirm report exists at workspace root.
2. **Live File Drift:** Assert cited source files have not been edited or relocated on disk.
3. **Role Boundary:** Enforce validator role; do not apply code modifications during verification.

---

## Living Report Invariant
- Confirmed evidence sufficiency transitions findings in `security_report.md` to `VERIFIED 🟠`.
- False positives transition to `FALSE POSITIVE ⚪`.

---

## Execution Steps

1. **Trigger Verification:**
   - **Mode A (CLI):** Run `torusguard verify`.
   - **Mode B (Chat):** Read cited lines via `view_file` and verify source-to-sink flow.
   - **Mode C (MCP):** Call `torusguard_verify`.
2. **Live Disk Line Match:** Read current code at cited line ranges; verify AST snippet matches.
3. **Audit Evidence Sufficiency:** Assess whether taint path is unbroken and caller context is exposed.
4. **Classify Status:** Assign verified state (`Confirmed`, `Plausible`, or `False Positive`).
5. **Update Living Ledger:** Update statuses in `security_report.md`.

---

## Output Card Format

```markdown
### 🧪 TorusGuard Evidence Verification
- **Report File:** `security_report.md`
- **Findings Evaluated:** [Count] findings
- **Confirmed Real:** [Count] verified flaws
- **False Positives Filtered:** [Count]
- **Status:** Evidence verified on disk
```

---

## Next Steps

1. Run `/torusguard harden` to build surgical patch bundles for verified flaws.
2. Run `/torusguard web-validate` if live endpoint probing is required.
