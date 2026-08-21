# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-08-21

### Fixed
- Refined Python stack detection for supported repository layouts (Django, DRF, FastAPI, Flask, SQLAlchemy, libraries, and mixed monorepos).
- Corrected false-positive conditions for service-layer ownership queries, explicit serializer `read_only_fields`, and bound LIKE parameters in SQLAlchemy.
- Improved evidence requirements for authorization (`TG-AUTH-007`), SSRF (`TG-SSRF-001`), mass assignment (`TG-AUTH-006`), and dependency findings.
- Corrected framework-specific remediation examples across Python platform guides.

### Added
- Added sanitized Python regression fixtures in `tests/fixtures/python/` covering both safe and vulnerable patterns.
- Added authorized repository validation template (`docs/validation/authorized-repo-validation-template.md`) and initial real-world evaluation records.
- Added automated CI workflows for fixture syntax validation, link integrity, and release tag verification.

### Changed
- Clarified when findings must be classified as `Manual Review` instead of `Confirmed` (e.g. domain service-layer authorization delegation).
- Refined detected stack output schema to mandate file and line evidence citations.

### Limitations
- TorusGuard remains a security guidance framework for AI coding agents, not an automated binary scanner or penetration-testing replacement.

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

## [0.2.0] - 2026-08-18

### Added
- 25 documented rules across 7 core areas with severity, detection, remediation, and verification.
- 5 core workflow commands: `init`, `audit`, `harden`, `check`, `verify`.
- Standardized templates for `SECURITY.md`, threat modeling, audit reports, deployment pre-flight, API endpoint reviews, and security exceptions.
- Framework security guides for React/Vite, Next.js, Express, Supabase, and Firebase.
- Paired vulnerable and hardened reference applications.

## [0.1.0] - 2026-08-18

### Added
- Initial portable AI-agent skill for web application security guidance.
