# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.2] - 2026-09-02

- **Dual-Track Distribution Architecture:** Decoupled TorusGuard into two clean, independent tracks:
  - *Track 1 (Universal AI Agent Skill):* Single `/torusguard` command for all AI agents (Kimi, Antigravity, Cursor, Copilot, Claude Code, Windsurf) installed via `npx skills add` with zero local file dependencies.
  - *Track 2 (Production NPM Package):* Standalone package installed via `npx torusguard init` that scaffolds `.torusguard/` and unlocks all 11 individual slash commands (`/torusguard-audit`, `/torusguard-harden`, `/torusguard-apply`, etc.).
- **Dual-Track Validation Test Suite (`harness/validate_v0_9_2_dual_track.py`):** Automated harness verifying standalone skill execution, npm scaffolding, command unlocking, and token budgets.
- **Autonomous IDE Slash Command Registration (`skills/torusguard/bootstrap.py`):** Scaffolding engine automatically registers `/torusguard` workflows in Antigravity (`.agent/workflows/torusguard.md`), Claude Code (`.claude/commands/torusguard.md`), and Cursor (`.cursor/rules/torusguard.mdc`).
- **Zero-Dependency NPM Runner (`bin/torusguard.js` & `package.json`):** Direct support for `npx torusguard` CLI bridging into the autonomous Python engine.
- **Content-Aware Diff Line Scanner (`.torusguard/scripts/diff_guard.py`):** Unified patch inspector evaluating proposed diff additions and deletions against security invariants:
  - `TG-DIFF-001`: Detects suspicious bypass comments (`# bypass auth`, `// nosec`), disabled TLS verification (`verify=False`), and explicit security skip flags.
  - `TG-DIFF-002`: Detects hardcoded credentials, live API keys, and JWT strings in patch additions.
  - `TG-DIFF-003`: Detects unmitigated deletion of tenant isolation filters (`.filter(tenant=...)`) in patch deletions.
- **Monorepo Sub-Scope Orchestration (`.torusguard/scripts/monorepo_detector.py`):** Multi-package workspace detector profiling Turborepo, pnpm, npm/yarn, and multi-service subdirectories, emitting structured package metadata.
- **Interactive Multi-Stack Playground (`demo/playground/`):** Hands-on test fixtures for FastAPI (`vulnerable_fastapi/main.py`) and Next.js (`vulnerable_nextjs/actions.ts`) demonstrating SQL injection, tenant data leaks, prompt injection, and exposed client secrets.
- **Workflow & Skill Bindings:** Integrated `diff_guard.py` into `/torusguard harden` and `/torusguard apply` workflows while preserving strict 1,000–1,500 token budgets across all 11 commands.
- **Diff & Monorepo Test Suite (`harness/validate_v0_9_2_diff_and_monorepo.py`):** Automated harness verifying diff security rules, monorepo detection, playground sinks, and token budgets.
- **Command-Engine Standard Workflows (`.torusguard/workflows/`):** Upgraded all 11 slash command execution playbooks to the production standard:
  - Formal YAML frontmatter (`description`, `tools`, `version: 0.9.2`, `agent`, `lifecycle-phase`, `required-skills`, `scripts-binding`).
  - Mandatory Pre-Flight Context Inspection preventing unauthorized mutations or runs.
  - "When to Use" decision tables clarifying exact operational scope.
  - Deterministic Phase-by-Phase CLI execution commands with arguments.
  - Failure Recovery & Cascade Rules (3-retry limit, HALT vs CONTINUE).
  - Strict Hallucination Guards preventing destructive actions.
  - Standardized Output Card Formats & Next Step routing.
- **Deepened Specialist Skills (`skills/` & `.torusguard/skills/`):** Enriched all 13 skills with concrete AST patterns for Python (Django, DRF, FastAPI, Flask, SQLAlchemy) and TypeScript (Next.js, Express, React), safe probe canaries, and two-way workflow cross-bindings (`workflow: .torusguard/workflows/<cmd>.md`).
- **Workflows & Skills Validation Suite (`harness/validate_v0_9_2_workflows_and_skills.py`):** Automated harness verifying 100% workflow frontmatter integrity, required sections, script bindings, skill line budgets ($\le 300$), mirror sync, and 1:1 cross-bindings.

## [0.9.1] - 2026-09-02

