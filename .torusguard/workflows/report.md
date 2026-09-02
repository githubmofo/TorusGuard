# /torusguard report — Executive Report & OASIS SARIF v2.1.0 Export

**Command:** `/torusguard report [run_id]`  
**Primary Agent:** `reviewer` (`.torusguard/agents/reviewer.md`)  
**Lifecycle Phase:** Phase 7 (Report & Export)

---

## Objective
Synthesize all static audit findings, runtime validation evidence, exploitability verdicts, and recheck outcomes into an executive-grade Markdown summary and standard OASIS SARIF v2.1.0 log.

---

## Execution Steps

### Step 1: Collect Run Artifacts
Read all state from the active run folder:
- `manifest.json` (status metrics, execution commit)
- `findings.md` (individual finding cards)
- `web-validation.md` (runtime probe audit)
- `recheck.md` (recheck results)

### Step 2: Render Executive Markdown Summary
Using `.torusguard/templates/audit-report.template.md`, render `summary.md` with:
1. Canonical `## Detected Stack` block.
2. Posture indicator badge (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Ready`).
3. Severity metrics table (Critical / High / Medium / Low).
4. Runtime exploitability matrix (Confirmed / Likely / Not Repro / Blocked).
5. Root-cause cluster breakdown.
6. Prioritized next steps.

### Step 3: Multi-Analysis SARIF v2.1.0 Export
Generate standard SARIF log conforming to OASIS v2.1.0:
- Tool driver: `TorusGuard v0.8.0`.
- Unique automation ID: `torusguard/v0.8.0/run-<timestamp>`.
- Embed `primaryLocationLineHash` on every result for GitHub Code Scanning deduplication.
- Write output to `.torusguard/runs/<run-id>/sarif.json`.

### Step 4: Output Summary
```markdown
📊 [TorusGuard] Executive Report & SARIF Exported
- Executive Report: .torusguard/runs/<run-id>/summary.md
- OASIS SARIF Log: .torusguard/runs/<run-id>/sarif.json
- Final Posture: 🟢 Ready (All high-risk findings remediated and rechecked clean)
```
