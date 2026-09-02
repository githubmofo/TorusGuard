---
description: Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: reviewer
lifecycle-phase: Phase 7 (Reporting & SARIF Export)
required-skills:
  - torusguard-report
scripts-binding:
  - .torusguard/scripts/sarif_exporter.py
  - .torusguard/scripts/run_manager.py
---

# /torusguard report — Unified Security Posture Report & SARIF Export

$ARGUMENTS

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Mandatory Pre-Flight Context Inspection

Before generating final security reports and SARIF logs, you MUST inspect:

1. **Active Run Folder Completion** → Ensure that audit findings, evidence verifications, and recheck results are populated in `.torusguard/runs/<active-run>/`.
2. **OASIS SARIF v2.1.0 Compliance** → Verify that generated SARIF passes schema validation with rules, results, physical locations, and fingerprints.
3. **Multi-Analysis Category Hygiene** → Ensure static findings are tagged with `automationDetails.id: "torusguard/static/"` and runtime findings with `"torusguard/runtime/"` to avoid GitHub Code Scanning collision.
4. **Credential Redaction Sign-Off** → Confirm that zero raw secrets, tokens, or plaintext passwords appear in the report or SARIF artifact.

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## When to Use /torusguard report

| Use `/torusguard report` when... | Use something else when... |
| :--- | :--- |
| Finishing a security review or audit run | Still discovering findings → `/torusguard audit` |
| Exporting SARIF v2.1.0 for GitHub / GitLab CI | Applying code fixes → `/torusguard apply` |
| Presenting executive summary to stakeholders | Verifying fixes → `/torusguard recheck` |
| Archiving run compliance artifacts | Checking workspace state → `/torusguard status` |

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Execution Steps (Fixed Order)

### Phase 1 — Aggregate Run Lifecycle Data
Load data from `.torusguard/runs/<active-run>/`:
- Initial static findings from `findings.md` and `findings.json`.
- Runtime probe evidence from `web-validation.md` and `replay.json`.
- Applied patches and recheck closure transitions from `recheck.md`.
- Overall run manifest metrics from `manifest.json`.

### Phase 2 — Generate OASIS SARIF v2.1.0 Log
Run the SARIF exporter script:
```bash
python .torusguard/scripts/sarif_exporter.py --run-dir .torusguard/runs/<active-run> --output .torusguard/runs/<active-run>/results.sarif
```
Verify generated SARIF:
- Contains `version: "2.1.0"`.
- Rule dictionary contains complete titles, descriptions, and help URIs.
- Results have exact `physicalLocation` with `uri`, `startLine`, and `primaryLocationLineHash`.

### Phase 3 — Render Canonical 9-Section Executive Markdown Report
Generate `.torusguard/runs/<active-run>/report.md`:
1. **Executive Summary & Posture Badge** (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Secure`).
2. **Run Metadata** (Run ID, Commit Hash, Date, Tool Version).
3. **Detected Stack & Architecture**.
4. **Scope & Authorization Audit**.
5. **Systemic Root-Cause Clusters Table**.
6. **Prioritized Finding Cards** (File, Line, Rule, Confidence Score, Evidence, Remediation).
7. **Remediation & Closure Ledger** (Patches applied, findings fixed).
8. **Regression & Health Audit**.
9. **Next Recommended Actions**.

### Phase 4 — Archive & Seal Run
Seal the active run folder:
- Write finalized counts and cryptographic hashes to `manifest.json`.
- Provide direct clickable links to the generated artifacts.

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Failure Recovery & Cascade Rules

```
SARIF export failure:   Run sarif_exporter.py with --verbose; fallback to basic SARIF template
Missing run data:       Warn about missing stages (e.g., 'No runtime checks executed'); continue
Invalid SARIF schema:   Validate against OASIS schema; strip unsupported custom properties
```

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Hallucination Guard

```
❌ Never omit unresolved High or Critical findings from the executive summary
❌ Never fabricate false 'Fixed' counts without verified recheck records
❌ Never include unmasked credentials or raw session tokens in report or SARIF
❌ Never claim '100% Secure' if any findings were skipped or downgraded without justification
```

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Security Report & SARIF Export Generated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run ID:             [run-YYYYMMDD-HHMMSS-audit]
Executive Posture:  🟢 SECURE (All Prioritized Findings Remediated)
Total Findings:     [0 Open · 1 Verified Fixed · 0 Regressions]
SARIF v2.1.0 Log:   .torusguard/runs/<run-id>/results.sarif
Executive Report:   .torusguard/runs/<run-id>/report.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CI/CD Integration:
- Upload results.sarif to GitHub Code Scanning or GitLab SAST
- View full card report in .torusguard/runs/<run-id>/report.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Audit Run Completed Successfully.
```

---

## Objective
Executive posture reporting, cluster analysis, signed compliance audit, and OASIS SARIF v2.1.0 structured export.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Report and SARIF generated | → Inspect `.torusguard/runs/<run-id>/report.md` |
| View workspace status | → `/torusguard status` |
| Start new audit on new branch | → `/torusguard audit` |