### Added
- **Autonomous Workspace Bootstrapper (`skills/torusguard/bootstrap.py`):** Self-contained, cross-platform Python installer that unpacks `.torusguard/` offline into any target project during `/torusguard init`.
- **Bundled Offline Template Payload (`skills/torusguard/payload/`):** Full `.torusguard/` template structure bundled inside the skill package so `npx skills add` downloads it locally and runs offline.
- **Standalone Zero-Dependency Installer (`install.py`):** Root CLI script enabling one-liner installation (`python install.py` or curl pipe).
- **Comprehensive System Architecture Guide (`.torusguard/ARCHITECTURE.md`):** Modeled after `.agent/ARCHITECTURE.md`, providing lifecycle flowcharts, agent authority contracts, Ponytail bounds, and directory topology.
- **Cryptographic Integrity Manifest (`.torusguard/.manifest.json`):** SHA-256 integrity ledger indexing all 88 workspace files with normalized cross-platform paths.
- **Manifest Builder & Tamper Detection Utility (`.torusguard/scripts/manifest_builder.py`):** CLI utility for `--check` validation and `--write` manifest generation.
- **Dual-Path Always-On Rules (`.torusguard/rules/TORUSGUARD.md`):** Mirror rule file enabling automatic rule discovery across various AI IDE rule crawlers.
- **Specialist Skills Mirror (`.torusguard/skills/`):** All 13 specialist skills mirrored locally inside `.torusguard/` for full self-containment.
- **End-to-End Installation Test Suite (`harness/validate_v0_9_1_installer.py`):** Automated simulation verifying external project scaffolding, offline unpacking, and manifest integrity.

## [0.9.0] - 2026-09-02

### Added
- **Granular Specialist Skills Architecture (`skills/`):** Decomposed TorusGuard into 12 self-contained, task-specific skills:
  - `skills/torusguard-init/SKILL.md`: Stack detection, framework mapping, and tailored rule activation.
  - `skills/torusguard-authorize/SKILL.md`: Target ownership verification, allowed host/path capture, and `scope.json` governance.
  - `skills/torusguard-audit/SKILL.md`: Deep static AST analysis, stable fingerprinting, root-cause clustering, and complete 0–100 rubric inline.
  - `skills/torusguard-verify/SKILL.md`: Evidence sufficiency auditing, active disk state re-verification, and finding score refinement.
  - `skills/torusguard-web-validate/SKILL.md`: Authorized HTTP/API probing, automatic credential redaction, and safety gate policy.
  - `skills/torusguard-exploit-check/SKILL.md`: Bounded exploitability confirmation across approved vulnerability classes (SQLi, XSS, SSRF, IDOR).
  - `skills/torusguard-harden/SKILL.md`: Governed remediation formulation under Ponytail Protocol limits ($\le 35$ add, $\le 25$ del) and diff generation.
  - `skills/torusguard-apply/SKILL.md`: Surgical patch application with pre-apply rollback snapshots and Human Gate confirmation.
  - `skills/torusguard-recheck/SKILL.md`: Targeted post-patch re-scan with 4-state transition tracking (Fixed, Partially Fixed, Not Fixed, Regression).
  - `skills/torusguard-report/SKILL.md`: Unified executive report generation and OASIS SARIF v2.1.0 structured export.
  - `skills/torusguard-status/SKILL.md`: Diagnostic read-only inspection of active configuration, rule counts, and run history.
- **Master Pipeline Orchestrator (`skills/torusguard-full/SKILL.md`):** Comprehensive end-to-end conductor orchestrating the full 7-stage security pipeline with stage gates and role handoffs.
- **Lazy Loading & Context Budget Discipline:** Every specialist skill embeds its own instructions, safety rules, and scoring models inline (58–165 lines each, strictly $\le 300$), eliminating cross-file context bloat.
- **Automated Skills Validation Harness (`harness/validate_v0_9_0_skills.py`):** 53 automated checks validating existence, YAML frontmatter, line budgets, required sections, router integrity, and script bindings across all 13 skills.

### Changed
- **Router Skill Update (`skills/torusguard/SKILL.md`):** Updated with specialist routing table for lazy loading and bumped version to `0.9.0`.
- **Command Registry (`.torusguard/config/slash-commands.json`):** Registered `/torusguard full` command for end-to-end pipeline execution.
- **Configuration Version:** Bumped `.torusguard/config/torusguard.json` to version `0.9.0`.

