---
description: Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: remediator
lifecycle-phase: Phase 4 (Remediation Formulation)
required-skills:
  - torusguard-harden
scripts-binding:
  - internal/harden/patch.go
  - internal/harden/reflection.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard harden — Governed Remediation & Bundle Packaging

$ARGUMENTS

---

## Objective
Formulate minimal, surgical code fixes bound by the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions), packaging unified diffs or semantic reflection patches into auditable remediation bundles ready for review.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard harden <candidate.patch \| patch.json>` | Shell validation of patch against Ponytail bounds. |
| **Mode B: AI Chat Slash** | `/torusguard harden` | Formulate semantic patch with Line-Level Reflection. |
| **Mode C: Native MCP Tool** | `torusguard_harden` | Automated validation of patch file or `find_snippet` / `replace_snippet`. |

---

## Mandatory Pre-Flight Context Inspection

Inspect finding targets and patch constraints before generating diffs:
1. **Target Finding (`security_report.md`):** Identify prioritized verified findings.
2. **Ponytail Protocol:** Enforce hard limit ($\le 35$ additions, $\le 25$ deletions). Ban rewrites.
3. **Sensitive Path Review:** Flag changes touching `auth/` or credentials for explicit sign-off.
4. **Behavior Preservation:** Ensure patch addresses flaw without breaking public APIs.
5. **Dry-Run Rule:** Do NOT apply changes to disk during harden; emit bundle for review.
6. **Zero Bypasses:** Reject `# nosec`, `verify=False`, or `InsecureSkipVerify` under rule `TG-DIFF-001`.

---

## Living Report Invariant
- Candidate patches transition findings in `security_report.md` into `CANDIDATE 🟡` status.
- Every patch strictly conforms to Ponytail bounds (<= 35 additions, <= 25 deletions).

---

## Execution Steps

1. **Select Target Finding:** Choose verified flaw from `security_report.md`.
2. **Examine Live Code Context:** Read surrounding lines ($\pm 3$) using bounded context extraction.
3. **Formulate Minimal Semantic Patch:** Formulate `find_snippet` and `replace_snippet`.
4. **Audit Patch Safety:** Run `torusguard harden` or call `torusguard_harden`.
5. **Package Bundle:** Prepare candidate patch ready for the Human Gate.

---

## Output Card Format

```markdown
### 🛠️ TorusGuard Remediation Bundle
- **Finding Target:** `TG-XXX-HASH` ([Vulnerability Name])
- **File Affected:** `src/path/to/file`
- **Line Churn:** +[Additions] / -[Deletions] (Ponytail: PASS)
- **Status:** READY FOR REVIEW — run `/torusguard apply` to execute
```

---

## Next Steps

1. Review proposed diff or semantic reflection snippet.
2. Run `/torusguard apply` or `torusguard apply` with Human Gate approval.
