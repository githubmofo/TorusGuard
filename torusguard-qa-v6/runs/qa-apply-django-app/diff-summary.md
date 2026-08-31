# TorusGuard v6 Unified Diff Summary

## Applied Patch: `fnd-01` (`views.py`)
```diff
--- a/views.py
+++ b/views.py
@@ -6,1 +6,1 @@
-invoice = Invoice.objects.get(id=invoice_id)
+invoice = get_object_or_404(Invoice, id=invoice_id, tenant_id=request.user.tenant_id)
```

## Applied Patch: `fnd-01` (`views.py`)
```diff
--- a/views.py
+++ b/views.py
@@ -8,2 +8,1 @@
-rendered = mark_safe(f"<h1>{invoice.title}</h1>")
-return render(request, "detail.html", {"content": rendered})
+return render(request, "detail.html", {"invoice": invoice})
```
