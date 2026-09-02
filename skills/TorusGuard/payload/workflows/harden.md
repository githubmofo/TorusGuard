---
description: Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: remediator
lifecycle-phase: Phase 4 (Remediation Formulation)
required-skills:
  - torusguard-harden
scripts-binding:
  - .torusguard/scripts/run_manager.py
---

# /torusguard harden — Governed Remediation & Bundle Packaging

$ARGUMENTS

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Mandatory Pre-Flight Context Inspection

Before formulating remediation patches, you MUST inspect:

1. **Active Finding Manifest (`.torusguard/runs/<latest-run>/findings.md`)** → Identify the prioritized findings targeted for remediation.
2. **The Ponytail Protocol Bounds** → Enforce hard line churn constraints: $\le 35$ additions and $\le 25$ deletions per bundle. No full-file rewrites.
3. **Sensitive Path Sign-Off** → Check if targeted files touch authentication, billing, or core database schema (`auth.py`, `models.py`, `settings.py`). If so, flag as `Requires Sensitive-Path Sign-Off`.
4. **Behavior Preservation** → Ensure the patch strictly fixes the security flaw without modifying unrelated business logic, API schemas, or test contracts.

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## When to Use /torusguard harden

| Use `/torusguard harden` when... | Use something else when... |
| :--- | :--- |
| Generating surgical patches for findings | Actually writing changes to disk → `/torusguard apply` |
| Formulating minimal unified diffs | Discovering vulnerabilities → `/torusguard audit` |
| Packaging 4-artifact remediation bundles | Checking if patches broke anything → `/torusguard recheck` |
| Reviewing security fixes before applying | Full automated pipeline → `/torusguard full` |

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Execution Steps (Fixed Order)

### Phase 1 — Target Selection & Finding Analysis
Select prioritized findings from the active run:
- Focus first on `Confirmed` and `High Confidence` clusters.
- Locate exact AST node responsible for the vulnerability.

### Phase 2 — Surgical Unified Diff Generation
Formulate minimal unified diff conforming to the **Ponytail Protocol**:
- **Max Additions**: $\le 35$ lines.
- **Max Deletions**: $\le 25$ lines.
- **Surgical edits only**: Parameterize queries, add tenant filters, insert Pydantic models, or add cookie security flags.
- **Zero Full-File Rewrites**: Only modify the exact vulnerable function.

### Phase 3 — Line Churn Verification
Count added and deleted lines in the generated unified diff.
If churn exceeds bounds:
- Partition into sequential sub-bundles (Bundle A, Bundle B), OR
- Escalate to `Requires Manual Architectural Refactor` if the change requires structural redesign.

### Phase 4 — Package the 4-Artifact Remediation Bundle
Create bundle directory under active run: `.torusguard/runs/<run-id>/patches/<bundle-id>/` containing:
1. `patch.diff`: Clean unified diff compatible with `git apply`.
2. `metadata.json`: Bundle ID, targeted finding IDs, line churn metrics, and author agent.
3. `explanation.md`: Clear technical explanation of the flaw, the fix rationale, and side-effect analysis.
4. `pre_apply/`: Empty staging folder reserved for pre-apply rollback snapshots.

### Phase 5 — Human Gate Readiness
Prepare diff preview for operator review. No files are modified on disk during `/torusguard harden`.

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Failure Recovery & Cascade Rules

```
Finding not found:    HALT — Verify finding ID against active run findings.md
Ponytail exceeded:    Partition into smaller sub-bundles or flag for manual refactor
Conflicting diff:     Re-read active disk file to resolve line drift; regenerate patch
Sensitive path:       Highlight with ⚠️ SENSITIVE PATH REQUIRES EXPLICIT APPROVAL
```

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Hallucination Guard

```
❌ Never touch or reformat unrelated lines of code
❌ Never delete existing tests, comments, or error handlers
❌ Never generate a patch that exceeds 35 additions or 25 deletions in a single bundle
❌ Never write changes to source files on disk during the harden phase (reserved for apply)
```

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Output Card Format

```markdown
🛡️ [TorusGuard] Remediation Bundle Packaged
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bundle ID:          [bundle-TG-DB-004-django-tenant-idor]
Target File:        [apps/invoices/views.py]
Target Finding:     [TG-DB-004-django-tenant-idor]
Ponytail Bounds:    Additions: +4 lines (limit: 35) ✅ | Deletions: -2 lines (limit: 25) ✅
Risk Level:         Low (Surgical query scoping)
Sensitive Path:     No (Standard view layer)
Bundle Path:        .torusguard/runs/<run-id>/patches/bundle-TG-DB-004/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Diff Preview:
```diff
@@ -42,3 +42,5 @@ def get_invoice(request, invoice_id):
-    invoice = Invoice.objects.get(id=invoice_id)
+    tenant = get_current_tenant(request)
+    invoice = Invoice.objects.filter(tenant=tenant, id=invoice_id).first()
+    if not invoice:
+        raise Http404("Invoice not found")
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Step: Run `/torusguard apply bundle-TG-DB-004` to review and write to disk.
```

---

## Objective
Governed remediation formulation under strict Ponytail Protocol bounds (<= 35 additions, <= 25 deletions) and bundle packaging.

---

## Next Steps

| Outcome | Next Command |
| :--- | :--- |
| Bundle generated and reviewed | → `/torusguard apply <bundle-id>` |
| Additional findings need hardening | → Continue `/torusguard harden` |
| Want end-to-end audit + patch | → `/torusguard full` |
