# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-08-21

### Added
- Added comprehensive Python security guides for **Django**, **Django REST Framework (DRF)**, **FastAPI**, **Flask**, and **SQLAlchemy**.
- Added Python dependency management and CI/CD supply-chain guidance (`pip-audit`, lockfile integrity, GitHub Actions hardening).
- Added automatic Python stack detection and reference module loading in `skills/torusguard/SKILL.md`.
- Added paired intentionally vulnerable and hardened Python reference applications (`examples/python/`) for Django, DRF, FastAPI, Flask, and SQLAlchemy with `fixes.md` remediation matrices.
- Added formal validation reports for Django, DRF, FastAPI, and Flask (`docs/validation/`).
- Added cross-platform rule parity documentation (`docs/validation/cross-platform-rule-parity.md`) demonstrating universal rule application across Node.js and Python.
- Added Python security rule mapping matrix (`docs/python-rule-mapping.md`).

### Changed
- Expanded `/torusguard audit` with framework-native Python remediation patterns.
- Preserved existing universal TorusGuard rule IDs (`TG-SEC-*`, `TG-AUTH-*`, `TG-INPUT-*`, `TG-SSRF-*`, `TG-CSRF-*`, `TG-RATE-*`, `TG-SUPPLY-*`, `TG-CACHE-*`).

### Security
- Enforced framework-native defenses (e.g. Django `CsrfViewMiddleware`, DRF `permission_classes`, FastAPI Pydantic v2 schemas).
- Clarified that TorusGuard remains a guidance framework for AI coding agents, not an automated binary scanner or penetration-testing replacement.

## [0.3.0] - 2026-08-19

### Added
- Added SSRF and outbound-request security rules under `rules/`.
- Added business-logic abuse and sensitive-flow review.
- Added mass-assignment and property-level authorization rules.
- Added CSRF and credentialed cross-origin request guidance.
- Added webhook signature, replay, and idempotency rules.
- Added GraphQL security guidance for depth, complexity, batching, and resolver authorization.
- Added WebSocket authentication, channel authorization, and message validation rules.
- Added dependency and CI/CD supply-chain guidance.
- Added cache and sensitive-response protection rules.
- Added advanced API examples and review templates.

### Changed
- Expanded `/torusguard audit` to detect API styles and advanced resource-consumption risks.
- Expanded `/torusguard verify` with advanced API and integration checks.
- Preserved all v0.2 rule IDs for compatibility.

## [0.2.0] - 2026-08-18

### Added
- Stable TorusGuard rule IDs across secrets, database exposure, input handling, authentication, abuse prevention, client exposure, and platform hardening.
- 25 documented security rules under `rules/`.
- Standardized audit report, security context, threat model, deployment pre-flight, endpoint review, and security exception templates.
- Vulnerable and hardened React + Express reference examples.
- Security implementation guides for React/Vite, Next.js, Express, Supabase, and Firebase.

## [0.1.0] - 2026-08-18

### Added
- Initial rules and references.
