# TorusGuard Skill Reference: Django REST Framework (DRF)

> **Loaded When:** Project uses `rest_framework` dependencies or imports.

---

## 🛡️ Key Inspection Areas & Rules

### 1. Permissions & Endpoint Exposure
* `TG-AUTH-001`: Inspect `settings.py` for `REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']`. If missing or set to `AllowAny`, verify that individual views specify explicit `permission_classes`.
* `TG-AUTH-007`: In `ModelViewSet` and API views, check if `get_queryset()` returns `Model.objects.all()` without filtering by `request.user` or tenant context.

### 2. Serializer Field Whitelists & Mass Assignment
* `TG-AUTH-006`: Inspect Serializer classes. Flag serializers where `fields = '__all__'` or where administrative/financial fields are not in `read_only_fields`.

### 3. Throttling & Rate Limits
* `TG-RATE-001`: Check authentication endpoints (login, password reset, register, OTP) for throttle classes (`UserRateThrottle`, `ScopedRateThrottle`).

### 4. Pagination Caps
* `TG-RATE-002`: Check custom pagination classes for `max_page_size`. If client-controlled `page_size_query_param` is enabled without a ceiling, flag as unbound resource risk.
