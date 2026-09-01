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

### ✅ v0.5.0 — Core Architecture & Workflow Release (2026-08-25)
- **Formal 6-Stage Finding Lifecycle:** `Detect` ──► `Classify` ──► `Verify` ──► `Remediate` ──► `Re-check` ──► `Archive`.
- **Formal JSON Schemas (`schemas/`):** Standardized schemas for findings, evidence, remediations, rule metadata, and lifecycle transitions.
- **Repeatable Automated Validation Harness (`harness/runner.py`):** Standalone harness executing schema validation, rule catalog integrity, educational fixture differentials, and lifecycle state assertions.
- **Core Workflow Package (`core/`):** Normalized data models, lifecycle manager, and Human-First report formatter.
- **Command Addition:** Added `/torusguard recheck` for differential verification of post-fix codebases.

### ✅ v0.5.1 — Finding Quality & Provenance Release (2026-08-25)
- **Structured Provenance Tracking:** Explicit provenance chains documenting discovery module, triggering input, decision path, and verification step.
- **Auditable 0–100 Confidence Scoring:** Transparent 5-factor mathematical rubric replacing subjective estimates.
- **Cryptographic Evidence Packaging:** Immutable SHA-256 checksums computed for all raw code evidence snippets.
- **Explicit Retest State Machine:** Formal post-fix retesting via `/torusguard recheck` before findings can transition to `Verified Fixed`.
- **New Schemas:** Added `provenance.schema.json`, `confidence.schema.json`, and `retest.schema.json`.

### ✅ v0.5.2 — Validation Engine & Deterministic Replay Release (2026-08-25)
- **7-Layer Validation Engine (`harness/engine/`):** `FixtureManager`, `ReplayRunner`, `ResultComparator`, `RegressionTracker`, `FalsePositiveAnalyzer`, `ValidationEvidenceCollector`, `ValidationReportEmitter`.
- **Multi-Pass Deterministic Replay (3x):** Verified identical serialized output hashes across repeated scan passes.
- **Differential Result Comparator:** Evaluates paired vulnerable vs hardened behavior with standardized outcome labels (`Vulnerable Confirmed`, `Hardened Safe`, `False Positive`, etc.).
- **Historical Regression Tracker:** Automated tracking ensuring baseline fixes from earlier releases remain clean.
- **New Schemas:** Added `fixture.schema.json` and `validation-run.schema.json`.

### ✅ v0.5.3 — Python Security Coverage & Framework Guidance (2026-08-25)
- **4 New Canonical Security Rules (64 Total):**
  - `TG-AUTH-008`: Untrusted Role or Tenant Header Injection (`X-User-Role`, `X-Tenant-ID`).
  - `TG-INPUT-005`: Unsafe Template Rendering & Disabled Autoescaping (`mark_safe`, `| safe`, `render_template_string`).
  - `TG-INPUT-006`: Path Traversal & Unsafe Upload Storage (`os.path.join` with client filename).
  - `TG-DB-004`: Missing Tenant Query Isolation in Multi-Tenant Models.
- **Framework-Native Remediations:** Added concrete Before/After remediation patterns for FastAPI, Flask, Django, DRF, and SQLAlchemy.
- **Validation Engine Expansion:** Added 3 new paired differential fixtures in `FixtureManager` (62 passed automated tests).

### ✅ v0.5.4 — Usability, Clarity & Actionable Remediation Release (2026-08-25)
- **9-Section Actionable Report Flow:** Standardized flow comprising Header, Executive Summary, Scope & Methodology, Summary Table, Detailed Findings, Prioritized Triage Roadmap, Retest Workflow, Limitations, and Appendix.
- **Remediation Priority Triage:** Findings classified by urgency (`Immediate P0`, `Near-Term P1`, `Backlog P2`).
- **Context Separation:** Strict separation of executive Business Impact from technical code mechanics.
- **Sensitive Data Masking:** Automated redaction of API keys (`sk_live_...`), GitHub tokens, JWTs, and passwords in evidence snippets.
- **Ticket-Ready Payloads:** Pre-formatted Markdown blocks ready to copy-paste into GitHub Issues, Jira, and Linear.
- **Validation Harness:** 64 automated tests passing with 100% pass rate (`python harness/runner.py`).