## [0.8.0] - 2026-09-02

### Added
- **Installable Skill Kit Architecture (`.torusguard/`):** Transformed TorusGuard into an installable AI agent skill kit deployable via `npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"`.
- **Master Always-On Rules (`.torusguard/TORUSGUARD.md`):** Comprehensive rules engine (`trigger: always_on`) covering the 7-stage lifecycle, 11-command routing table, 5 agent roles, Ponytail patch governance ($\le 35$ additions, $\le 25$ deletions), 5-factor 0–100 confidence scoring, and card-style reporting standards.
- **5 Specialist Agent Definitions (`.torusguard/agents/`):** Dedicated agent profiles with formal responsibilities and safety contracts: `profiler.md`, `auditor.md`, `validator.md`, `remediator.md`, and `reviewer.md`.
- **11 Lifecycle Workflows (`.torusguard/workflows/`):** Complete execution guides for `/torusguard init`, `authorize`, `audit`, `verify`, `web-validate`, `exploit-check`, `harden`, `apply`, `recheck`, `report`, and `status`.
- **5 Python Utility Scripts (`.torusguard/scripts/`):** Standalone pure Python CLI utilities for agent and CI automation: `stack_detect.py`, `finding_scorer.py`, `sarif_exporter.py`, `run_manager.py`, and `safety_gate.py`.
- **Self-Contained Framework References (`.torusguard/references/`):** Embedded security guides for Django, DRF, FastAPI, Flask, SQLAlchemy, Next.js, Express, React/Vite, Supabase, and Firebase.
- **Active Rules Activation System (`.torusguard/rules/active/`):** Dynamic stack-tailored rule activation mechanism with rule taxonomy guide in `.torusguard/rules/README.md`.
- **4 Canonical Output Templates (`.torusguard/templates/`):** Standard templates for `authorization.template.md`, `audit-report.template.md`, `remediation-bundle.template.md`, and `finding-card.template.md`.

### Changed
- **Lean Workspace Bootstrapper (`skills/torusguard/SKILL.md`):** Refactored from a monolithic 153-line guide into a lean 53-line workspace bootstrapper that checks for `.torusguard/TORUSGUARD.md` and delegates execution.
- **Git Tracking Optimization (`.gitignore`):** Hardened `.gitignore` to track the `.torusguard/` skill kit while cleanly ignoring runtime output under `.torusguard/runs/`.

## [0.7.0] - 2026-09-01

### Added
- **Scope & Legal Authorization Gate (`core/authorization.py`):** Requires signed target ownership confirmation or written consent, whitelisted hosts, allowed path prefixes, forbidden sensitive paths, and request budgets before any probe is executed. Emits `scope.json` and `authorization.md`.
- **Safety Review Gates (`core/safety_gate.py`):** Tiered risk evaluation (`Auto-Allowed`, `Approval Required`, `Manual Only`) blocking destructive actions (`/admin/delete`, `/system/shutdown`) and recording safety evaluations in `safety-decisions.json`.
- **Web Validation & Secret Redaction (`core/runtime_validator.py`, `core/runtime_evidence.py`):** Bounded HTTP probing engine with session cookie tracking, request/response logging, and automatic Bearer JWT/token redaction.
- **Bounded Exploitability Confirmation (`core/exploit_checker.py`):** Safe, single-step verification probes for Auth Bypass, Cross-Tenant IDOR, Header Trust Injection, Path Traversal, and Debug/Config Exposure across 5 formal statuses (`Runtime Confirmed`, `Runtime Likely`, `Needs Manual Review`, `Not Reproducible in Scope`, `Blocked by Environment / Controls`).
- **Browser-Assisted Verification (`core/browser_verifier.py`):** Verification of client-side route guards and unauthenticated DOM exposure with navigation depth limits.
- **4-Role Multi-Agent Workflow (`core/agent_roles.py`):** Explicit authority separation and handoff contracts between Profiler, Validator, Remediator, and Reviewer roles with audit trails in `agent-handoffs.md` and `role-audit.json`.
- **Replayable Validation Traces (`core/replay_trace.py`):** Deterministic verification sequences serialized to `replay.json` and `replay.md` with rerun execution support.
- **Unified Reporting & Multi-Analysis SARIF (`core/v070_reporter.py`, `core/sarif.py`):** Merged Markdown reporting and partitioned SARIF v2.1.0 exports via `automationDetails.id: torusguard/runtime/`.
- **Comprehensive Runtime Validation Harness (`harness/validate_v0_7_0_runtime.py`):** 67 automated assertions covering an exhaustive 10-phase senior QA and release audit (100% pass rate).

