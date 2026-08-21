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

### ✅ v0.4.0 — Python Platform Security (2026-08-21)
- Deep, native security guides and reference modules for **Django**, **Django REST Framework (DRF)**, **FastAPI**, **Flask**, and **SQLAlchemy**.
- Python dependency management, deterministic lockfile rules, `pip-audit`, and CI/CD hardening.
- Automatic Python framework detection in `skills/torusguard/SKILL.md`.
- Paired vulnerable and hardened reference applications in `examples/python/` with `fixes.md` remediation matrices.
- Formal validation reports for Django, DRF, FastAPI, and Flask in `docs/validation/`.
- Cross-Platform Rule Parity analysis (`docs/validation/cross-platform-rule-parity.md`) demonstrating universal rule consistency across Node.js and Python.
- Python security rule mapping matrix (`docs/python-rule-mapping.md`).

---

## 🎯 Next Milestone: v0.5.0 — Serverless & Edge Compute Security

**Primary Focus:** Guardrails for modern serverless runtimes and edge compute platforms.

- [ ] **Cloudflare Workers Security Guide:** Request context isolation, KV/D1 binding authorization, and subrequest bounding.
- [ ] **Vercel Edge Functions & Server Actions:** Next.js Server Actions authorization, ephemeral memory state leak prevention, and cache revalidation limits.
- [ ] **AWS Lambda / Serverless Framework:** Cold-start credential reuse, IAM execution boundaries, and environment secret loading.
- [ ] **New Serverless Rules (`TG-EDGE-*`):** Rules for memory-state leakage and ephemeral execution timeouts.

---

## 🔭 Future Horizons: v1.0.0 — Stable Multi-Platform Standard

- **Broader Ecosystem Guides:** Go (Fiber / Gin), Ruby on Rails, and Spring Boot.
- **Automated Catalog Linter:** GitHub Actions CI workflow to validate Markdown structure, rule IDs, and link integrity.
- **Interactive Playground / Multi-Language Fixture Suite:** Broadened automated test fixtures for local evaluation.

---

## 💡 Proposing a Roadmap Item
Have an idea for a new feature, platform guide, or security domain? Open a [Feature Request](https://github.com/githubmofo/TorusGuard/issues/new?template=feature_request.md) or start a discussion in our repository!
