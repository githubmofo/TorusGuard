# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.2] - 2026-08-25

### Added
- **Validation Engine (`harness/engine/`):** 7-layer validation engine supporting fixture management, deterministic replay, differential comparisons, regression tracking, and false-alarm diagnostics.
- **Deterministic Multi-Pass Replay (`ReplayRunner`):** Multi-pass (3x) execution verification with SHA-256 serialized output hash assertions.
- **Differential Result Comparator (`ResultComparator`):** Evaluates vulnerable vs hardened behavior with standardized outcome labels (`Vulnerable Confirmed`, `Hardened Safe`, `False Positive`, `False Negative`, `Needs Review`, `Regression Detected`).
- **Historical Regression Tracker (`RegressionTracker`):** Automated tracking ensuring baseline fixes from earlier releases (v0.4.1+) remain clean.
- **False-Positive & Diagnostic Analyzer (`FalsePositiveAnalyzer`):** Root-cause diagnosis and remediation guidance for rule discrepancies.
- **New Schemas (`schemas/`):** Added `fixture.schema.json` and `validation-run.schema.json`.
- **Validation Harness Suite:** Expanded `harness/runner.py` with 56 automated validation tests (100% pass rate).

## [0.5.1] - 2026-08-25

### Added
- **Structured Provenance Tracking:** Every finding records an explicit provenance chain (discovery module, triggering input, decision path, verification step).
- **Auditable 0–100 Confidence Scoring Model:** Replaced subjective confidence with an objective 5-factor mathematical rubric (evidence quality, reproduction, confirmations, environmental clarity, manual review).
- **Cryptographic Evidence Packaging:** Implemented immutable SHA-256 checksums computed for all raw code evidence snippets.
- **Explicit Retest & Closure State Machine:** Added `RetestRecord` to track post-fix verification, post-fix evidence hashes, and formal closure states (`Verified Fixed`).
- **New Schemas (`schemas/`):** Added `provenance.schema.json`, `confidence.schema.json`, and `retest.schema.json`.
- **Validation Harness Enhancements:** Extended `harness/runner.py` with confidence scoring tests, provenance integrity checks, and retest assertions (42/42 tests passing).

### Changed
- Standardized canonical `Finding` object schema across all rule modules.
- Strict isolation of objective technical **Raw Facts** from **AI Risk Interpretation**.
- Enhanced Human-First audit reports with confidence point breakdowns, provenance decision chains, and cryptographic evidence hashes.

## [0.5.0] - 2026-08-25

### Added
- **Formal 6-Stage Finding Lifecycle:** Implemented state machine transitions across `Detect` ──► `Classify` ──► `Verify` ──► `Remediate` ──► `Re-check` ──► `Archive`.
- **Formal JSON Schemas (`schemas/`):** Defined normalized schemas for findings, evidence, remediations, rule metadata, and lifecycle transitions.
- **Repeatable Automated Validation Harness (`harness/runner.py`):** Standalone test runner executing schema validation, catalog integrity, educational fixture differential checks, regression suites, and lifecycle state assertions.
- **Core Engine & Workflow Package (`core/`):** Pydantic-style normalized models, lifecycle manager with constraint enforcement, and report formatter.
- **Lifecycle & Architecture Documentation:** Added `docs/architecture/v0.5.0-workflow-architecture.md` and `docs/workflow/finding-lifecycle.md`.
- **Command Addition:** Added `/torusguard recheck` command for differential verification of post-fix codebases.

### Changed
- Standardized evidence modality typing (`source`, `runtime`, `test`, `manual_review`).
- Normalized confidence taxonomy (`Confirmed`, `Likely`, `Needs Review`, `Informational`, `Not Applicable`).
- Enhanced Human-First audit reports with card-style layout, traffic-light posture indicators, and side-by-side Before/After remediation diffs.
- Updated `skills/TorusGuard/SKILL.md` to `v0.5.0` integrating the new finding lifecycle.

### Limitations
- TorusGuard is an open-source Markdown-first guidance framework for AI coding agents; findings marked `Needs Review` require manual verification of out-of-band architecture.

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