### ✅ v0.5.5 — Folder-per-Run & Ponytail Integration (2026-08-26)
- **Folder-per-Run Architecture (`RunFolder`):** Isolated execution folders (`.torusguard/runs/run-YYYYMMDD-HHMMSS/`) strictly grouping findings, remediation guides, logs, and patches for auditability.
- **Ponytail Agent Integration (`/torusguard apply`):** Direct application of remediation via the Ponytail skill, producing constrained, safe, and minimal patches without rewriting large code segments.
- **Rule Precision Calibration:** Criteria for routing ambiguous proxy/gateway patterns to `Needs Review` to avoid false positive escalation.
- **Closed-Loop Workflow:** Formalized `Harden ──► Apply ──► Recheck` workflow bridging AI remediation suggestions with auditable, reproducible codebase patches.

### ✅ v0.5.6 — Large-Project Validation Suite & Rule Tuning Architecture (2026-08-27)
- **10 Large-Project Validation Harness (`harness/validate_large_projects.py`):** Standardized multi-repository runner supporting 14,000+ files across 10 major Python ecosystem targets.
- **Multi-Project Manifest & Seed Tracking (`projects/manifest.yaml`):** Standardized repository declarations, exclusions, and synthetic vulnerability seed injection.
- **Context-Aware Rule Tuning Guardrails:** Hardened rules (`TG-AUTH-008`, `TG-INPUT-005`, `TG-INPUT-006`, `TG-DB-004`) to suppress false positives from framework utilities while preserving true positive detection.
- **Seeded-Case Recall Measurement:** Formal benchmarking framework for calculating recall on known vulnerabilities.
- **Ponytail Patch Quality Tracking Ledger:** Auditable diff metrics (line churn, 0 unrelated files changed, test pass confirmation).
- **Transparent Pilot Readiness Classification:** Honest evaluation framework distinguishing simulated runs from human-triaged scans.

### ✅ v0.6.0 — Governed Remediation & Targeted Recheck System (2026-08-31)
- **Isolated Run Folder System (`RunManager`):** Dedicated execution folders (`runs/<run-id>/`) containing all 10 standard audit artifacts.
- **Line-Shift Invariant Finding Fingerprints (`IdentityEngine`):** Deterministic fingerprint hashing based on AST sink signatures that survive line shifts.
- **Root-Cause Clustering Engine (`ClusteringEngine`):** Automatic grouping of related findings into systemic root-cause clusters.
- **Structured Remediation Bundles (`BundleManager`):** Standardized 5-file packages per cluster.
- **Minimal Patch Governance (`PatchGovernor`):** Strict line churn bounds ($\le 35$ additions, $\le 25$ deletions).
- **Targeted Recheck Engine (`TargetedRechecker`):** Differential re-audits scoped strictly to modified files.
- **SARIF v2.1.0 JSON Export (`SarifExporter`):** Standard OASIS SARIF v2.1.0 output for CI/CD and SIEM.

### ✅ v0.6.1 — Scale & Complexity Hardening (2026-08-31)
- **Monorepo & Deep-Hierarchy Support:** Multi-framework applications (Django + FastAPI + Flask + Shared ORM) and 8-level directory resolution without truncation.
- **Automated Generated/Vendor Noise Suppression:** Auto-filtering of `migrations/`, `dist/`, `build/`, `node_modules/`.
- **High-Density Root-Cause Collapsing:** Collapses 250+ repeated alerts into 3 actionable clusters with hotspot metrics.
- **Readable Report Guardrails:** Collapsible `<details>` tables triggered at 25+ findings.
- **Scale Benchmarking:** Tested on 2,500+ files and 1,000+ SARIF items ($< 0.10\text{s}$ execution time).

### ✅ v0.6.2 — Modern Stack Compatibility (2026-08-31)
- **Modern Stack Profiler (`StackProfiler`):** Detection of framework version families (Django 5.x, FastAPI 0.100+, SQLAlchemy 2.0, Next.js 14+) and package managers (uv, Poetry, PEP 621).
- **Async-Native Remediation:** Idiomatic patches for async view coroutines (`await aget()`) and async database queries (`AsyncSession`).
- **FastAPI & Pydantic v2 Compatibility:** `Annotated[User, Depends()]` dependency injections.
- **SQLAlchemy 2.0 select() Scoping:** Modern 2.0 select statement query scoping for multi-tenant isolation.
- **Frontend Server Action Security:** Detection and remediation of Next.js 14 Server Actions (`"use server"`).
- **Container & Supply Chain Security:** Hardening of Dockerfiles (non-root user, secret protection) and GitHub Actions.

