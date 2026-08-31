# Minimal Patch Plan for `fnd-01`

```diff
--- a/app.py
+++ b/app.py
@@ -2,1 +2,1 @@
-SECRET_KEY = "sk_live_1234567890"
+SECRET_KEY = os.environ["APP_SECRET_KEY"]
```
