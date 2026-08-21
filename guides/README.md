# TorusGuard Framework Guides

Stack-specific security checklists and implementation patterns for TorusGuard audits and hardening.

---

## 🌐 JavaScript & TypeScript Frameworks

| Guide | Stack | Primary Rules |
|---|---|---|
| [react-vite-security.md](react-vite-security.md) | React + Vite | `TG-SEC-002`, `TG-DB-001`, `TG-CLIENT-001`, `TG-CLIENT-002` |
| [nextjs-security.md](nextjs-security.md) | Next.js App/Pages Router | `TG-SEC-002`, `TG-AUTH-002`, `TG-CLIENT-001` |
| [express-security.md](express-security.md) | Node.js + Express | `TG-INPUT-001`, `TG-PLATFORM-001` … `004`, `TG-RATE-*` |
| [supabase-security.md](supabase-security.md) | Supabase BaaS | `TG-DB-002`, `TG-DB-003`, `TG-AUTH-003` |
| [firebase-security.md](firebase-security.md) | Firebase BaaS | `TG-DB-003`, `TG-AUTH-002`, `TG-AUTH-003` |

---

## 🐍 Python Frameworks (v0.4.0)

| Guide | Stack | Primary Rules |
|---|---|---|
| [python/django.md](python/django.md) | Django Web Framework | `TG-SEC-001`, `TG-PLATFORM-001` … `003`, `TG-CSRF-001`, `TG-AUTH-006`, `TG-AUTH-007` |
| [python/django-rest-framework.md](python/django-rest-framework.md) | Django REST Framework (DRF) | `TG-AUTH-001`, `TG-AUTH-006`, `TG-AUTH-007`, `TG-RATE-001`, `TG-RATE-002` |
| [python/fastapi.md](python/fastapi.md) | FastAPI & Pydantic | `TG-AUTH-001`, `TG-AUTH-006`, `TG-AUTH-007`, `TG-SSRF-001`, `TG-WEBHOOK-001` |
| [python/flask.md](python/flask.md) | Flask & Werkzeug | `TG-SEC-001`, `TG-AUTH-007`, `TG-CSRF-001`, `TG-INPUT-004` |
| [python/sqlalchemy.md](python/sqlalchemy.md) | SQLAlchemy ORM & Core | `TG-INPUT-003`, `TG-AUTH-006`, `TG-AUTH-007` |
| [python/python-dependencies.md](python/python-dependencies.md) | Python Supply Chain & CI/CD | `TG-SUPPLY-001`, `TG-SUPPLY-002`, `TG-SUPPLY-004` |

---

*Use with `/torusguard check <area>` and the matching reference module in `skills/TorusGuard/references/`.*
