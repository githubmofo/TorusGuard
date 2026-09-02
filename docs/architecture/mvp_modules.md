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
- **Responsibility:** Evaluates the active 64+ `TG-*` rule definitions against target files, filtering out exclusions (`.venv`, `node_modules`, `migrations`).
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

---

## 3. Evolutionary Roadmap to v1.0.0
- **v0.5.x - v0.6.x (Completed):** File-level static analysis, Markdown reports, 64 rules, Ponytail governed remediation, line churn governance ($\le 35$ additions, $\le 25$ deletions), and multi-tenant clustering.
- **v0.7.0 (Completed):** Authorized runtime validation, bounded HTTP/browser probes, deterministic replay traces, and dual-category SARIF export.
- **v0.8.0 (Completed):** AI-agent security skill kit, 5 specialist agent roles (`profiler`, `auditor`, `validator`, `remediator`, `reviewer`), and 11 slash commands.
- **v0.9.0 - v0.9.1 (Completed):** Granular specialist skills architecture, autonomous offline bootstrapper (`bootstrap.py`), standalone CLI installer (`install.py`), and cryptographic integrity manifest (`.manifest.json`).
- **v0.9.2 (Current):** Two-tier command-engine standard (`.torusguard/workflows/` and `.torusguard/skills/`), 70+ canonical security rules (including `TG-EDGE-*` and `TG-AGENT-*`), and zero-hallucination boundaries.
- **v1.0.0 (Target):** Polyglot language server protocol (LSP) integration, automated GitHub PR review actions, and continuous real-time background validation.
