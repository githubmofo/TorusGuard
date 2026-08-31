# Minimal Patch Plan for `fnd-01`

```diff
--- a/main.py
+++ b/main.py
@@ -13,2 +13,2 @@
-async def admin_panel(x_user_role: str = Header(None)):
-    if x_user_role != "admin":
+async def admin_panel(current_user = Depends(get_verified_current_user)):
+    if "admin" not in current_user.roles:
```
