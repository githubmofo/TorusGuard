# TorusGuard Project Roadmap

This document outlines the development milestones, past releases, and future priorities for TorusGuard.

> **Note on Open Source Roadmap:** Roadmap items represent current architectural priorities and community goals, not contractual commitments or fixed delivery deadlines. Priorities evolve based on community feedback, vulnerability research, and contributor support.

---

## 🏁 Completed Milestones

### ✅ v0.1.0 — Foundation & Core Skill (2026-08-18)
- Initial portable Markdown skill definition (`skills/torusguard/SKILL.md`).
- Core reference modules across secrets, frontend database access, input validation, and auth.
- Basic `/torusguard` command dispatch.

### ✅ v0.2.0 — Structured Audit Framework (2026-08-18)
- Established stable TorusGuard Rule IDs (`TG-SEC-*`, `TG-DB-*`, `TG-INPUT-*`, `TG-AUTH-*`, `TG-RATE-*`, `TG-CLIENT-*`, `TG-PLATFORM-*`).
- 25 documented rule files with unsafe/safe examples and remediation guidance.
- Standardized templates (`SECURITY.md`, threat models, audit reports, pre-flight checklists).
- Vulnerable and hardened React + Express reference applications.
- Framework implementation guides for React/Vite, Next.js, Express, Supabase, and Firebase.

### ✅ v0.3.0 — Advanced Web & API Security (2026-08-19)
- Expanded catalog to 60+ rules covering modern attack surfaces:
  - SSRF & outbound network boundaries (`TG-SSRF-*`)
  - Business-logic & flow abuse (`TG-BIZ-*`)
  - Mass assignment & property-level authorization (`TG-AUTH-006`, `TG-AUTH-007`)
  - Webhook signature, replay, and idempotency validation (`TG-WEBHOOK-*`)
  - GraphQL depth/complexity and resolver authorization (`TG-GQL-*`)
  - WebSocket handshake auth, message validation, and rate limits (`TG-WS-*`)
  - Supply-chain dependencies and CI/CD secret exposure (`TG-SUPPLY-*`)
  - Sensitive response cache controls (`TG-CACHE-*`)
- Formal validation suite on OWASP NodeGoat and FastAPI.
- Human-First output formatting standard for audit reports.

---

## 🎯 Next Milestone: v0.4.0 — Python Platform Expansion

**Primary Focus:** Expanding first-class guide and rule coverage for Python web ecosystems.

- [ ] **FastAPI & Pydantic Security Guide:** Native Request body validation, OAuth2 password/bearer workflows, and CORS.
- [ ] **Django Security Guide:** Django ORM SQLi prevention, CSRF middleware configuration, secure cookie settings, and session store hardening.
- [ ] **Python ORM / ODM Rule Mapping:** Safe query construction patterns for SQLAlchemy, Django ORM, and Tortoise.
- [ ] **Serverless & Edge Function Guardrails (`TG-EDGE-*`):** Request-scoped state isolation for Vercel Edge and AWS Lambda.

---

## 🔭 Future Horizons: v1.0.0 & Beyond

- **Broader Ecosystem Guides:** Go (Fiber / Gin), Ruby on Rails, and Spring Boot security guides.
- **Next.js App Router & Server Actions Deep-Dive:** Guardrails for React Server Actions, Server Components, and data cache revalidation leaks.
- **Automated Catalog Linter:** GitHub Actions CI workflow to validate Markdown structure, rule IDs, and link integrity.
- **Comprehensive Fixture Library:** Expanded educational test applications covering diverse languages and architectures.

---

## 💡 Proposing a Roadmap Item
Have an idea for a new feature, platform guide, or security domain? Open a [Feature Request](https://github.com/githubmofo/TorusGuard/issues/new?template=feature_request.md) or start a discussion in our repository!
