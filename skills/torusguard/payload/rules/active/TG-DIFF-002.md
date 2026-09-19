---
id: TG-DIFF-002
name: Secret and Token Ingestion in Patch Additions
severity: CRITICAL
category: Patch Governance / Secret Exposure
cwe: CWE-798
---

# TG-DIFF-002: Secret and Token Ingestion in Patch Additions

## Summary
Flags unified diff additions (`+`) that introduce hardcoded live API tokens, JWT strings, private key headers, or credentials into source files during remediation.

## Detection Invariants
- Additions containing regex patterns matching API keys (`sk_live_`, `ak_live_`).
- Additions introducing raw Bearer JWT tokens (`eyJ...`).
- Additions introducing private key blocks (`-----BEGIN PRIVATE KEY-----`).

## Remediation
Load credentials from environment variables (`os.environ["API_KEY"]` or `process.env.API_KEY`). Never hardcode secrets in remediation diffs.
