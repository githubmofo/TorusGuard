---
name: torusguard-full
description: Master 7-stage security pipeline orchestrator — coordinates discovery, authorization, static audit, runtime validation, governed remediation, recheck, and reporting.
version: 0.9.2
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Bash, Edit, Write
scripts-binding:
  - .torusguard/scripts/stack_detect.py
  - .torusguard/scripts/safety_gate.py
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/sarif_exporter.py
---

# TorusGuard Full — Master 7-Stage Pipeline Orchestrator

## Objective
Execute the full, closed-loop TorusGuard security lifecycle from stack discovery through static scanning, runtime validation, Ponytail remediation, differential re-check, and SARIF export under strict governance.

---

## 7-Stage Security Pipeline
0. Init (Baseline) ──► 1. Authorize (Scope) ──► 2. Audit (AST Scan) ──► 3. Validate (Evidence/Exploit) ──► 4. Harden (Ponytail Patch) ──► 5. Apply (Backup & Edit) ──► 6. Recheck (Regression) ──► 7. Report (SARIF)

---

## Specialist Skill Routing
- **Phase 0:** `torusguard-init` (`profiler`)
- **Phase 1:** `torusguard-authorize` (`reviewer`)
- **Phase 2:** `torusguard-audit` (`auditor`)
- **Phase 3:** `torusguard-verify` / `torusguard-exploit-check` (`validator`)
- **Phase 4:** `torusguard-harden` (`remediator`)
- **Phase 5:** `torusguard-apply` (`remediator`)
- **Phase 6:** `torusguard-recheck` (`reviewer`)
- **Phase 7:** `torusguard-report` (`reviewer`)

---

## Pipeline Execution Instructions
1. **Init:** Detect stack via `stack_detect.py` and activate rules in `.torusguard/rules/active/`.
2. **Authorize:** Verify target ownership and TTL in `.torusguard/config/scope.json`.
3. **Audit:** Scan ASTs; assign fingerprints; cluster root causes; compute confidence scores.
4. **Validate:** Audit evidence sufficiency; optionally send bounded probe canary.
5. **Harden:** Formulate surgical diffs bound by Ponytail limits ($\le 35$ add, $\le 25$ del).
6. **Apply:** Save `.bak` snapshot in `pre_apply/`; obtain Human Gate; apply patch.
7. **Recheck:** Re-scan modified files; assert findings are `Fixed` with zero regressions.
8. **Report:** Export OASIS SARIF v2.1.0 and emit signed markdown summary.

---

## Confidence Scoring Rubric
Evaluates Evidence (35 pts), Reproduction (25 pts), Corroboration (15 pts), Environment (15 pts), and Review Status (10 pts) into 4 bands: Confirmed (90–100), High (70–89), Medium (50–69), Needs Review (<50).

---

## Safety & Governance
- Human Gate mandatory before code modifications in Phase 5.
- Enforce Ponytail line bounds ($\le 35$ additions, $\le 25$ deletions).
- Never dispatch network probes outside authorized scope in `scope.json`.

---

## Output Format
```markdown
🏆 [TorusGuard] 7-Stage Security Pipeline Complete
- Run ID: run-YYYYMMDD-HHMMSS | Status: SECURE / AUDITED
- Findings: <Total> (<Fixed> Fixed · <Open> Remaining)
- SARIF Log: `.torusguard/runs/<run_id>/results.sarif`
- Report: `.torusguard/runs/<run_id>/report.md`
```
