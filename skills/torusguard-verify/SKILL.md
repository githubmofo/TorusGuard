---
name: torusguard-verify
description: Verify evidence sufficiency, audit live disk state, and calculate objective 0–100 confidence scores for findings.
version: 0.9.2
workflow: .torusguard/workflows/verify.md
tools: Read, Grep, Glob, Write
scripts-binding:
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Verify — Evidence Verification & Confidence Scoring

## Objective
Evaluate finding evidence sufficiency, audit cited source code against current live disk state, re-compute confidence scores using the auditable 5-factor rubric, and eliminate false positives before remediation.

---

## Execution Steps

### Step 1: Load Findings
Read findings from `.torusguard/runs/<latest-run>/findings.md` or parse active findings list.

### Step 2: Live Disk Cross-Check
For each finding:
1. Open cited source file on disk.
2. Verify cited line numbers and context match the stored `primaryLocationLineHash`.
3. If file has been modified or deleted, flag as `Stale Context / Requires Re-scan`.

### Step 3: Evidence Sufficiency Evaluation
Audit each finding across the 5 rubric dimensions:
1. **Evidence Quality (Max 35)**:
   - Direct AST match with source citation = 35 pts.
   - Text regex match without AST parsing = 20 pts.
   - Indirect heuristic indicator = 10 pts.
2. **Reproduction Success (Max 25)**:
   - Deterministic unit test or runtime trace exists = 25 pts.
   - Partial trace or simulated path = 15 pts.
   - Purely static inference = 0 pts.
3. **Independent Confirmations (Max 15)**:
   - Confirmed in 3+ independent callers/files = 15 pts.
   - Confirmed in 2 files = 10 pts.
   - Single isolated file = 5 pts.
4. **Environmental Clarity (Max 15)**:
   - Direct routable endpoint with visible controller = 15 pts.
   - Minor middleware indirection = 8 pts.
   - Ambiguous or unreachable dead code = 0 pts.
5. **Manual Review Status (Max 10)**:
   - Verified by security engineer = 10 pts.
   - Secondary agent consensus = 5 pts.
   - Unreviewed = 0 pts.

### Step 4: Recalculate Confidence Scores
Execute `finding_scorer.py`:
```bash
python .torusguard/scripts/finding_scorer.py --evidence AST_MATCH --repro TEST_REPRO --independent MULTI_FILE --clarity DIRECT_ROUTE
```
Update confidence bands:
- `Confirmed`: Score $\ge 90$
- `High Confidence`: Score $70–89$
- `Medium Confidence`: Score $50–69$
- `Needs Review`: Score $< 50$

### Step 5: Update Finding Status
Update findings ledger in the active run folder with verified scores and evidence notes.

---

## Evidence Sufficiency Checklist
```
□ Cited file exists on disk and lines match primaryLocationLineHash
□ AST data flow from untrusted source to sensitive sink is verifiable
□ Finding is not dead code or disabled by feature flag
□ No competing security middleware (WAF, route guard) neutralizes the flaw
□ Confidence score mathematically verified across all 5 dimensions
```

---

## Safety Constraints
- Strictly non-destructive analysis; no files are modified.
- Never inflate confidence scores without verifiable concrete evidence.
- Findings scoring below 50 must be labeled `Needs Review` and excluded from automated patch generation.

---

## Output Format
```markdown
🛡️ [TorusGuard] Evidence Verification Completed
- Findings Audited: <Count>
- Confirmed (Score >= 90): <Count>
- High Confidence (70-89): <Count>
- Medium Confidence (50-69): <Count>
- Needs Review (< 50): <Count>
- False Positives Cleared: <Count>

Next Step: Run `/torusguard harden` to package remediation bundles for Confirmed findings.
```
