# TorusGuard v6 Unified Diff Summary

## Applied Patch: `fnd-01` (`main.py`)
```diff
--- a/main.py
+++ b/main.py
@@ -7,3 +7,4 @@
-async def fetch_url(url: str):
+async def fetch_url(url: HttpUrl):
+    if url.host not in ALLOWED_DOMAINS: raise HTTPException(400)
```

## Applied Patch: `fnd-01` (`main.py`)
```diff
--- a/main.py
+++ b/main.py
@@ -13,2 +13,2 @@
-async def admin_panel(x_user_role: str = Header(None)):
-    if x_user_role != "admin":
+async def admin_panel(current_user = Depends(get_verified_current_user)):
+    if "admin" not in current_user.roles:
```
