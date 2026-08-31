# Minimal Patch Plan for `fnd-01`

```diff
--- a/views.py
+++ b/views.py
@@ -8,2 +8,1 @@
-rendered = mark_safe(f"<h1>{invoice.title}</h1>")
-return render(request, "detail.html", {"content": rendered})
+return render(request, "detail.html", {"invoice": invoice})
```
