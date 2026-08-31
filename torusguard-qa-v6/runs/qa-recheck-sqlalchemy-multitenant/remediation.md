# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Missing Tenant Query Isolation in SQLAlchemy

- **Target Finding:** `fnd-01` (`TG-DB-004`)
- **Target Files:** `queries.py`

### What Is Wrong
Query filters by ID without tenant boundary enforcement.

### What Should Change
Add tenant_id predicate to query filter.

### Proposed Minimal Diff
```diff
--- a/queries.py
+++ b/queries.py
@@ -5,1 +5,1 @@
-return db.query(Account).filter(Account.id == account_id).first()
+return db.query(Account).filter(Account.id == account_id, Account.tenant_id == tenant_id).first()
```

### Verification After Change
Query account belonging to another tenant and assert None returned.

---
