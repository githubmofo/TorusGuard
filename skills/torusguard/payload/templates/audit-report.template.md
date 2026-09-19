# TorusGuard Security Audit & Runtime Verification Report

> **TorusGuard Version:** `{{torusguard_version}}`  
> **Target:** `{{target_name}}`  
> **Run ID:** `{{run_id}}`  
> **Timestamp:** `{{timestamp}}`  

---

## Detected Stack
- **Language:** {{stack_language}}
- **Framework:** {{stack_framework}}
- **Data Layer:** {{stack_data_layer}}
- **Dependency Files:** {{stack_dependency_files}}
- **Detection Confidence:** {{stack_confidence}}

---

## Executive Posture
**Posture:** {{posture_indicator}}  
**Average Confidence Score:** `{{avg_confidence_score}}/100`

### Finding Summary
| Severity | Count | Confirmed | Needs Review | Remediated |
| :--- | :---: | :---: | :---: | :---: |
| 🔴 **Critical** | {{critical_count}} | {{critical_confirmed}} | {{critical_review}} | {{critical_fixed}} |
| 🟠 **High** | {{high_count}} | {{high_confirmed}} | {{high_review}} | {{high_fixed}} |
| 🟡 **Medium** | {{medium_count}} | {{medium_confirmed}} | {{medium_review}} | {{medium_fixed}} |
| 🔵 **Low** | {{low_count}} | {{low_confirmed}} | {{low_review}} | {{low_fixed}} |

---

## Root-Cause Clusters
{{cluster_summary_table}}

---

## Detailed Findings
{{finding_cards_section}}

---

## Governance & Safety Audit Statement
This execution complied with TorusGuard v0.8.0 governance rules:
- **Authorization Gate:** {{authorization_status}}
- **Patch Governance (Ponytail):** Additions $\le 35$, Deletions $\le 25$.
- **Token Redaction:** All captured authorization headers, bearer tokens, and passwords were redacted.

---

## Prioritized Next Steps
1. **Remediate Confirmed Sinks:** Run `/torusguard harden` to package remediation bundles.
2. **Apply Governed Fixes:** Run `/torusguard apply <bundle_id>` to apply targeted fixes.
3. **Verify Fixes:** Run `/torusguard recheck` to ensure no regressions exist.
