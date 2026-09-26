---
name: torusguard-verify
description: Verify finding evidence sufficiency, audit live code line matches, and calibrate 0–100 confidence scores.
version: 2.0.0
workflow: .torusguard/workflows/verify.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - .torusguard/scripts/report_sync.py
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Verify — Finding Evidence Verification & Calibration

## Objective
Audit the evidence sufficiency of candidate findings by reading current disk lines, evaluating unbroken taint source-to-sink flow, filtering false alarms, and calibrating final 0–100 confidence scores.

---

## Tri-Mode Parity

| Mode | Command / Tool | Governed Behavior |
| :--- | :--- | :--- |
| **Mode A: CLI Terminal** | `torusguard verify` | Verifies evidence across findings on disk, asserts line matches. |
| **Mode B: AI Chat Slash** | `/torusguard verify` | Performs live code inspection, audits source-to-sink taint flows. |
| **Mode C: Native MCP Tool**| `torusguard_audit` / verify | Diagnostic validation of candidate security findings. |

---

## Execution Steps

1. **Locate Target Findings:** Load active findings from `security_report.md` or `.torusguard/runs/<latest-run>/findings.md`.
2. **Live Disk Line Match:** Inspect exact cited lines using `view_file` to confirm code presence on disk. Do not rely on stale line numbers.
3. **Audit Evidence Sufficiency:** Verify source-to-sink flow against criteria below.
4. **Calibrate Confidence Score:**
   ```bash
   torusguard verify
   ```
5. **Update State:** Mark finding as `Confirmed`, `Needs Review`, or `False Positive`.
6. **Emit Verified Evidence:** Save report in `.torusguard/runs/<run_id>/verified-evidence.md`.

---

## Evidence Sufficiency Rubric
A finding is verified as sufficient when:
- **Direct AST Match:** The vulnerable API or sink call exists on disk at the cited location.
- **Exposed Surface:** The sink is reachable from an external route, view, or public method.
- **Absence of Sanitizer:** No escaping function, parameterization, or validating middleware neutralizes the input.
- **Taint Integrity:** Untrusted request data flows into the sink without structural validation.

---

## Living Report Ground Truth
- Always inspect `security_report.md` at workspace root before acting.
- Update finding statuses after completion to eliminate hallucination.

## Safety Constraints
- Read-only analysis; no files are modified.
- Never guess line numbers; always verify via active disk read.
- Downgrade findings with sanitizer presence to `False Positive`.

---

## Output Format
```markdown
🧪 [TorusGuard] Finding Verification Complete (AI Assisted)
- Findings Audited: <Count> | Confirmed Real: <Count>
- False Positives Filtered: <Count> | Refined Mean Score: <Score>/100
- Artifact: `.torusguard/runs/<run_id>/verified-evidence.md`
Next: Run `/torusguard harden` to formulate surgical fixes for confirmed flaws.
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Stale Line Reliance** | Assumes finding line number matches current disk state without inspecting active file. | Read live disk lines via `view_file` to verify the exact AST sink is located at that line. |
| **Sanitizer Blindness** | Flags parameterized queries or sanitized inputs as SQLi because raw SQL keywords exist. | Inspect surrounding lines ($\pm 3$) for parameter bindings (`?`, `$1`, prep statements) or sanitizers. |
| **Test Fixture Confusion** | Confirms vulnerabilities inside mock test files or test suites as production risks. | Check file path against test exclusion patterns (`_test.go`, `.test.ts`, `fixtures/`). Test vulnerabilities must be contextualized or ignored. |
| **Hallucinated Reachability** | Confirms private internal functions with no external caller as exploitable web attack surfaces. | Verify if the tainted source is actually reachable from public handlers or API routes. |

---

## ✅ Pre-Flight Self-Audit

Before calibrating or confirming any finding:
- [ ] Did I read the live file content directly from disk?
- [ ] Did I verify the exact cited code exists and matches the AST rule pattern?
- [ ] Did I check for neutralizing middleware, sanitizers, or parameterization in the context window?
- [ ] Did I verify that the file is not an excluded test fixture or mock?
- [ ] Is the confidence score (0-100) calibrated against real evidence, not assumptions?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Read cited file lines on disk to verify presence of the reported sink.
BUILD:   Trace source-to-sink flow and check for existing sanitizers or validators.
CONFIRM: Calibrate confidence score and record verified status in security_report.md.
```
