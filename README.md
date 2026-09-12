<div align="center">
  <img src="TorusGuard.png" alt="TorusGuard Autonomous Security Engine Banner" width="560" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">

  # TorusGuard

  ### Autonomous Security Guardrails, Governed Remediation & Living Verification for AI-Built Applications

  <p align="center">
    <strong>Zero Telemetry · Zero External Python Dependencies · Pure Standard-Library Architecture · 100% Local-First</strong>
  </p>

  [![npm version](https://img.shields.io/badge/npm-v1.3.5-cb3837.svg?style=flat-square&logo=npm)](https://www.npmjs.com/package/torusguard)
  [![GitHub Packages](https://img.shields.io/badge/GitHub%20Packages-v1.3.5-181717.svg?style=flat-square&logo=github)](https://github.com/githubmofo/TorusGuard/pkgs/npm/torusguard)
  [![Release](https://img.shields.io/badge/Release-v1.3.5-blue.svg?style=flat-square)](https://github.com/githubmofo/TorusGuard/releases/latest)
  [![Tests](https://img.shields.io/badge/Tests-81%2F81%20Passing-brightgreen.svg?style=flat-square)](harness/runner.py)
  [![Security Health](https://img.shields.io/badge/Health%20Score-100%2F100%20Hardened-brightgreen.svg?style=flat-square)](security_report.md)
  [![Rules Catalog](https://img.shields.io/badge/Rules%20Catalog-74%20Rules%20%7C%2018%20Families-indigo.svg?style=flat-square)](rules/)
  [![Terminal Standard](https://img.shields.io/badge/Terminal-75--col%20Standard-informational.svg?style=flat-square)](.torusguard/scripts/term_ui.py)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
  [![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B%20(Zero%20Deps)-blue.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
  [![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-339933.svg?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org)
  [![SARIF: v2.1.0](https://img.shields.io/badge/SARIF-v2.1.0%20OASIS-purple.svg?style=flat-square)](.torusguard/schemas/)
  [![OWASP: Top 10](https://img.shields.io/badge/OWASP-Top%2010%20Aligned-orange.svg?style=flat-square)](docs/architecture/SECURITY_ARCHITECTURE.md)
  [![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local%20Zero--Egress-success.svg?style=flat-square)](docs/overview/security-philosophy.md)
</div>

---

> ### 🛡️ The Architecture Behind the Emblem
> In the emblem above, the **central golden keyhole shield** represents unbreakable secret protection and authentication integrity. It is enveloped by a continuous, interlocking **torus ring**—symbolizing TorusGuard's closed-loop autonomous security lifecycle:
>
> $$\mathbf{Detect} \;\longrightarrow\; \mathbf{Verify} \;\longrightarrow\; \mathbf{Harden} \;\longrightarrow\; \mathbf{Apply} \;\longrightarrow\; \mathbf{Recheck} \;\longrightarrow\; \mathbf{Memory}$$
>
> AI coding assistants (Cursor, Claude Code, Copilot, Windsurf) build software at superhuman speed, but routinely leak private keys into client bundles, drop tenant partition filters, or inject raw user input into LLM system prompts.
> 
> **TorusGuard forms an unbroken local guardrail around your codebase.** It audits static ASTs, runtime-verifies exploitability with inert canaries, synthesizes minimal surgical diffs adhering to the **Ponytail Protocol** ($\le 35$ additions, $\le 25$ deletions), and eliminates hallucinations by maintaining a verifiable single source of truth in `security_report.md`.

---

## 📑 Table of Contents

1. [Developer Overview & Value Proposition](#-developer-overview--value-proposition)
2. [Why TorusGuard? (Traditional SAST vs. AI Coding vs. TorusGuard)](#-why-torusguard)
3. [Installation & Setup Guide (npm & CLI)](#-installation--setup-guide-npm--cli)
4. [Quickstart: The 5-Step Core Lifecycle](#-quickstart-the-5-step-core-lifecycle)
5. [Dual-Strategy Command Matrix (CLI & AI Chat Parity)](#-dual-strategy-command-matrix-cli--ai-chat-parity)
6. [74 Canonical Security Rules Catalog (18 Families Across 6 Pillars)](#-74-canonical-security-rules-catalog-18-families-across-6-pillars)
7. [Ponytail Remediation Protocol & Rollback Safety](#-ponytail-remediation-protocol--rollback-safety)
8. [Living Security Report Ground Truth (`security_report.md`)](#-living-security-report-ground-truth-security_reportmd)
9. [Visual HTML Dashboard & SARIF v2.1.0 Export](#-visual-html-dashboard--sarif-v210-export)
10. [AI Editor Guardrails Auto-Sync](#-ai-editor-guardrails-auto-sync)
11. [Monorepo Fleet Support & Git Pre-Commit Diff Guard](#-monorepo-fleet-support--git-pre-commit-diff-guard)
12. [Verification & Test Harness (81/81 Passing Harness Explained)](#-verification--test-harness)
13. [Security Policy & Responsible Disclosure](#-security-policy--responsible-disclosure)
14. [License](#-license)

---

## 💡 Developer Overview & Value Proposition

When developers use AI coding agents to write features, models optimize for *getting the code to run* rather than *defensive architecture*. Common failure modes include:
- **Exposing Private Credentials:** Leaking `process.env.SUPABASE_SERVICE_ROLE_KEY` or master database connection strings into Next.js `'use client'` bundles.
- **Dropping Tenant Boundaries:** Querying Prisma or Mongoose by record ID without scoping by tenant (`where: { id }` instead of `where: { id, tenantId }`).
- **Prompt Injection Vulnerabilities:** Interpolating untrusted user chat messages directly into system prompts.
- **Destructive AI Rewrites:** When asked to fix a minor bug, AI models rewrite entire 500-line files, introducing fresh regressions and breaking surrounding business logic.

**TorusGuard solves this deterministically:**
- **Zero-Egress Local Execution:** 100% of scanning and patching happens on your machine. Zero code or tokens are transmitted to external servers.
- **Zero Pip Dependencies:** Pure Python standard library (`pathlib`, `re`, `json`, `difflib`, `shutil`). No virtualenv conflicts or broken build wheels.
- **Ponytail Churn Bounds:** Patches are constrained strictly to $\le 35$ additions and $\le 25$ deletions. Surrounding business logic is never rewritten.
- **Human Gate & Instant Undo:** Every change requires interactive approval with syntax-highlighted diffs, backed up byte-for-byte in `.torusguard/snapshots/` with instant 1-command rollback.

### 🌐 The Browser-Code Truth Invariant
> **"If the browser receives it, users can inspect it via DevTools."**  
> Frontend environment variables, client JavaScript bundles, and React Server Action payloads cannot conceal secrets. TorusGuard strictly enforces that database credentials, service role keys, private API secrets, and tenant boundaries remain exclusively on trusted server runtimes.

---

## ⚔️ Why TorusGuard?

| Security Dimension | Traditional SAST (SonarQube, Snyk) | Raw AI Coding Agents | TorusGuard v1.3.5 Engine |
|:---|:---:|:---:|:---:|
| **Target Architecture** | Human-written legacy codebases | High-churn AI code generation | **AI-built full-stack applications** |
| **Remediation Model** | PDF reports & Jira tickets | Destructive full-file rewrites | **Ponytail Protocol** ($\le 35$ add, $\le 25$ del) |
| **Fix Preservation** | None (scans from scratch) | Forgets context across chats | **Adaptive Security Memory** & Golden Recipes |
| **Editor Sync** | Heavy background language daemons | Bloated prompt context ($> 2,000$ tokens) | **Stack-Adaptive Rules** ($\le 300$ prompt tokens) |
| **Ground-Truth State** | External proprietary web dashboard | Ephemeral chat context (hallucinates) | **Living Security Ledger** (`security_report.md`) |
| **Pre-Commit Defense** | Slow server-side webhooks | None (commits insecure code) | **Git Pre-Commit Diff Guard** ($< 200\text{ ms}$) |
| **Privacy & Telemetry** | Cloud code upload / SaaS | Third-party cloud LLMs | **100% Local, Zero-Egress Guarantee** |

---

## 📦 Installation & Setup Guide (npm & CLI)

TorusGuard is designed to be effortless to adopt in any project. There are no configuration servers, databases, or complex background daemons.

### 📋 Prerequisites
- **Node.js:** 18.0.0 or higher
- **Python:** 3.10 or higher (**Pure standard library** — **zero `pip` dependencies required**)

> [!IMPORTANT]
> **Zero Pip Dependencies Guarantee:** TorusGuard's core Python engine relies strictly on the Python standard library (`pathlib`, `re`, `json`, `difflib`, `shutil`, `sys`, `os`, `argparse`, `hashlib`). You **never** need to create a Python virtualenv (`venv`), run `pip install`, or configure external wheels. It works out of the box with your system Python.

---

### 1. Zero-Install Runner (Recommended)
Run TorusGuard instantly in any repository without installing anything globally:

```bash
# Run any command directly via npx
npx torusguard init
npx torusguard audit
npx torusguard status
```

### 2. Project Dev Dependency
Lock TorusGuard into your project's `package.json` for all team members and CI/CD pipelines:

```bash
npm install -D torusguard
```

Add convenience scripts to your `package.json`:
```json
{
  "scripts": {
    "security:audit": "torusguard audit",
    "security:harden": "torusguard harden",
    "security:recheck": "torusguard recheck",
    "security:status": "torusguard status"
  }
}
```

### 3. Global Installation
If you prefer having the `torusguard` binary available system-wide across all terminal sessions:

```bash
npm install -g torusguard
```

### 4. AI Agent Skill Installation
Install TorusGuard as a native AI assistant skill for Cursor, Claude Code, Cline, or Antigravity:

```bash
npx skills add torusguard
```

---

### 🔍 What Happens on First Run (`init`)
When you execute `npx torusguard init` in your repository:
1. **Polyglot Profiling:** Automatically detects 16+ languages (Go, Rust, Java, C#, PHP, Python, TypeScript) and 30+ frameworks without manual configuration.
2. **Scaffolding:** Creates a local `.torusguard/` directory containing active security rules, schemas, and runners.
3. **Editor Rules Synchronization:** Automatically compiles compact, language-specific guardrails into `.cursorrules`, `CLAUDE.md`, `.agent/rules/torusguard.md`, and `.windsurfrules` ($\le 300$ prompt tokens).
4. **Living Ledger Initialization:** Creates `security_report.md` at workspace root to track finding states without hallucination.
5. **Baseline Policy:** Emits a production-ready `SECURITY.md` for responsible disclosure.

---

## ⚡ Quickstart: The 5-Step Core Lifecycle

Run the complete autonomous governance cycle in 60 seconds from your terminal:

```bash
# Step 1: Initialize workspace and profile stack
npx torusguard init

# Step 2: Run AST static security audit across 74 rules
npx torusguard audit

# Step 3: Synthesize minimal surgical candidate patches
npx torusguard harden

# Step 4: Review syntax-highlighted diffs and apply with rollback backup
npx torusguard apply

# Step 5: Differentially recheck modified files to verify fix closure
npx torusguard recheck
```

> 💡 **Prefer AI Chat?** Every step above can be triggered directly in your AI assistant chat using `/torusguard init`, `/torusguard audit`, `/torusguard harden`, `/torusguard apply`, and `/torusguard recheck`!

---

## ⌨️ Dual-Strategy Command Matrix (CLI & AI Chat Parity)

TorusGuard guarantees **100% operational parity** between terminal CLI execution and AI chat slash commands. Terminal outputs strictly adhere to a **75-column visual width** with Unicode emojis and ANSI stripping.

### 🔄 Core Remediation Lifecycle

| Lifecycle Stage | Mode A: Terminal CLI | Mode B: AI Chat Command | Governed Action & Primary Artifact |
|:---|:---|:---|:---|
| **1. Init** | `npx torusguard init` | `/torusguard init` | Profiles workspace, activates rules, initializes `.torusguard/` |
| **2. Audit** | `npx torusguard audit` | `/torusguard audit` | 74-rule AST scan, line-shift fingerprints, updates `security_report.md` |
| **3. Harden** | `npx torusguard harden` | `/torusguard harden` | Synthesizes Ponytail diffs ($\le 35$ add, $\le 25$ del) into candidate bundles |
| **4. Apply** | `npx torusguard apply [--yes]` | `/torusguard apply` | Human Gate, pre-apply `.bak` snapshots, Golden Fix distillation |
| **5. Rollback**| `npx torusguard rollback` | `/torusguard rollback` | Instant restoration from pre-apply snapshots in `.torusguard/snapshots/` |
| **6. Recheck** | `npx torusguard recheck` | `/torusguard recheck` | Differential AST re-scan; marks findings `RESOLVED 🟢` in living report |

### 📊 Intelligence, Memory & Reporting

| Capability | Mode A: Terminal CLI | Mode B: AI Chat Command | Governed Action & Primary Artifact |
|:---|:---|:---|:---|
| **Status** | `npx torusguard status` | `/torusguard status` | 75-column diagnostic overview of health score, stack, memory & rules |
| **Recipes** | `npx torusguard recipes` | `/torusguard recipes` | Explores verified Golden Fix patterns stored in `.torusguard/memory/` |
| **Report** | `npx torusguard report --html` | `/torusguard report` | Emits single-file dark-mode HTML posture report & OASIS SARIF v2.1.0 |
| **Rules Sync**| `npx torusguard rules sync` | `/torusguard rules sync`| Synchronizes prompt guardrails across Cursor, Claude, Antigravity, Windsurf |
| **Diff Guard**| `npx torusguard diff-guard` | `/torusguard diff-guard`| Audits git diffs for security bypasses; `--install-hook` binds pre-commit |

### 🧪 Runtime Verification & Bounded Probing

| Capability | Mode A: Terminal CLI | Mode B: AI Chat Command | Governed Action & Primary Artifact |
|:---|:---|:---|:---|
| **Authorize** | `npx torusguard authorize` | `/torusguard authorize` | Target domain allowlisting, cryptographic ownership proof, TTL limits |
| **Verify** | `npx torusguard verify` | `/torusguard verify` | Asserts evidence sufficiency & live disk line-shift fingerprint matches |
| **Validate** | `npx torusguard web-validate` | `/torusguard web-validate`| Authorized non-destructive HTTP probing with transparent audit headers |
| **Exploit** | `npx torusguard exploit-check`| `/torusguard exploit-check`| Bounded single-step exploitability confirmation using inert sentinels |

---

## 📋 74 Canonical Security Rules Catalog (18 Families Across 6 Pillars)

TorusGuard's AST scanner inspects polyglot source trees across 74 canonical security rules organized into **6 core security pillars** across 18 families:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    74 CANONICAL RULES ACROSS 6 PILLARS                      │
└─────────────────────────────────────────────────────────────────────────────┘
  1. Secrets & Identity       ──► TG-SEC (7)  · TG-AUTH (8) · TG-CLIENT (2)
  2. Data & Injection Defense ──► TG-DB (4)   · TG-INPUT (6) · TG-CSRF (2)
  3. AI Agent & LLM Security  ──► TG-AGENT (4)
  4. Network & Real-Time      ──► TG-SSRF (4) · TG-WEBHOOK (4) · TG-WS (4)
  5. Platform & API Limits    ──► TG-RATE (3) · TG-GQL (4) · TG-PLATFORM (4)
                                  TG-CACHE (3) · TG-EDGE (2)
  6. Supply Chain & Governance──► TG-SUPPLY (6) · TG-BIZ (4) · TG-DIFF (3)
```

| Pillar | Family Prefix | Rules | Critical Invariant Enforced |
|:---|:---|:---:|:---|
| **🔑 Secrets & Client Bundles** | `TG-SEC`, `TG-CLIENT` | **9** | Zero hardcoded API keys, JWT secrets, private certificates, or server keys in client bundles. |
| **🛡️ Authentication & Sessions** | `TG-AUTH`, `TG-CSRF` | **10** | Timing-safe string compares, strong password hashing, algorithm verification, SameSite cookies. |
| **🗄️ Database & Input Safety** | `TG-DB`, `TG-INPUT` | **10** | Parameterized SQL queries, multi-tenant isolation (`where: { tenantId }`), path sanitization. |
| **🤖 AI Agent & LLM Guardrails** | `TG-AGENT` | **4** | Structural user prompt isolation, delimiter wrapping, shell tool sandboxing, MCP least-privilege. |
| **🌐 Network, Webhooks & WS** | `TG-SSRF`, `TG-WEBHOOK`, `TG-WS` | **12** | Private IP range blocking (`169.254.169.254`), HMAC-SHA256 signature checks, WS origin validation. |
| **⚡ Platform, Edge & Governance** | `TG-RATE`, `TG-GQL`, `TG-PLATFORM`, `TG-CACHE`, `TG-EDGE`, `TG-SUPPLY`, `TG-BIZ`, `TG-DIFF` | **29** | Auth rate limiting, GraphQL depth bounds, Helmet headers, lockfile integrity, zero `# nosec` bypasses. |

<details>
<summary><strong>🔍 Click to expand full 18-family catalog breakdown</strong></summary>

<br>

- **`TG-SEC` (Secrets & API Tokens — 7 rules):** Detects hardcoded JWT secrets, private certificates, cloud API keys, environment variable leakage, and secrets in URL queries or logs.
- **`TG-AUTH` (Authentication & Access Control — 8 rules):** Enforces constant-time string comparisons, strong password hashing (`bcrypt`/`argon2`), JWT algorithm pinning, mass assignment prevention, and server-side role verification.
- **`TG-DB` (Database Partitioning & Injection — 4 rules):** Mandates tenant-scoped queries across Prisma, Mongoose, SQLAlchemy, and GORM; eliminates raw SQL string concatenation.
- **`TG-INPUT` (Input Validation & Traversal — 6 rules):** Enforces safe path sanitization (`path.basename`), command argument escaping, safe DOM text assignments, and server-side file upload bounds.
- **`TG-RATE` (Rate Limiting & Resource Protection — 3 rules):** Enforces rate-limiting middleware on authentication routes, pagination bounds, and request payload size limits.
- **`TG-AGENT` (AI Agent & LLM Defense — 4 rules):** Enforces structural separation of user prompts from system instructions, inert XML delimiters, and containerized tool execution.
- **`TG-SSRF` (Server-Side Request Forgery — 4 rules):** Restricts dynamic outbound HTTP calls, blocks AWS/cloud metadata access (`169.254.169.254`), and enforces request timeouts.
- **`TG-WEBHOOK` (Webhook Verification — 4 rules):** Mandates cryptographic HMAC-SHA256 signature validation before body parsing, replay prevention, and timestamp expiration.
- **`TG-WS` (WebSocket Security — 4 rules):** Enforces handshake authentication, origin validation, channel-level authorization, and frame size caps.
- **`TG-CSRF` (Cross-Site Request Forgery — 2 rules):** Enforces anti-CSRF tokens on state-changing operations and `SameSite` cookie attributes.
- **`TG-GQL` (GraphQL Protection — 4 rules):** Enforces query depth limiting, production introspection suppression, and field-level resolver authorization.
- **`TG-SUPPLY` (Supply Chain Integrity — 6 rules):** Audits dependency lockfile presence, checks against known CVEs, prevents `--no-audit` build flags, and inspects build scripts.
- **`TG-BIZ` (Business Logic Bounds — 4 rules):** Validates negative quantity inputs, coupon/discount boundaries, and race-condition transaction locks.
- **`TG-CACHE` (Cache Isolation — 3 rules):** Enforces `Cache-Control: no-store, private` on authenticated responses and sanitizes unkeyed request headers.
- **`TG-CLIENT` (Client Bundle Hygiene — 2 rules):** Forbids importing private server environment variables into browser bundles and suppresses production source maps.
- **`TG-PLATFORM` (Server Hardening — 4 rules):** Enforces Helmet HTTP security headers, CORS origin whitelisting, cookie `secure` flags, and debug mode suppression.
- **`TG-DIFF` (Polyglot Diff Integrity — 3 rules):** Intercepts security bypass comments (`# nosec`, `InsecureSkipVerify: true`) and asserts Ponytail patch budgets.
- **`TG-EDGE` (Edge & Serverless Limits — 2 rules):** Prevents cross-request memory leaks in Cloudflare Workers and enforces subrequest fan-out limits.

</details>

---

## ✂️ Ponytail Remediation Protocol & Rollback Safety

Traditional AI coding assistants routinely destroy functional features by attempting full-file rewrites. TorusGuard strictly enforces the **Ponytail Protocol**:

$$\Delta \text{Lines} \le 35\text{ Additions}, \quad \Delta \text{Lines} \le 25\text{ Deletions}$$

### 🛡️ Pre-Apply Rollback Snapshots
Before modifying a single file on disk, `apply_runner.py` creates a byte-for-byte backup:
```text
.torusguard/snapshots/<run_id>/<target_file>.bak
```

If a patch causes unforeseen behavior or test failures, execute an instant 1-command rollback:
```bash
npx torusguard rollback
```
All affected files are immediately restored to their exact pre-patch byte state.

---

## 📜 Living Security Report Ground Truth (`security_report.md`)

To eliminate AI hallucination, TorusGuard maintains `security_report.md` at the workspace root as the single source of truth across all CLI commands and AI chat sessions.

### 🔄 Lifecycle State Machine
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SECURITY REPORT LIFECYCLE STATE MACHINE                 │
└─────────────────────────────────────────────────────────────────────────────┘
  [ OPEN 🔴 ] ──(verify)──► [ VERIFIED 🟠 ] ──(harden)──► [ CANDIDATE 🟡 ]
                                                                 │
                                                               (apply)
                                                                 │
                                                                 ▼
  [ RESOLVED 🟢 ] ◄──(recheck: confirmed)── [ APPLIED 🔵 ]
         │
         └──(recheck: failed)──► [ REGRESSED ❌ ]
```

### 🧮 Posture Health Score (0–100)
The Health Score dynamically reflects the open risk ledger:
$$\text{Penalty} = (25 \times \text{Critical}) + (15 \times \text{High}) + (5 \times \text{Medium}) + (2 \times \text{Low})$$
$$\text{Score} = \max(0, \min(100, 100 - \text{Penalty}))$$

*When all findings are verified closed via differential recheck, the repository achieves **Health Score: 100/100 🟢 Hardened & Secure**.*

---

## 📊 Visual HTML Dashboard & SARIF v2.1.0 Export

Generate a standalone, zero-external-CDN, dark-mode visual posture dashboard:
```bash
npx torusguard report --html
```
- **SVG Circular Posture Gauge:** Animated visual health score ($0-100$).
- **7-Stage Closed-Loop Pipeline:** Visual state timeline across all lifecycle phases.
- **Golden Fix Recipes Grid:** Syntax-highlighted unified diffs with Ponytail metrics.
- **Zero-CDN Architecture:** Completely offline-ready; embeds all styles and assets inline.

To integrate with **GitHub Code Scanning**, export standard SARIF:
```bash
npx torusguard report > results.sarif
```

---

## 🤖 AI Editor Guardrails Auto-Sync

TorusGuard compiles project security invariants, golden recipes, and active guardrails into prompt-optimized rule files:
```bash
npx torusguard rules sync
```

### Supported AI Editors:
- **Cursor:** Injects non-destructive rules into `.cursorrules`
- **Claude Code:** Injects non-destructive rules into `CLAUDE.md`
- **Antigravity IDE:** Injects non-destructive rules into `.agent/rules/torusguard.md`
- **Windsurf:** Injects non-destructive rules into `.windsurfrules`

*All rules are compiled under a strict overhead ceiling of $\le 300$ prompt tokens to preserve AI reasoning context.*

---

## 🏢 Monorepo Fleet Support & Git Pre-Commit Diff Guard

TorusGuard automatically discovers and profiles multi-package workspaces:
- **Monorepo Ecosystems:** pnpm workspaces, npm/yarn workspaces, Cargo workspaces, Go multi-module workspaces, Gradle multi-project builds.
- **Universal Polyglot Profiler:** Automatically identifies 16+ languages and maps ORM boundaries independently per sub-package.
- **Pre-Commit Diff Guard:** Run `npx torusguard diff-guard --install-hook` to bind `.git/hooks/pre-commit` and block security bypasses before code is committed.

---

## 🧪 Verification & Test Harness

### What Happens When You Run `npm test`?
TorusGuard enforces a strict **100% pass requirement across 81 test suites** before every release.

When a developer runs:
```bash
npm test
```
The test harness invokes `python harness/runner.py` directly using the Python standard library. It systematically verifies:
1. **JSON Schema Validity:** 10 formal schemas (`finding`, `evidence`, `remediation`, `rule`, `lifecycle`, `provenance`, etc.).
2. **74-Rule Catalog Integrity:** AST detection accuracy across all 18 security families.
3. **Line-Shift Fingerprinting:** Stable anchor matching across file edits without line number drift.
4. **Secret Redaction:** Stripe secret keys and JWT tokens safely masked.
5. **Deterministic Replay:** 3-pass differential validation across Django, DRF, FastAPI, Flask, and SQLAlchemy fixtures.
6. **Ponytail Patch Churn Bounds:** Verifying line budgets ($\le 35$ additions, $\le 25$ deletions).
7. **Living Security Report State Transitions:** Discovery (`OPEN 🔴`), Candidate (`CANDIDATE 🟡`), Applied (`APPLIED 🔵`), and Verified Closure (`RESOLVED 🟢`).

```bash
# Run formal TorusGuard test harness
npm test

# Expected Output:
# ================================================================================
# SUMMARY: 81 Passed | 0 Failed
# ================================================================================
```

To validate diff guard and monorepo profiling independently:
```bash
python harness/validate_v0_9_2_diff_and_monorepo.py
```

---

## 🔒 Security Policy & Responsible Disclosure

If you believe you have discovered a security vulnerability in TorusGuard itself, please report it responsibly and privately through [GitHub Private Vulnerability Reporting](https://github.com/githubmofo/TorusGuard/security/advisories/new) or contact the project maintainers. Do not file public issues for undisclosed security flaws. For complete details, consult [SECURITY.md](SECURITY.md).

---

## 📄 License

TorusGuard is released under the [MIT License](LICENSE).  
Copyright (c) 2026 Jenish Lad ([@githubmofo](https://github.com/githubmofo)).
