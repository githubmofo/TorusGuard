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
- Cross-Platform Rule Parity analysis (`docs/validation/cross-platform-rule-parity.md`).

### ✅ v0.4.1 — Python Validation & Quality Patch (2026-08-21)
- Refined Python stack detection across Django (`manage.py`), DRF (`pyproject.toml`), FastAPI, Flask (`requirements.txt`), Flask+SQLAlchemy, libraries, and mixed monorepos.
- Added 10 paired safe and vulnerable Python regression fixtures in `tests/fixtures/python/`.
- Established evidence-confidence standards for service-layer authorization and serializer mass-assignment protection.
- Created authorized repository validation template and legal/ethical scoping boundaries.

### ✅ v0.5.0 — Architecture & Workflow Release (2026-08-25)
- **Formal 6-Stage Finding Lifecycle:** `Detect` ──► `Classify` ──► `Verify` ──► `Remediate` ──► `Re-check` ──► `Archive`.
- **Formal JSON Schemas (`schemas/`):** Standardized schemas for findings, evidence, remediations, rule metadata, and lifecycle transitions.
- **Repeatable Automated Validation Harness (`harness/runner.py`):** Standalone harness executing schema validation, rule catalog integrity, educational fixture differentials, and lifecycle state assertions.
- **Core Workflow Package (`core/`):** Normalized data models, lifecycle manager, and Human-First report formatter.
- **Command Addition:** Added `/torusguard recheck` for differential verification of post-fix codebases.

---

## 🎯 Next Incremental Milestones: v0.5.x Series

The v0.5.0 architecture enables rapid, predictable incremental platform expansions:

### 🚀 v0.5.1 — Cloudflare Workers & Serverless Edge Isolation
- [ ] Cloudflare Workers Security Guide: Request context isolation, KV/D1/R2 binding authorization, subrequest bounding.
- [ ] Rule `TG-EDGE-001`: Cloudflare Worker global memory state leak prevention.
- [ ] Paired vulnerable and hardened edge worker fixtures.

### 🚀 v0.5.2 — Next.js App Router Server Actions Security
- [ ] Next.js Server Actions Authorization: Direct action endpoint session/role checks.
- [ ] Rule `TG-EDGE-002`: Ephemeral memory state leak prevention during edge SSR.
- [ ] Revalidation rate limits and cache tag poisoning prevention.

### 🚀 v0.5.3 — AWS Lambda & Ephemeral Runtimes
- [ ] Cold-start credential reuse, IAM execution boundaries, environment secret loading.
- [ ] Rule `TG-EDGE-003`: Ephemeral execution timeout & subrequest bounding.

### 🚀 v0.5.4 — Microservice Mesh & Distributed Authorization
- [ ] JWT propagation, RPC gateway boundary enforcement, internal mTLS requirements.

---

## 🔭 Future Horizons: v1.0.0 — Stable Multi-Platform Standard

- **Broader Ecosystem Guides:** Go (Fiber / Gin), Ruby on Rails, and Spring Boot.
- **Automated Catalog Linter:** GitHub Actions CI workflow to validate Markdown structure, rule IDs, and link integrity.
- **Interactive Playground / Multi-Language Fixture Suite:** Broadened automated test fixtures for local evaluation.

---

## 💡 Proposing a Roadmap Item
Have an idea for a new feature, platform guide, or security domain? Open a [Feature Request](https://github.com/githubmofo/TorusGuard/issues/new?template=feature_request.md) or start a discussion in our repository!
