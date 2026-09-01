# TorusGuard Issue Registry & Tracking Log

This document provides a transparent, centralized record of **fixed historical defects**, **resolved false alarms**, and **current known limitations / open issues** in TorusGuard v0.7.0.

---

## 🎯 Current Known Issues & Limitations (v0.7.0)

The following items are tracked in [`ROADMAP_v0_7_1.md`](ROADMAP_v0_7_1.md) for incremental resolution:

### 1. PatchGovernor Diff Content Keyword Escalation
- **Status:** Open (Tracked for `v0.7.1`)
- **Severity:** Low / Governance
- **Description:** `PatchGovernor.evaluate_patch()` inspects file path strings for sensitive keywords (`auth`, `tenant`, `token`, `secret`) to trigger `Mandatory Security Sign-Off`. If a diff modifies a generic file path (e.g., `apps/core/views.py`) and introduces auth logic changes (`new_auth()`), keyword escalation is not triggered automatically unless manually flagged.
- **Workaround:** Configure `strict_high_risk_escalation=True` or explicitly flag sensitive review files in PR configurations.
- **Target Resolution:** v0.7.1 will parse added diff lines (`+`) for domain keywords.

### 2. Protocol Boundaries: GraphQL & WebSocket Runtime Probes
- **Status:** Open (Tracked for `v0.7.2`)
- **Severity:** Low / Coverage
- **Description:** Runtime exploitability confirmation (`/torusguard exploit-check`) currently targets HTTP REST APIs. Rules `TG-GQL-*` and `TG-WS-*` provide static detection and remediation guidance, but lack automated bounded network probes.
- **Workaround:** Use static audit results and verify GraphQL complexity or WebSocket auth using manual curl/wscat verification commands provided in rule files.
- **Target Resolution:** v0.7.2 introduces GraphQL query complexity and WebSocket handshake runtime probes.

### 3. Container Build-Chain Multi-Stage Analysis
- **Status:** Open (Tracked for `v0.7.2`)
- **Severity:** Low / Coverage
- **Description:** Dockerfile security analysis inspects single-stage Dockerfile directives for root user execution and hardcoded secrets. It does not trace intermediate build-stage secret propagation across multi-stage `COPY --from` layers.
- **Workaround:** Combine TorusGuard with specialized container scanners (e.g., Trivy or Docker Scout).
- **Target Resolution:** v0.7.2 will model multi-stage build cache persistence.

### 4. Agentic AI & MCP Permission Scoping
- **Status:** Open (Tracked for `v0.7.1` / `v0.8.0`)
- **Severity:** Medium / Emerging Surface
- **Description:** Agentic repositories (such as Hermes Agent, AutoPentest-AI, or MCP servers) feature novel attack surfaces (prompt injection in project files, overly broad tool execution, persistent session leakage) not covered by traditional web application rule families.
- **Target Resolution:** v0.7.1 introduces the dedicated `TG-AGENT-*` rule family (`TG-AGENT-001` through `TG-AGENT-004`).

---

## 🛠️ Resolved & Fixed Issues (Historical & Recent Releases)

### Fixed in v0.7.0
- **High-Complexity Monolithic Controllers:** Refactored 5 high-complexity engine functions across `core/authorization.py`, `core/governance.py`, `core/sarif.py`, `core/runtime_validator.py`, and `core/v070_workflow.py` into modular, single-responsibility helpers with zero regressions.
- **Public API Coverage Gap:** Restructured `core/__init__.py` into 3 explicit architectural tiers and expanded `__all__` from 38 symbols to 58 public classes and enums.
- **Uncontrolled Probing Risk:** Enforced hard legal authorization checks (`core/authorization.py`) preventing any HTTP request without an active, unexpired `scope.json` manifest.
- **Multi-Analysis SARIF Overwrites:** Implemented `automationDetails.id: torusguard/runtime/` to partition static and runtime alerts, preventing SARIF overwrite collisions in GitHub Code Scanning.

### Fixed in v0.6.3
- **Finding ID Line-Shift Drift:** Resolved finding identity drift when developers add comments or refactor non-security code by deriving stable `FindingFingerprint` from AST sink signatures rather than raw line numbers.
- **GitHub SARIF Deduplication:** Added `partialFingerprints.primaryLocationLineHash` to comply strictly with GitHub Code Scanning deduplication standards, eliminating duplicate alerts across PR commits.
- **Modern Framework False Positives:** Fixed false positives on safe Django 5.x async coroutines, FastAPI `Annotated` dependencies, SQLAlchemy 2.0 chained `select()`, and Next.js 14 Server Actions.

### Fixed in v0.6.1
- **Monorepo Directory Collisions:** Fixed truncation bugs when resolving 8-level deeply nested paths across polyglot multi-app repositories (Django + FastAPI + Flask + Shared ORM).
- **Vendor/Build Artifact Noise:** Added automatic path suppression for `migrations/`, `dist/`, `build/`, `*.min.js`, and `*.pb.go`.
- **Markdown Report Bloat:** Added automatic `<details>` collapsing when finding count exceeds 25 items, preventing unreadable multi-megabyte audit reports.

### Fixed in v0.5.6
- **False Alarms on Framework Utilities:** Hardened context-aware AST matching for `TG-AUTH-008`, `TG-INPUT-005`, `TG-INPUT-006`, and `TG-DB-004` to eliminate false alarms on standard framework helper calls.

### Fixed in v0.5.4
- **Credential Exposure in Evidence Logs:** Implemented automated regex masking (`mask_sensitive_data`) in evidence collectors to redact live Stripe keys (`sk_live_...`), GitHub tokens, JWTs, and passwords before persisting logs.

### Fixed in v0.5.1
- **Subjective Confidence Scoring:** Replaced arbitrary confidence percentages with an objective 5-factor mathematical rubric (Evidence Quality 35 pts, Reproduction 25 pts, Confirmations 15 pts, Environment 15 pts, Review 10 pts).
- **Evidence Tampering Risk:** Added cryptographic SHA-256 integrity checksums to raw code excerpts.

### Fixed in v0.4.1
- **Service-Layer Auth False Positives (`TG-AUTH-007`):** Corrected rule logic to route controllers delegating auth to domain service layers to `Needs Review` (< 50 pts) instead of falsely confirming IDOR.
- **SQLAlchemy Parameter Binding (`TG-INPUT-002`):** Corrected false alarms on bound `LIKE` queries using parameter dictionaries.

---

## 📢 Reporting New Issues

To submit an issue or report a bug:
- **Bug Reports:** [Open a Bug Report](https://github.com/githubmofo/TorusGuard/issues/new?template=bug_report.md)
- **False Positives:** [Open a False Positive Report](https://github.com/githubmofo/TorusGuard/issues/new?template=false_positive.md)
- **Rule Proposals:** [Submit a Security Rule Proposal](https://github.com/githubmofo/TorusGuard/issues/new?template=rule_proposal.md)
- **Security Vulnerabilities in TorusGuard:** Report privately via [GitHub Security Advisories](https://github.com/githubmofo/TorusGuard/security/advisories/new) per [`SECURITY.md`](SECURITY.md).
