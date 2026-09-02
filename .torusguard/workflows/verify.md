# /torusguard verify — Finding Confidence & Evidence Verification

**Command:** `/torusguard verify [finding_id]`  
**Primary Agent:** `validator` (`.torusguard/agents/validator.md`)  
**Lifecycle Phase:** Phase 2.5 (Evidence Verification)

---

## Objective
Verify the evidence sufficiency of a specific finding or all findings from the latest audit, evaluate AST code context, check for mitigating middleware or service layers, and compute the auditable 0–100 confidence score.

---

## Execution Steps

### Step 1: Load Finding & Context
1. Load finding details from the latest run folder (`.torusguard/runs/<latest>/findings.md` or JSON).
2. Fetch the referenced source code file and line numbers.

### Step 2: Code & Context Evaluation
1. Check if the line snippet contains exact syntax matching the vulnerability pattern.
2. Check caller hierarchy:
   - Does a higher-level decorator, middleware, or dependency guard the route?
   - If an authorization guard or domain service handles the check, reduce confidence score accordingly.

### Step 3: Compute Rubric Breakdown
Compute points across the 5 dimensions:
```markdown
### Confidence Breakdown: [TG-FIND-XXXX]
- Evidence Quality: 35/35 (Exact AST pattern verified)
- Reproduction Success: 0/25 (Static audit only; no runtime execution)
- Independent Confirmations: 15/15 (Corroborated across 3 models)
- Environmental Clarity: 15/15 (Direct controller-to-query path)
- Manual Review: 0/10 (Pending human review)
Total Score: 65/100 -> Medium Confidence
```

### Step 4: Recommend Next Step
- Score $\ge 90$: Prioritize immediate remediation with `/torusguard harden`.
- Score $50–89$: Recommend live verification with `/torusguard web-validate` or `/torusguard exploit-check`.
- Score $< 50$: Classify as `Needs Review` and prompt developer for manual architectural confirmation.
