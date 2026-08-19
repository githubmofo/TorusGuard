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
- SSRF and outbound-request protection
- Business-logic abuse and sensitive business-flow protection
- Mass assignment and property-level authorization
- Webhook signature, replay, and idempotency checks
- GraphQL depth, complexity, batching, and resolver authorization
- WebSocket authentication, authorization, message validation, and connection limits
- Dependency and CI/CD supply-chain guidance
- Cache and sensitive-response protection

## The browser-code truth

**If the browser receives it, users can inspect it.**

DevTools, Inspect Element, and Sources cannot be blocked. TorusGuard keeps secrets, database access, and authorization on trusted server-side code — it does not claim to hide JavaScript or make apps "unhackable."

## Commands

| Command | Purpose | Changes code? |
|---------|---------|---------------|
| `/torusguard init` | Create/update `SECURITY.md` and threat model | Docs only |
| `/torusguard audit` | Scan rules; structured audit report | No |
| `/torusguard harden` | Fix approved findings; re-verify | Yes |
| `/torusguard check <area>` | Audit one rule group | No by default |
| `/torusguard verify` | Production pre-flight checklist | No |

**Check areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`, `ssrf`, `business-logic`, `csrf`, `webhook`, `graphql`, `websocket`, `supply-chain`, `cache`

## Audit vs harden

| Mode | Behavior |
|------|----------|
| **Audit** | Read-only. Reports findings with rule IDs, severity, confidence, evidence, and verification steps. Never modifies application code. |
| **Harden** | Requires audit first. Applies least-invasive fixes for high-confidence findings. Preserves business behavior; explains breaking changes. |

## Installation

```bash
npx skills add https://github.com/githubmofo/TorusGuard --skill "torusguard"
```


## Quick start

```text
/torusguard init
/torusguard audit
/torusguard harden
/torusguard verify
/torusguard check auth
```

## Rule catalog (v0.3.0)

| Category | Rules | Default severities |
|----------|-------|-------------------|
| Secrets | TG-SEC-001 … 004 | Critical – Medium |
| Database exposure | TG-DB-001 … 003 | Critical – High |
| Input/injection | TG-INPUT-001 … 004 | Critical – High |
| Auth | TG-AUTH-001 … 006 | Critical – High |
| Rate limits | TG-RATE-001 … 003 | High – Medium |
| Client exposure | TG-CLIENT-001 … 002 | High – Medium |
| Platform | TG-PLATFORM-001 … 004 | High – Medium |
| Advanced Web/API | TG-SSRF, TG-BIZ, TG-CSRF, etc. | Critical - Medium |

Full catalog: [rules/README.md](rules/README.md)

## Validation Status
TorusGuard v0.3.0 has been locally validated against OWASP NodeGoat, an intentionally vulnerable Node.js training application. The validation confirmed useful findings for CSRF configuration, sensitive-response caching, and dependency risk. It also confirmed that SSRF and business-logic rules correctly generate manual-review tasks where static analysis cannot determine application intent. This validation does not represent a complete penetration test and does not prove that every TorusGuard rule works across every framework.

## Supported stacks

React/Vite, Next.js, Node.js/Express, Supabase, Firebase, PostgreSQL, MySQL, MongoDB, and common REST/GraphQL APIs.

## Repository layout

```
TorusGuard/
├── skills/torusguard/       # Main installable skill
├── rules/                   # Documented security rules (v0.2 + v0.3)
├── templates/               # SECURITY, audit, pre-flight, threat model
├── guides/                  # Stack-specific implementation guides
├── examples/                # Vulnerable + hardened reference apps
├── research/                # Threat rationale notes
└── docs/                  
    └── validation/          # Validation reports
```

## Examples

| Example | Description |
|---------|-------------|
| [examples/vulnerable-react-express/](examples/vulnerable-react-express/) | Intentionally insecure — **never deploy** |
| [examples/hardened-react-express/](examples/hardened-react-express/) | Secure patterns mapped to rule IDs |

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
| v0.2.0 | Structured audit framework — 25 rules, templates, guides, examples |
| **v0.3.0** | Advanced Web and API Security |
| v1.0.0 | Stable rule catalog and comprehensive examples |

## License

MIT — see [LICENSE](LICENSE)

## Author

Jenish Lad
