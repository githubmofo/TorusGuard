# Hardened Fixes Matrix: DRF API

| Risk | Rule ID | Hardened Implementation |
|---|---|---|
| IDOR in ViewSet | `TG-AUTH-007` | `def get_queryset(self): return Invoice.objects.filter(owner=self.request.user)` |
| Role Injection in Serializer | `TG-AUTH-006` | `read_only_fields = ['id', 'role', 'is_staff']` |
| Missing Throttle on Sensitive View | `TG-RATE-001` | `throttle_classes = [ScopedRateThrottle]` with `throttle_scope = 'sensitive_action'` |
| Unbounded Pagination Query | `TG-RATE-002` | `max_page_size = 100` |
