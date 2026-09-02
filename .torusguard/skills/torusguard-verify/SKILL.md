---
name: torusguard-verify
description: Verify finding evidence sufficiency, audit live code line matches, and calibrate 0–100 confidence scores.
version: 0.9.2
workflow: .torusguard/workflows/verify.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Verify — Finding Evidence Verification & Calibration

## Objective
Audit the evidence sufficiency of candidate findings by reading current disk lines, evaluating unbroken taint source-to-sink flow, filtering false alarms, and calibrating final 0–100 confidence scores.

---

## Execution Steps

1. **Locate Target Findings:** Load active findings from `.torusguard/runs/<latest-run>/findings.md`.
2. **Live Disk Line Match:** Inspect exact cited lines using `view_file` to confirm code presence.
3. **Audit Evidence Sufficiency:** Verify source-to-sink flow against criteria below.
4. **Calibrate Confidence Score:**
   ```bash
   python .torusguard/scripts/finding_scorer.py --run <run_dir> --verify
   ```
5. **Update State:** Mark finding as `Confirmed`, `Needs Review`, or `False Positive`.
6. **Emit Verified Evidence:** Save report in `.torusguard/runs/<run_id>/verified-evidence.md`.

---

## Evidence Sufficiency
A finding is verified as sufficient when:
- **Direct AST Match:** The vulnerable API or sink call exists on disk at the cited location.
- **Exposed Surface:** The sink is reachable from an external route, view, or public method.
- **Absence of Sanitizer:** No escaping function, parameterization, or validating middleware neutralizes the input.
- **Taint Integrity:** Untrusted request data flows into the sink without structural validation.

---

## Safety Constraints
- Read-only analysis; no files are modified.
- Never guess line numbers; always verify via active disk read.
- Downgrade findings with sanitizer presence to `False Positive`.

---

## Output Format
```markdown
🧪 [TorusGuard] Finding Verification Complete
- Findings Audited: <Count> | Confirmed Real: <Count>
- False Positives Filtered: <Count> | Refined Mean Score: <Score>/100
- Artifact: `.torusguard/runs/<run_id>/verified-evidence.md`
Next: Run `/torusguard harden` to formulate surgical fixes for confirmed flaws.
```
