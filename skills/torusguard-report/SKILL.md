---
name: torusguard-report
description: Generate unified executive security posture reports and export valid OASIS SARIF v2.1.0 logs for CI/CD.
version: 0.9.2
workflow: .torusguard/workflows/report.md
tools: Read, Grep, Glob, Bash, Write
scripts-binding:
  - .torusguard/scripts/sarif_exporter.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Report — Posture Reporting & SARIF v2.1.0 Export

## Objective
Aggregate findings, runtime evidence, and closure transitions from the active run, render a comprehensive 9-section executive markdown report, and export a strictly compliant OASIS SARIF v2.1.0 log for CI/CD integration.

---

## Execution Steps

### Step 1: Collect Run Metrics
Read from `.torusguard/runs/<active-run>/`:
- Initial static findings from `findings.md`.
- Runtime probe evidence from `web-validation.md`.
- Closure transitions from `recheck.md`.
- Run metadata from `manifest.json`.

### Step 2: Determine Executive Posture
Classify repository security posture:
- **`🔴 ACTION REQUIRED`**: 1+ Open Critical/High findings remain unaddressed.
- **`🟡 WARNINGS FOUND`**: Medium/Low findings open, or findings awaiting manual review.
- **`🟢 SECURE`**: All prioritized findings verified fixed, zero active regressions.

### Step 3: Render Canonical 9-Section Report
Write `.torusguard/runs/<run-id>/report.md`:
1. **Executive Posture & Summary**: High-level posture badge and finding counts.
2. **Metadata**: Run ID, commit hash, date, version.
3. **Detected Stack**: Framework, language, and data layer.
4. **Scope & Safety Audit**: Authorized target, paths, and probe methods.
5. **Systemic Clusters**: Grouped root-cause clusters table.
6. **Prioritized Finding Cards**: Detailed cards with line citations and confidence scores.
7. **Remediation & Closure Ledger**: Applied patches and verified fixes.
8. **Regression Audit**: Results of post-patch verification.
9. **Next Steps**: Recommended actions for developers.

### Step 4: Export OASIS SARIF v2.1.0 Log
Run the SARIF exporter:
```bash
python .torusguard/scripts/sarif_exporter.py --run-dir .torusguard/runs/<run-id> --output .torusguard/runs/<run-id>/results.sarif
```

---

## SARIF v2.1.0 Output Specification
Ensure generated SARIF adheres to OASIS v2.1.0 standards:
- Root schema: `https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json`
- `version`: `"2.1.0"`
- `runs[0].tool.driver`: Name `"TorusGuard"`, version `"0.9.2"`, rules catalog with descriptions.
- `runs[0].results`: Array of findings with `ruleId`, `level` (error/warning/note), `message`, and `locations[0].physicalLocation`.
- `primaryLocationLineHash`: Line-shift invariant fingerprint attached to each result.
- `automationDetails.id`: Unique analysis category (`"torusguard/static/"` or `"torusguard/runtime/"`).

---

## Safety Constraints
- Never include unmasked secrets, tokens, or passwords in reports or SARIF exports.
- Never report a finding as `Fixed` without verified recheck records.
- Preserve all findings (open, fixed, or mitigated) in the historical run record.

---

## Output Format
```markdown
🛡️ [TorusGuard] Security Report & SARIF Export Generated
- Run ID: <run-id>
- Executive Posture: <🟢 SECURE | 🔴 ACTION REQUIRED | 🟡 WARNINGS>
- Findings Breakdown: <Total> Total (<Fixed> Fixed · <Open> Open)
- SARIF v2.1.0 File: .torusguard/runs/<run-id>/results.sarif
- Executive Markdown: .torusguard/runs/<run-id>/report.md

CI Integration: Upload results.sarif to GitHub Code Scanning or GitLab SAST.
```
