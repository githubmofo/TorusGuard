# TorusGuard v6 Unified Diff Summary

## Applied Patch: `fnd-01` (`app.py`)
```diff
--- a/app.py
+++ b/app.py
@@ -1,1 +1,2 @@
-DEBUG = True
+import os
+DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

## Applied Patch: `fnd-01` (`app.py`)
```diff
--- a/app.py
+++ b/app.py
@@ -2,1 +2,1 @@
-SECRET_KEY = "sk_live_1234567890"
+SECRET_KEY = os.environ["APP_SECRET_KEY"]
```
