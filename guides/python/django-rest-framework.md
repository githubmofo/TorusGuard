# Django REST Framework (DRF) Security Guide (TorusGuard v0.4.0)

> **Scope:** API security standards for Django REST Framework APIs. Covers default permissions, object-level authorization, serializer mass assignment, throttling, pagination caps, and sensitive data filtering.

---

## 🛡️ 1. Default Permission Classes (`TG-AUTH-001`, `TG-AUTH-003`)

Never leave `DEFAULT_PERMISSION_CLASSES` unconfigured or set to `AllowAny` globally.

### Safe Configuration (`settings.py`)
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # ✅ Secure by default
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'sensitive_action': '5/minute',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

---

## 👤 2. Object-Level Permissions & Queryset Scoping (`TG-AUTH-007`)

### ❌ Unsafe Pattern: Unscoped `get_queryset()`
```python
# VULNERABLE: Any authenticated user can view/edit any invoice by ID
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()  # ❌ Exposes all tenant records
    serializer_class = InvoiceSerializer
```

### ✅ Safe Pattern: Scoped Queryset + Custom Permission
```python
# SAFE: Scope queryset strictly to current authenticated user/organization
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsInvoiceOwner]

    def get_queryset(self):
        return Invoice.objects.filter(owner=self.request.user)

# Custom Object Permission
class IsInvoiceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

---

## 📝 3. Serializers & Mass Assignment (`TG-AUTH-006`)

Never allow client updates to sensitive fields like `role`, `is_verified`, `balance`, or `tenant_id`.

### ❌ Unsafe Pattern
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # ❌ Allows client to set is_staff, is_superuser, groups
```

### ✅ Safe Pattern
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'is_staff']
        read_only_fields = ['id', 'is_staff']  # ✅ Client cannot modify is_staff
```

---

## 🚦 4. Throttling & Resource Limits (`TG-RATE-001`)

* Apply dedicated scoped throttles to sensitive endpoints (login, password reset, OTP verification, payment initiation).
* **Important Design Note:** Throttling is one layer in defense-in-depth and does not replace authentication, CAPTCHA, or anomaly detection.

```python
class PasswordResetView(APIView):
    throttle_scope = 'sensitive_action'
    # ...
```

---

## 📄 5. Pagination & Unbounded Queries (`TG-RATE-002`)

Always configure a hard ceiling (`max_page_size`) on paginated endpoints to prevent attackers from executing denial-of-service queries like `?page_size=1000000`.

```python
class SafePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # ✅ Enforce hard upper bound
```

---

## 📋 Manual Review Checklist for DRF

- [ ] `DEFAULT_PERMISSION_CLASSES` defaults to `IsAuthenticated`.
- [ ] ViewSets override `get_queryset()` to enforce user/tenant scoping.
- [ ] Serializers use explicit `read_only_fields` for all privilege and financial fields.
- [ ] Sensitive actions have dedicated `ScopedRateThrottle` applied.
- [ ] Pagination enforces `max_page_size` limits.
