# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.2.0] - 2026-08-31

### Added
- **Modern Stack Profiler (`core/stack_profiler.py`):** Automatic detection of framework version families (Django 5.x, FastAPI 0.100+, SQLAlchemy 2.0, Next.js 14+) and package managers (uv, Poetry, PEP 621).
- **Async-Native Remediation:** Idiomatic before/after patches for async view coroutines (`await aget()`) and async database queries (`AsyncSession`).
- **FastAPI & Pydantic v2 Compatibility:** `Annotated[User, Depends()]` dependency injections and `pydantic-settings` environment configuration.
- **SQLAlchemy 2.0 select() Scoping:** Modern 2.0 select statement query scoping for multi-tenant isolation.
- **Frontend Server Action Security:** Detection and remediation of unauthenticated Next.js 14 Server Actions (`"use server"`).
- **Container & Supply Chain Security:** Hardening of Dockerfiles (secrets, non-root user) and GitHub Actions (`permissions: read-all`, SHA pinning).
- **Modern Stack Validation Harness (`harness/validate_v6_2_modern_stacks.py`):** 19 automated modern stack tests.

## [6.1.0] - 2026-08-31

### Added
- **Monorepo & Deep-Hierarchy Support:** Unified multi-application discovery (Django + FastAPI + Flask + Shared ORM) and 8-level directory resolution without identity collisions.
- **Automated Generated/Vendor Noise Suppression:** Auto-filtering of non-actionable paths (`migrations/`, `node_modules/`, `dist/`, `build/`, `*.min.js`, `*.pb.go`).
- **High-Density Root-Cause Collapsing:** Ability to group and collapse 250+ repeated vulnerability alerts into systemic root-cause clusters with module hotspot metrics.
- **Readable Report Guardrails:** Collapsible `<details>` tables triggered at 25+ findings to prevent unreadable Markdown report bloat.
- **Sub-Second Scale Performance:** Tested on 2,500+ files and 1,000+ SARIF items ($< 0.10\text{s}$ execution time).
- **Scale & Complexity Benchmark Harness (`harness/validate_v6_1_scale.py`):** 23 automated stress assertions.

## [6.0.0] - 2026-08-31

### Added
- **Run Folder & Artifact Registry (`core/run_manager.py`):** Dedicated, isolated run directory (`runs/<run-id>/`) containing `manifest.json`, `summary.md`, `findings.md`, `remediation.md`, `apply-plan.md`, `recheck.md`, `evidence.json`, `diff-summary.md`, `changed-files.txt`, `sarif.json`, and `logs/`.
- **Line-Shift Invariant Finding Fingerprints (`core/identity.py`):** Deterministic fingerprint hashing based on Rule ID, normalized file path, code region hash, and sink signatures that survive minor code refactorings and line shifts.
- **Root-Cause Clustering Engine (`core/clustering.py`):** Automatic grouping of related findings into systemic root-cause clusters (`cluster-tenant-isolation`, `cluster-path-traversal`, `cluster-template-escaping`, `cluster-header-trust`, `cluster-idor-scoping`, `cluster-rate-limiting`, `cluster-ssrf-network`, `cluster-webhook-auth`, `cluster-secrets`).
- **Structured Remediation Bundles (`core/bundle.py`):** Standardized remediation packages per finding (`finding.md`, `remediation.md`, `minimal_patch_plan.md`, `verify-after-change.md`, `metadata.json`).
- **Minimal Patch Governance & Policy Enforcement (`core/governance.py`):** Enforces strict limits on line churn and file modifications, rejects boilerplate/comments, and escalates sensitive contexts (auth, crypto, tenant isolation, DB, uploads).
- **Targeted Recheck Engine (`core/rechecker.py`):** Differential re-audits scoped strictly to modified files and adjacent trust boundaries with explicit status transitions (`Confirmed Fixed`, `Partially Fixed`, `Needs Manual Review`, `Regressed`, `Not Reproducible`).
- **SARIF v2.1.0 JSON Export (`core/sarif.py`):** Standard SARIF export for CI/CD, GitHub Advanced Security, and SIEM interoperability.
- **Unified v6 Workflow Controller (`core/v6_workflow.py`):** End-to-end orchestration of scan, cluster, harden, apply, recheck, and report cycles.

