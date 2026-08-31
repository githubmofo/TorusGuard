# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Unvalidated Outbound HTTP Request (SSRF)

- **Target Finding:** `fnd-01` (`TG-SSRF-001`)
- **Target Files:** `main.py`

### What Is Wrong
Outbound HTTP request made directly to unvalidated user-supplied URL.

### What Should Change
Validate URL host against strict allowlist and validate format with HttpUrl.

### Proposed Minimal Diff
```diff
--- a/main.py
+++ b/main.py
@@ -7,3 +7,4 @@
-async def fetch_url(url: str):
+async def fetch_url(url: HttpUrl):
+    if url.host not in ALLOWED_DOMAINS: raise HTTPException(400)
```

### Verification After Change
Send request with url=http://169.254.169.254 and assert 400 rejection.

---

## 🛠️ Bundle: `bundle-fnd-01` — Untrusted Role Header Injection

- **Target Finding:** `fnd-01` (`TG-AUTH-008`)
- **Target Files:** `main.py`

### What Is Wrong
Authorization decision trusts unverified client request header.

### What Should Change
Derive user roles from validated JWT session dependency.

### Proposed Minimal Diff
```diff
--- a/main.py
+++ b/main.py
@@ -13,2 +13,2 @@
-async def admin_panel(x_user_role: str = Header(None)):
-    if x_user_role != "admin":
+async def admin_panel(current_user = Depends(get_verified_current_user)):
+    if "admin" not in current_user.roles:
```

### Verification After Change
Send spoofed X-User-Role header without authentication and assert 403.

---
