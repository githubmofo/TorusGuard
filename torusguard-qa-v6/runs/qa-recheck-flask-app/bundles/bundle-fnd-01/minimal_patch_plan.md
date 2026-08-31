# Minimal Patch Plan for `fnd-01`

```diff
--- a/app.py
+++ b/app.py
@@ -16,1 +16,2 @@
-f.save(os.path.join("/var/uploads", f.filename))
+safe_name = secure_filename(f.filename)
+f.save(os.path.join("/var/uploads", safe_name))
```
