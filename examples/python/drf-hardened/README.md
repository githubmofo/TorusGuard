# Hardened DRF API Reference Application

> **Purpose:** Reference implementation demonstrating TorusGuard-compliant security patterns for Django REST Framework APIs.

---

## 🛡️ Applied Security Controls

1. **Default Deny Permissions (`TG-AUTH-001`):** `DEFAULT_PERMISSION_CLASSES` set to `IsAuthenticated`.
2. **Tenant Scoping (`TG-AUTH-007`):** ViewSets override `get_queryset()` to filter records by `request.user`.
3. **Protected Serializer Fields (`TG-AUTH-006`):** Serializers declare strict `read_only_fields` for roles and permissions.
4. **Scoped Throttling (`TG-RATE-001`):** Sensitive authentication actions configure scoped throttle rates.
5. **Bounded Pagination (`TG-RATE-002`):** Custom pagination classes enforce `max_page_size`.

See [fixes.md](fixes.md) for remediation details.
