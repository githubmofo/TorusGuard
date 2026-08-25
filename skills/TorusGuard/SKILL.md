---
name: torusguard
description: Security guardrails and structured verification workflow for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, Django, DRF, FastAPI, Flask, SQLAlchemy, and Python APIs.
---

# TorusGuard (v0.5.0)

**Tagline:** Security guardrails and structured verification workflow for AI-built web apps.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard is a Markdown-first, portable AI-agent skill and security workflow engine. It is not an npm package, hosted SaaS service, browser extension, or black-box vulnerability scanner. It guides audit, verification, remediation, and re-checking through structured rules, normalized evidence schemas, and human-friendly references.

TorusGuard must never claim it can block DevTools, make an application 100% secure, or replace professional penetration testing, manual code review, compliance audits, or formal threat modeling.

---

## 🔄 Finding Lifecycle (v0.5.0 Architecture)

TorusGuard operates on a 6-stage lifecycle for every candidate security finding:

```text
[ Detect ] ──► [ Classify ] ──► [ Verify ] ──► [ Remediate ] ──► [ Re-check ] ──► [ Archive ]
```

1. **Detect:** Scan repository source code, environment templates, and configuration files.
2. **Classify:** Assign a canonical Rule ID (`TG-*`), taxonomy category, risk severity, and initial confidence.
3. **Verify:** Validate evidence sufficiency and reachable data flow. If evidence is ambiguous, force status to `Needs Review`.
4. **Remediate:** Formulate least-invasive, framework-native code modifications with before/after diffs.
5. **Re-check:** Re-audit modified code to verify that the vulnerability is resolved (`Verified Safe`).
6. **Archive:** Preserve timestamped verification evidence in the project audit record.

---

## 🛠️ Core Commands

| Command | Lifecycle Phase | Purpose | Changes Code? |
|---------|:---:|---------|:---:|
| `/torusguard init` | Baseline | Create/update project `SECURITY.md`, threat model, and finding registry | Docs only |
| `/torusguard audit` | Detect & Classify | Scan codebase; produce a Human-First normalized audit report | No |
| `/torusguard verify` | Verify | Validate evidence sufficiency and check manual review assumptions | No |
| `/torusguard harden` | Remediate | Propose least-invasive, framework-idiomatic code fixes | Yes (on approval) |
| `/torusguard recheck` | Re-check | Execute differential re-audit on post-fix code to assert resolution | No |

**Audit focus areas:** `auth`, `input`, `database`, `files`, `secrets`, `supply-chain`, `network`, `ssrf`, `webhooks`, `websockets`, `graphql`, `business-logic`, `rate-limit`, `client`, `platform`, `cache`, `django`, `drf`, `fastapi`, `flask`, `sqlalchemy`.

---

## 🔍 Stack Detection & Reference Loading

When executing `/torusguard audit`, inspect repository files and output the detected stack block:

### Standard Detected Stack Output Format
```markdown
## Detected Stack
- Language: Python / JavaScript / TypeScript
- Framework: Django / DRF / FastAPI / Flask / Next.js / Express / None
- Data layer: SQLAlchemy / Django ORM / Supabase / None
- Dependency files: pyproject.toml / requirements.txt / package.json
- Detection evidence: <file and line reference, e.g. manage.py:5>
- Detection confidence: Confirmed / Likely / Needs Review
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

## 🌟 Human-First Output Standard

**All files and messages generated for developers must be human-first, structured, and easy to read.**
Every generated report must follow this card-style hierarchy:

1. **Stack Statement at Top:** Standard `## Detected Stack` block with specific file and line citations.
2. **Executive Summary:** Posture indicator (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Ready`), metric table, and a 2-3 sentence overview.
3. **Card-Style Finding Layout:**
   - Title & Badges: Severity (`🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`) | Confidence (`🔒 Confirmed`, `⚠️ Likely`, `🔍 Needs Review`)
   - Exact Location (`file:line` or symbol)
   - **Risk & Rationale:** Plain-English explanation of adversarial abuse.
   - **Evidence Snippet:** Exact code excerpt with type (`source`, `runtime`, `test`, `manual_review`).
   - **Remediation & Diff:** Framework-native **Before / After** diff.
   - **Verification Method:** Step-by-step test instructions.
4. **Clear Next Steps:** Prioritized 1-2-3 actions.

---

## ⚖️ Evidence Confidence & Rules of Engagement

- **Confirmed:** Directly proven in source code or configuration with reachable data flow.
- **Likely:** Strong indicators present; runtime/deployment verification recommended.
- **Needs Review:** Requires developer business context (e.g. service-layer authorization, cloud IAM, upstream proxy).
- **Informational:** Defensive best practice, not an active vulnerability.

### Strict Safety & Evidence Constraints:
- Never report a finding as `Confirmed` without direct source code snippet evidence.
- If a controller delegates authorization to a domain service layer, classify as `Needs Review` (`TG-AUTH-007`).
- Never report an unpinned dependency as exploitable without an advisory or audit result (`TG-SUPPLY-002`).
- Never report SSRF as `Confirmed` merely because an HTTP client is imported; verify user control over the destination URL (`TG-SSRF-001`).
- Never include real production credentials or tokens in generated reports.
