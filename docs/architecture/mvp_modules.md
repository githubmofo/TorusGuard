# TorusGuard MVP Core Modules & Subsystem Breakdown

## 1. Overview
This document specifies the core Minimum Viable Product (MVP) modules comprising the TorusGuard engine, defining their boundaries, class interfaces, and progression toward the v1.0.0 milestone.

---

## 2. MVP Module Catalog

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        TorusGuard Core Modules                         │
│                                                                        │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────┐ │
│  │ 1. Stack Detector    │  │ 2. Rule Matcher     │  │ 3. Confidence  │ │
│  │ (Detect framework)   │  │ (AST & Heuristics)  │  │ (0-100 Rubric) │ │
│  └──────────────────────┘  └─────────────────────┘  └────────────────┘ │
│                                                                        │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────┐ │
│  │ 4. Provenance Engine │  │ 5. Report Formatter │  │ 6. Rechecker   │ │
│  │ (Evidence Hasher)    │  │ (9-Section Markdown)│  │ (Retest FSM)   │ │
│  └──────────────────────┘  └─────────────────────┘  └────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Module 1: Stack Detector (`core/stack_detector.py`)
- **Responsibility:** Analyzes workspace files to automatically identify active web stacks and framework ecosystems (Django, DRF, FastAPI, Flask, SQLAlchemy, Express, Next.js).
- **Interface:** `detect_stack(workspace_path: Path) -> StackProfile`

### Module 2: Rule Matcher (`core/rule_matcher.py`)
- **Responsibility:** Evaluates the active 74 `TG-*` rule definitions across 18 families against target files, filtering out exclusions (`.venv`, `node_modules`, `migrations`).
- **Interface:** `evaluate_rules(stack: StackProfile, files: list[Path]) -> list[RawSignal]`

### Module 3: Confidence Calculator (`core/confidence.py`)
- **Responsibility:** Calculates the 5-factor mathematical rubric score (0–100) and assigns confidence classification bands (`Confirmed`, `High Confidence`, `Needs Review`).
- **Interface:** `calculate_confidence(evidence: EvidencePayload) -> ConfidenceRecord`

### Module 4: Provenance & Masking Engine (`core/provenance.py`)
- **Responsibility:** Computes SHA-256 evidence hashes and redacts sensitive credentials (API keys, JWTs, passwords) before disk serialization.
- **Interface:** `package_evidence(raw_code: str) -> MaskedEvidence`

### Module 5: Human-First Report Formatter (`core/formatter.py`)
- **Responsibility:** Formats validated findings into the standardized 9-section Markdown report and renders ticket-ready payloads for issue trackers.
- **Interface:** `format_audit_report(findings: list[Finding]) -> str`

### Module 6: Retest & Recheck Engine (`core/recheck.py`)
- **Responsibility:** Performs post-fix differential analysis, asserting whether a vulnerability has transitioned to `Verified Fixed` without introducing secondary regressions.
- **Interface:** `verify_patch(finding_id: str, original_hash: str) -> RetestRecord`

### Module 7: Governed Remediation & Ponytail Engine (`scripts/ponytail_remediation.py`)
- **Responsibility:** Packages 4-artifact remediation bundles conforming strictly to Ponytail churn bounds ($\le 35$ additions, $\le 25$ deletions) with pre-apply rollback backups (`pre_apply/<file>.bak`).
- **Interface:** `formulate_remediation(finding: Finding) -> RemediationBundle`

### Module 8: Adaptive Security Memory Engine (`scripts/memory_engine.py`)
- **Responsibility:** Manages 4-tier persistent local intelligence (`memory/events/`, `patterns.json`, `context.json`, `profile.json`, `golden_recipes/`), TTL decay, and file proximity scoring.
- **Interface:** `record_event(type, data)`, `get_context_window(file_path, role)`

### Module 9: Universal Polyglot Stack Profiler & Monorepo Detector (`core/stack_profiler.py`, `scripts/monorepo_detector.py`)
- **Responsibility:** Profiles 16+ languages, 30+ frameworks, 20+ ORMs, and navigates monorepo hierarchies across npm/pnpm/yarn, Cargo, Go work, and Gradle.
- **Interface:** `profile_workspace(path: Path) -> PolyglotProfile`, `discover_monorepo(path: Path) -> MonorepoMap`

### Module 10: Content-Aware Diff Guard & Pre-Commit Hook (`scripts/diff_guard.py`)
- **Responsibility:** Audits unified diffs for language security bypasses, credential ingestion, tenant boundary removals, and regression watch violations. Installs pre-commit hooks via `--install-hook`.
- **Interface:** `audit_diff(diff_text: str) -> list[DiffViolation]`, `install_pre_commit_hook(repo_path: Path)`

### Module 11: AI IDE Rules Compiler (`scripts/rules_sync.py`)
- **Responsibility:** Compiles project security invariants, golden recipes, and active guardrails into prompt-optimized rule files for Cursor, Claude Code, Antigravity, and Windsurf ($\le 300$ token ceiling).
- **Interface:** `sync_ide_rules(workspace_path: Path, format: str)`

