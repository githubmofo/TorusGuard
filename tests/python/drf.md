# DRF Rule Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-AUTH-007` | Object Ownership IDOR | `views.py` | `InvoiceViewSet` queries `Invoice.objects.all()` | Flagged as Tenant Scoping / IDOR Risk | Confirmed |
| `TG-AUTH-006` | Mass Assignment | `serializers.py` | `UserSerializer` lacks `read_only_fields` on role | Flagged as Mass Assignment Risk | Confirmed |
| `TG-RATE-001` | Missing Throttling | `views.py` | Password reset view lacks throttle classes | Flagged as Rate Limit Defect | Likely |
| `TG-RATE-002` | Unbounded Pagination | `pagination.py` | `PageNumberPagination` missing `max_page_size` | Flagged as Resource Consumption Risk | Confirmed |
| `TG-AUTH-001` | Default Permissions | `settings.py` | `REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']` | Verified Default Deny Configuration | Confirmed |
