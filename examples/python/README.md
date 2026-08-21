# TorusGuard Python Reference Applications (v0.4.0)

> **⚠️ WARNING:** The vulnerable example projects in this directory exist solely for educational testing and demonstration of TorusGuard security rules. They must never be deployed to production or exposed to public networks. All secrets and data are fake.

---

## 📁 Paired Reference Fixtures

| Framework | Vulnerable Example | Hardened Example | Key Rules Demonstrated |
|---|---|---|---|
| **Django** | [`django-vuln/`](django-vuln/) | [`django-hardened/`](django-hardened/) | `TG-SEC-001`, `TG-PLATFORM-003`, `TG-AUTH-007`, `TG-AUTH-006`, `TG-CACHE-001` |
| **DRF** | [`drf-vuln/`](drf-vuln/) | [`drf-hardened/`](drf-hardened/) | `TG-AUTH-007`, `TG-AUTH-006`, `TG-RATE-001`, `TG-RATE-002` |
| **FastAPI** | [`fastapi-vuln/`](fastapi-vuln/) | [`fastapi-hardened/`](fastapi-hardened/) | `TG-SSRF-001`, `TG-WEBHOOK-001`, `TG-AUTH-006` |
| **Flask** | [`flask-vuln/`](flask-vuln/) | [`flask-hardened/`](flask-hardened/) | `TG-SEC-001`, `TG-AUTH-007`, `TG-INPUT-004`, `TG-CSRF-001` |
| **SQLAlchemy** | [`sqlalchemy-vuln/`](sqlalchemy-vuln/) | [`sqlalchemy-hardened/`](sqlalchemy-hardened/) | `TG-INPUT-003`, `TG-AUTH-007`, `TG-AUTH-006` |
