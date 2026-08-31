# TorusGuard v6 Remediation Bundles

## 🛠️ Bundle: `bundle-fnd-01` — Missing Multi-Tenant Query Scoping

- **Target Finding:** `fnd-01` (`TG-DB-004`)
- **Target Files:** `views.py`

### What Is Wrong
Direct object query lacks tenant ownership scope.

### What Should Change
Scope query by request.user.tenant_id.

### Proposed Minimal Diff
```diff
--- a/views.py
+++ b/views.py
@@ -6,1 +6,1 @@
-invoice = Invoice.objects.get(id=invoice_id)
+invoice = get_object_or_404(Invoice, id=invoice_id, tenant_id=request.user.tenant_id)
```

### Verification After Change
Query an invoice belonging to a different tenant and confirm 404.

---

## 🛠️ Bundle: `bundle-fnd-01` — Disabled Template Autoescaping via mark_safe

- **Target Finding:** `fnd-01` (`TG-INPUT-005`)
- **Target Files:** `views.py`

### What Is Wrong
mark_safe bypasses HTML autoescaping on user input.

### What Should Change
Pass raw invoice model to template and rely on autoescaping.

### Proposed Minimal Diff
```diff
--- a/views.py
+++ b/views.py
@@ -8,2 +8,1 @@
-rendered = mark_safe(f"<h1>{invoice.title}</h1>")
-return render(request, "detail.html", {"content": rendered})
+return render(request, "detail.html", {"invoice": invoice})
```

### Verification After Change
Inject script tag in title and confirm escaping in rendered HTML.

---
