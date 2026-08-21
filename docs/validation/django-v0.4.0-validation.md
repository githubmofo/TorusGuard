# TorusGuard v0.4.0 Validation Report: Django

> **Target:** Django Reference Fixture (`examples/python/django-vuln/`)  
> **Framework:** Django 4.2 LTS / SQLite  
> **Test Mode:** Local Simulated `/torusguard audit` & `/torusguard harden`  
> **Status:** Validation Completed Successfully  

---

## 🎯 1. Test Scope & Purpose
Validate that TorusGuard rules accurately detect Django-specific security configurations, ORM lookups, ModelForms, and secret exposures without false positives on standard framework mechanisms.

---

## 🔍 2. Verified Findings

### 🔴 1. Hardcoded Secret Key (`TG-SEC-001`)
* **Classification:** `Confirmed`
* **Evidence:** `config/settings.py` contains `SECRET_KEY = "django-insecure-test-key-12345"`.
* **Impact:** Compromises session signature integrity and password reset token security.
* **Remediation:** Replace with `os.environ.get("DJANGO_SECRET_KEY")`.
* **Verified in:** [`examples/python/django-hardened/config/settings.py`](../../examples/python/django-hardened/README.md)

### 🔴 2. Missing Object Ownership Check / IDOR (`TG-AUTH-007`)
* **Classification:** `Confirmed`
* **Evidence:** `accounts/views.py` queries `Document.objects.get(id=doc_id)` without checking `owner=request.user`.
* **Impact:** Any authenticated user can read or modify documents belonging to other users by incrementing numeric IDs.
* **Remediation:** Filter queryset by `owner=request.user` or use a permission mixin.

### 🟠 3. Mass Assignment via ModelForm (`TG-AUTH-006`)
* **Classification:** `Confirmed`
* **Evidence:** `accounts/forms.py` sets `fields = '__all__'`.
* **Impact:** Client requests can inject administrative fields (e.g. `is_staff`, `is_superuser`).
* **Remediation:** Enforce explicit field whitelist (`fields = ['first_name', 'last_name', 'email']`).

### 🟡 4. Sensitive Profile View Caching (`TG-CACHE-001`)
* **Classification:** `Confirmed`
* **Evidence:** Authenticated profile route returns sensitive personal data without `@never_cache`.
* **Impact:** Upstream intermediate caching proxies could serve cached user data to unauthorized parties.
* **Remediation:** Apply `@never_cache` decorator.

---

## ⚖️ 3. Validation Limitations
- Validated against local test fixtures; does not replace manual architecture reviews or deployment checklist execution (`python manage.py check --deploy`).
