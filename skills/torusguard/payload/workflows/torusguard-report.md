---
description: Executive posture reporting, interactive HTML dashboard generation, directory attack surface heatmap, and OASIS SARIF v2.1.0 structured export.
tools: Read, Grep, Glob, Bash, Write
version: 2.2.0
agent: reviewer
lifecycle-phase: Phase 7 (Reporting & SARIF Export)
required-skills:
  - torusguard-report
scripts-binding:
  - .torusguard/scripts/html_reporter.py
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/sarif_exporter.py
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/term_ui.py
---

# /torusguard report — Unified Security Posture Report & SARIF / HTML Export

$ARGUMENTS

---

## Objective
Generate an executive security posture report, interactive dark-mode HTML dashboard (`report.html`), and schema-compliant OASIS SARIF v2.1.0 log (`results.sarif`) with zero network dependencies.

---

## Dual Mode Execution Syntax

| Target Artifact | Mode A: Terminal CLI | Mode B: AI Chat Slash Command | Output Location |
| :--- | :--- | :--- | :--- |
| **Interactive HTML Dashboard** | `npx torusguard report --html` | `/torusguard report --html` or `/torusguard-report` | `report.html` (workspace root) + `.torusguard/runs/report-latest.html` |
| **OASIS SARIF v2.1.0 Log** | `npx torusguard report --sarif` | `/torusguard report --sarif` | `.torusguard/runs/results-latest.sarif` |
| **Combined (Both)** | `npx torusguard report --html --sarif` | `/torusguard report --html --sarif` | Both `report.html` and `results-latest.sarif` in a single pass |
| **Custom Path** | `npx torusguard report --html --out <path>` | `/torusguard report --out <path>` | Specified path + latest run mirror |
| **Monorepo Subproject** | `npx torusguard report --target <dir> --html` | `/torusguard report --target <dir>` | `<dir>/report.html` |

---

## Mandatory Pre-Flight Context Inspection

Inspect run records and reporting parameters before generating release artifacts:
1. **Active Run Records:** Ensure target run folder or `.torusguard/runs/` contains valid run records.
2. **Dual-Ledger Ground Truth:** Confirm that `security_report.md` at workspace root is in lockstep with findings.
3. **SARIF v2.1.0 Schema:** Validate output structure against official OASIS SARIF standard (`sarif-schema-2.1.0.json`).
4. **Multi-Analysis Category:** Tag static findings under category `torusguard/static` to prevent CI collisions.
5. **Zero External CDN:** Ensure all icons, gauges, and scripts in `report.html` are 100% self-contained and offline-ready.
6. **Secret Masking:** Ensure zero unredacted authorization tokens or API keys appear in report text.

---

## Interactive Dashboard Features (v2.2.0)

When viewing `report.html` in any browser:
1. **Safe Defenses vs Harmed Exposure:** Complete Defended Invariants inventory across all 74 rules in 18 architectural families. Clean codebases earn 100/100 (74 Defended, 0 Harmed).
2. **Directory Attack Surface Heatmap:** Visual directory tree of exposure risk. Clicking any directory card filters the findings table to that specific folder.
3. **Golden Recipe Explorer:** Distilled, verified fix patterns with before/after code templates and one-click clipboard copying.
4. **Prescriptive Next Best Defenses:** Stack-aware security recommendations with copyable `npx torusguard harden` commands.
5. **Client-Side Exporters:** Zero-network buttons to download OASIS SARIF v2.1.0 and CSV records directly from browser memory.
6. **Multi-Agent AI Prompt Presets:** One-click prompts tailored for Cursor (`.cursorrules`), Claude Code (`CLAUDE.md`), Antigravity, and GitHub Copilot.
7. **Print & PDF Styling:** Built-in high-contrast `@media print` layout for boardroom and compliance distribution.

---

## Execution Steps

1. **Detect Mode & Arguments:**
   - Parse `--html`, `--sarif`, `--out`, `--target`, and `--run` from `$ARGUMENTS`.
   - If no format flag is specified in chat, default to generating the visual HTML dashboard (`report.html`).
2. **Execute Reporter Scripts:**
   - **For SARIF:**
     ```bash
     python .torusguard/scripts/sarif_exporter.py [--output <path>] [--root <target>]
     ```
   - **For HTML:**
     ```bash
     python .torusguard/scripts/html_reporter.py [--out <path>] [--root <target>]
     ```
3. **Synchronize Dual Ledger:**
   - Verify `security_report.md` matches `report.html` findings and posture score.
4. **Emit 75-Column Visual Summary Card:**
   - Present markdown output card with direct clickable links to both `report.html` and `security_report.md`.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Security Posture Report Emitted
- **Posture Score:** [Score]/100 ([Status Label])
- **Invariants Defended:** [N] Defended · [M] Harmed (74 Rules)
- **Living Ledger:** [security_report.md](file:///path/to/security_report.md)
- **HTML Dashboard:** [report.html](file:///path/to/report.html)
- **SARIF v2.1.0 Export:** [results-latest.sarif](file:///path/to/results-latest.sarif)
- **Status:** COMPLETE — dual-ledger synchronized
```

---

## Failure Recovery

- **Missing Run Folder:** Auto-discover the latest timestamped run in `.torusguard/runs/`.
- **Windows File Lock:** `html_reporter.py` uses atomic temporary write swapping with exponential retry.
- **Missing SARIF Input:** Auto-discovers findings from the latest audit run in `.torusguard/runs/`.
- **Clean Workspace:** Emits 100/100 posture score with all 74 defended invariants listed.
