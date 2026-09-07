# TorusGuard Custom Rules Directory

Place your custom organization-specific, framework-specific, or proprietary library rules here.
Any markdown files (`*.md`) or JSON files (`*.json`) placed in this directory will be automatically indexed during `/torusguard-audit` and finding scoring.

---

## Example Custom Rule: `TG-CUSTOM-001.md`

```markdown
# TG-CUSTOM-001: Require Organization UUID on All Multi-Tenant Queries

**Rule ID:** TG-CUSTOM-001
**Severity:** High
**Category:** database-safety
**Confidence Base:** 85

### Description
Ensure all database operations on multi-tenant tables enforce explicit `org_id` or `tenant_id` boundaries.

### Unsafe Pattern
```python
db.execute("SELECT * FROM invoices WHERE status = 'paid'")
```

### Safe Remediation
```python
db.execute("SELECT * FROM invoices WHERE status = 'paid' AND org_id = %s", [current_org_id])
```
```