### Module 12: Visual Single-File HTML Reporter (`scripts/html_reporter.py`)
- **Responsibility:** Generates standalone, zero-external-CDN dark-mode visual dashboards (`.torusguard/runs/report-latest.html`) with animated SVG gauges, lifecycle state displays, and interactive diff viewers.
- **Interface:** `generate_html_report(run_dir: Path, output_path: Path)`

### Module 13: Cryptographic Manifest Engine (`scripts/manifest_builder.py`)
- **Responsibility:** Generates and verifies SHA-256 integrity digests across all 112 distribution files in `.torusguard/` and `skills/torusguard/payload/`.
- **Interface:** `generate_manifest(dir: Path) -> ManifestRecord`, `verify_manifest(dir: Path) -> bool`

### Module 14: Living Security Report Ground-Truth Engine (`scripts/report_sync.py`)
- **Responsibility:** Maintains `security_report.md` at workspace root as the single source of truth across CLI commands and AI chat sessions. Manages lifecycle transitions (`OPEN 🔴` $\rightarrow$ `VERIFIED 🟠` $\rightarrow$ `CANDIDATE 🟡` $\rightarrow$ `APPLIED 🔵` $\rightarrow$ `RESOLVED 🟢`) and dynamic 0–100 health scoring.
- **Interface:** `sync_audit_findings(findings)`, `transition_finding(id, status, metadata)`

### Module 15: Standardized 75-Column Terminal Visual Width Engine (`scripts/term_ui.py`)
- **Responsibility:** Mathematical terminal rendering engine guaranteeing strict 75 visual columns across all commands (`audit`, `harden`, `apply`, `recheck`, `status`). Strips ANSI escape sequences and accounts for wide emojis and zero-width variation selectors.
- **Interface:** `render_card(title, fields, width=75)`, `render_box(lines, width=75)`

### Module 16: Autonomous Ponytail Remediation Engine (`scripts/harden_runner.py`, `scripts/apply_runner.py`)
- **Responsibility:** Synthesizes surgical diffs bounded by $\le 35$ additions and $\le 25$ deletions across 19 vulnerability classes with byte-for-byte pre-apply snapshots in `.torusguard/snapshots/<run_id>/`.
- **Interface:** `formulate_candidate_patches(findings)`, `apply_patches_with_human_gate(bundles)`

---

## 3. Evolutionary Roadmap to v1.3.5
- **v0.5.x - v0.6.x (Completed):** File-level static analysis, Markdown reports, 64 rules, Ponytail governed remediation, line churn governance ($\le 35$ additions, $\le 25$ deletions), and multi-tenant clustering.
- **v0.7.0 (Completed):** Authorized runtime validation, bounded HTTP/browser probes, deterministic replay traces, and dual-category SARIF export.
- **v0.8.0 (Completed):** AI-agent security skill kit, 5 specialist agent roles (`profiler`, `auditor`, `validator`, `remediator`, `reviewer`), and 11 slash commands.
- **v0.9.0 - v0.9.1 (Completed):** Granular specialist skills architecture, autonomous offline bootstrapper (`bootstrap.py`), standalone CLI installer (`install.py`), and cryptographic integrity manifest (`.manifest.json`).
- **v0.9.2 (Completed):** Two-tier command-engine standard (`.torusguard/workflows/` and `.torusguard/skills/`), 70+ canonical security rules (including `TG-EDGE-*` and `TG-AGENT-*`), and zero-hallucination boundaries.
- **v1.0.0 (Completed):** Adaptive Security Memory Engine (`.torusguard/memory/`), 4-tier memory hierarchy, 90-day TTL decay, and memory-augmented confidence scoring.
- **v1.1.0 (Completed):** File/rule proximity scoring, Golden Fix Recipe learning, role-tailored context windows, and Git pre-commit hooks.
- **v1.2.0 (Completed):** AI IDE Rules Auto-Sync Engine (`rules_sync.py`) for Cursor, Claude Code, Antigravity, and Windsurf ($\le 400$ token ceiling) and visual single-file HTML posture report (`html_reporter.py`).
- **v1.3.0 (Completed):** Universal Polyglot Security Engine supporting 16+ languages, 30+ frameworks, 20+ ORMs, monorepo fleet discovery (`monorepo_detector.py`), test-path false positive suppression (`is_test_path()`), 1-command git hook installer (`diff_guard.py --install-hook`), multi-stack IDE rules deduplication ($\le 300$ tokens), polyglot HTML dashboard, and 26-repository enterprise portfolio evaluation (100.0% pass rate, 0-byte residual footprint).
- **v1.3.5 (Current Active Release Line):** Full 74-rule AST security coverage across all 18 families, Living Security Report ground truth engine (`security_report.md`) with zero hallucination, 19 Ponytail remediation patch templates, 75-column terminal visual width standard, 100/100 verified health score, and 81/81 passing harness tests.

