---
name: torusguard-report
description: Generate executive posture reports, export OASIS SARIF v2.1.0 logs, and render dark-mode HTML dashboards via CLI or AI Agent.
version: 2.2.0
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
Aggregate findings, verification traces, and recheck results into an auditable executive security report, export schema-compliant OASIS SARIF v2.1.0 logs for CI/CD pipelines, and render zero-dependency single-file visual HTML posture reports with full dual-mode parity.

---

## Execution Steps

### Mode A: Automated CLI Execution
Run the report engine from your terminal:
```bash
# Generate visual dark-mode HTML dashboard (defaults to report.html at project root)
npx torusguard report --html

# Export OASIS SARIF v2.1.0 for GitHub Code Scanning / CI
npx torusguard report --sarif

# Generate both HTML and SARIF in a single pass
npx torusguard report --html --sarif

# Custom HTML output location
npx torusguard report --html --out ./docs/security-audit.html

# Target a specific subproject / monorepo package
npx torusguard report --target ./apps/api --html
```

**Under the Hood:**
- Invokes `python .torusguard/scripts/html_reporter.py` to compile self-contained, offline-ready HTML reports with dynamic filtering, posture gauge, directory attack surface heatmap, and golden recipe explorer at `report.html` (workspace root) and mirrors to `.torusguard/runs/report-latest.html`.
- Invokes `python .torusguard/scripts/sarif_exporter.py` to produce OASIS SARIF v2.1.0 logs at `.torusguard/runs/results-latest.sarif`.
- Finalizes `manifest.json` metrics and updates historical posture scoring.
- Displays standardized 75-column terminal cards adhering to visual width invariants.

### Mode B: In-Session AI Chat Agent Reporting
When generating security posture summaries in AI chat:
1. **Aggregate Run Data:** Inspect `findings.json`, `remediation.md`, and `recheck.md` from the active run.
2. **Calculate Posture Score:** Compute posture score ($0$–$100$) based on severity weighting (Critical: 25, High: 15, Medium: 5, Low: 2). Clean repositories earn 100/100 across 74 defended invariants.
3. **Format Executive Card:** Present finding counts, closed vulnerabilities, remaining risks, and compliance posture.
4. **Export Artifacts:** Verify that `report.html` and `results-latest.sarif` are serialized to disk.
5. **Keep Living Ledger in Lockstep:** Ensure `security_report.md` reflects all findings and verified closures.

---

## Zero-CDN & Offline Guarantee
- Zero external `<script>` or `<link>` tags. All styles, fonts, SVG icons, and scripts are embedded directly inside `report.html`.
- Full offline inspection: can be opened directly via `file:///` without an active internet connection.
- In-browser artifact downloads (SARIF v2.1.0 and CSV) use native `URL.createObjectURL(new Blob(...))` with zero network calls.

---

## SARIF v2.1.0 Output Specification
- **Schema:** `https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json`
- **Tool Driver:** `name: TorusGuard`, `semanticVersion: 1.3.6`, full rules catalog in `driver.rules`.
- **Automation Details:** `automationDetails.id: "torusguard/static"` to avoid collisions in multi-scanner CI/CD pipelines.
- **Fingerprints:** `partialFingerprints.primaryLocationLineHash` with SHA-256 context hash.

---

## Safety Constraints
- Never display raw secrets, tokens, or credentials in terminal outputs or emitted reports.
- Enforce read-only state for `report` actions — never modify source code during report generation.
- Ensure atomic writes with fallback retry to prevent corrupt reports during concurrent browser viewing.
- Respect monorepo target boundaries when `--target` is specified.

---

## Output Format
```markdown
### 🛡️ TorusGuard Security Posture Report Emitted
- **Posture Score:** 100 / 100 (OPTIMAL DEFENSE)
- **Invariants Defended:** 74 Defended · 0 Harmed (74 Rules)
- **HTML Dashboard:** `report.html` (View in browser)
- **SARIF v2.1.0 Export:** `.torusguard/runs/results-latest.sarif` (Ready for CI)
- **Living Ledger:** `security_report.md` (Synchronized in lockstep)
```

## Living Report Ground Truth
- Read `security_report.md` in the workspace root before taking any action. Update the relevant finding card after completing remediation.
