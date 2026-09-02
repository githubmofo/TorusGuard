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
Executive posture reporting, cluster analysis, signed compliance audit, and SARIF v2.1.0 export.

---

## Mandatory Pre-Flight Context Inspection

Inspect run records and reporting parameters before generating release artifacts:
1. **Active Run Records:** Ensure target run folder contains `findings.json` or `findings.md`.
2. **SARIF v2.1.0 Schema:** Validate output structure against official OASIS SARIF standard.
3. **Multi-Analysis Category:** Tag static findings under category `torusguard/static` to prevent CI collision.
4. **Secret Masking:** Ensure zero unredacted authorization tokens or API keys appear in report.
5. **Role Boundary:** Enforce reviewer agent sign-off before archiving run results.

---

## When to Use /torusguard report

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| Concluding a security review cycle or audit milestone | Run `/torusguard report` |
| Exporting SARIF v2.1.0 logs for GitHub Code Scanning | Run `/torusguard report` |
| Sharing executive posture summaries with stakeholders | Run `/torusguard report` |
| Applying code modifications | Run `/torusguard apply` |
| Re-checking modified files | Run `/torusguard recheck` |

---

## Execution Steps

1. **Aggregate Lifecycle Data:** Load all finding cards, verification traces, and recheck logs.
2. **Export OASIS SARIF v2.1.0:**
   ```bash
   python .torusguard/scripts/sarif_exporter.py --run <run_dir> --output <run_dir>/results.sarif
   ```
3. **Compile Executive Markdown Report:** Generate `report.md` with executive summary, posture score, and metrics.
4. **Sign Off Run Manifest:** Update `.torusguard/runs/<run_id>/manifest.json` with final status counts.
5. **Archive Results:** Confirm artifacts (`report.md`, `results.sarif`, `summary.md`) are saved on disk.

---

## Failure Recovery

- **SARIF Schema Error:** Re-run `sarif_exporter.py` with schema validation flag to locate invalid properties.
- **Empty Findings List:** Emit valid clean report indicating zero security vulnerabilities detected.
- **Missing Run Folder:** Point script to latest valid timestamped run in `.torusguard/runs/`.
- **Halt Trigger:** Abort if unredacted private secrets are detected in output text.

---

## Hallucination Guard

- ❌ Never invent vulnerability counts not backed by actual findings in the run ledger.
- ❌ Never generate invalid SARIF JSON with missing physical location URIs.
- ✅ Always export standard-compliant SARIF v2.1.0 with AST line fingerprints.

---

## Output Card Format

```markdown
### 📊 TorusGuard Security Posture Report
- **Run ID:** `run-YYYYMMDD-HHMMSS`
- **Total Findings:** [Count] ([Fixed] Fixed, [Open] Open)
- **Security Posture Score:** [Score]/100
- **SARIF v2.1.0 Export:** `.torusguard/runs/<run_id>/results.sarif`
- **Executive Report:** `.torusguard/runs/<run_id>/report.md`
- **Status:** COMPLETE — report published
```

---

## Next Steps

1. Upload `results.sarif` to GitHub Code Scanning via `.github/workflows/`.
2. Share `report.md` with engineering stakeholders and project maintainers.
