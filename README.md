<div align="center">
  <img src="TorusGuard.png" alt="TorusGuard Banner" width="400">
</div>

# TorusGuard

**Security guardrails and structured verification workflow for AI-built web applications.**

TorusGuard is a Markdown-first, portable AI-agent skill and security workflow engine. It helps developers and AI coding agents audit, verify, harden, and re-check modern web applications through structured rules, normalized evidence schemas, and human-friendly remediation workflows across frontend database isolation, secrets management, input validation, authentication, rate limits, SSRF, webhooks, and production deployment safety.

---

## Why This Exists

AI code generators accelerate product development, but they can easily introduce critical security oversights—such as client-side database queries, exposed API secrets, missing authorization checks, or unvalidated outbound requests. Security decisions still require structure, boundaries, and systematic verification. TorusGuard gives AI coding agents the context, guardrails, and deterministic workflow needed to build and deploy securely.

### Core Principle: The Browser-Code Truth
> **If the browser receives it, users can inspect it.**  
> DevTools, Inspect Element, and the Sources tab cannot be blocked. TorusGuard enforces that database credentials, sensitive business logic, and authorization decisions must always remain on trusted server-side code.

---

## 🔄 The 6-Stage Finding Lifecycle (v0.5.0 Architecture)

TorusGuard v0.5.0 introduces a formal state machine governing every candidate security finding:

```text
┌───────────┐     ┌────────────┐     ┌───────────┐     ┌─────────────┐     ┌───────────┐     ┌───────────┐
│ 1. Detect │ ──► │ 2.Classify │ ──► │ 3. Verify │ ──► │ 4.Remediate │ ──► │ 5.Recheck │ ──► │ 6.Archive │
└───────────┘     └────────────┘     └───────────┘     └─────────────┘     └───────────┘     └───────────┘
```

1. **Detect:** Scan repository source code, environment templates, and manifests.
2. **Classify:** Assign a canonical Rule ID (`TG-*`), taxonomy category, risk severity, and initial confidence.
3. **Verify:** Validate evidence sufficiency and reachable data flow. If evidence is ambiguous, force status to `Needs Review`.
4. **Remediate:** Formulate least-invasive, framework-native code modifications with before/after diffs.
5. **Re-check:** Re-audit modified code to verify that the vulnerability is resolved (`Verified Safe`).
6. **Archive:** Preserve timestamped verification evidence in the project audit record.

---

## Key Features

- **Markdown-First & Agent-Portable:** Works out-of-the-box in Cursor, Antigravity, Claude Code, Cline, Codex, Gemini CLI, and other agent environments without requiring external compilation or runtime daemons.
- **Formal Data & Evidence Schemas (`schemas/`):** Strict JSON schemas for findings, evidence typing (`source`, `runtime`, `test`, `manual_review`), and remediation objects.
- **Repeatable Validation Harness (`harness/`):** Standalone automated test harness validating schemas, 60-rule catalog integrity, and differential fixture behavior.
- **Framework-Aware Security Catalog:** 60+ structured security rules across secrets, database access, input validation, authentication, rate limits, SSRF, CSRF, webhooks, GraphQL, WebSockets, and supply chain.
- **Multi-Ecosystem Support:** Deep, framework-idiomatic guidance for JavaScript/TypeScript (Node.js, Express, React, Vite, Next.js) and Python (Django, DRF, FastAPI, Flask, SQLAlchemy).
- **Human-First Findings:** Generates clear, readable audit reports featuring severity levels, plain-English risk explanations, and concrete Before/After code snippets.

---

## Current Release: v0.5.1 (Provenance & Auditable Confidence Release)

TorusGuard v0.5.1 standardizes finding normalization, provenance tracking, and auditable confidence scoring:
- **Canonical Finding Model:** Standardized schema across all rule categories with structured provenance chains.
- **Auditable 0–100 Confidence Scoring:** Transparent 5-factor mathematical rubric replacing subjective estimates.
- **Cryptographic Evidence Packaging:** Immutable SHA-256 checksums for raw code evidence snippets.
- **Explicit Retest State Machine:** Formal post-fix retesting via `/torusguard recheck` before findings can transition to `Verified Fixed`.
- **Automated Validation Harness:** Standalone test runner (`python harness/runner.py`) with 42/42 passing assertions.

*Read the complete release notes in [docs/releases/v0.5.1.md](docs/releases/v0.5.1.md).*

---

## Supported Platforms & Frameworks

### 🐍 Python
* **[Django Guide](guides/python/django.md)** — Settings, CSRF, ORM queries, ModelForms, object ownership.
* **[Django REST Framework Guide](guides/python/django-rest-framework.md)** — Default permissions, ViewSets, serializers, throttles, pagination.
* **[FastAPI Guide](guides/python/fastapi.md)** — Pydantic v2 schemas, dependencies, outbound SSRF checks, HMAC webhooks.
* **[Flask Guide](guides/python/flask.md)** — Factory setup, session cookies, CSRFProtect, Werkzeug upload boundaries.
* **[SQLAlchemy Guide](guides/python/sqlalchemy.md)** — Parameterized `text()` bindings, query scoping, update allowlists.
* **[Python Dependencies & CI/CD](guides/python/python-dependencies.md)** — Reproducible lockfiles, `pip-audit`, GitHub Actions pinning.
* **[Python Rule Mapping Matrix](docs/python-rule-mapping.md)** — Framework implementation matrix for universal rule IDs.

