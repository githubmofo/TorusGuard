---
id: TG-DIFF-003
name: Unintentional Removal of Tenant Filter in Patch Deletions
severity: HIGH
category: Patch Governance / Tenant Isolation
cwe: CWE-284
---

# TG-DIFF-003: Unintentional Removal of Tenant Filter in Patch Deletions

## Summary
Flags unified diff deletions (`-`) where tenant isolation scoping queries (e.g. `.filter(tenant=...)` or `where tenant_id =`) are removed without being reinstated in the corresponding patch additions.

## Detection Invariants
- Deleted lines matching `.filter(tenant=` or `tenant_id =`.
- Corresponding added lines omitting equivalent tenant parameter bindings.

## Remediation
Ensure multi-tenant database queries retain tenant boundary clauses across all refactorings and bug fixes.
