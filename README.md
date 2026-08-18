# TorusGuard

**Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, auth, rate limits, and production exposure.**

TorusGuard is a portable AI-agent security skill for AI-built web applications. It audits and hardens common security issues including hardcoded secrets, frontend database queries or admin keys, unsafe input validation, SQL/NoSQL injection, authentication and authorization flaws, IDOR, missing rate limits, unsafe CORS, public production source maps, and insecure deployment configuration.

## What TorusGuard Does

- Guides AI agents to build secure-by-default web applications
- Audits repositories before changing code
- Identifies frontend, backend, database, auth, and deployment risks
- Applies stack-aware safe implementation patterns
- Generates a persistent project `SECURITY.md` with your app's security context

## What TorusGuard Does Not Do

- Replace a professional penetration test
- Guarantee PCI-DSS, HIPAA, ISO 27001, SOC 2, or GDPR compliance
- Detect every business-logic vulnerability
- Block DevTools or hide browser JavaScript (see below)
- Provide a hosted dashboard or SaaS product

## Core Principle

**Anything sent to the browser is public.**

DevTools, Inspect Element, and browser Sources cannot be blocked — browsers must receive JavaScript to execute it. TorusGuard prevents secrets and privileged logic from reaching the browser, disables public production source maps, and moves authorization and database access to trusted server code.

## Installation

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```

Or copy `skills/torusguard/` to your agent's skills directory:

| Agent | Path |
|-------|------|
| Cursor (project) | `.cursor/skills/torusguard/` |
| Cursor (personal) | `~/.cursor/skills/torusguard/` |

## Commands

| Command | Purpose |
|---------|---------|
| `/torusguard init` | Analyze project and create `SECURITY.md` |
| `/torusguard audit` | Scan repository and report vulnerabilities (no code changes) |
| `/torusguard harden` | Fix approved findings and re-check |
| `/torusguard check <area>` | Audit one area: `secrets`, `frontend-db`, `input`, `auth`, `rate-limit`, `client-exposure`, `platform` |

## Supported Stacks

React/Vite, Next.js, Node.js/Express, Supabase, Firebase, PostgreSQL, MySQL, MongoDB, and common REST APIs.

## Seven Security Areas

1. **Secrets and environment** — No hardcoded keys, proper `.env` handling
2. **Frontend database protection** — No SQL or DB drivers in browser code
3. **Input validation and injection** — Schema validation, parameterized queries
4. **Authentication and authorization** — Secure cookies, IDOR prevention
5. **Rate limiting and abuse** — Login, OTP, contact form protection
6. **Client code exposure** — Source maps, CSP, no secrets in bundles
7. **Platform hardening** — CORS, Helmet, error sanitization, HTTPS

## Quick Start

```text
/torusguard init
/torusguard audit
/torusguard harden
/torusguard check auth
```

## Before / After Example

This repository includes two demo apps:

| App | Description |
|-----|-------------|
| [`examples/vulnerable-express-react-app/`](examples/vulnerable-express-react-app/) | Intentionally insecure React + Vite + Express app |
| [`examples/hardened-express-react-app/`](examples/hardened-express-react-app/) | Secure counterpart with all fixes applied |

Each vulnerability in the demo maps to a reference module under `skills/torusguard/references/`.

## Repository Structure

```
TorusGuard/
├── skills/torusguard/
│   ├── SKILL.md              # Main skill entry point
│   └── references/           # Detailed security modules
├── examples/                   # Vulnerable + hardened demo apps
├── research/                   # Threat rationale and research notes
└── scripts/                    # Validation scripts
```

## Development

```bash
npm run validate
npm run check-examples
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome security rule proposals, false-positive reports, and stack-specific examples.

## Security Reporting

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities in TorusGuard itself.

## Roadmap

- **v0.2** — Machine-readable rule catalog (`TG-001`, etc.)
- **v0.3** — CLI detector (`npx torusguard detect`)
- **v0.4** — CI integration for pull requests
- **v0.5** — AI remediation plans (`/torusguard plan TG-001`)

## License

MIT — see [LICENSE](LICENSE)

## Author

Jenish Lad — TorusGuard v0.1.0
