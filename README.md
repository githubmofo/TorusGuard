<div align="center">
  <img src="TorusGuard.png" alt="TorusGuard Banner" width="420">

  # TorusGuard

  **Security guardrails, governed remediation, and authorized runtime validation for AI-built web applications.**

  [![Release](https://img.shields.io/badge/Release-v0.7.0-blue.svg?style=flat-square)](https://github.com/githubmofo/TorusGuard/releases)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
  [![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square)](https://python.org)
  [![Validation: 100%](https://img.shields.io/badge/Validation-351%2F351%20Pass%20(100%25)-brightgreen.svg?style=flat-square)](harness/)
  [![SARIF: v2.1.0](https://img.shields.io/badge/SARIF-v2.1.0%20OASIS-purple.svg?style=flat-square)](schemas/)
</div>

---

## 💡 Executive Summary

AI coding assistants accelerate software engineering, but they frequently introduce high-risk security anti-patterns: querying databases directly from client-side bundles, exposing service-role keys, omitting tenant isolation scopes, or trusting unsanitized proxy headers.

**TorusGuard** is an open-source, Markdown-first security guidance system and verification engine. It bridges static security audits with **governed, minimal-churn remediation** and **safe, authorized runtime validation**—guaranteeing that vulnerabilities are identified, confirmed, patched, and verified without breaking codebases or deploying weaponized exploits.

### 🌐 The Core Principle: The Browser-Code Truth
> **"If the browser receives it, users can inspect it."**  
> DevTools, Inspect Element, and network breakpoints cannot be disabled. TorusGuard enforces that database credentials, sensitive business logic, and authorization boundaries must always reside on trusted server-side code.

---

## 🔄 The 7-Stage Closed-Loop Finding Lifecycle

Every candidate vulnerability transitions through an auditable, deterministic state machine:

```text
┌───────────┐     ┌────────────┐     ┌───────────┐     ┌─────────────┐     ┌──────────┐     ┌───────────┐     ┌───────────┐
│ 1. Detect │ ──► │ 2.Classify │ ──► │ 3. Verify │ ──► │ 4.Remediate │ ──► │ 5. Apply │ ──► │ 6.Recheck │ ──► │ 7.Archive │
└───────────┘     └────────────┘     └───────────┘     └─────────────┘     └──────────┘     └───────────┘     └───────────┘
```

1. **Detect (`/torusguard audit`):** Scans source code, manifests, and configurations against 64 canonical security rules.
2. **Classify:** Derives AST-invariant `FindingFingerprint` hashes and collapses repeated alerts into systemic root-cause clusters.
3. **Verify (`/torusguard web-validate` / `exploit-check`):** Executes bounded, passive HTTP/browser probes against authorized endpoints to confirm reachability.
4. **Remediate (`/torusguard harden`):** Generates self-contained 5-file Remediation Bundles with framework-idiomatic Before/After fixes.
5. **Apply (`/torusguard apply`):** Employs the **Ponytail engine** to apply surgical, minimal patches governed by strict line churn limits ($\le 35$ additions, $\le 25$ deletions).
6. **Recheck (`/torusguard recheck`):** Scopes differential re-audits strictly to modified files, asserting `Confirmed Fixed` or detecting regressions.
7. **Archive:** Preserves cryptographic SHA-256 evidence digests and exports OASIS-compliant SARIF v2.1.0 reports for GitHub Code Scanning.

---

## 🏗️ Architectural Foundations

TorusGuard is organized into three decoupled architectural tiers in `core/`:

```text
                               TORUSGUARD ENGINE (v0.7.0)
+---------------------------------------------------------------------------------------+
| TIER 3: AUTHORIZED RUNTIME VALIDATION & MULTI-AGENT GOVERNANCE                        |
|  - TargetScope & AuthorizationManager (Explicit legal consent & host/path whitelist)  |
|  - SafetyGate (Auto-Allowed GETs vs Approval Required state changes vs Manual Only)   |
|  - WebValidator & RedactionEngine (Bounded HTTP probing with Bearer/token redaction)  |
|  - ExploitChecker (Safe verification for Auth, IDOR, Header Trust, Path Traversal)    |
|  - BrowserVerifier (Client route guards & unauthenticated DOM inspection)            |
|  - RoleOrchestrator (Profiler, Validator, Remediator, Reviewer handoffs)              |
|  - ReplayManager (Deterministic JSON replay traces)                                   |
+-------------------------------------------+-------------------------------------------+
                                            | Extends & Enriches
+-------------------------------------------v-------------------------------------------+
| TIER 2: GOVERNED REMEDIATION & RESILIENT DETECTION                                    |
|  - IdentityEngine (Line-shift invariant finding fingerprints)                         |
|  - ClusteringEngine (Systemic root-cause grouping & hotspot analysis)                 |
|  - BundleManager (5-file structured remediation packaging)                            |
|  - PatchGovernor (Minimal churn limits & sensitive-path escalation)                   |
|  - TargetedRechecker (Scoped differential verification & regression alerts)           |
|  - SarifExporter (GitHub Code Scanning deduplication via primaryLocationLineHash)    |
|  - StackProfiler (Framework version families & package manager detection)             |
+-------------------------------------------+-------------------------------------------+
                                            | Builds Upon
+-------------------------------------------v-------------------------------------------+
| TIER 1: CANONICAL MODELS, LIFECYCLE & PROVENANCE                                      |
|  - Finding, Evidence, Remediation data models (16 JSON schemas)                       |
|  - FindingLifecycleManager (Deterministic 7-stage state machine)                      |
|  - ReportFormatter (Human-First card layout & sensitive secret masking)              |
+---------------------------------------------------------------------------------------+
```

---

## 🚀 Quick Start

### 1. Installation into AI Agents
Install TorusGuard into Cursor, Antigravity, Claude Code, Cline, Codex, or Gemini CLI using the open `skills` CLI:

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```

### 2. Core Workflow Commands

| Command | Role / Phase | Purpose | Modifies Code? |
|---|:---:|---|:---:|
| `/torusguard init` | Setup | Generates a project `SECURITY.md`, threat model, and baseline. | ❌ Docs only |
| `/torusguard audit` | Profiler / Detect | Scans codebase, generates stable IDs, and clusters findings. | ❌ No |
| `/torusguard authorize` | Safety Gate | Enforces target ownership proof and strict scope allowlists. | ❌ No |
| `/torusguard web-validate` | Validator | Bounded HTTP probing and session tracking with secret redaction. | ❌ No |
| `/torusguard exploit-check`| Validator | Safe, single-step exploitability confirmation across 5 statuses. | ❌ No |
| `/torusguard harden` | Remediator | Emits 5-file remediation bundles and surgical patch plans. | ❌ No |
| `/torusguard apply` | Remediator | Applies bounded, governed patches ($\le 35$ additions, $\le 25$ deletions). | ⚠️ Yes (Governed) |
| `/torusguard recheck` | Reviewer | Differentially audits modified files to verify fixes and catch regressions. | ❌ No |

---

## 📂 Run Folder System (`RunManager`)

Every execution is completely self-contained within an isolated directory (`runs/<run-id>/`):

```text
runs/run-20260901-113000/
├── manifest.json            # Execution metadata, git commit hash, and summary counts
├── summary.md               # Executive summary and root-cause cluster matrix
├── findings.md              # Detailed finding cards with code excerpts and remediation
├── web-validation.md        # HTTP interaction log and endpoint status codes
├── requests.json            # Redacted request payloads (tokens/passwords masked)
├── responses.json           # Redacted response payloads
├── session-notes.md         # Active session cookies and tenant context
├── replay.json              # Deterministic replay trace for regression verification
├── sarif.json               # OASIS SARIF v2.1.0 export for CI/CD & GitHub Code Scanning
└── logs/                    # Execution telemetry and safety gate audit log
```

---

## 🛡️ Supported Stacks & Frameworks

### 🐍 Python Ecosystem
- **[Django Guide](guides/python/django.md):** Settings, CSRF, ORM queries, ModelForms, object ownership, and async coroutines (`aget()`).
- **[Django REST Framework Guide](guides/python/django-rest-framework.md):** Default permissions, ViewSets, serializers, throttles, and pagination.
- **[FastAPI Guide](guides/python/fastapi.md):** Pydantic v2 schemas, `Annotated` dependency injection, SSRF boundaries, and HMAC webhooks.
- **[Flask Guide](guides/python/flask.md):** Factory patterns, secure session cookies, `CSRFProtect`, and path traversal storage limits.
- **[SQLAlchemy Guide](guides/python/sqlalchemy.md):** Bound query parameters, 2.0 `select()` statements, and multi-tenant isolation.
- **[Python Dependencies & CI/CD](guides/python/python-dependencies.md):** Deterministic lockfiles (`uv`, Poetry, pip-tools), `pip-audit`, and GitHub Actions SHA pinning.

### 🌐 JavaScript & TypeScript Ecosystem
- **[React + Vite Guide](guides/react-vite-security.md):** Frontend env variable boundaries, build artifact leakage, and source maps.
- **[Next.js Guide](guides/nextjs-security.md):** App Router / Pages Router security, Server Components, and Next.js 14 Server Action authorization (`"use server"`).
- **[Supabase Guide](guides/supabase-security.md):** Row-Level Security (RLS), service-role key isolation, and secure client queries.
- **[Firebase Guide](guides/firebase-security.md):** Firestore Security Rules, client SDK boundaries, and privileged admin tasks.

---

## 📋 Project Documentation & Governance

| Document | Purpose |
|---|---|
| 🛡️ **[Security Philosophy](docs/overview/security-philosophy.md)** | Strict legal authorization, non-destructive probing, and safety review gates |
| 🧪 **[Testing Playbook](docs/usage/testing-playbook.md)** | Step-by-step verification guide using internal fixtures and OWASP Juice Shop |
| 🗺️ **[Development Roadmap](ROADMAP_v0_7_1.md)** | Prioritized v0.7.1+ backlog (`TG-AGENT-*`, diff line scanning, GraphQL/WebSockets) |
| 👥 **[Maintainer Guide](MAINTAINERS.md)** | Maintainer security hygiene, mandatory MFA, branch protection, and release signing |
| 🔄 **[Refactoring Notes](REFACTORING_NOTES_v0_7.md)** | Structural refactoring log, module decomposition, and merge verification |

---

## 🚫 What TorusGuard Deliberately Is Not

To maintain technical honesty and safety:
- **Not a weaponized offensive pentest tool:** TorusGuard strictly avoids brute-forcing, denial-of-service, memory corruption, and autonomous lateral movement.
- **Not an unbounded vulnerability scanner:** Probes are bounded, single-step assertions against authorized endpoints with strict request budgets.
- **Not client-side DRM:** Browser-delivered JavaScript cannot be hidden from DevTools; security must reside on the backend.
- **Not an "unhackable" guarantee:** Security is continuous; TorusGuard provides structured guardrails, not absolute immunity.

---

## 👥 Author & Community

- **Creator & Lead Maintainer:** **Jenish Lad** ([@githubmofo](https://github.com/githubmofo))
- **Contributing:** Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening a pull request.
- **Security Inquiries:** Please follow our [Security Policy](SECURITY.md) for private vulnerability reporting.
- **License:** Open source under the [MIT License](LICENSE).