### ✅ v0.6.3 — Final Drift, Upload & Sensitive-Path Hardening (2026-08-31)
- **Multi-Commit Drift Invariance:** Invariant fingerprints verified across multi-commit refactorings.
- **GitHub Code Scanning SARIF Deduplication:** Added `partialFingerprints` (`primaryLocationLineHash`) to eliminate duplicate security alerts in GitHub PRs.
- **Sensitive-Path Review Levels:** Stricter escalation hierarchy (`Automatic`, `Peer Review Recommended`, `Mandatory Security Sign-Off`) blocking auto-apply on Auth, Tenancy, Secrets, Crypto, Storage, and CI/CD.
- **Modern-Stack Negative Test Suite:** Verified zero false positives on safe Django 5.x async, FastAPI `Annotated`, SQLAlchemy 2.0 select, and Next.js 14 Server Actions.

### ✅ v0.7.0 — Authorized Runtime Validation & Bounded Exploitability (2026-09-01)
- **Target Authorization Gate:** Enforces target ownership proof and strict scope limits (`scope.json`, `authorization.md`).
- **Safety Review Gates:** Tiered risk evaluation (`Auto-Allowed`, `Approval Required`, `Manual Only`) blocking destructive actions.
- **Bounded Exploitability Confirmation:** Safe, single-step verification probes across 5 formal statuses (`Runtime Confirmed`, `Runtime Likely`, `Needs Manual Review`, `Not Reproducible in Scope`, `Blocked by Controls`).
- **4-Role Multi-Agent Workflow:** Explicit authority separation and handoff contracts between Profiler, Validator, Remediator, and Reviewer roles (`role-audit.json`, `agent-handoffs.md`).
- **Replayable Validation Traces:** Deterministic verification sequences serialized to `replay.json` and `replay.md`.
- **Multi-Analysis SARIF v2.1.0:** Partitioned category exports via `automationDetails.id: torusguard/runtime/`.
- **Structural Architecture Refactoring:** Modular clean-tier refactor across core engine with 100% test pass rate.

---

## 🎯 Upcoming Milestones: v0.7.1+ Series

Detailed specifications and priorities are tracked in [`ROADMAP_v0_7_1.md`](../ROADMAP_v0_7_1.md):

### 🚀 v0.7.1 — PatchGovernor Diff Line Scanning & Agent Security (Q4 2026)
- [ ] **Content-Aware Diff Line Scanning:** Extend `PatchGovernor` to scan added/modified unified diff lines for sensitive domain keywords (`auth`, `tenant`).
- [ ] **`TG-AGENT-*` Rule Family:** First-class rules for agentic AI architectures:
  - `TG-AGENT-001`: Direct/Indirect Prompt Injection in System Context Files.
  - `TG-AGENT-002`: Unsafe Tool Dispatch & Shell Execution without Sandboxing.
  - `TG-AGENT-003`: Overly Broad MCP Tool Scoping & Credential Access.
  - `TG-AGENT-004`: Persistent Memory & Cross-Session Information Leakage.

### 🚀 v0.7.2 — GraphQL, WebSockets & Container Build Chains (Q1 2027)
- [ ] **GraphQL & WebSocket Runtime Probes:** Bounded complexity introspection and WebSocket channel authorization assertions.
- [ ] **Multi-Stage Container Build Inspection:** Detecting build-time secret persistence and layer caching leaks.
- [ ] **CI/CD Permission Modeling:** GitHub Actions least privilege and OIDC trust policy analysis.

### 🚀 v0.8.0 — Sandboxed Replay & Full Agentic MCP Suite (Q2 2027)
- [ ] Headless Chromium sandbox integration inside bounded Docker environments.
- [ ] Bidirectional WebSocket state-machine recording and deterministic replay.
- [ ] Full MCP server security evaluation testbed.

---

## 🔭 Future Horizons: v1.0.0 — Stable Multi-Platform Standard

- **Broader Ecosystem Guides:** Go (Fiber / Gin), Ruby on Rails, and Spring Boot.
- **Automated Catalog Linter:** GitHub Actions CI workflow to validate Markdown structure, rule IDs, and link integrity.
- **Interactive Playground / Multi-Language Fixture Suite:** Broadened automated test fixtures for local evaluation.

---

## 💡 Proposing a Roadmap Item
Have an idea for a new feature, platform guide, or security domain? Open a [Feature Request](https://github.com/githubmofo/TorusGuard/issues/new?template=feature_request.md) or start a discussion in our repository!
