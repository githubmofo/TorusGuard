# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Server-Side Template Injection (SSTI)

- **Target Finding:** `fnd-01` (`TG-INPUT-005`)
- **Target Files:** `app.py`

### What Is Wrong
User input formatted directly into template string.

### What Should Change
Render static template file with contextual autoescaping.

### Proposed Minimal Diff
```diff
--- a/app.py
+++ b/app.py
@@ -10,1 +10,1 @@
-return render_template_string(f"Hello {name}")
+return render_template("greet.html", name=name)
```

### Verification After Change
Send name={{7*7}} and verify output contains literal {{7*7}} instead of 49.

---

## 🛠️ Bundle: `bundle-fnd-01` — Unsafe File Path Traversal

- **Target Finding:** `fnd-01` (`TG-INPUT-006`)
- **Target Files:** `app.py`

### What Is Wrong
Filename passed directly from client without sanitization.

### What Should Change
Sanitize with werkzeug secure_filename.

### Proposed Minimal Diff
```diff
--- a/app.py
+++ b/app.py
@@ -16,1 +16,2 @@
-f.save(os.path.join("/var/uploads", f.filename))
+safe_name = secure_filename(f.filename)
+f.save(os.path.join("/var/uploads", safe_name))
```

### Verification After Change
Send filename=../../etc/cron.d/job and confirm path traversal is blocked.

---
