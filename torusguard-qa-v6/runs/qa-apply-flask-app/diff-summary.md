# TorusGuard v6 Unified Diff Summary

## Applied Patch: `fnd-01` (`app.py`)
```diff
--- a/app.py
+++ b/app.py
@@ -10,1 +10,1 @@
-return render_template_string(f"Hello {name}")
+return render_template("greet.html", name=name)
```

## Applied Patch: `fnd-01` (`app.py`)
```diff
--- a/app.py
+++ b/app.py
@@ -16,1 +16,2 @@
-f.save(os.path.join("/var/uploads", f.filename))
+safe_name = secure_filename(f.filename)
+f.save(os.path.join("/var/uploads", safe_name))
```
