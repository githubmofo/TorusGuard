# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Production Debug Mode Enabled

- **Target Finding:** `fnd-01` (`TG-PLATFORM-003`)
- **Target Files:** `app.py`

### What Is Wrong
DEBUG is statically enabled.

### What Should Change
Load DEBUG from environment variables.

### Proposed Minimal Diff
```diff
--- a/app.py
+++ b/app.py
@@ -1,1 +1,2 @@
-DEBUG = True
+import os
+DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### Verification After Change
Check DEBUG setting resolution in production.

---

## 🛠️ Bundle: `bundle-fnd-01` — Hardcoded Secret Key

- **Target Finding:** `fnd-01` (`TG-SEC-001`)
- **Target Files:** `app.py`

### What Is Wrong
Hardcoded secret exposed in source code.

### What Should Change
Load SECRET_KEY from environment variables.

### Proposed Minimal Diff
```diff
--- a/app.py
+++ b/app.py
@@ -2,1 +2,1 @@
-SECRET_KEY = "sk_live_1234567890"
+SECRET_KEY = os.environ["APP_SECRET_KEY"]
```

### Verification After Change
Verify secret key is not in source control.

---
