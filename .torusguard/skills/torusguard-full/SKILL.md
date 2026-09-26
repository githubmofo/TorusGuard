---
name: torusguard-full
description: Master 7-stage security pipeline orchestrator — coordinates discovery, authorization, static audit, runtime validation, governed remediation, recheck, and reporting.
version: 2.0.0
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Bash, Edit, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - internal/harden/patch.go
  - internal/apply/apply.go
  - .torusguard/scripts/report_sync.py
---

# TorusGuard Full — Master 7-Stage Pipeline Orchestrator

## Objective
Execute the full, closed-loop TorusGuard security lifecycle from stack discovery through static scanning, runtime validation, Ponytail remediation, differential re-check, and SARIF export under strict governance.

---

## Tri-Mode Pipeline Parity

| Stage | Mode A: Terminal CLI | Mode B: AI Chat Slash | Mode C: Native MCP Tool |
| :--- | :--- | :--- | :--- |
| **0. Init** | `torusguard init` | `/torusguard init` | Init + `torusguard_status` |
| **1. Authorize** | `torusguard authorize` | `/torusguard authorize` | Safety Gate Boundary |
| **2. Audit & Vision** | `torusguard audit` / `ocr-scan` | `/torusguard audit` / `ocr-scan` | `torusguard_audit` / `torusguard_ocr_scan` |
| **3. Verify** | `torusguard verify` | `/torusguard verify` | `torusguard_verify` |
| **4. Harden** | `torusguard harden` | `/torusguard harden` | `torusguard_harden` |
| **5. Apply** | `torusguard apply [--yes]` | `/torusguard apply` | Human Gate Approval |
| **6. Recheck** | `torusguard recheck` | `/torusguard recheck` | `torusguard_recheck` |
| **7. Report** | `torusguard report --html` | `/torusguard report` | `torusguard://security_report` |

---

## 7-Stage Security Pipeline
```
0. Init ──► 1. Authorize ──► 2. Audit ──► 3. Validate ──► 4. Harden ──► 5. Apply ──► 6. Recheck ──► 7. Report
(Baseline)   (Scope Gate)     (AST Scan)   (Evidence)     (Ponytail)   (Human Gate)  (Regression)   (SARIF/HTML)
```

---

## Specialist Skill Routing
- **Phase 0:** `torusguard-init` (`profiler`)
- **Phase 1:** `torusguard-authorize` (`reviewer`)
- **Phase 2:** `torusguard-audit` (`auditor`) / `torusguard-ocr-scan` (`vision`)
- **Phase 3:** `torusguard-verify` / `torusguard-exploit-check` (`validator`)
- **Phase 4:** `torusguard-harden` (`remediator`)
- **Phase 5:** `torusguard-apply` (`remediator`)
- **Phase 6:** `torusguard-recheck` (`reviewer`)
- **Phase 7:** `torusguard-report` (`reviewer`)

---

## Pipeline Execution Instructions
1. **Init:** Detect stack via `torusguard init` and activate tailored rules in `.torusguard/rules/active/`.
2. **Authorize:** Verify target ownership and TTL in `.torusguard/config/scope.json`.
3. **Audit:** Scan ASTs via `torusguard audit` (or `torusguard ocr-scan` for visual assets); assign fingerprints; compute confidence scores.
4. **Validate:** Audit evidence sufficiency; optionally send bounded probe canary.
5. **Harden:** Formulate surgical diffs bound by Ponytail limits ($\le 35$ additions, $\le 25$ deletions).
6. **Apply:** Capture `.bak` snapshot in `.torusguard/snapshots/`; obtain Human Gate; apply patch via `torusguard apply`.
7. **Recheck:** Re-scan modified files via `torusguard recheck`; assert findings are `Fixed` with zero regressions.
8. **Report:** Export OASIS SARIF v2.1.0 and emit visual HTML dashboard via `torusguard report --html`.

---

## Living Report Ground Truth
- Always inspect `security_report.md` at workspace root before acting.
- Update finding statuses after completion to eliminate hallucination.

## Safety & Governance
- Human Gate mandatory before code modifications in Phase 5.
- Enforce Ponytail line bounds ($\le 35$ additions, $\le 25$ deletions).
- Never dispatch network probes outside authorized scope in `scope.json`.
- Zero security bypasses permitted (`TG-DIFF-001`).

---

## Output Format
```markdown
🏆 [TorusGuard] 7-Stage Security Pipeline Complete
- Run ID: run-YYYYMMDD-HHMMSS | Status: SECURE / AUDITED
- Findings: <Total> (<Fixed> Fixed · <Open> Remaining)
- SARIF Log: `.torusguard/runs/<run_id>/results.sarif`
- Report: `.torusguard/runs/<run_id>/report.md`
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Pipeline Step Skipping** | Jumps directly from Audit to Apply without verifying evidence or validating Ponytail patch bounds. | Follow the 7 stages in sequential order; each stage gate must be satisfied. |
| **Human Gate Bypass** | Writes modifications directly to disk without presenting candidate diffs or awaiting user confirmation. | Always require explicit Human Gate confirmation before Phase 5 (`torusguard apply`). |
| **Full File Rewrites** | Rewrites complete source files during remediation, causing massive line churn and regression risk. | Formulate surgical patches respecting Ponytail bounds ($\le 35$ add, $\le 25$ del) using Line-Level Reflection. |
| **Unsynchronized State** | Generates reports that don't match the statuses in `security_report.md`. | Keep `security_report.md` synchronized at every phase transition as the single living source of truth. |

---

## ✅ Pre-Flight Self-Audit

Before orchestrating the full pipeline:
- [ ] Are all prerequisite tools (`torusguard` binary) available?
- [ ] Is `security_report.md` inspected prior to initiating any scans or fixes?
- [ ] Are all patches bounded by Ponytail limits and verified without security bypasses?
- [ ] Is a `.bak` snapshot captured before any disk modification?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Review current workspace security posture and verify phase prerequisites.
BUILD:   Execute the pipeline stage by stage using designated specialist skills.
CONFIRM: Validate final SARIF, HTML report, and synchronized security_report.md.
```
