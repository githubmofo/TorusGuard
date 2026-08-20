<div align="center">
  <img src="TorusGuard.png" alt="TorusGuard Banner" width="400">
</div>

# TorusGuard

**Security guardrails for AI-built web applications.**

TorusGuard is a Markdown-first, portable AI-agent skill that helps developers audit and harden AI-built web applications. It provides structured rules, references, and remediation workflows across frontend database isolation, secrets management, input validation, authentication, rate limits, SSRF, webhooks, and production deployment safety.

---

## Why This Exists

AI code generators accelerate product development, but they can easily introduce critical security oversights—such as client-side database queries, exposed API secrets, missing authorization checks, or unvalidated outbound requests. Security decisions still require structure, boundaries, and systematic verification. TorusGuard gives AI coding agents the context and guardrails needed to build and deploy securely.

### Core Principle: The Browser-Code Truth
> **If the browser receives it, users can inspect it.**  
> DevTools, Inspect Element, and the Sources tab cannot be blocked. TorusGuard enforces that database credentials, sensitive business logic, and authorization decisions must always remain on trusted server-side code.

---

## Key Features

- **Markdown-First & Agent-Portable:** Works out-of-the-box in Cursor, Antigravity, Claude Code, Cline, Codex, Gemini CLI, and other agent environments without requiring npm dependencies or compilation.
- **Framework-Aware Security Catalog:** 60+ structured security rules across secrets, database access, input validation, authentication, rate limits, SSRF, CSRF, webhooks, GraphQL, WebSockets, and supply-chain dependencies.
- **Human-First Findings:** Generates clear, readable audit reports featuring severity levels, plain-English risk explanations, and concrete before/after code snippets.
- **Evidence-Confidence System:** Distinguishes verified code vulnerabilities from architecture-dependent manual review items.
- **Least-Invasive Hardening:** Modifies only code directly tied to verified findings while preserving business logic and application routes.

---

## Current Release Scope (v0.3.0)

TorusGuard v0.3.0 (*Advanced Web and API Security*) expands baseline guardrails into modern API architectures:

- **Server-Side Request Forgery (SSRF):** Internal network protection, DNS rebinding awareness, and outbound request bounding (`TG-SSRF-*`).
- **Business-Logic & Flow Abuse:** Replayable operations, sensitive parameter tampering, and state validation (`TG-BIZ-*`).
- **Authorization & Mass Assignment:** Property-level authorization and payload filtering (`TG-AUTH-006`, `TG-AUTH-007`).
- **Webhooks & Integrations:** Signature validation, replay prevention, and idempotency (`TG-WEBHOOK-*`).
- **GraphQL & WebSockets:** Query depth/complexity limits, resolver authorization, connection limits, and handshake auth (`TG-GQL-*`, `TG-WS-*`).
- **Supply Chain & Caching:** Lockfile integrity, CVE review boundaries, and sensitive response header caching (`TG-SUPPLY-*`, `TG-CACHE-*`).

---

## Quick Start

### 1. Installation
Install TorusGuard into your AI coding tool using the open `skills` CLI:

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```

### 2. Workflow
Once installed, interact with your AI assistant in chat using the `/torusguard` command:

1. **Initialize Project Security Baseline:**
   ```text
   /torusguard init
   ```
2. **Audit Codebase (Read-Only Scan):**
   ```text
   /torusguard audit
   ```
3. **Harden & Apply Fixes:**
   ```text
   /torusguard harden
   ```
4. **Pre-Flight Deployment Verification:**
   ```text
   /torusguard verify
   ```

---

## Core Commands

| Command | Purpose | Modifies Code? |
|---|---|:---:|
| `/torusguard init` | Generates a project `SECURITY.md` and readable threat model. | ❌ Docs only |
| `/torusguard audit` | Scans repository against TorusGuard rules and outputs a structured report. | ❌ No |
| `/torusguard harden` | Applies least-invasive, safe fixes for confirmed findings from the audit report. | ✅ Yes |
| `/torusguard check <area>` | Audits a single rule category (e.g., `auth`, `ssrf`, `database`, `secrets`). | ❌ No |
| `/torusguard verify` | Runs a production pre-flight deployment verification checklist. | ❌ No |

**Supported Check Areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`, `ssrf`, `business-logic`, `csrf`, `webhook`, `graphql`, `websocket`, `supply-chain`, `cache`.

