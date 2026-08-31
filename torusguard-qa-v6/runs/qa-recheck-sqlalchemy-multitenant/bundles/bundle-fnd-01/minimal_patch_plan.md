# Minimal Patch Plan for `fnd-01`

```diff
--- a/queries.py
+++ b/queries.py
@@ -5,1 +5,1 @@
-return db.query(Account).filter(Account.id == account_id).first()
+return db.query(Account).filter(Account.id == account_id, Account.tenant_id == tenant_id).first()
```
