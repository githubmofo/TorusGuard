# Minimal Patch Plan for `fnd-01`

```diff
--- a/storage.py
+++ b/storage.py
@@ -6,2 +6,4 @@
-dest = os.path.join(UPLOAD_DIR, raw_filename)
+safe_name = secure_filename(raw_filename)
+dest = (UPLOAD_DIR / safe_name).resolve()
```
