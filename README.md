<div align="center">
  <img src="TorusGuard.png" alt="TorusGuard Logo" width="300">
</div>

# <img src="assets/icon.svg" width="32" height="32" valign="middle" alt="TorusGuard Icon" /> TorusGuard

> **Security guardrails for AI-built web applications.**

TorusGuard is a Markdown-first, portable AI-agent skill that helps developers audit and harden AI-built web applications. It provides actionable, framework-aware guidance to secure secrets, frontend database access, input validation, authentication, rate limits, and production exposure.

*Note: TorusGuard is **not** an npm package, hosted service, browser extension, or automated vulnerability scanner. It is a contextual guidance framework for developers and their AI coding assistants.*

---

## 🎯 Value Proposition

When building applications rapidly with AI, security fundamentals can sometimes be overlooked. TorusGuard integrates directly into your workflow to ensure your applications are robust against common web vulnerabilities before they hit production.

### What it Protects Against
TorusGuard's comprehensive rule catalog addresses critical attack vectors:

* **Authentication & Authorization:** Weak authentication, client-only authorization, IDOR, mass assignment, and property-level authorization.
* **Network & Architecture:** SSRF, outbound-request protection, and unsafe CORS.
* **Business Logic:** Sensitive business-flow protection, replayable operations, and webhook integrity (signature, replay, idempotency).
* **Data & Input:** Missing input validation, SQL injection, XSS, unsafe uploads, and frontend database exposure.
* **Infrastructure & State:** Hardcoded secrets, tracked `.env` files, unbounded resource consumption (rate limits), and caching vulnerabilities.
* **Modern APIs:** GraphQL (depth, complexity, batching) and WebSocket (handshake auth, channel auth, message validation).
* **Supply Chain:** Dependency risks, CI/CD secret exposure, and unpinned actions.

---

## 🧠 Core Philosophy: The Browser-Code Truth

**If the browser receives it, users can inspect it.**

DevTools, Inspect Element, and the Sources tab cannot be blocked. TorusGuard enforces the principle that secrets, direct database access, and authorization decisions must remain in trusted server-side code. It does not claim to hide JavaScript or make applications magically "unhackable."

---

## 🚀 Getting Started

### Installation
TorusGuard is installed as a skill for your AI coding assistant.

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```

### Quick Start Workflow
Once installed, interact with your AI assistant using the following command sequence to secure your project:

1. **Initialize:** Setup your security baseline.
   ```text
   /torusguard init
   ```
2. **Audit:** Identify vulnerabilities without modifying code.
   ```text
   /torusguard audit
   ```
3. **Harden:** Apply recommended fixes for identified vulnerabilities.
   ```text
   /torusguard harden
   ```
4. **Verify:** Run a final pre-flight check before deployment.
   ```text
   /torusguard verify
   ```

---

## 🛠️ Command Reference

| Command | Description | Modifies Code? |
|---------|-------------|:---:|
| `/torusguard init` | Generates or updates `SECURITY.md` and the project threat model. | ❌ Docs only |
| `/torusguard audit` | Scans the codebase against the TorusGuard rule catalog and generates a structured audit report. | ❌ No |
| `/torusguard harden` | Applies least-invasive, secure fixes for high-confidence findings from the audit. Preserves business logic. | ✅ Yes |
| `/torusguard check <area>` | Audits a specific rule group (e.g., `auth`, `ssrf`, `database`). | ❌ No |
| `/torusguard verify` | Executes a comprehensive production pre-flight security checklist. | ❌ No |

### Check Areas
You can narrow your focus by passing specific areas to the `check` command:
`secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`, `ssrf`, `business-logic`, `csrf`, `webhook`, `graphql`, `websocket`, `supply-chain`, `cache`

---

## 📚 Rule Catalog (v0.3.0)

TorusGuard v0.3.0 includes an advanced, structured catalog of security rules spanning modern architectures.

| Category | Rule Prefix | Default Severities |
|----------|-------------|--------------------|
| **Secrets Management** | `TG-SEC-` | Critical – Medium |
| **Database Exposure** | `TG-DB-` | Critical – High |
| **Input & Injection** | `TG-INPUT-` | Critical – High |
| **Authentication & AuthZ** | `TG-AUTH-` | Critical – High |
| **Rate Limiting & DoS** | `TG-RATE-` | High – Medium |
| **Client Exposure** | `TG-CLIENT-` | High – Medium |
| **Platform Hardening** | `TG-PLATFORM-` | High – Medium |
| **Server-Side Request Forgery** | `TG-SSRF-` | Critical – High |
| **Business Logic & Flows** | `TG-BIZ-` | Critical – High |
| **Webhooks** | `TG-WEBHOOK-` | Critical – High |
| **GraphQL** | `TG-GQL-` | Critical – High |
| **WebSockets** | `TG-WS-` | Critical – High |
| **Supply Chain & CI/CD** | `TG-SUPPLY-` | Critical – High |
| **Caching** | `TG-CACHE-` | High – Medium |

*For the complete catalog and individual rule definitions, see [rules/README.md](rules/README.md).*

---

## 🏗️ Supported Stacks

TorusGuard is framework-agnostic but provides highly tailored guidance for:
* **Frontend/Fullstack:** React, Vite, Next.js
* **Backend:** Node.js, Express, common REST & GraphQL APIs
* **Databases/BaaS:** PostgreSQL, MySQL, MongoDB, Supabase, Firebase

---

## 📁 Repository Structure

```text
TorusGuard/
├── skills/torusguard/       # Main installable skill and reference documents
├── rules/                   # Comprehensive documented security rules (v0.2 + v0.3)
├── templates/               # Standardized templates (SECURITY, audit, pre-flight, threat model)
├── guides/                  # Stack-specific implementation and hardening guides
├── examples/                # Vulnerable & hardened reference applications
├── research/                # Threat rationale and vulnerability research notes
└── docs/                  
    └── validation/          # Official validation reports (e.g., NodeGoat)
```

---

## ✅ Validation Status

TorusGuard v0.3.0 has been locally validated against **OWASP NodeGoat** (an intentionally vulnerable Node.js training application) and a custom vulnerable **FastAPI** test application. 

The validation confirmed actionable findings for CSRF configurations, sensitive-response caching, and dependency risks. It also verified that TorusGuard successfully generates structured manual-review tasks for complex logic issues (like SSRF and business-logic abuse) where static analysis alone cannot determine application intent.

---

## ⚠️ Limitations

TorusGuard is an exceptional tool for elevating baseline security, but it **does not replace**:
1. Professional Penetration Testing
2. Compliance Certification (SOC2, HIPAA, etc.)
3. Manual Threat Modeling
4. Human judgment for false positives, complex business-logic flaws, and infrastructural configurations (e.g., Database RLS, cloud IAM).

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. 
When proposing new rules via issues, please include unsafe/safe code examples and verification steps.

---

## 🔒 Security Reporting

Please report TorusGuard vulnerabilities **privately**. See [SECURITY.md](SECURITY.md) for our disclosure policy. **Do not use public GitHub Issues for security disclosures.**

---

## 🗺️ Roadmap

| Version | Focus | Status |
|---------|-------|:---:|
| `v0.1.0` | Core skill and reference modules | ✅ Released |
| `v0.2.0` | Structured audit framework (25 rules, templates, guides) | ✅ Released |
| `v0.3.0` | Advanced Web and API Security (GraphQL, Webhooks, SSRF, etc.) | ✅ Released |
| `v1.0.0` | Stable rule catalog and comprehensive integration examples | 🚧 Planned |

---

## 📝 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---
*Maintained by Jenish Lad*
