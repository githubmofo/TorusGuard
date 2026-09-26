<p align="center">
  <img src="TorusGuard.png" alt="TorusGuard Logo" width="200" />
</p>

<h1 align="center">TorusGuard</h1>

<p align="center">
  <strong>The Hybrid Governance Security Engine for AI-built web applications.</strong><br>
  <em>Pairs the intelligence of your AI Agent with a deterministic Go CLI to enforce strict security boundaries and patch limits.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/githubmofo/TorusGuard/releases"><img src="https://img.shields.io/badge/version-v2.1.0-orange.svg" alt="Version"></a>
  <a href="https://www.npmjs.com/package/torusguard"><img src="https://img.shields.io/badge/npm-v2.1.0-CB3837?logo=npm&logoColor=white" alt="npm: v2.1.0"></a>
  <img src="https://img.shields.io/badge/Privacy-Local_First-success" alt="Privacy: Local First">
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen" alt="Dependencies: Zero">
  <img src="https://img.shields.io/badge/SARIF-v2.1.0-6C3483" alt="SARIF">
  <img src="https://img.shields.io/badge/OWASP-Top_10-000000?logo=owasp&logoColor=white" alt="OWASP">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Unit%20Tests-100%25%20Passing-brightgreen?logo=go&logoColor=white" alt="Unit Tests: 100% Passing">
  <img src="https://img.shields.io/badge/Polyglot%20Tests-36%2F36%20Repos%20Passed-brightgreen?logo=checkmarx&logoColor=white" alt="Polyglot Tests: 36/36 Repos Passed">
  <img src="https://img.shields.io/badge/Tri--Mode%20E2E-16%2F16%20Verified-blue?logo=checkmarx&logoColor=white" alt="Tri-Mode E2E: 16/16 Verified">
  <img src="https://img.shields.io/badge/Vision%20OCR-Tested%20%26%20Verified-blueviolet?logo=tesseract&logoColor=white" alt="Vision OCR: Tested & Verified">
  <img src="https://img.shields.io/badge/Rules%20Verified-86%2F86%20Rules-success" alt="Rules: 86/86 Verified">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tri--Mode-CLI%20%7C%20Chat%20%7C%20MCP-blue" alt="Tri-Mode Parity">
  <img src="https://img.shields.io/badge/Go-1.25-00ADD8?logo=go&logoColor=white" alt="Go">
  <img src="https://img.shields.io/badge/Node.js-18+-339933?logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Rust-2021-DEA584?logo=rust&logoColor=white" alt="Rust">
</p>

---

## Table of Contents

