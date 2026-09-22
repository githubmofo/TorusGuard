# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0-alpha] — 2026-09-22

### Added
- **Multi-Modal Vision OCR Engine** (`internal/scanner/ocr.go`): Optical character recognition powered by Tesseract OCR (v5.4.0) with `--dpi 300` resolution enhancement. Automatically discovers leaked API keys (`TG-SEC-001`), AWS credentials (`TG-SEC-002`), GitHub PATs (`TG-SEC-003`), Database URIs (`TG-SEC-004`), Private Keys (`TG-SEC-005`), and JWTs (`TG-SEC-006`) within architecture diagrams and screenshot assets (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`).
- **OCR Memory Bounds & DoS Invariant**: Enforced 10MB memory safety envelope on all image scanning to satisfy TorusGuard Invariant #10.
- **Native Model Context Protocol (MCP) Server** (`cmd/torusguard/mcp.go`): JSON-RPC 2.0 stdio server providing standard agent integration for Antigravity, Cursor, Windsurf, and Claude Code.
- **MCP Native Tools**: Implemented and registered `torusguard_audit`, `torusguard_ocr_scan`, `torusguard_harden`, `torusguard_recheck`, and `torusguard_status`.
- **MCP Living Resources**: Exposed `torusguard://security_report` and `torusguard://rules_catalog` for instant LLM context ingestion.
- **MCP Output Truncation Safeguard**: Built-in 32,000-character truncation ceiling (`maxOutputChars = 32000`) preventing context overflow attacks.
- **Tri-Mode Parity Architecture**: Unified operational parity across Mode A (Terminal CLI), Mode B (AI Chat Slash Commands), and Mode C (Native MCP Protocol).
- **16-Repository Mass Test Validation**: Verified 100% pass rate across 16 major language/framework ecosystems in 8.32 seconds.
- **Go Native CLI Engine**: Rewrote the entire TorusGuard engine as a zero-dependency, single-binary Go CLI (`cmd/torusguard/main.go`).
- **17-Command Router**: Implemented `init`, `status`, `audit`, `verify`, `harden`, `apply`, `rollback`, `recheck`, `report`, `recipes`, `authorize`, `web-validate`, `exploit-check`, `ocr-scan`, `mcp`, `update`, and `help` commands via unified switch router.
- **Heuristic AST Scanner** (`internal/scanner/scanner.go`): Polyglot regex-based static analysis for Go, JavaScript, TypeScript, and Python source files with secret detection and SQL injection heuristics.
- **Ponytail Protocol Enforcement** (`internal/harden/patch.go`): Native line-counting bounds validation (≤35 additions, ≤25 deletions per patch bundle).
- **Pre-Apply Snapshot Engine** (`internal/apply/snapshot.go`): Byte-for-byte `.bak` backup of target source files before patch application with path traversal prevention via `filepath.Clean()`.
- **Patch Application via `git apply`** (`internal/apply/apply.go`): Parses unified diff format to extract target filenames and applies patches with Human Gate (`--yes`) enforcement.
- **Dynamic SARIF v2.1.0 Reporting** (`internal/report/sarif.go`): Generates structured SARIF JSON from actual scan findings with proper `results` mapping.
- **Dark-Mode HTML Reports** (`internal/report/html.go`): Single-file visual posture dashboards.
- **Cryptographic Authorization Tokens** (`internal/validate/validate.go`): Generates 16-byte `crypto/rand` tokens with TTL, saved to `.torusguard/auth.json`. Panics on entropy failure (fail-closed).
- **HTTP Security Probing** (`internal/validate/validate.go`): `web-validate` sends requests with `X-TorusGuard-Audit` headers, checks for `Content-Security-Policy`, and blocks SSRF to private IP ranges and `169.254.169.254`.
- **Bounded Exploit Check** (`internal/validate/validate.go`): Sends inert SQL injection payloads to verify backend error handling.
- **Evidence Verification** (`internal/validate/validate.go`): `verify` command cross-references `security_report.md` against live disk state.
- **Terminal UI System** (`internal/termui/`): 75-column formatted output with Unicode emoji width calculation and ANSI escape sequences.
- **Stack Detection** (`internal/workspace/`): Automatic detection of Go, Node.js, Python, and other project types.
- **Rule Catalog Loader** (`internal/rules/`): Loads TG-* security rule definitions from `.torusguard/rules/`.
- **Golden Fix Recipe Memory** (`internal/memory/`): Persistent storage and retrieval of verified remediation patterns.
- **Differential Re-Scan** (`internal/recheck/`): Targeted re-scan of modified files to confirm fix closure.

### Security Hardening
- **Removed hardcoded fallback token**: `generateToken()` now panics on `crypto/rand` failure instead of returning a predictable string.
- **Path traversal prevention**: Snapshot engine validates all paths with `filepath.Clean()` and rejects `../` escapes.
- **DoS resilience**: Scanner enforces 10,000-file maximum and 5-minute `context.WithTimeout`.
- **5MB file size limit**: Scanner skips files larger than 5MB to prevent memory exhaustion.
- **SSRF defense**: `web-validate` resolves hostnames and blocks private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and AWS metadata (`169.254.169.254`).

### Changed
- Migrated from Python/Node.js hybrid architecture to pure Go single binary.
- SARIF report generator now maps actual findings from `security_report.md` instead of emitting empty results.
- Apply command now snapshots the *target source file* (not the patch file itself).

---

## [1.4.0] - 2026-09-15

### Added
- npm package wrapper (`bin/torusguard.js`) for `npx torusguard` usage.
- AI agent integration files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`).
- 74 security rules across 18 architectural families.
- Workspace scaffolding via `npx torusguard init`.

### Fixed
- Workflow path case sensitivity for cross-platform CI.

---

## [1.3.6] - 2026-09-12

### Added
- **Enterprise Remediation Hub**: Enhanced remediation workflow with compliance framework integration.
- **Compliance Frameworks**: Added compliance mapping for SOC 2, HIPAA, PCI-DSS, and GDPR.
- **Dark/Light Theme Switcher**: Added theme toggle to HTML posture reports.

### Fixed
- Resolved compliance frameworks IDE type inference in `html_reporter.py`.
- Fixed portfolio dictionary type annotations in `validate_large_projects`.

---

## [1.3.5] - 2026-09-11

### Added
- **74 Canonical Security Rules**: Expanded rule catalog from 64 to 74 rules across 18 architectural families.
- **Living Verification Architecture**: Hardened detection rules with continuous re-verification support.
- Architecture mermaid flowcharts in README documentation.

---

## [1.3.4] - 2026-09-10

### Added
- **Standardized 75-Column Terminal UI**: All CLI outputs adhere to 75 visual columns with Unicode emoji width calculation, ANSI escape stripping, and visual truncation with ellipsis.
- **Expanded Remediation Engine**: Enhanced `harden` and `apply` with comprehensive dual-mode guidance.
- **Comprehensive Dual-Mode Skills**: Added specialist skill routing for all 13 TorusGuard sub-commands in `SKILL.md`.

---

## [1.3.3] - 2026-09-09

### Added
- **Robust AI Agent Fallback**: Standalone operation mode when `.torusguard/` workspace is absent, applying universal security invariants.
- **Polyglot Stack Detection**: Expanded detection from 2 to 16+ languages with 30+ framework recognition.

---

## [1.3.2] - 2026-09-09

### Added
- Enhanced `harden` DOM `innerHTML` remediation patterns.
- Fixed `apply` lifecycle UX for cleaner developer experience.

---

## [1.3.1] - 2026-09-08

### Fixed
- **CLI Dispatcher Command Routing** (`bin/torusguard.js`): Added dedicated dispatch routing for `npx torusguard audit`, preventing fallback into `bootstrap.py` which caused `unrecognized arguments: audit`. Added handlers for `harden`, `apply`, `rollback`, `recheck`, and `recipes`.
- **Pre-Commit Diff Guard False Positive Elimination** (`diff_guard.py`): Added `is_exempt_diff_path()` to bypass documentation files, AI editor prompt instructions, rule definition manifests, and test fixtures.

---

## [1.3.0] - 2026-09-07

### Added
- **Dual-Strategy Governance Architecture** (Terminal CLI & AI Chat Workflows): Full governance flow in standard terminal environments where AI chat slash commands are not available.
  - `npx torusguard harden`: Formulates surgical candidate patch bundles under Ponytail Protocol bounds (≤35 additions, ≤25 deletions).
  - `npx torusguard apply`: Interactive terminal Human Gate authorization with syntax-highlighted diffs. Auto-distills verified fixes into Golden Fix Recipes.
  - `npx torusguard rollback`: Instant one-command rollback restoring all `.bak` files from `.torusguard/snapshots/`.
  - `npx torusguard recheck`: Targeted differential AST scan with `Confirmed Fixed` vs `Regressed` state machine.
  - `npx torusguard recipes`: Explores distilled Golden Fix Recipes with Ponytail metrics and interactive unified diff snippets.
- **Universal Polyglot Stack Detector**: 16+ languages, 30+ frameworks, 20+ ORMs. Multi-language fallback census and multi-stack monorepo discovery.
- **Polyglot Content-Aware Diff Guard** (`diff_guard.py`): Multi-language security bypass detection for Go, Java, C#, PHP, and Rust. Multi-ORM tenant boundary stripping detection for GORM, LINQ, Entity Framework, and Prisma.
- **Stack-Adaptive AI IDE Rules Compiler** (`rules_sync.py`): Dynamic rule tailoring per ecosystem with ≤400 token budget overhead.
- **Polyglot Reference Ecosystem**: Dedicated security hardening guides for Go, Rust, Java, and C# in `.torusguard/references/`.
- **1-Command Git Pre-Commit Hook Installer**: `npx torusguard diff-guard --install-hook` and `--uninstall-hook`.
- **Visual HTML Posture Report**: 7-stage interactive pipeline flow with dual CLI/chat prompts.
- **26-Repository Real-World Portfolio Evaluation**.

---

## [1.1.0] - 2026-09-04

### Added
- **Advanced Memory Engine**: Implemented adaptive security memory with context decay and Golden Fix pattern persistence.
- **Governance Lifecycle Flowchart**: Added visual dual-track governance architecture.

---

## [1.0.0] - 2026-09-03

### Added
- **General Availability Release**: Adaptive security memory engine and formal GA milestone.
- **Finding Lifecycle State Machine**: Implemented formal 6-stage lifecycle (`Detect` → `Classify` → `Verify` → `Remediate` → `Re-check` → `Archive`).

---

## [0.9.5] - 2026-09-01

### Added
- **Terminal UI Overhaul**: Modern box UI cards, visual trust indicators, and rich ANSI formatting.
- **Socket Alert Fix**: Resolved WebSocket security alert rendering.
- **Registry Parity**: Synchronized npm package with GitHub Packages.

---

## [0.9.4] - 2026-08-30

### Added
- Enhanced Mermaid flowcharts documenting core innovations.
- Updated documentation across MAINTAINERS, CONTRIBUTING, CHANGELOG, and SECURITY.

---

## [0.9.3] - 2026-08-30

### Added
- npm publication with corrected `bin` paths and repository URL.
- Root `SKILL.md` single discovery with universal silent flag.

---

## [0.9.2] - 2026-08-29

### Added
- **Dual-Track Architecture**: Universal AI Skill and Production NPM Package.
- Multi-agent support for Kimi, VS Code Copilot, Windsurf, Cursor, and Antigravity.

---

## [0.6.1] - 2026-09-01

### Added
- **Modern Stack Compatibility Module**: Extended AST detection patterns for Next.js 14+ App Router, React Server Components, tRPC v11, and edge-native patterns.
- Readable report guardrails with collapsible `<details>` tables triggered at 25+ findings.
- Sub-second scale performance: tested on 2,500+ files and 1,000+ SARIF items (<0.10s execution time).
- **Scale & Complexity Benchmark Harness** (`harness/validate_v0_6_1_scale.py`): 23 automated stress assertions.

---

## [0.6.0] - 2026-08-31

### Added
- **Run Folder & Artifact Registry** (`core/run_manager.py`): Dedicated, isolated run directories with `manifest.json`, `summary.md`, `findings.md`, `remediation.md`, SARIF, and logs.
- **Line-Shift Invariant Finding Fingerprints** (`core/identity.py`): Deterministic fingerprint hashing that survives minor code refactorings and line shifts.
- **Root-Cause Clustering Engine** (`core/clustering.py`): Automatic grouping of related findings into systemic root-cause clusters.
- **Structured Remediation Bundles** (`core/bundle.py`): Standardized remediation packages per finding.
- **Minimal Patch Governance & Policy Enforcement** (`core/governance.py`): Enforces strict limits on line churn with escalation for sensitive contexts.
- **Targeted Recheck Engine** (`core/rechecker.py`): Differential re-audits with explicit status transitions.
- **SARIF v2.1.0 JSON Export** (`core/sarif.py`): Standard SARIF export for CI/CD and SIEM interoperability.

---

## [0.5.6] - 2026-08-27

### Added
- **Large-Project Validation Suite** (`harness/validate_large_projects.py`): Multi-repository validation across 14,000+ files and 10 frameworks.
- **Multi-Repository Manifest** (`projects/manifest.yaml`): Standardized configuration for target repository profiles.
- Context-aware rule tuning to eliminate false positives.
- Seeded-case recall measurement framework.

---

## [0.5.5] - 2026-08-26

### Added
- Rule precision calibration for `Needs Review` vs `Confirmed` classification.
- Ponytail remediation safety protocol with dry-run syntax assertions.
- Enhanced recheck verification state machine with `New Risk` regression detection.

---

## [0.5.4] - 2026-08-25

### Added
- **9-Section Actionable Report Architecture**: Header, Executive Summary, Scope & Methodology, Summary Table, Detailed Findings, Prioritized Triage Roadmap, Retest Workflow, Limitations, and Appendix.
- Remediation priority triage (`Immediate P0`, `Near-Term P1`, `Backlog P2`).
- Automated sensitive data masking for Stripe keys, GitHub tokens, JWTs, and passwords.
- Ticket-ready issue tracker payloads for GitHub Issues, Jira, and Linear.
- Validation harness expansion to 64 automated checks.

---

## [0.5.3] - 2026-08-25

### Added
- **4 New Canonical Security Rules (64 Total)**: `TG-AUTH-008` (Header Injection), `TG-INPUT-005` (Template Rendering), `TG-INPUT-006` (Path Traversal), `TG-DB-004` (Tenant Isolation).
- Framework-native remediations for FastAPI, Flask, Django, DRF, and SQLAlchemy.
- Validation engine expansion to 62 automated checks.

---

## [0.5.2] - 2026-08-25

### Added
- **7-Layer Validation Engine** (`harness/engine/`): Fixture management, deterministic replay, differential comparisons, regression tracking, and false-alarm diagnostics.
- **Deterministic Multi-Pass Replay**: 3x execution verification with SHA-256 hash assertions.
- **Historical Regression Tracker**: Automated tracking ensuring baseline fixes remain clean.
- New schemas: `fixture.schema.json` and `validation-run.schema.json`.

---

## [0.5.1] - 2026-08-25

### Added
- **Structured Provenance Tracking**: Every finding records discovery module, triggering input, decision path, and verification step.
- **Auditable 0–100 Confidence Scoring Model**: 5-factor mathematical rubric replacing subjective confidence.
- **Cryptographic Evidence Packaging**: SHA-256 checksums for all raw code evidence snippets.
- **Explicit Retest & Closure State Machine**: `RetestRecord` with post-fix evidence hashes.

---

## [0.5.0] - 2026-08-25

### Added
- **Formal 6-Stage Finding Lifecycle**: `Detect` → `Classify` → `Verify` → `Remediate` → `Re-check` → `Archive`.
- **Formal JSON Schemas** (`schemas/`): Normalized schemas for findings, evidence, remediations, rules, and lifecycle transitions.
- **Repeatable Automated Validation Harness** (`harness/runner.py`): Schema validation, catalog integrity, educational fixtures, and lifecycle assertions.
- **Core Engine & Workflow Package** (`core/`): Pydantic-style normalized models, lifecycle manager, and report formatter.
- Added `/torusguard recheck` command for differential verification.

---

## [0.4.1] - 2026-08-21

### Fixed
- Refined Python stack detection for Django, DRF, FastAPI, Flask, SQLAlchemy, and mixed monorepos.
- Corrected false-positive conditions for service-layer ownership queries and bound LIKE parameters.
- Added sanitized Python regression fixtures in `tests/fixtures/python/`.
- Added authorized repository validation template.

---

## [0.4.0] - 2026-08-21

### Added
- Comprehensive Python security guides for Django, DRF, FastAPI, Flask, and SQLAlchemy.
- Python dependency management and CI/CD supply-chain guidance.
- Automatic Python stack detection and reference module loading.
- Paired vulnerable and hardened Python reference applications in `examples/python/`.
- Cross-platform rule parity documentation.

---

## [0.3.0] - 2026-08-19

### Added
- SSRF and outbound-request security rules.
- Business-logic abuse and sensitive-flow review.
- Mass-assignment and property-level authorization rules.
- CSRF and credentialed cross-origin request guidance.
- Webhook signature, replay, and idempotency rules.
- GraphQL security guidance (depth, complexity, batching, resolver authorization).
- WebSocket authentication, channel authorization, and message validation rules.
- Dependency and CI/CD supply-chain guidance.
- Cache and sensitive-response protection rules.

---

## [0.2.0] - 2026-08-18

### Added
- 25 documented rules across 7 core areas with severity, detection, remediation, and verification.
- 5 core workflow commands: `init`, `audit`, `harden`, `check`, `verify`.
- Standardized templates for `SECURITY.md`, threat modeling, audit reports, and deployment pre-flight.
- Framework security guides for React/Vite, Next.js, Express, Supabase, and Firebase.
- Paired vulnerable and hardened reference applications.

---

## [0.1.0] - 2026-08-18

### Added
- Initial portable AI-agent skill for web application security guidance.
