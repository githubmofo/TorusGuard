# TorusGuard Python Security Rule Mapping (v0.5.3)

> **Purpose:** Demonstrates how universal TorusGuard security rule IDs map across Python web frameworks (Django, Django REST Framework, FastAPI, Flask, and SQLAlchemy) without inventing redundant language-specific rule IDs.

---

## 🗺️ Framework Implementation Matrix

| Security Area | TorusGuard Rule IDs | Django | Django REST Framework (DRF) | FastAPI | Flask | SQLAlchemy |
|---|---|---|---|---|---|---|
| **Input Validation** | `TG-INPUT-001`, `TG-INPUT-002`, `TG-INPUT-005`, `TG-INPUT-006` | `forms.Form`, `ModelForm`, custom `clean_<field>()`, `format_html()` | Serializer fields, custom field validators | Pydantic v2 `BaseModel`, `Field(..., min_length=1)` | WTForms, Marshmallow, `render_template(..., context)` | Explicit schema boundary before DB persistence |
| **Authentication** | `TG-AUTH-001`, `TG-AUTH-002`, `TG-AUTH-004`, `TG-AUTH-008` | `django.contrib.auth`, session middleware, `@login_required` | `authentication_classes = [JWTAuthentication, SessionAuthentication]` | `Depends(get_current_user)`, OAuth2 password/bearer | `flask_login`, `@login_required`, session cookies | N/A (Data layer only) |
| **Authorization & Ownership** | `TG-AUTH-003`, `TG-AUTH-007`, `TG-AUTH-008` | `UserPassesTestMixin`, `@user_passes_test`, queryset `.filter(user=request.user)` | `permission_classes`, custom `BasePermission`, `has_object_permission` | `SecurityScopes`, dependency checks, scoped database queries | Route decorators, session-based ownership validation | Model query scoping (`filter_by(user_id=current_user.id)`) |
| **CSRF Protection** | `TG-CSRF-001`, `TG-CSRF-002` | `CsrfViewMiddleware`, `{% csrf_token %}`, `CSRF_COOKIE_SECURE` | Relevant for session-authenticated API views with cookie auth | Relevant for cookie-authenticated browser API endpoints | `flask_wtf.CSRFProtect`, `SameSite=Strict` cookies | N/A |
| **Mass Assignment** | `TG-AUTH-006` | Explicit `fields = [...]` in `ModelForm` (never `fields = '__all__'`) | Serializer `read_only_fields`, explicit writable fields | Explicit request schemas (never unpack `User(**req.dict())`) | Schema allowlists (never unpack raw `request.json` to model) | Explicit column assignments or `.pick()` updates |
| **Rate Limiting & DoS** | `TG-RATE-001`, `TG-RATE-002`, `TG-RATE-003` | `django-ratelimit`, reverse-proxy (Nginx/Cloudflare) | `AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle` | `slowapi` (`Limiter`), Redis token-bucket middleware | `Flask-Limiter`, Redis-backed rate limiting | Connection pooling limits (`pool_size`, `max_overflow`) |
| **ORM & Database Safety** | `TG-DB-001`, `TG-DB-004`, `TG-INPUT-003` | Parameterized ORM queries, scoped querysets (`filter(tenant=...)`) | Queryset scoping and parameterized ORM lookups | SQLAlchemy parameterized `text(:param)` bindings | Parameterized queries via Flask-SQLAlchemy | Bound parameters, avoid `text(f"SELECT ... {input}")`, enforce tenant filter |
| **File Upload Safety** | `TG-INPUT-004`, `TG-INPUT-006` | `FileField(upload_to=...)`, file extension/MIME/size validation | `MultiPartParser`, serializer file validation | `UploadFile`, byte size streaming caps, UUID storage | `secure_filename(file.filename)`, size caps, MIME sniff | Store in isolated object storage (S3), never execute |
| **SSRF & Outbound Requests** | `TG-SSRF-001`, `TG-SSRF-002`, `TG-SSRF-004` | Validate external URLs before `requests.get()` or `urllib` | Validate external webhook / callback URLs | Validate destination with `httpx` or `requests`, block private IPs | Validate user URLs before `requests.get()`, block `127.0.0.1`/`169.254` | N/A |
| **Dependency & Supply Chain** | `TG-SUPPLY-001` … `TG-SUPPLY-005` | `requirements.txt`, `pip-audit`, lockfiles (`poetry.lock`, `uv.lock`) | `requirements.txt`, `pip-audit`, lockfiles | `pyproject.toml`, `pip-audit`, pinned dependencies | `requirements.txt`, `pip-audit`, lockfiles | Pin driver versions (e.g. `asyncpg`, `psycopg2-binary`) |
| **Cache & Sensitive Responses** | `TG-CACHE-001`, `TG-CACHE-002` | `@never_cache`, `Cache-Control: no-store` on user profile views | `Cache-Control: no-store, private` on sensitive endpoints | Response headers `Cache-Control: no-store` on private routes | `@after_request` header injection (`no-store`) | Avoid caching sensitive query results across users |

---

## 🎯 Universal Rule ID Breakdown

