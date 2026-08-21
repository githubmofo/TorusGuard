# TorusGuard Python Security Guides (v0.4.0)

This directory contains framework-specific security guides for Python applications.

---

## 📚 Available Guides

* **[Django Security Guide](django.md):** Production settings, CSRF middleware, ORM queries, ModelForms, object-level authorization, and file uploads.
* **[Django REST Framework (DRF) Guide](django-rest-framework.md):** Default permissions, object-level authorization, serializer field whitelists, rate throttling, and pagination caps.
* **[FastAPI Security Guide](fastapi.md):** Pydantic v2 schemas, dependency authentication, object ownership scoping, SSRF mitigation, and HMAC webhook verification.
* **[Flask Security Guide](flask.md):** Application factory configuration, session cookie flags, Flask-WTF CSRF protection, and Werkzeug upload handling.
* **[SQLAlchemy Security Guide](sqlalchemy.md):** Parameterized queries, `text()` bindings, multi-tenant query scoping, and bulk update protection.
* **[Python Dependency & CI/CD Guide](python-dependencies.md):** Deterministic lockfiles, `pip-audit`, and pinned GitHub Actions.
