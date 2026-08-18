# TorusGuard

**Security guardrails for AI-built web apps.**

Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, auth, rate limits, and production exposure.

TorusGuard is a Markdown-first, portable AI-agent skill that helps developers audit and harden AI-built web applications. It is **not** an npm package, hosted service, browser extension, or automated vulnerability scanner.

## What it protects against

- Hardcoded secrets and tracked `.env` files
- Frontend database queries, drivers, and privileged admin keys
- Missing input validation, SQL injection, XSS, and unsafe uploads
- Weak authentication, client-only authorization, and IDOR
- Missing rate limits and unbounded resource consumption
- Public production source maps and sensitive client bundle content
- Unsafe CORS, missing security headers, verbose errors, and missing body limits

## The browser-code truth

**If the browser receives it, users can inspect it.**

DevTools, Inspect Element, and Sources cannot be blocked. TorusGuard keeps secrets, database access, and authorization on trusted server-side code — it does not claim to hide JavaScript or make apps "unhackable."

## Commands

| Command | Purpose | Changes code? |
|---------|---------|---------------|
| `/TorusGuard init` | Create/update `SECURITY.md` and threat model | Docs only |
| `/TorusGuard audit` | Scan 25 rules; structured audit report | No |
| `/TorusGuard harden` | Fix approved findings; re-verify | Yes |
| `/TorusGuard check <area>` | Audit one rule group | No by default |
| `/TorusGuard verify` | Production pre-flight checklist | No |

**Check areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`

## Audit vs harden

| Mode | Behavior |
|------|----------|
| **Audit** | Read-only. Reports findings with rule IDs, severity, confidence, evidence, and verification steps. Never modifies application code. |
| **Harden** | Requires audit first. Applies least-invasive fixes for high-confidence findings. Preserves business behavior; explains breaking changes. |

## Installation

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "TorusGuard"
```

Or copy `skills/TorusGuard/` to your agent skills directory:

| Agent | Path |
|-------|------|
| Cursor (project) | `.cursor/skills/TorusGuard/` |
| Cursor (personal) | `~/.cursor/skills/TorusGuard/` |

## Quick start

```text
/TorusGuard init
/TorusGuard audit
/TorusGuard harden
/TorusGuard verify
/TorusGuard check auth
```

## Rule catalog (v0.2.0)

| Category | Rules | Default severities |
|----------|-------|-------------------|
| Secrets | TG-SEC-001 … 004 | Critical – Medium |
| Database exposure | TG-DB-001 … 003 | Critical – High |
| Input/injection | TG-INPUT-001 … 004 | Critical – High |
| Auth | TG-AUTH-001 … 005 | Critical – High |
| Rate limits | TG-RATE-001 … 003 | High – Medium |
| Client exposure | TG-CLIENT-001 … 002 | High – Medium |
| Platform | TG-PLATFORM-001 … 004 | High – Medium |

Full catalog: [rules/README.md](rules/README.md)

## Supported stacks

React/Vite, Next.js, Node.js/Express, Supabase, Firebase, PostgreSQL, MySQL, MongoDB, and common REST APIs.

## Repository layout

```
TorusGuard/
├── skills/TorusGuard/       # Main installable skill
├── rules/                   # 25 documented security rules
├── templates/               # SECURITY, audit, pre-flight, threat model
├── guides/                  # Stack-specific implementation guides
├── examples/                # Vulnerable + hardened reference apps
├── research/                # Threat rationale notes
└── docs/releases/           # Release notes
```

## Examples

| Example | Description |
|---------|-------------|
| [examples/vulnerable-react-express/](examples/vulnerable-react-express/) | Intentionally insecure — **never deploy** |
| [examples/hardened-react-express/](examples/hardened-react-express/) | Secure patterns mapped to rule IDs |

## Templates and guides

**Templates:** [SECURITY](templates/SECURITY.template.md), [threat model](templates/threat-model.template.md), [audit report](templates/audit-report.template.md), [deployment pre-flight](templates/deployment-preflight.template.md), [endpoint review](templates/api-endpoint-review.template.md), [security exception](templates/security-exception.template.md)

**Guides:** [React/Vite](guides/react-vite-security.md), [Next.js](guides/nextjs-security.md), [Express](guides/express-security.md), [Supabase](guides/supabase-security.md), [Firebase](guides/firebase-security.md)

## Limitations

TorusGuard does not replace penetration testing, compliance certification, or threat modeling. It cannot detect every business-logic flaw or block DevTools. Findings require human judgment for false positives and manual items (RLS, Firebase rules, infrastructure).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Propose rules via issue template; include unsafe/safe examples and verification steps.

## Security reporting

Report TorusGuard vulnerabilities **privately** — see [SECURITY.md](SECURITY.md). Do not use public GitHub Issues for security disclosures.

## Roadmap

| Version | Focus |
|---------|-------|
| v0.1.0 | Core skill and reference modules |
| **v0.2.0** | Structured audit framework — 25 rules, templates, guides, examples |
| v0.3.0 | Optional local detector (not npm-published by default) |
| v1.0.0 | Stable rule catalog and comprehensive examples |

## License

MIT — see [LICENSE](LICENSE)

## Author

Jenish Lad
