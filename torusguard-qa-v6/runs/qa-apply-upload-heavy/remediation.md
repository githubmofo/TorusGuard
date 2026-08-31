# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Path Traversal in Storage Handler

- **Target Finding:** `fnd-01` (`TG-INPUT-006`)
- **Target Files:** `storage.py`

### What Is Wrong
raw_filename joined to destination path without canonicalization.

### What Should Change
Sanitize filename and assert resolved path resides within UPLOAD_DIR.

### Proposed Minimal Diff
```diff
--- a/storage.py
+++ b/storage.py
@@ -6,2 +6,4 @@
-dest = os.path.join(UPLOAD_DIR, raw_filename)
+safe_name = secure_filename(raw_filename)
+dest = (UPLOAD_DIR / safe_name).resolve()
```

### Verification After Change
Provide ../../../etc/passwd as raw_filename and assert rejection.

---