## [0.5.6] - 2026-08-27

### Added
- **Large-Project Validation Suite (`harness/validate_large_projects.py`):** Multi-repository validation harness supporting large-scale codebases with over 14,000+ files across 10 frameworks/libraries.
- **Multi-Repository Manifest (`projects/manifest.yaml`):** Standardized configuration defining target repository profiles, exclusion patterns, test triggers, and seeded vulnerability benchmarks.
- **Context-Aware Rule Tuning & Guardrails:** Hardened detection rules (`TG-AUTH-008`, `TG-INPUT-005`, `TG-INPUT-006`, `TG-DB-004`) to eliminate false positives and gracefully downgrade incomplete evidence to `Needs Review`.
- **Seeded-Case Recall Measurement:** Formal benchmarking framework for measuring detection recall using non-production seeded test vulnerabilities.
- **Ponytail Patch Quality Tracking Ledger:** Granular recording of remediation diff metrics, line churn, unintended side effects, and recheck verification status.
- **Transparent Pilot Readiness Classification:** Formal policy distinguishing simulated dry-runs from real-world triage, replacing unmeasured claims with clear pilot validation criteria.

## [0.5.5] - 2026-08-26

### Added
- **Rule Precision Calibration:** Formal criteria for routing ambiguous or infrastructure-delegated patterns to `Needs Review` rather than false `Confirmed` findings.
- **Ponytail Remediation Safety Protocol:** Enforced least-invasive patch generation limits, mandatory dry-run syntax assertions, and automated rejection of unrelated file churn.
- **Differential Retest Hardening:** Enhanced `/torusguard recheck` verification state machine to detect regressions (`New Risk`) in automated remediation patches.

## [0.5.4] - 2026-08-25

### Added
- **9-Section Actionable Report Architecture (`core/formatter.py`):** Standardized report structure comprising Header, Executive Summary, Scope & Methodology, Summary Table, Detailed Findings, Prioritized Triage Roadmap, Retest Workflow, Limitations, and Appendix.
- **Remediation Priority Triage:** Added `RemediationPriority` (`Immediate P0`, `Near-Term P1`, `Backlog P2`) enabling multi-stakeholder triage.
- **Business vs Technical Context Separation:** Explicit separation between executive business impact and deep technical mechanics in finding cards.
- **Automated Sensitive Data Masking (`mask_sensitive_data`):** Redacts Stripe keys, GitHub tokens, JWTs, and passwords from raw evidence snippets.
- **Ticket-Ready Issue Tracker Payloads:** Pre-formatted copy-pasteable Markdown snippets for GitHub Issues, Jira, and Linear.
- **Validation Harness Expansion:** Expanded `harness/runner.py` with 64 automated checks (100% pass rate).

## [0.5.3] - 2026-08-25

### Added
- **4 New Canonical Security Rules (64 Total):**
  - `TG-AUTH-008`: Untrusted Role or Tenant Header Injection (`X-User-Role`, `X-Tenant-ID`).
  - `TG-INPUT-005`: Unsafe Template Rendering & Disabled Autoescaping (`mark_safe`, `| safe`, `render_template_string`).
  - `TG-INPUT-006`: Path Traversal & Unsafe Upload Storage (`os.path.join` with client filename).
  - `TG-DB-004`: Missing Tenant Query Isolation in Multi-Tenant Models.
- **Framework-Native Remediations:** Added concrete Before/After remediation patterns for FastAPI, Flask, Django, DRF, and SQLAlchemy.
- **Validation Engine Expansion:** Added 3 new paired differential fixtures in `FixtureManager`, bringing the test suite to 62 automated checks (100% pass rate).

### Changed
- Updated Python Rule Mapping Matrix (`docs/python-rule-mapping.md`) to reflect expanded rule coverage.

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
