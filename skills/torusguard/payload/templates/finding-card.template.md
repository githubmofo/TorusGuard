### [{{rule_id}}] {{finding_title}}

**Severity:** `{{severity_badge}}` | **Auditable Confidence:** `{{confidence_score}}/100 {{confidence_band_badge}}`  
**Finding ID:** `{{finding_id}}` | **Fingerprint:** `{{fingerprint_hash}}`  
**Target Location:** `{{file_path}}:{{line_number}}` (`{{code_symbol}}`)  
**Lifecycle Status:** `{{lifecycle_status}}` | **Exploitability:** `{{exploitability_status}}`  

---

#### 1. Provenance Chain
- **Detection Rule:** `{{rule_id}}` (CWE-{{cwe_id}})
- **Triggering Input:** `{{triggering_source}}`
- **Sink Path:** `{{sink_expression}}`

#### 2. Raw Verified Evidence
```{{code_language}}
{{raw_evidence_snippet}}
```
> **Evidence Checksum (SHA-256):** `{{evidence_sha256}}`

#### 3. Objective Facts vs AI Interpretation
- **Verified Facts:** {{raw_facts_summary}}
- **AI Risk Analysis:** {{ai_interpretation}}

#### 4. Remediation Diff (Minimal Churn)
```diff
{{remediation_diff_preview}}
```

#### 5. Retest & Verification
- **Verification Method:** {{verification_method}}
- **Current Retest Status:** `{{retest_status}}`
