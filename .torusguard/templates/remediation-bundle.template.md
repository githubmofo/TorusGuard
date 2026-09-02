# Remediation Bundle: `{{bundle_id}}`

**Cluster ID:** `{{cluster_id}}`  
**Target Rule:** `{{rule_id}}` (`{{rule_title}}`)  
**Affected Files:** `{{affected_files}}`  

---

## 1. Problem Statement & Risk
{{problem_statement}}

**Adversarial Abuse & Practical Impact:**  
{{risk_explanation}}

---

## 2. Governed Minimal Patch Plan
- **Max Additions Boundary:** $\le 35$ lines (Proposed: `+{{additions_count}}`)
- **Max Deletions Boundary:** $\le 25$ lines (Proposed: `-{{deletions_count}}`)
- **Governance Review Level:** `{{governance_review_level}}`

### Framework-Native Diff
```diff
{{candidate_patch_diff}}
```

---

## 3. Verification & Retest Method
{{verification_method}}

---

## 4. Residual Risk & Edge Cases
{{residual_risk_notes}}
