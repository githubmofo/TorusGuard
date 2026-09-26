---
description: Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: reviewer
lifecycle-phase: Phase 7 (Reporting & SARIF Export)
required-skills:
  - torusguard-report
scripts-binding:
  - internal/report/html.go
  - internal/report/sarif.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard report — Unified Security Posture Report & SARIF Export

$ARGUMENTS

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 export.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard report --html [--sarif]` | Shell compilation of HTML dashboard and SARIF log. |
| **Mode B: AI Chat Slash** | `/torusguard report` | Executive summary generation and posture calculation. |
| **Mode C: Native MCP Tool** | `torusguard://security_report` | Agent reads resource payload directly from living report. |

---

## Mandatory Pre-Flight Context Inspection

Inspect run records and reporting parameters before generating release artifacts:
1. **Living Report State:** Ensure `security_report.md` exists and reflects latest findings.
2. **SARIF v2.1.0 Schema:** Validate output structure against official OASIS SARIF standard.
3. **Multi-Analysis Category:** Tag static findings under category `torusguard/static` to prevent CI collision.
4. **Secret Masking:** Ensure zero unredacted authorization tokens or API keys appear in report.
5. **Zero-CDN Guarantee:** Ensure HTML report contains zero external CDN script dependencies.

---

## Living Report Invariant
- Executive posture reports incorporate health scoring and metrics from `security_report.md`.
- Emits visual dark-mode HTML (`--html`) and OASIS SARIF v2.1.0 (`--sarif`).

---

## Execution Steps

1. **Trigger Report Generation:**
   - **Mode A (CLI):** Run `torusguard report --html --sarif`.
   - **Mode B (Chat):** Calculate posture score from `security_report.md` and present summary card.
   - **Mode C (MCP):** Query resource `torusguard://security_report`.
2. **Compile Visual HTML:** Generate zero-dependency dark-mode HTML dashboard at `report.html`.
3. **Export SARIF v2.1.0:** Produce schema-compliant SARIF log for CI/CD pipelines.
4. **Sign Off Ledger:** Confirm artifacts are persisted to disk.

---

## Output Card Format

```markdown
### 📊 TorusGuard Security Posture Report
- **Posture Score:** 100/100 (OPTIMAL DEFENSE)
- **Total Invariants:** 74 Defended across 18 families
- **HTML Dashboard:** `report.html`
- **SARIF v2.1.0 Export:** `results.sarif`
- **Living Ledger:** `security_report.md`
```

---

## Next Steps

1. Upload `results.sarif` to GitHub Code Scanning via `.github/workflows/`.
2. Open `report.html` in browser for visual audit presentation.