### Changed
- **Structural Architecture Refactor (`core/`):** Decomposed high-complexity controllers into single-responsibility helpers across `authorization.py`, `governance.py`, `sarif.py`, `runtime_validator.py`, and `v070_workflow.py`.
- **Architectural Tiering & Public API:** Formally structured `core/__init__.py` into Tier 1 (Models/Lifecycle), Tier 2 (Governed Remediation), and Tier 3 (Runtime Validation), declaring all 58 public symbols in `__all__`.
- **Continuous Validation & Governance (`SECURITY.md` & `MAINTAINERS.md`):** Established pre-release validation gates and maintainer security checklist.

### Added
- **Multi-Commit Drift Invariance:** Line-shift invariant fingerprinting verified across multi-commit refactorings.
- **GitHub Code Scanning SARIF Deduplication (`core/sarif.py`):** Added `partialFingerprints` with `primaryLocationLineHash` and `torusguard/v6/identity` to eliminate duplicate security alerts in GitHub PRs.
- **Sensitive-Path Review Levels (`core/governance.py`):** Stricter escalation hierarchy (`Automatic`, `Peer Review Recommended`, `Mandatory Security Sign-Off`) blocking auto-apply on Auth, Tenancy, Secrets, Crypto, Storage, and CI/CD.
- **Modern-Stack Negative Test Suite (`harness/validate_v0_6_3_hardening.py`):** Verified zero false positives on safe Django 5.x async, FastAPI `Annotated`, SQLAlchemy 2.0 select, and Next.js 14 Server Actions.
- **Cross-Artifact Consistency Engine:** Verified synchronization across Manifests, Summaries, Findings, Remediation Bundles, and SARIF JSON.

## [0.6.2] - 2026-08-31

### Added
- **Modern Stack Profiler (`core/stack_profiler.py`):** Automatic detection of framework version families (Django 5.x, FastAPI 0.100+, SQLAlchemy 2.0, Next.js 14+) and package managers (uv, Poetry, PEP 621).
- **Async-Native Remediation:** Idiomatic before/after patches for async view coroutines (`await aget()`) and async database queries (`AsyncSession`).
- **FastAPI & Pydantic v2 Compatibility:** `Annotated[User, Depends()]` dependency injections and `pydantic-settings` environment configuration.
- **SQLAlchemy 2.0 select() Scoping:** Modern 2.0 select statement query scoping for multi-tenant isolation.
- **Frontend Server Action Security:** Detection and remediation of unauthenticated Next.js 14 Server Actions (`"use server"`).
- **Container & Supply Chain Security:** Hardening of Dockerfiles (secrets, non-root user) and GitHub Actions (`permissions: read-all`, SHA pinning).
- **Modern Stack Validation Harness (`harness/validate_v0_6_2_modern_stacks.py`):** 19 automated modern stack tests.

## [0.6.1] - 2026-08-31

### Added
- **Monorepo & Deep-Hierarchy Support:** Unified multi-application discovery (Django + FastAPI + Flask + Shared ORM) and 8-level directory resolution without identity collisions.
- **Automated Generated/Vendor Noise Suppression:** Auto-filtering of non-actionable paths (`migrations/`, `node_modules/`, `dist/`, `build/`, `*.min.js`, `*.pb.go`).
- **High-Density Root-Cause Collapsing:** Ability to group and collapse 250+ repeated vulnerability alerts into systemic root-cause clusters with module hotspot metrics.
- **Readable Report Guardrails:** Collapsible `<details>` tables triggered at 25+ findings to prevent unreadable Markdown report bloat.
- **Sub-Second Scale Performance:** Tested on 2,500+ files and 1,000+ SARIF items ($< 0.10\text{s}$ execution time).
- **Scale & Complexity Benchmark Harness (`harness/validate_v0_6_1_scale.py`):** 23 automated stress assertions.

## [0.6.0] - 2026-08-31

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