### 🌐 JavaScript & TypeScript
* **[React + Vite Guide](guides/react-vite-security.md)** — Frontend environment variables, build artifact leakage, source maps.
* **[Next.js Guide](guides/nextjs-security.md)** — App Router / Pages Router security, Server Components, API routes.
* **[Node.js + Express Guide](guides/express-security.md)** — Middleware hardening, CORS, Helmet, session cookies, rate limiting.
* **[Supabase Guide](guides/supabase-security.md)** — Row-Level Security (RLS), service role key isolation, database policies.
* **[Firebase Guide](guides/firebase-security.md)** — Firestore Security Rules, client SDK boundaries, privileged admin tasks.

---

## Quick Start

### 1. Installation
Install TorusGuard into your AI coding tool using the open `skills` CLI:

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```

### 2. Workflow Commands

| Command | Lifecycle Phase | Purpose | Modifies Code? |
|---|:---:|---|:---:|
| `/torusguard init` | Baseline | Generates a project `SECURITY.md`, threat model, and baseline. | ❌ Docs only |
| `/torusguard audit` | Detect & Classify | Scans repository against TorusGuard rules and outputs a structured report. | ❌ No |
| `/torusguard verify` | Verify | Validates evidence sufficiency and checks manual review criteria. | ❌ No |
| `/torusguard harden` | Remediate | Applies least-invasive, safe fixes for confirmed findings. | ✅ Yes |
| `/torusguard recheck` | Re-check | Re-evaluates post-fix code to assert resolution (`Verified Safe`). | ❌ No |

---

## How to Verify Findings

When an audit report is generated:
1. **Inspect Evidence Snippet:** Confirm the cited file path and line numbers exist in your active codebase.
2. **Review Confidence Classification:**
   - **`Confirmed`:** Proved with direct source code or configuration evidence.
   - **`Needs Review`:** Requires verifying out-of-band context (e.g. domain service layer, upstream API gateway, cloud IAM).
3. **Execute Verification Command:** Run the documented test command in the finding's `Verification` section.

---

## How to Fix Findings

1. **Review Proposed Diffs:** Run `/torusguard harden` to generate framework-native, least-invasive code modifications.
2. **Apply Changes:** Update the affected code following the provided safe patterns.
3. **Run Differential Re-check:** Execute `/torusguard recheck` to verify that the finding transitions to `Verified Safe`.

---

## Validation & Quality Harness

TorusGuard maintains a repeatable automated validation harness:

```bash
python harness/runner.py
```

The harness runs across:
- **Schema Validation:** Verifies all schemas in `schemas/`.
- **Rule Catalog Integrity:** Validates 60 unique `TG-*` rule IDs with 0 duplicates.
- **Differential Fixtures:** Tests vulnerable vs hardened pairs in `examples/python/`.
- **Stack Detection Fixtures:** Tests 7 repository layouts in `tests/fixtures/python/stack-detection/`.
- **Regression Suite:** Executes 10 paired Python regression fixtures in `tests/fixtures/python/`.
- **Lifecycle Assertions:** Validates state machine transitions.

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
├── schemas/                 # Formal JSON schemas (finding, evidence, remediation, rule, lifecycle)
├── core/                    # Core workflow models, lifecycle state machine, and formatter
├── harness/                 # Repeatable automated validation harness runner
├── skills/TorusGuard/       # Portable skill instructions and reference modules
├── rules/                   # 60+ documented security rules across 9 lifecycle categories
├── templates/               # Standardized templates (SECURITY, audit, pre-flight)
├── guides/                  # Stack-specific implementation guides (Node.js & Python)
├── examples/                # Educational vulnerable & hardened reference applications
├── docs/                    
│   ├── architecture/        # Architecture specifications (v0.5.0 workflow architecture)
│   ├── workflow/            # Finding lifecycle and verification guides
│   ├── releases/            # Release notes (v0.2.0, v0.3.0, v0.4.0, v0.4.1, v0.5.0)
│   ├── python-rule-mapping.md # Universal rule mapping across Python stacks
│   ├── validation/          # Official validation reports & real-world records
│   └── roadmap.md           # Project roadmap & milestones
└── tests/                   # Test fixtures and regression test suites
```

---

## Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) before submitting an issue or pull request.

---

## Security

Please review our [Security Policy](SECURITY.md) for private responsible disclosure instructions. Do not file public GitHub issues for security vulnerabilities.

---

## License

TorusGuard is licensed under the [MIT License](LICENSE).  
Copyright (c) 2026 Jenish Lad.
