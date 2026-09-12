# TorusGuard v0.3.0 External Repository Validation Report
Target: FastAPI Vulnerable App

> 🛡️ **TorusGuard Validation Heritage:** This document preserves empirical validation records for this framework and milestone. For the current v1.3.5 active release line, 74-rule AST engine, living security report ground truth (`security_report.md`), and automated test suite (81/81 passing via `npm test`), refer to the [Validation Suite Overview](README.md) and root [README](../../README.md).

Test type: Local, authorized repository review
Status: Validation completed

## Scope
- Repository: Local FastAPI Test
- Purpose: Validate TorusGuard against a Python/FastAPI stack.

## Verified Findings
### TG-SSRF-001
Status: Confirmed configuration finding
Evidence: The `/fetch` route directly passes a user-supplied URL to `requests.get()` without an allowlist or private IP filter.
Impact: SSRF

### TG-WEBHOOK-001
Status: Confirmed
Evidence: `/webhook` accepts an unauthenticated POST payload with no signature verification.

### TG-AUTH-006 (Mass Assignment)
Status: Manual review
Evidence: `/update_profile` accepts a raw `dict` which could map directly to model updates.