---

## Validation Summary

TorusGuard v0.3.0 has been locally validated against real-world and test architectures:

1. **[OWASP NodeGoat](docs/validation/nodegoat-v0.3.0-validation.md):** An intentionally vulnerable Node.js / Express / MongoDB training application.
2. **[FastAPI Test Application](docs/validation/fastapi-v0.3.0-validation.md):** A Python / FastAPI application testing SSRF, webhook signatures, and mass-assignment detection.

### Evidence-Confidence Classification
TorusGuard classifies every audit finding by confidence level:
- **`Confirmed`:** Directly observed in source code or configuration (e.g., hardcoded secret, missing CSRF middleware, public source map).
- **`Likely`:** Strong static indicators; requires runtime or deployment environment confirmation.
- **`Manual Review`:** Architectural or business-context decisions that static analysis cannot reliably determine (e.g., business workflow logic, database RLS policies).
- **`Informational`:** Hardening advice and defensive best practices.

*Read the complete validation summary in [docs/validation/README.md](docs/validation/README.md).*

---

## What TorusGuard Is Not

To maintain technical honesty and clear boundaries:
- **Not an automated vulnerability scanner:** TorusGuard is a contextual guidance framework for developers and AI agents. It does not replace dynamic application security testing (DAST) or static binary analyzers.
- **Not a penetration-testing replacement:** It elevates baseline security hygiene but cannot replace authorized professional penetration testing.
- **Not an "unhackable" guarantee:** No tool can guarantee 100% security.
- **Not a client-side DRM:** Browser-delivered JavaScript cannot be hidden from DevTools; security must reside on the backend.

---

## Project Structure Overview

```text
TorusGuard/
├── skills/torusguard/       # Portable skill instructions and reference modules
├── rules/                   # 60+ documented security rules across 14 categories
│   ├── authorization/       # Mass assignment, object authorization
│   ├── business-logic/      # Workflow state, replay protection
│   ├── database/            # Frontend database access isolation
│   ├── input/               # SQLi, XSS, upload validation
│   ├── secrets/             # Hardcoded keys, .env, build artifact leakage
│   ├── ssrf/                # Outbound request & network boundary checks
│   └── webhook/             # Signature validation, replay prevention
├── templates/               # Standardized templates (SECURITY, audit, pre-flight)
├── guides/                  # Stack-specific implementation guides (React, Next.js, Express)
├── examples/                # Educational vulnerable & hardened reference applications
├── docs/                    
│   ├── validation/          # Official validation reports & methodology
│   ├── roadmap.md           # Project roadmap & milestones
│   └── demo.md              # Sample audit walkthrough & finding format
└── tests/                   # Test fixtures and rule validation matrices
```

---

## Roadmap

- **v0.1.0 (Released):** Initial core skill and reference modules.
- **v0.2.0 (Released):** Baseline 25-rule catalog, templates, guides, and reference apps.
- **v0.3.0 (Released):** Advanced Web and API Security (SSRF, Webhooks, GraphQL, WebSockets, Cache).
- **v0.4.0 (In Progress):** Python & Django / FastAPI native platform expansion.
- **v1.0.0 (Planned):** Full rule freeze, expanded test fixtures, and multi-framework coverage.

*See [docs/roadmap.md](docs/roadmap.md) for full milestone details.*

---

## Contributing

Contributions are welcome! You can help by proposing new security rules, improving existing guidance, reporting false positives, or adding framework implementation guides.

Please review [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) before submitting an issue or pull request.

---

## Security

If you discover a security issue within the TorusGuard repository or its skill definitions, please review our [Security Policy](SECURITY.md) for private responsible disclosure instructions. Do not file public GitHub issues for security vulnerabilities.

---

## License

TorusGuard is licensed under the [MIT License](LICENSE).  
Copyright (c) 2026 Jenish Lad.
