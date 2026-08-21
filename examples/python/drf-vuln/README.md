# Intentionally Vulnerable Example: DRF API
> **WARNING:** This project exists only to test and demonstrate TorusGuard guidance. Do not deploy it, expose it to the internet, reuse its security patterns, or add real credentials. All secrets, users, payment values, and tokens are fake and nonfunctional.

---

## 🎯 Educational Purpose
Demonstrates common DRF API vulnerability patterns:
1. **`TG-AUTH-007`**: `InvoiceViewSet` queries `Invoice.objects.all()` without scoping to `request.user` (IDOR).
2. **`TG-AUTH-006`**: `UserSerializer` exposes writable `is_staff` and `role` fields (Mass Assignment).
3. **`TG-RATE-001`**: Sensitive password-reset view missing rate throttling.
4. **`TG-RATE-002`**: Unbounded pagination query param `?page_size=1000000` without a ceiling.

See [fixes.md](fixes.md) and [../drf-hardened/](../drf-hardened/) for the hardened counterpart.
