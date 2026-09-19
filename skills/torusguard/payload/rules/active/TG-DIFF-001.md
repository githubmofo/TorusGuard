---
id: TG-DIFF-001
name: Accidental Security Check Bypass in Patch
severity: CRITICAL
category: Patch Governance / Diff Safety
cwe: CWE-693
---

# TG-DIFF-001: Accidental Security Check Bypass in Patch Additions

## Summary
Flags unified diff additions (`+`) that introduce bypass comments (`# bypass auth`, `// nosec`), disabled certificate checks (`verify=False`), or explicit bypass flags (`skip_auth=True`).

## Detection Invariants
- Additions containing comments: `bypass auth`, `skip security check`, `disable_token_check`.
- Additions setting `verify=False` in network HTTP clients.
- Additions disabling CSRF protection (`@csrf_exempt`).

## Remediation
Ensure security controls remain active in generated patches. Never disable certificate checks or bypass authentication barriers to make code pass tests.
