---
name: torusguard
description: Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, auth, rate limits, and production exposure.
---

# TorusGuard

TorusGuard is a portable AI-agent security skill for AI-built web applications. It audits and hardens common security issues including hardcoded secrets, frontend database queries or admin keys, unsafe input validation, SQL/NoSQL injection, authentication and authorization flaws, IDOR, missing rate limits, unsafe CORS, public production source maps, and insecure deployment configuration.

**Core principle:** Anything sent to the browser is public. DevTools cannot be blocked. Security comes from server-side enforcement, not hiding client code.

## When to Activate

Use this skill when the user:

- Builds a full-stack web application
- Adds login, signup, reset-password, OTP, payment, contact, upload, or admin features
- Adds an API endpoint or connects a database
- Uses Supabase, Firebase, PostgreSQL, MySQL, MongoDB, Prisma, Drizzle, or Sequelize
- Deploys an application or asks to review, audit, or fix security
- Asks about rate limiting, secrets, source maps, or CORS

## Commands

| Command | Purpose | Changes code? |
|---------|---------|---------------|
| `/torusguard init` | Understand project and create `SECURITY.md` | Yes (docs only) |
| `/torusguard audit` | Scan repository and report vulnerabilities | No |
| `/torusguard harden` | Fix approved findings and re-check | Yes |
| `/torusguard check <area>` | Audit one area: `secrets`, `frontend-db`, `input`, `auth`, `rate-limit`, `client-exposure`, `platform` | No by default |

## Mandatory Security Read

Before editing application code, produce this summary and wait until stack/auth/routes are identified:

```text
Security Read
- Stack: [frontend, backend, database]
- Authentication: [mechanism]
- Public surfaces: [routes]
- Sensitive assets: [data types]
- Trust boundary: browser -> API -> database
- High-risk areas: [login abuse, IDOR, uploads, etc.]
```

Identify: frontend framework, backend framework, database, auth mechanism, deployment config, public routes, sensitive routes, and data types handled.

## Security Modules

Load detailed rules only when auditing or hardening that area:

| Module | Reference |
|--------|-----------|
| Secrets and environment | [secrets-and-config.md](references/secrets-and-config.md) |
| Frontend database protection | [frontend-no-db.md](references/frontend-no-db.md) |
| Input validation and injection | [input-and-injection.md](references/input-and-injection.md) |
| Auth, sessions, authorization | [auth-and-sessions.md](references/auth-and-sessions.md) |
| Rate limiting and abuse | [rate-limit-and-abuse.md](references/rate-limit-and-abuse.md) |
| Client code exposure | [client-code-exposure.md](references/client-code-exposure.md) |
| Platform and HTTP hardening | [platform-hardening.md](references/platform-hardening.md) |

## Hard Bans

Never produce or approve code that:

1. Hardcodes database URLs, JWT secrets, passwords, or API keys in source
2. Exposes service-role or admin credentials to the browser
3. Runs SQL queries or imports DB drivers in frontend files
4. Concatenates user input into SQL strings
5. Uses `eval`, `Function()`, or shell execution with untrusted input
6. Renders unsanitized user HTML via `dangerouslySetInnerHTML`
7. Stores auth tokens in `localStorage` without documented tradeoffs
8. Checks roles or authorization only in frontend routing
9. Trusts client-provided `userId`, `role`, or `isAdmin`
10. Uses MD5/SHA1/plaintext for passwords
11. Sets `Access-Control-Allow-Origin: *` with credentials
12. Returns production stack traces or raw DB errors to clients
13. Logs passwords, tokens, session IDs, or full auth headers
14. Treats frontend env vars (`VITE_*`, `NEXT_PUBLIC_*`, `REACT_APP_*`) as secret

## Workflow: `/torusguard init`

1. Detect project structure, frameworks, env files, and deployment config
2. Identify public endpoints and sensitive assets
3. Map trust boundaries
4. Create root-level `SECURITY.md` using the template below
5. Do **not** alter application code

