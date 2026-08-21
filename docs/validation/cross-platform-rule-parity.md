# Cross-Platform Security Rule Parity (TorusGuard v0.4.0)

> **Purpose:** Demonstrates that TorusGuard's universal rule catalog operates consistently across distinct language ecosystems (Node.js/JavaScript and Python), adapting detection and remediation to framework-native mechanisms without mutating rule intent.

---

## 🗺️ Cross-Platform Parity Matrix

| Universal Rule ID | Rule Concept | Node.js / Express Implementation | Django | Django REST Framework (DRF) | FastAPI | Flask | Cross-Platform Parity Result |
|---|---|---|---|---|---|---|---|
| **`TG-CSRF-001`** | Missing CSRF Protection | `csurf` middleware active on session routes | `CsrfViewMiddleware` + `{% csrf_token %}` | Session auth viewsets with cookie sessions | Cookie-authenticated browser endpoints | `Flask-WTF` `CSRFProtect(app)` | **Universal:** Core concept identical; detection targets framework middleware. |
| **`TG-AUTH-006`** | Mass Assignment | `req.body` unpacked into Mongoose/Sequelize model | `ModelForm` `fields = '__all__'` | Serializer missing `read_only_fields` on roles | Direct `dict` parameter or `User(**req.dict())` | Raw `request.json` assigned directly to ORM model | **Universal:** Object parameter injection mitigated by explicit field allowlists. |
| **`TG-AUTH-007`** | Missing Object Authorization (IDOR) | Numeric ID lookup without `user_id` query filter | Model lookup missing `owner=request.user` | ViewSet `get_queryset()` returns `Model.objects.all()` | Database lookup missing `current_user.id` filter | Query missing `user_id == session['user_id']` | **Universal:** Multi-tenant query scoping enforced at data-access boundary. |
| **`TG-SSRF-001`** | Server-Side Request Forgery | `axios.get(req.query.url)` without IP validation | Unvalidated `requests.get()` in view | Unvalidated outbound webhook/fetch utility | Unvalidated `httpx.get()` or `requests.get()` | Unvalidated `requests.get()` in route | **Universal:** Outbound HTTP client call bounded by DNS check & private IP blocklist. |
| **`TG-SUPPLY-002`** | Dependency Vulnerability Review | `package-lock.json` + `npm audit` | `requirements.txt` + `pip-audit` | `requirements.txt` + `pip-audit` | `pyproject.toml` + `pip-audit` | `requirements.txt` + `pip-audit` | **Ecosystem-Specific:** Tooling differs (`npm audit` vs `pip-audit`), rule intent is identical. |
| **`TG-CACHE-001`** | Sensitive Cache Exposure | `helmet.noCache()` or `Cache-Control: no-store` | `@never_cache` decorator | `Cache-Control: no-store, private` header | `Response.headers['Cache-Control'] = 'no-store'` | `@after_request` header injection | **Universal:** HTTP cache directives prevent intermediate proxy caching of PII. |

---

## 🎯 What This Parity Analysis Proves

1. **Universal Security Concepts:** Attack vectors (IDOR, Mass Assignment, CSRF, SSRF, Cache Leakage) are architectural and universal across programming languages.
2. **Framework-Native Remediation:** TorusGuard adapts fixes to the idiomatic defense mechanisms of each framework (e.g. Django `ModelForm` fields vs FastAPI Pydantic models).
3. **Consistent Confidence Scoring:** Rules apply the same evidence-confidence standards (`Confirmed`, `Likely`, `Manual Review`, `Informational`) regardless of runtime stack.

---

## ⚠️ What This Does NOT Prove

- Does not prove that every Python application is automatically 100% covered by static rules.
- Does not guarantee that third-party extensions (e.g. custom Django middleware) adhere to standard framework defaults without manual review.
- Does not replace active dynamic security testing or developer threat modeling.
