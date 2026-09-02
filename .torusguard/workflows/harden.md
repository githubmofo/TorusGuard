# /torusguard harden — Governed Remediation Bundle Packaging

**Command:** `/torusguard harden [run_id]`  
**Primary Agent:** `remediator` (`.torusguard/agents/remediator.md`)  
**Lifecycle Phase:** Phase 4 (Remediation Formulation)

---

## Objective
Package findings into self-contained, cluster-specific Remediation Bundles featuring framework-native Before / After diffs, bounded additions and deletions, and prioritized by runtime exploitability findings.

---

## Execution Steps

### Step 1: Load Findings & Exploitability State
1. Load findings from the latest run folder or specified `run_id`.
2. Prioritize clusters containing `Runtime Confirmed` or `High Confidence` findings.

### Step 2: Formulate Remediation Bundles
For each root-cause cluster:
1. Create a dedicated bundle folder: `.torusguard/runs/<run-id>/bundles/<cluster-id>/`.
2. Generate framework-specific Before / After code diffs using guidelines from `.torusguard/references/`.
3. Check diff against **Ponytail Governance Rules**:
   - Additions $\le 35$ lines.
   - Deletions $\le 25$ lines.
   - If limits exceeded, break down into atomic steps or flag as architectural change.
4. Check for high-risk context keywords (`auth`, `password`, `token`, `secret`, `tenant`, `admin`). If present, attach `[MANDATORY SECURITY SIGN-OFF]` flag.

### Step 3: Bundle Artifacts
Write bundle artifacts:
- `finding.md`: Concise description of flaw and practical risk.
- `minimal_patch_plan.md`: Step-by-step minimal intervention plan.
- `candidate.patch`: Ready-to-apply unified diff.
- `bundle.json`: Structured bundle metadata.

### Step 4: Write Unified Plan
Generate `.torusguard/runs/<run-id>/remediation.md` listing all candidate bundles and their patch sizes.

### Step 5: Output Summary
```markdown
🔧 [TorusGuard] Remediation Bundles Formulated
- Total Bundles: <Count>
- Governed Patches (<=35 lines add): All compliant
- High-Risk Context Bundles: <Count requiring sign-off>
- Remediation Plan: .torusguard/runs/<run-id>/remediation.md

Next Step: Run `/torusguard apply [bundle-id]` to review and apply a patch.
```