| Universal Rule ID | Rule Title | Python Application & Verification Approach | Default Severity | Evidence Confidence |
|---|---|---|:---:|:---:|
| `TG-SEC-001` | Hardcoded Secrets | Inspect `settings.py`, `.env`, and config files for hardcoded API keys/passwords. | 🔴 Critical | Confirmed |
| `TG-SEC-002` | Public Environment Secrets | Verify frontend configs don't expose backend Python secrets. | 🔴 Critical | Confirmed |
| `TG-INPUT-001` | Server-Side Input Validation | Check that Pydantic models, ModelForms, or Serializers enforce field types/lengths. | 🟠 High | Confirmed |
| `TG-INPUT-003` | SQL Injection Prevention | Inspect raw SQL calls (`.raw()`, `text()`, `connection.cursor()`) for f-strings or `.format()`. | 🔴 Critical | Confirmed |
| `TG-INPUT-005` | Unsafe Template Rendering & Escaping | Detect `mark_safe` on user inputs, `| safe` filter in Jinja2, or `render_template_string()`. | 🟠 High | Confirmed |
| `TG-INPUT-006` | Path Traversal & Unsafe Upload Storage | Inspect file uploads using raw `file.filename` in `os.path.join` without sanitization. | 🔴 Critical | Confirmed |
| `TG-AUTH-001` | Missing Authentication | Check route decorators (`@login_required`, `Depends(get_current_user)`, `permission_classes`). | 🔴 Critical | Confirmed |
| `TG-AUTH-003` | Missing Server-Side Authorization | Verify that tenant/user role checks occur on the server, not solely in frontend tokens. | 🔴 Critical | Confirmed |
| `TG-AUTH-006` | Mass Assignment | Check that models are not populated with unfiltered `req.body`, `request.json`, or `**dict`. | 🟠 High | Confirmed |
| `TG-AUTH-007` | Missing Property-Level Authorization (IDOR) | Verify that object lookups by ID enforce ownership (`user=request.user` or tenant ID filter). | 🔴 Critical | Confirmed |
| `TG-AUTH-008` | Untrusted Role/Tenant Header Injection | Verify roles and tenant IDs are derived from authenticated tokens, not raw headers. | 🔴 Critical | Confirmed |
| `TG-DB-004` | Missing Tenant Query Isolation | Enforce tenant scoping (`tenant_id == user.tenant_id`) across multi-tenant database queries. | 🔴 Critical | Confirmed |
| `TG-CSRF-001` | Missing CSRF Protection | Check that CSRF middleware is active for cookie/session-based state-changing endpoints. | 🟠 High | Confirmed |
| `TG-SSRF-001` | User-Controlled Server-Side URL Fetch | Inspect `requests.get()`, `httpx.get()`, `urllib.request` using user-supplied URLs. | 🔴 Critical | Confirmed |
| `TG-SSRF-002` | Missing Internal Network Protection | Check that outbound requests validate DNS and block private IP ranges (`10.0.0.0/8`, `169.254.0.0/16`). | 🟠 High | Likely |
| `TG-RATE-001` | Missing Rate Limiting on Sensitive Endpoints | Verify login, OTP, and expensive endpoints have throttling classes or middleware enabled. | 🟠 High | Likely / Manual |
| `TG-SUPPLY-001` | Missing or Ignored Lockfile | Ensure lockfiles (`poetry.lock`, `Pipfile.lock`, `requirements.lock`) are tracked in git. | 🟡 Medium | Confirmed |
| `TG-SUPPLY-002` | Vulnerable Dependency Review Missing | Ensure dependencies are scanned via `pip-audit` or automated security advisories. | 🟠 High | Confirmed |
| `TG-CACHE-001` | Sensitive Response Publicly Cacheable | Verify authenticated profile/billing endpoints send `Cache-Control: no-store, private`. | 🟡 Medium | Confirmed / Likely |
| `TG-EDGE-003` | AWS Lambda Ephemeral & Cold-Start Security | Isolate STS credentials, clean `/tmp` storage in `finally:`, enforce boto3 socket timeouts. | 🟠 High | Confirmed |
| `TG-AGENT-001` | System Prompt Injection Boundaries | Ensure user input to Python LLM agents is passed in `user` role or strictly delimited. | 🔴 Critical | Confirmed |
| `TG-AGENT-002` | Unsandboxed Shell Tool Dispatch | Enforce container sandboxing, command allowlists, and timeout limits on agent tool calls. | 🔴 Critical | Confirmed |
| `TG-AGENT-003` | Broad MCP & Database Scoping | Restrict MCP server filesystem mounts and database connection strings to least-privilege. | 🔴 Critical | Confirmed |
| `TG-AGENT-004` | Cross-Session Vector Memory Isolation | Enforce tenant/session ID metadata filtering on vector database queries (pgvector, Chroma). | 🔴 Critical | Confirmed |

---

## 🔗 Platform Guides Reference Index
- [Django Security Guide](../guides/python/django.md)
- [Django REST Framework Security Guide](../guides/python/django-rest-framework.md)
- [FastAPI Security Guide](../guides/python/fastapi.md)
- [Flask Security Guide](../guides/python/flask.md)
- [SQLAlchemy Security Guide](../guides/python/sqlalchemy.md)
- [Python Dependency & CI/CD Guide](../guides/python/python-dependencies.md)
