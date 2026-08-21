# TorusGuard v0.4.0 Validation Report: Django REST Framework (DRF)

> **Target:** DRF Reference Fixture (`examples/python/drf-vuln/`)  
> **Framework:** Django REST Framework 3.14+  
> **Test Mode:** Local Simulated `/torusguard audit` & `/torusguard harden`  
> **Status:** Validation Completed Successfully  

---

## 🎯 1. Test Scope & Purpose
Validate that TorusGuard rules accurately evaluate DRF ViewSets, ModelSerializers, Throttling policies, and Pagination caps.

---

## 🔍 2. Verified Findings

### 🔴 1. Object Ownership & Tenant Scoping IDOR (`TG-AUTH-007`)
* **Classification:** `Confirmed`
* **Evidence:** `views.py` sets `queryset = Invoice.objects.all()` without filtering by `request.user`.
* **Impact:** Any authenticated user can read or modify invoices belonging to other tenants.
* **Remediation:** Override `get_queryset()` to scope objects to `request.user`.

### 🟠 2. Serializer Field Mass Assignment (`TG-AUTH-006`)
* **Classification:** `Confirmed`
* **Evidence:** `serializers.py` includes `role` and `is_staff` in writable serializer fields.
* **Impact:** Callers can escalate privileges via PATCH/PUT requests.
* **Remediation:** Declare `read_only_fields = ['role', 'is_staff']`.

### 🟠 3. Missing Throttle on Sensitive Endpoint (`TG-RATE-001`)
* **Classification:** `Likely` (depends on upstream reverse proxy configuration)
* **Evidence:** Password reset API lacks `ScopedRateThrottle` configuration.
* **Impact:** Susceptible to automated credential stuffing or OTP brute forcing.
* **Remediation:** Apply `throttle_classes = [ScopedRateThrottle]`.

### 🟡 4. Unbounded Pagination Size (`TG-RATE-002`)
* **Classification:** `Confirmed`
* **Evidence:** Pagination class enables `page_size_query_param` without configuring `max_page_size`.
* **Impact:** Callers can request excessively large datasets in a single query causing memory exhaustion.
* **Remediation:** Enforce `max_page_size = 100`.

---

## ⚖️ 3. Validation Limitations
- Throttling alone does not prevent distributed brute-force attacks; rate limiting is one layer in defense-in-depth.