- [What Is TorusGuard?](#what-is-torusguard)
- [Features](#-features)
- [Autonomous Architecture & Workflow](#-autonomous-architecture--workflow)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Commands](#-commands)
- [Project Structure](#-project-structure)
- [Security Invariants & Rule Governance](#-security-invariants--rule-governance)
- [AI Agent Integration](#-ai-agent-integration)
- [Verified Test Suite & Benchmarks](#-verified-test-suite--mass-benchmarks)
- [Non-Negotiable Invariants](#-non-negotiable-invariants)
- [Contributing](#-contributing)
- [License](#-license)
- [Documentation](#-documentation)

---

## What Is TorusGuard?

TorusGuard is a **zero-dependency, single-binary security engine** that scans, hardens, and validates AI-generated codebases. It enforces 86 security rules across 22 architectural families and works across three unified operational modes (**Tri-Mode Parity**):

- **Mode A: Terminal CLI (Go Binary)** — A deterministic scanner and enforcer that runs in your terminal or CI/CD pipeline (`torusguard <command>`).
- **Mode B: AI Chat Slash Commands** — Integrates natively with Antigravity, Cursor, Claude Code, Windsurf, VS Code, and other AI coding assistants via slash commands (`/torusguard <command>`).
- **Mode C: Native MCP Tools** — Stdio Model Context Protocol (JSON-RPC 2.0) interface exposing autonomous security tools and living resources directly to AI agents.

TorusGuard ensures that the code your AI assistant writes is secure *before* it reaches production.

---

## ✨ Features

- **86 Security Rules** across 22 families (Secrets, Auth, SQL Injection, SSRF, CSRF, GraphQL, Supply Chain, Containers, Git History, ReDoS, AI & RAG, and more)
- **First-Principles Security Suite** — Built-in native scanners for Dockerfile/Compose privilege bounds, Git commit log secret mining, exponential regex backtracking, and cross-tenant vector isolation
- **Heuristic AST Scanner** — Polyglot static analysis for Go, JavaScript, TypeScript, and Python
- **Line-Level Reflection Module** — Semantic patch synthesis (`find_snippet` / `replace_snippet`) that accurately replaces exact code blocks without brittle line-number offsets
- **1/9th Token Bounded Context Extraction** — AST context extraction (±3 lines) via `scanner.ExtractContext` to keep review prompts hyper-efficient and prevent context saturation
- **Ponytail Protocol** — Surgical patch bounds (≤35 additions, ≤25 deletions) to prevent full-file rewrites
- **Pre-Apply Snapshots** — Automatic `.bak` rollback snapshots before every code modification
- **SARIF v2.1.0 Export** — Standards-compliant output for GitHub Advanced Security, VS Code, and other SARIF consumers
- **Dark-Mode HTML Reports** — Single-file visual posture dashboards
- **Golden Fix Recipes** — Persistent memory of verified security patterns for reuse
- **SSRF Defense** — Built-in private IP blocking and AWS metadata protection in the web validator
- **Fail-Closed Cryptography** — No fallback tokens; panics on entropy failure
- **DoS Resilience** — 10,000-file scan limit and 5-minute context timeout to prevent resource exhaustion
- **16+ Language Stack Detection** — Go, Rust, Java, C#, PHP, Ruby, Kotlin, Elixir, Dart, Swift, Python, TypeScript, and more
- **Multi-Modal Vision OCR** — Scans architecture diagrams, mockups, and screenshots (`.png`, `.jpg`, `.webp`) via Tesseract OCR to detect leaked keys, tokens, and credentials
- **Native MCP Server (Model Context Protocol)** — Exposes standard JSON-RPC 2.0 stdio tools and resources for direct agent integration
- **Tri-Mode Parity** — Terminal CLI, AI Chat slash commands, and Native MCP Tools share identical governance workflows

---

## 🧪 Proven Compatibility

TorusGuard’s static scanner and enforcement binary have been rigorously tested and confirmed compatible across **20 major technology stacks and frameworks**:

| Ecosystem | Tested Frameworks & Runtimes |
|-----------|------------------------------|
| **JavaScript / TypeScript** | React, Next.js, Express, Vue, Angular, SvelteKit, NestJS |
| **Python** | Django, Flask, FastAPI, raw Python scripts |
| **Go** | Gin |
| **Java / C# (.NET)** | Spring Boot, ASP.NET Core, .NET Core Middleware |
| **Ruby** | Ruby on Rails, Sinatra |
| **PHP** | Laravel, Symfony |
| **Rust** | Actix Web |

---

## 🏗️ Autonomous Architecture & Workflow

TorusGuard uses a **tri-track architecture** where intelligence, deterministic enforcement, and agent tool execution are cleanly separated across three unified operational modes:

```mermaid
flowchart TD
    subgraph Ingress["Unified Tri-Mode Ingress"]
        ModeA["<b>Mode A: Terminal CLI</b><br/><code>torusguard &lt;cmd&gt;</code><br/>Deterministic Single Binary"]
        ModeB["<b>Mode B: AI Chat Slash Commands</b><br/><code>/torusguard &lt;cmd&gt;</code><br/>Cursor &bull; Claude &bull; Windsurf &bull; Antigravity"]
        ModeC["<b>Mode C: Native MCP Tools</b><br/><code>torusguard_*</code> (10 Tools &bull; 2 Resources)<br/>Stdio JSON-RPC 2.0 Agent Server"]
    end

    Ingress --> Router["<b>Command Router &amp; Dispatcher</b><br/>cmd/torusguard (21 Commands)"]

    subgraph Core["TorusGuard Core Security Engine (Go Single Binary)"]
        direction TB
        subgraph Scanners["First-Principles &amp; Multi-Modal Scanner Suite"]
            AST["<b>Polyglot AST &amp; Heuristic Scanner</b><br/>Go &bull; TS/JS &bull; Python &bull; SQL &bull; Auth &bull; SSRF &bull; CSRF"]
            OCR["<b>Multi-Modal Vision OCR Engine</b><br/>Tesseract v5.4.0 &bull; Leaked Keys in PNG/JPG &le;10MB"]
            Container["<b>Container &amp; Dockerfile Auditor</b><br/>Root Execution &bull; Docker Sockets &bull; Build Secrets"]
            GitMine["<b>Git History Secret Miner</b><br/>Past Commits &bull; Diff Logs &bull; Remote Credentials"]
            ReDoS["<b>ReDoS Complexity Analyzer</b><br/>Polynomial &amp; Exponential Backtracking Loops"]
            AIGuard["<b>AI Agent &amp; RAG Vector Guard</b><br/>Prompt Injection &bull; Tenant Vector Contamination"]
        end

        subgraph Governance["Governance &amp; Remediation Pipeline"]
            Harden["<b>Harden &amp; Line Reflection</b><br/>Ponytail Bounds: &le;35 Add &bull; &le;25 Del"]
            Snapshot["<b>Pre-Apply Snapshot Engine</b><br/>Byte-for-Byte Rollback Backups in .torusguard/snapshots/"]
            HumanGate{"<b>Human Gate Authorization</b><br/>Explicit --yes Confirmation Required"}
            Recheck["<b>Differential Recheck Engine</b><br/>Zero-Regression Fix Closure"]
        end
    end

    Router --> Scanners
    Scanners --> Ledger[("<b>Living Security Ledger</b><br/><code>security_report.md</code><br/>Single Source of Truth")]
    Ledger --> Harden
    Harden --> Snapshot
    Snapshot --> HumanGate
    HumanGate -- Approved --> Recheck
    Recheck --> Outputs["<b>Enterprise Outputs</b><br/>OASIS SARIF v2.1.0 &bull; Dark-Mode HTML Report &bull; Golden Fix Distillation"]

    classDef ingressStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef scannerStyle fill:#0f172a,stroke:#818cf8,stroke-width:2px,color:#f8fafc;
    classDef govStyle fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#f8fafc;
    classDef ledgerStyle fill:#312e81,stroke:#a78bfa,stroke-width:2px,color:#f8fafc;
    classDef outStyle fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#f8fafc;

    class ModeA,ModeB,ModeC ingressStyle;
    class AST,OCR,Container,GitMine,ReDoS,AIGuard scannerStyle;
    class Harden,Snapshot,HumanGate,Recheck govStyle;
    class Ledger ledgerStyle;
    class Outputs outStyle;
```

> 🌐 **Interactive Architecture Visualizations:**
> - [**System Architecture Diagram** (HTML)](docs/architecture/torusguard-architecture.html) — Dynamic zoomable/pannable pipeline with dark/light themes, live view switching (Tri-Mode Ingress, AST Engine, Multi-Modal Vision OCR, Ponytail Bounds, Fail-Closed Recovery), and SVG/PNG export.
> - [**Governed Remediation Workflow** (HTML)](docs/architecture/torusguard-governance.workflow.html) — Step-by-step visual trace of the 7-stage remediation loop, safety gates, and automatic rollback path.

**Key design decisions:**
- **Tri-Mode Parity:** The CLI (Mode A), Chat Slash Commands (Mode B), and Native MCP Tools (Mode C) share the exact same underlying governance and validation rules.
- **Multi-Modal Vision OCR:** Images, architecture diagrams, and screenshots are automatically scanned for leaked secrets using Tesseract OCR, bounded by strict 10MB memory safety limits.
- **Deterministic Enforcement:** The **Go binary** handles all deterministic operations (AST scanning, bounds checking, snapshotting, reporting).
- **AI Intelligence:** The **AI agent** handles intelligence-requiring tasks (patch generation, root-cause analysis, remediation formulation).
- **Living Ground Truth:** All modes synchronize with `security_report.md` to prevent finding drift or hallucination.
- **Zero-Bypass Guardrails:** Neither human nor AI can bypass Ponytail Protocol bounds (≤35 additions, ≤25 deletions) or the Human Gate before modifying code.


---

## 📋 Prerequisites

- **Go 1.25+** (to build from source)
- **Git** (for `git apply` patch operations)
- **Node.js 18+** (for npm package installation)

---

## 🚀 Installation

### Option 1: npm (Primary)

```bash
npm install -g torusguard
```

Or use directly without installing:

```bash
npx torusguard init
```

<a href="https://www.npmjs.com/package/torusguard">
  <img src="https://img.shields.io/badge/npm-v2.1.0-CB3837?logo=npm&logoColor=white" alt="npm package">
</a>

### Option 2: Build from Source (Recommended for Contributors)

```bash
git clone https://github.com/githubmofo/TorusGuard.git
cd TorusGuard
go build -o torusguard ./cmd/torusguard
```

### Option 3: Go Install

```bash
go install github.com/torusguard/torusguard/cmd/torusguard@latest
```

---

## 💻 Usage

### Quick Start

```bash
# Initialize TorusGuard in your project
torusguard init

# Run a full security audit
torusguard audit

# Check workspace posture
torusguard status

# Generate an HTML report
torusguard report --html

# Generate a SARIF report
torusguard report --sarif
```

### Remediation Workflow

```bash
# Validate a candidate patch against Ponytail bounds
torusguard harden fix.patch

# Apply the patch with rollback snapshot (requires --yes for Human Gate)
torusguard apply --yes fix.patch

# Verify the fix was applied correctly
torusguard recheck

# Roll back if something went wrong
torusguard rollback
```

### Runtime Validation

```bash
# Generate authorization token for runtime probing
torusguard authorize

# Probe a running application for security headers
torusguard web-validate

# Send bounded inert payloads to test input handling
torusguard exploit-check
```

---

## 🔧 Commands

| Command          | Description                                                    |
| :--------------- | :------------------------------------------------------------- |
| `init`           | Scaffold `.torusguard/` workspace, detect stack, activate rules |
| `status`         | Diagnostic overview of posture, stack, and active rules         |
| `audit`          | Static heuristic security scan against active TG-* rules       |
| `verify`         | Live disk line match audit and evidence sufficiency check       |
| `harden`         | Validate patches against Ponytail Protocol bounds              |
| `apply`          | Apply patches with pre-apply `.bak` rollback snapshots         |
| `rollback`       | Instant restoration from pre-apply snapshots                   |
| `recheck`        | Differential re-scan on modified files                         |
| `report`         | Generate HTML (`--html`) or SARIF (`--sarif`) posture reports  |
| `recipes`        | Manage the Golden Fix recipe library                           |
| `authorize`      | Generate cryptographic auth tokens for runtime probing         |
| `web-validate`   | Authorized HTTP probing with `X-TorusGuard-Audit` headers      |
| `ocr-scan`       | Run Tesseract OCR secret scan on images/diagrams (<10MB)       |
| `container`      | Audit Dockerfile, compose, and container configurations        |
| `git-mine`       | Mine git commit history for leaked secrets & creds             |
| `redos`          | Analyze regex patterns for catastrophic backtracking           |
| `ai-guard`       | Scan AI/LLM code for prompt injection & RAG flaws              |
| `mcp`            | Run native Model Context Protocol (MCP) server over stdio      |
| `update`         | Self-update the TorusGuard engine                              |
| `help`           | Show interactive command guide                                 |

---

## 📁 Project Structure

```
TorusGuard/
├── cmd/torusguard/       # CLI entry point, command router & MCP server
│   ├── main.go           # CLI command router
│   └── mcp.go            # Model Context Protocol (MCP) JSON-RPC 2.0 stdio server
├── internal/
│   ├── apply/            # Patch application + pre-apply snapshot engine
│   ├── harden/           # Ponytail Protocol bounds enforcement & line-level reflection
│   │   ├── patch.go      # Ponytail Protocol bounds verification
│   │   └── reflection.go # Line-level reflection & semantic replacement
│   ├── memory/           # Golden Fix recipe persistence
│   ├── recheck/          # Differential re-scan engine
│   ├── report/           # SARIF v2.1.0 + dark-mode HTML generators
│   ├── rules/            # TG-* rule catalog loader
│   ├── scanner/          # Heuristic polyglot security scanner + Tesseract OCR
│   │   ├── scanner.go    # Polyglot code AST & heuristic scanner
│   │   └── ocr.go        # Multi-modal Vision OCR secret detection
│   ├── termui/           # 75-column terminal UI formatting
│   ├── validate/         # authorize / web-validate / exploit-check / verify
│   └── workspace/        # init + polyglot stack detection
├── .torusguard/          # Generated workspace state
│   ├── rules/            # Active security rule definitions
│   ├── schemas/          # JSON schemas for findings, recipes, etc.
│   ├── memory/           # Persistent security context
│   └── snapshots/        # Pre-apply rollback backups
├── docs/                 # Architecture and usage documentation
├── bin/                  # npm package CLI wrapper
├── go.mod                # Go module (github.com/torusguard/torusguard)
└── package.json          # npm package definition
```

---

## 🔒 Security Invariants & Rule Governance

TorusGuard enforces **86 security invariants across 22 architectural families** covering Secrets, Authentication, Multi-Tenant Database Isolation, Input Sanitization, Rate Limiting, AI Agent Prompt Injection, SSRF, Webhooks, WebSockets, CSRF, GraphQL, Supply Chain, Business Logic, Cache Poisoning, Client Bundles, Platform Headers, Polyglot Bypasses, Edge Timeouts, Container & Docker Safety, Git History Secret Mining, Regular Expression Backtracking (ReDoS), and Vector Database RAG Isolation.

> 📘 **Full Rules Catalog & Invariants:**  
> The complete rulebook with formal invariant definitions, severity scores, and testing signatures is maintained in [`AGENTS.md`](AGENTS.md) and the [`rules/`](rules/) directory.  
> You can also explore verified Golden Fix patterns anytime via `torusguard recipes` or stream the live catalog over MCP via `torusguard://rules_catalog`.

---

## 🤖 AI Agent Integration

TorusGuard works natively inside AI coding assistants. Add the configuration file to your project root and your AI agent automatically enforces TorusGuard security invariants.

### Supported Agents

| Agent                | Configuration File    | Status |
| :------------------- | :-------------------- | :----- |
| Antigravity (Gemini) | `AGENTS.md`           | ✅ Full support |
| Claude Code          | `CLAUDE.md`           | ✅ Full support |
| Cursor               | `.cursorrules`        | ✅ Full support |
| Windsurf             | `.windsurfrules`      | ✅ Full support |
| VS Code Copilot      | `AGENTS.md`           | ✅ Full support |
| Kimi                 | `SKILL.md`            | ✅ Full support |

### Slash Commands (AI Chat Mode)

```
/torusguard init          # Initialize workspace
/torusguard audit         # Run security + OCR scan; sync security_report.md
/torusguard ocr-scan      # Scan diagram or image assets for leaked credentials
/torusguard harden        # Formulate remediation patches
/torusguard apply         # Apply patches with Human Gate
/torusguard recheck       # Verify fix closure
/torusguard report        # Generate posture report
/torusguard status        # Check posture overview
/torusguard full          # End-to-end 7-stage pipeline
```

### Native MCP Tools (Agent Toolkit Mode)

When configured with `.agents/mcp_config.json` or `mcp_config.json`, AI coding agents gain native tool calling:

- `torusguard_audit`: Deep static AST scan + Vision OCR; writes `security_report.md`
- `torusguard_ocr_scan`: Dedicated image credential analysis via Tesseract (5-10MB bounds)
- `torusguard_container`: Audits container files for root execution, docker socket exposure, and privileged mode
- `torusguard_git_mine`: Mines git commit history and config for leaked credentials and tokens
- `torusguard_redos`: Analyzes regex patterns for catastrophic exponential backtracking
- `torusguard_ai_guard`: Audits AI agent prompt templates, tool registries, and vector database queries
- `torusguard_verify`: Asserts evidence sufficiency & line-shift invariant fingerprint matches
- `torusguard_harden`: Validates remediation diff against Ponytail Protocol bounds
- `torusguard_recheck`: Differential re-scan confirming fix closure
- `torusguard_status`: Workspace posture and tech stack inspection
- `torusguard://security_report`: MCP Resource reading the living security report
- `torusguard://rules_catalog`: MCP Resource exploring verified rules catalog & Golden Fix patterns

---

## 🧪 Verified Test Suite & Mass Benchmarks

TorusGuard undergoes rigorous automated multi-tier testing across polyglot stacks, multi-modal vision assets, and agent communication protocols:

| Testing Tier | Scope & Target Stacks | Pass Rate | Verified Capabilities |
| :--- | :--- | :---: | :--- |
| **Go Engine & Unit Tests** | `cmd/torusguard`, `internal/scanner`, `internal/*` | **100% Passing** | Deterministic AST matching, 74 rule patterns, JSON-RPC 2.0 MCP protocol. |
| **Mass Polyglot Benchmarks** | **20 Enterprise Tech Stacks** (Go, Python, Java, Node, Rust, PHP, C#, Ruby, Svelte, Vue, Angular) | **20/20 Passed** | Framework auto-profiling, heuristic AST analysis, finding deduplication. |
| **Tri-Mode & Vision E2E** | **16 Diverse Framework Repos** (React, Next.js, Express, Django, FastAPI, Spring Boot, etc.) | **16/16 Passed** | Mode A (CLI) + Mode B (Slash Commands) + Mode C (Native MCP Tools) + Multi-Modal Vision OCR. |
| **Multi-Modal Vision OCR** | Diagram & Image assets (`.png`, `.jpg`, etc.) via Tesseract v5.4.0 | **100% Recall** | Secrets detection (`TG-SEC-001` - `TG-SEC-007`), 10MB DoS bounding, OCR character substitution tolerance. |
| **Ponytail Churn Limits** | Surgical patch validation across all 74 rules | **Bounded** | Line bounds (≤35 additions, ≤25 deletions), zero-bypass verification (`TG-DIFF-001`). |

All test environments are completely sandboxed, verified with byte-for-byte assertions, and cleaned up automatically.

---

## 🛡️ Non-Negotiable Invariants

1. **Browser-Code Truth:** Never expose secrets in frontend bundles.
2. **Multi-Tenant Isolation:** Always scope DB lookups by tenant/user ownership.
3. **Ponytail Churn Bounds:** Patches ≤35 additions, ≤25 deletions. No full-file rewrites.
4. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`.
5. **Snapshots Before Edits:** Mandatory `.bak` backup before every modification.
6. **Fail-Closed Cryptography:** Panic on entropy failure. No fallback tokens.
7. **SSRF Boundary Enforcement:** Block private IPs and cloud metadata before probing.
8. **DoS Resilience:** 10,000-file max, 5-minute timeout.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit changes: `git commit -m "feat: add your feature"`
4. Push to branch: `git push origin feat/your-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

---

## 📄 License

[MIT](LICENSE) © 2026 Jenish Lad

---

## 📚 Documentation

| Document                                                  | Description                              |
| :-------------------------------------------------------- | :--------------------------------------- |
| [Architecture](docs/architecture/ARCHITECTURE.md)         | System design and module relationships   |
| [Security Architecture](docs/architecture/SECURITY_ARCHITECTURE.md) | Threat model and security design |
| [Detection Engine](docs/architecture/DETECTION_ENGINE.md) | Scanner internals and rule matching      |
| [API Specification](docs/architecture/API_SPECIFICATION.md) | CLI argument specification             |
| [Security Philosophy](docs/overview/security-philosophy.md) | Core design principles               |
| [Testing Playbook](docs/usage/testing-playbook.md)        | Testing guide and CI integration         |
| [Demo Guide](docs/demo.md)                                | Quick start and full lifecycle demo      |
| [Roadmap](docs/roadmap.md)                                | Feature roadmap and release planning     |
| [SECURITY.md](SECURITY.md)                                | Vulnerability disclosure policy          |
| [CHANGELOG.md](CHANGELOG.md)                              | Version history and release notes        |
