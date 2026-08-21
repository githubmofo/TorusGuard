# Real-World Validation Record: Django + DRF Application

- **Repository:** Anonymized Django/DRF Multi-Tenant SaaS Platform
- **Authorization:** Maintainer-permitted local code review evaluation
- **Repository Version / Commit SHA:** `4f9b8c2e10a7b3d95e0c1f6a8e4b7c2d1a3e5f79`
- **Stack Detected:** Python 3.11, Django 4.2 LTS, Django REST Framework 3.14, PostgreSQL (psycopg2-binary), `pyproject.toml` (Poetry)
- **TorusGuard Version:** v0.4.0
- **Date Tested:** 2026-08-21

---

## 🔍 Findings

| Rule ID | Classification | Evidence | Maintainer Outcome |
|---|---|---|---|
| `TG-AUTH-007` | **Manual Review** | Organization billing ViewSet relies on a service-layer query rather than direct `get_queryset()` user filter | **Disputed as Non-Issue:** Verified that organization ownership check is enforced in the underlying `BillingService.get_account()` layer. |
| `TG-AUTH-006` | **Confirmed** | `UserProfileSerializer` declared `fields = '__all__'` without adding `is_billing_admin` to `read_only_fields` | **Confirmed & Remediated:** Maintainer updated serializer with explicit `read_only_fields = ['is_billing_admin', 'tier']`. |
| `TG-RATE-001` | **Likely** | Password reset endpoint (`/api/v1/auth/password-reset/`) lacked DRF `throttle_classes` | **Confirmed & Remediated:** Added `ScopedRateThrottle` with rate `'5/minute'`. |
| `TG-SUPPLY-001` | **Informational** | `poetry.lock` present and tracked in git | **Verified:** Deterministic dependency lockfile confirmed. |

---

## 📊 Results Summary

- **Confirmed Findings:** 1 (Serializer mass assignment on privilege flag)
- **Likely Findings:** 1 (Missing endpoint throttle)
- **Manual Review Findings:** 1 (Service-layer ownership scoping)
- **False Positives:** 0
- **Missed Issues Reported by Maintainer:** 0
- **Rule Wording Improvements:** Clarified in `TG-AUTH-007` that ownership can be satisfied either via ORM query filtering or inside service-layer domain logic.
- **Documentation Improvements:** Added DRF service-layer pattern to [guides/python/django-rest-framework.md](../../guides/python/django-rest-framework.md).
