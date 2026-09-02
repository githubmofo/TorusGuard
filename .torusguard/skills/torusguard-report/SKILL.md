---
name: torusguard-report
description: Generate unified security posture reports and export OASIS SARIF v2.1.0 logs for CI/CD integration.
version: 0.9.2
workflow: .torusguard/workflows/report.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/sarif_exporter.py
  - .torusguard/scripts/run_manager.py
---

# TorusGuard Report — Unified Security Posture Report & SARIF Export

## Objective
Aggregate findings, verification traces, and recheck results into a signed executive security summary and export schema-compliant OASIS SARIF v2.1.0 logs for CI/CD pipelines.

---

## Execution Steps

1. **Aggregate Run Data:** Read findings, verified evidence, and recheck records from active run.
2. **Export OASIS SARIF v2.1.0:**
   ```bash
   python .torusguard/scripts/sarif_exporter.py --run <run_dir> --output <run_dir>/results.sarif
   ```
3. **Compile Executive Markdown Report:** Generate `report.md` with posture score, open/closed finding tables, and risk breakdown.
4. **Update Run Manifest:** Finalize `manifest.json` status counts.
5. **Archive Release Artifacts:** Ensure `report.md` and `results.sarif` are serialized to disk.

---

## SARIF v2.1.0 Output Specification
- **Version:** `$schema: https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json`, `version: 2.1.0`.
- **Tool Driver:** `name: TorusGuard`, `semanticVersion: 0.9.2`, full rules catalog in `driver.rules`.
- **Category Hygiene:** Set `automationDetails.id: "torusguard/static"` to avoid collisions in multi-analysis CI.
- **Fingerprinting:** Populate `partialFingerprints.primaryLocationLineHash` with SHA-256 context hash.

---

## Safety Constraints
- Redact all tokens, passwords, and API keys before saving report.
- Strictly read-only reporting; no source code modifications.
- Ensure SARIF passes JSON schema validation.

---

## Output Format
```markdown
📊 [TorusGuard] Security Posture Report Emitted
- Run ID: <Run ID> | Posture Score: <Score>/100
- Findings: <Total> (<Fixed> Fixed · <Open> Open)
- SARIF Export: `.torusguard/runs/<run_id>/results.sarif`
- Executive Report: `.torusguard/runs/<run_id>/report.md`
```
