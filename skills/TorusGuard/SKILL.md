---
name: torusguard
description: Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, Django, DRF, FastAPI, Flask, SQLAlchemy, and Python APIs.
---

# TorusGuard (v0.4.1)

**Tagline:** Security guardrails for AI-built web apps.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard is a Markdown-first, portable AI-agent skill. It is not an npm package, hosted service, browser extension, or automated vulnerability scanner. It guides audit and remediation through structured rules, templates, and human-friendly references.

TorusGuard must never claim it can block DevTools, make an application fully secure, or replace professional penetration testing, code review, compliance work, or threat modeling.

## When to Activate

Use when the user builds or deploys web apps, adds APIs, connects databases, implements auth, reviews security, audits repositories, fixes vulnerabilities, or asks about rate limits, secrets, source maps, SSRF, webhooks, or CORS.

## Commands

| Command | Purpose | Changes code? |
|---------|---------|:---:|
| `/torusguard init` | Create/update project `SECURITY.md` and readable threat model | Docs only |
| `/torusguard audit` | Scan codebase; produce a clean, human-readable audit report | No |
| `/torusguard harden` | Fix approved findings; re-verify | Yes |
| `/torusguard check <area>` | Audit one rule group | No by default |
| `/torusguard verify` | Production pre-flight checklist | No |

**Check areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`, `ssrf`, `business-logic`, `csrf`, `webhook`, `graphql`, `websocket`, `supply-chain`, `cache`, `python`, `django`, `drf`, `fastapi`, `flask`, `sqlalchemy`.

---

## 🔍 Stack Detection & Reference Loading

When executing `/torusguard audit`, inspect the repository files and declare the detected stack:

### Standard Detected Stack Output Format
```markdown
## Detected Stack
- Language: Python / JavaScript / TypeScript
- Framework: Django / DRF / FastAPI / Flask / Next.js / Express / None
- Data layer: SQLAlchemy / Django ORM / Supabase / None
- Dependency files: pyproject.toml / requirements.txt / package.json
- Detection evidence: <file and line reference, e.g. manage.py:5>
- Detection confidence: Confirmed / Likely / Manual Review
```

### Detection Evidence Mapping
| Detected File / Indicator | Target Stack | Reference Modules to Load |
|---|---|---|
| `package.json`, `next.config.js` | Next.js | `secrets-and-config.md`, `client-code-exposure.md`, `platform-hardening.md` |
| `express`, `server.js`, `app.js` | Node.js / Express | `input-and-injection.md`, `auth-and-sessions.md`, `csrf-and-cross-origin.md` |
| `manage.py`, `settings.py`, `django` | Django | `python-security-overview.md`, `django-security.md`, `python-dependencies.md` |
| `rest_framework` | DRF | `drf-security.md`, `django-security.md`, `python-security-overview.md` |
| `fastapi`, `FastAPI()` (in code) | FastAPI | `fastapi-security.md`, `sqlalchemy-security.md`, `python-dependencies.md` |
| `flask`, `Flask(__name__)` | Flask | `flask-security.md`, `sqlalchemy-security.md`, `python-dependencies.md` |
| `sqlalchemy` (in imports/models) | SQLAlchemy | `sqlalchemy-security.md` |
| `requirements.txt`, `pyproject.toml` | Python Supply Chain | `python-dependencies.md` |

---

## 🌟 Human-First Output Standard (Critical)

**All files and messages generated for the developer must be human-first and easy to read.**
Avoid dense, unreadable multi-column tables. Every generated report must prioritize clear visual hierarchy:

1. **Stack Statement at Top:** Use the standard `## Detected Stack` block with specific file and line evidence.
2. **Executive Summary:** Traffic-light posture indicator (`🔴 Action Required` / `🟡 Warnings` / `🟢 Ready`), finding count summary table, and a 2-3 sentence plain-English status overview.
3. **Card-Style Finding Layout:** Present each finding as a clean section with:
   - Clear Title & Severity Emoji (`🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`)
   - Exact Location (`file:line`) and Rule ID (`TG-...`)
   - **The Risk in Plain English:** Explain what an attacker could do without confusing jargon.
   - **Evidence & Fix Snippet:** Show the exact offending code and the safe **Before / After** fix.
4. **Clear Next Steps:** Simple, prioritized 1-2-3 remediation steps so the user knows what to do next.

---

## Evidence Confidence Levels
- **Confirmed**: Directly observed in source code or configuration.
- **Likely**: Strong indicators present; runtime/deployment verification recommended.
- **Manual review**: Requires developer business context (e.g. service-layer authorization, cloud IAM).
- **Informational**: Hardening recommendation or best practice.

## Rules of Engagement Constraints
- Never report an outdated dependency as exploitable without an advisory or audit result.
- Never report cache vulnerability solely because a middleware call is commented out; inspect actual response headers.
- Never call SSRF confirmed merely because a project uses an HTTP client; verify user control over the destination URL.
- Never call IDOR confirmed if a view delegates lookup to a service layer; classify as Manual Review.
- Never call business-logic abuse confirmed without identifying a concrete workflow and abuse path.
- Never claim that a static Markdown skill executed a real scan unless an actual scanner was used.
- Never include sensitive values from the target repository in an audit report.
