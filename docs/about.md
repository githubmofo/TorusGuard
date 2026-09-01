# About TorusGuard

**TorusGuard** is an open-source, Markdown-first security guidance framework and authorized runtime verification system built specifically for modern web application developers, security engineers, and AI coding agents.

---

## 🌟 Mission & Vision

As generative AI accelerates software engineering, AI coding assistants are generating vast quantities of web application code at unprecedented velocity. However, AI code generators frequently introduce critical security anti-patterns:
- Querying databases directly from frontend client code.
- Exposing private API secrets and service-role keys in browser bundles.
- Omitting multi-tenant scoping predicates (`organization_id`, `tenant_id`) in database queries.
- Creating unprotected routes susceptible to IDOR and mass assignment.
- Fetching user-controlled URLs without SSRF safeguards.

**TorusGuard's mission** is to provide AI agents and human engineers with the structured context, strict guardrails, and deterministic verification workflows needed to catch, govern, and fix vulnerabilities before production deployment.

---

## 💡 The Core Principle: The Browser-Code Truth

> **"If the browser receives it, users can inspect it."**

DevTools, network tabs, breakpoints, and client-side debuggers cannot be blocked. Client-side validation is merely UX, not security. TorusGuard enforces that database credentials, sensitive business calculations, authorization checks, and tenant isolation decisions must always reside on trusted server-side code.

---

## 🏗️ Architectural Foundations

TorusGuard operates across three distinct architectural tiers:

### Tier 1: Canonical Data Models, Lifecycle & Provenance (v0.5 base)
- **7-Stage Closed-Loop Finding Lifecycle:** `Detect` ➔ `Classify` ➔ `Verify` ➔ `Remediate` ➔ `Apply` ➔ `Recheck` ➔ `Archive`.
- **Formal Schemas (`schemas/`):** 16 strict JSON schemas standardizing findings, evidence, remediations, rules, lifecycles, and replay traces.
- **Auditable 0–100 Confidence Rubric:** Mathematical scoring based on Evidence Quality (35 pts), Reproduction (25 pts), Confirmations (15 pts), Environment (15 pts), and Review (10 pts).
- **Cryptographic Evidence Packaging:** Immutable SHA-256 checksums computed on raw code excerpts to guarantee tamper-proof audit trails.

### Tier 2: Governed Remediation & Resilient Detection (v0.6 engine)
- **Isolated Run Folders (`RunManager`):** Every audit operates inside a self-contained execution directory (`runs/<run-id>/`) containing all audit ledgers and SARIF exports.
- **Line-Shift Invariant Fingerprints (`IdentityEngine`):** Finding identities derived from AST sink signatures that survive whitespace and comment refactorings.
- **Root-Cause Clustering (`ClusteringEngine`):** Groups repeated findings into systemic root-cause clusters to prevent developer notification fatigue.
- **Minimal Patch Governance (`PatchGovernor`):** Strictly constrains automated code edits ($\le 35$ additions, $\le 25$ deletions per file) and blocks sweeping boilerplate rewrites.
- **Targeted Recheck Verification (`TargetedRechecker`):** Differential re-audits scoped strictly to modified files, asserting `Confirmed Fixed` or detecting `Regressed` code.
- **SARIF v2.1.0 & GitHub Code Scanning:** Built-in deduplication fingerprints (`primaryLocationLineHash`) eliminating duplicate alert noise across PR commits.

### Tier 3: Authorized Runtime Validation & Multi-Agent Roles (v0.7 engine)
- **Target Authorization Gate (`AuthorizationManager`):** Enforces explicit written consent, target ownership proof, whitelisted hosts, and request quotas before any network query is permitted.
- **Tiered Safety Review Gates (`SafetyGate`):** Enforces `Auto-Allowed`, `Approval Required`, and `Manual Only` boundaries, permanently blocking destructive endpoints (`/admin/delete`, `/system/shutdown`).
- **Bounded Exploitability Confirmation (`ExploitChecker`):** Safe, single-step verification probes evaluating Auth Bypass, IDOR, Header Trust, Path Traversal, and Debug Exposure across 5 honest statuses (`Runtime Confirmed`, `Runtime Likely`, `Needs Manual Review`, `Not Reproducible in Scope`, `Blocked by Controls`).
- **4-Role Multi-Agent Workflow (`RoleOrchestrator`):** Formally separates responsibilities between Profiler, Validator, Remediator, and Reviewer roles.
- **Deterministic Replay Traces (`ReplayManager`):** Serializes verification sequences into replayable, scope-enforced traces (`replay.json`).

---

## 🚫 What TorusGuard Deliberately Is Not

To maintain technical honesty, clarity, and safety:
1. **Not a Weaponized Offensive Pentest Agent:** TorusGuard strictly avoids brute forcing, denial of service, memory corruption, and autonomous lateral movement.
2. **Not an Unbounded Binary Scanner:** It does not disassemble compiled binaries or execute arbitrary network port scans.
3. **Not Client-Side DRM:** Browser-delivered JavaScript cannot be hidden from DevTools; security must reside on the backend.
4. **Not an "Unhackable" Guarantee:** Security is continuous; TorusGuard provides structured guardrails, not absolute immunity.

---

## 👥 Author & Governance

- **Creator & Project Lead:** Jenish Lad ([@githubmofo](https://github.com/githubmofo))
- **Maintainer Hygiene:** Strict branch protection, mandatory hardware MFA, zero committed secrets, and reproducible lockfiles detailed in [`MAINTAINERS.md`](../MAINTAINERS.md).
- **Security & Responsible Disclosure:** Coordinated private vulnerability reporting detailed in [`SECURITY.md`](../SECURITY.md).
- **Issue Tracking & Roadmap:** Transparent defect tracking in [`KNOWN_ISSUES.md`](../KNOWN_ISSUES.md) and development milestones in [`ROADMAP_v0_7_1.md`](../ROADMAP_v0_7_1.md).
- **License:** Open source under the [MIT License](../LICENSE).
