# Remediation Mapping: DRF Vulnerable -> Hardened

| Vulnerability | Rule ID | Vulnerable File | Hardened File | Security Control Applied |
|---|---|---|---|---|
| Unscoped Invoices (IDOR) | `TG-AUTH-007` | `views.py` | `views.py` | Override `get_queryset()` to filter by `request.user` |
| Writable Role / Mass Assignment | `TG-AUTH-006` | `serializers.py` | `serializers.py` | Add `read_only_fields = ['role', 'is_staff']` |
| Missing Throttle on Auth View | `TG-RATE-001` | `views.py` | `views.py` | Apply `throttle_classes = [ScopedRateThrottle]` |
| Unbounded Pagination Size | `TG-RATE-002` | `pagination.py` | `pagination.py` | Enforce `max_page_size = 100` |
