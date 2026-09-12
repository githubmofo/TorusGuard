---
name: torusguard-report
description: Generate executive posture reports, export OASIS SARIF v2.1.0 logs, and render dark-mode HTML dashboards via CLI or AI Agent.
version: 1.3.5
workflow: .torusguard/workflows/report.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/html_reporter.py
  - .torusguard/scripts/sarif_exporter.py
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/term_ui.py
---

# TorusGuard Report — Posture Reporting & SARIF / HTML Export

## Objective
Aggregate findings, verification traces, and recheck results into an auditable executive security report, export schema-compliant OASIS SARIF v2.1.0 logs for CI/CD pipelines, and render zero-dependency single-file visual HTML posture reports.

---

## Two Execution Modes

### Mode A: Automated CLI Execution
Run the report engine from your terminal:
```bash
# Generate visual dark-mode HTML dashboard
npx torusguard report --html

# Export OASIS SARIF v2.1.0 for GitHub Code Scanning / CI
npx torusguard report --sarif

# Generate both HTML and SARIF for latest run
npx torusguard report --html --sarif

# Generate report for a specific project directory
npx torusguard report ./examples/vulnerable-react-express --html

# Target a specific run ID
npx torusguard report --run run-20260910-121618-audit --html
```
**Under the Hood:**
- Invokes `python .torusguard/scripts/html_reporter.py` to compile self-contained, offline-ready HTML reports with dynamic filtering, posture gauge, and cluster summaries at `.torusguard/runs/<run_id>/report.html`.
- Invokes `python .torusguard/scripts/sarif_exporter.py` to produce OASIS SARIF v2.1.0 logs at `.torusguard/runs/<run_id>/results.sarif`.
- Finalizes `manifest.json` metrics and updates historical posture scoring.
- Displays 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Reporting
When generating security posture summaries in AI chat:
1. **Aggregate Run Data:** Inspect `findings.json`, `remediation.md`, and `recheck.md` from the active run.
2. **Calculate Posture Score:** Compute posture score ($0$–$100$) based on severity weighting (Critical: 25, High: 15, Medium: 5, Low: 2).
3. **Format Executive Card:** Present finding counts, closed vulnerabilities, remaining risks, and compliance posture.
4. **Export Artifacts:** Verify that `report.html` and `results.sarif` are serialized to disk.

---

## SARIF v2.1.0 Specification
- **Schema:** `https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json`
- **Tool Driver:** `name: TorusGuard`, `semanticVersion: 1.3.5`, full rules catalog in `driver.rules`.
- **Automation Details:** `automationDetails.id: "torusguard/static"` to avoid collisions in multi-scanner CI/CD pipelines.
- **Fingerprints:** `partialFingerprints.primaryLocationLineHash` with SHA-256 context hash.

---

## Output Card Format
```markdown
### 📊 TorusGuard Security Posture Report Emitted
- **Run ID:** `run-20260910-121618-audit`
- **Posture Score:** 85 / 100 (HIGH SECURITY)
- **Findings Summary:** 3 Evaluated · 2 Confirmed Fixed · 1 Unresolved
- **HTML Dashboard:** `.torusguard/runs/<run_id>/report.html` (View in browser)
- **SARIF v2.1.0 Export:** `.torusguard/runs/<run_id>/results.sarif` (Ready for CI)
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.