```markdown
# Security Context

## Stack
- Frontend:
- Backend:
- Database:
- Authentication:
- Hosting:

## Sensitive Assets
- User credentials:
- Personal data:
- Payment data:
- API tokens:
- Files:

## Public Endpoints
- Method and path:

## Trust Boundaries
- Browser -> API
- API -> Database
- API -> Third-party services

## Security Controls
- Input validation:
- Authentication:
- Authorization:
- Rate limiting:
- Security headers:
- Logging:

## Known Risks / Follow-ups
- [ ]
```

## Workflow: `/torusguard audit`

1. Read project `SECURITY.md` if it exists
2. Detect stack and scan all seven modules
3. Report findings — **do not change code**
4. Include file path and line number when available
5. Assign risk: Critical, High, Medium, Low, Informational
6. Distinguish verified, not found, and needs manual review

```markdown
# TorusGuard Audit Report

## Security Read
- Stack:
- Auth:
- Database:
- Public routes:

## Critical Findings
| ID | Finding | Location | Risk | Recommended Fix |
|---|---|---|---|---|

## High Findings
| ID | Finding | Location | Risk | Recommended Fix |
|---|---|---|---|---|

## Passed Checks
- [x] Example passed check

## Manual Review Required
- Example: Verify Supabase RLS policies

## Pre-Flight Result
FAIL / PASS WITH WARNINGS / PASS
```

## Workflow: `/torusguard harden`

1. Run or read the latest audit
2. Present exact proposed changes before applying
3. Apply least-invasive safe fixes only
4. Do not remove business features or replace entire auth systems without approval
5. Do not change DB schema unless necessary
6. Explain any new dependency
7. Re-run audit and report unresolved risks

## Workflow: `/torusguard check <area>`

Audit a single module. Valid areas: `secrets`, `frontend-db`, `input`, `auth`, `rate-limit`, `client-exposure`, `platform`.

Use the corresponding reference file. Output a focused report for that area only.

## Pre-Flight Release Gate

**FAIL** deployment pre-flight if any of these are true:

- [ ] Real secret, API key, password, service-role key, or database URL in tracked source
- [ ] Database query, DB driver, or privileged admin SDK in frontend code
- [ ] Public POST endpoint with no auth, rate limit, or explicit justification
- [ ] User input reaches SQL via string concatenation
- [ ] User input reaches HTML rendering without appropriate handling
- [ ] Passwords use plaintext, MD5, or SHA1
- [ ] Authorization happens only in frontend
- [ ] Sensitive resource route lacks ownership or role checks
- [ ] Cookie auth lacks appropriate CSRF protection
- [ ] CORS uses wildcard origin with credentials
- [ ] Public production source maps expose original source unintentionally
- [ ] Production errors expose stack traces or internal secrets
- [ ] Uploads lack authorization, type checks, or size limits

## IDOR Test

For every sensitive route, ask:

> Can User A change the resource ID in this request and access User B's resource?

If yes, the route **fails** the audit.

## Browser Code Truth

State explicitly when relevant:

- DevTools and Inspect Element cannot be blocked
- Browser-delivered JavaScript is public
- Disable public production source maps; upload privately to monitoring tools if needed
- Move secrets, authorization, and database logic server-side

## Supported Stacks

React/Vite, Next.js, Node.js/Express, Supabase, Firebase, PostgreSQL, MySQL, MongoDB, and common REST APIs. Load framework-specific guidance from reference modules; do not apply Express middleware to Firebase-only apps.

## What TorusGuard Does Not Do

- Replace professional penetration testing
- Guarantee PCI-DSS, HIPAA, ISO 27001, SOC 2, or GDPR compliance
- Detect every business-logic vulnerability
- Block DevTools or obfuscate frontend code as primary security
- Provide hosted dashboards or SaaS

## Examples

See repository `examples/vulnerable-express-react-app/` and `examples/hardened-express-react-app/` for before/after patterns.
