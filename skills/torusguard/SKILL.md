---
name: torusguard
description: Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, and APIs.
---

# TorusGuard

**Tagline:** Security guardrails for AI-built web apps.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard is a Markdown-first, portable AI-agent skill. It is not an npm package, hosted service, browser extension, or automated vulnerability scanner. It guides audit and remediation through structured rules, templates, and references.

TorusGuard must never claim it can block DevTools, make an application fully secure, or replace professional penetration testing, code review, compliance work, or threat modeling.

## When to Activate

Use when the user builds or deploys web apps, adds APIs, connects databases, implements auth, reviews security, audits repositories, fixes vulnerabilities, or asks about rate limits, secrets, source maps, or CORS.

## Commands

| Command | Purpose | Changes code? |
|---------|---------|---------------|
| `/torusguard init` | Create/update project `SECURITY.md` and threat model | Docs only |
| `/torusguard audit` | Scan all 25 rules; produce audit report | No |
| `/torusguard harden` | Fix approved findings; re-verify | Yes |
| `/torusguard check <area>` | Audit one rule group | No by default |
| `/torusguard verify` | Production pre-flight checklist | No |

**Check areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`

## Mandatory Security Read

Before editing application code, print:

```text
Security Read
- Stack: [frontend, backend, database, deployment]
- Authentication: [mechanism]
- Public surfaces: [routes]
- Sensitive assets: [data types]
- Trust boundaries: [browser -> API -> DB -> third parties]
- Relevant modules: [secrets, database, input, auth, rate-limit, client, platform]
- Auto-verifiable vs manual-review: [list]
```

In existing repositories: **audit before hardening**. Do not rewrite unrelated product UI or features.

## Rule Catalog (v0.2.0)

Load rule details from `rules/` when auditing or hardening.

| Area | Rule IDs |
|------|----------|
| Secrets | TG-SEC-001 … TG-SEC-004 |
| Database exposure | TG-DB-001 … TG-DB-003 |
| Input/injection | TG-INPUT-001 … TG-INPUT-004 |
| Auth | TG-AUTH-001 … TG-AUTH-005 |
| Rate limits | TG-RATE-001 … TG-RATE-003 |
| Client exposure | TG-CLIENT-001 … TG-CLIENT-002 |
| Platform | TG-PLATFORM-001 … TG-PLATFORM-004 |

Full catalog: [rules/README.md](../../rules/README.md)

## Reference Modules

Load only relevant references during audit/harden:

| Area | Reference | Rules |
|------|-----------|-------|
| secrets | [secrets-and-config.md](references/secrets-and-config.md) | TG-SEC-* |
| database | [frontend-no-db.md](references/frontend-no-db.md) | TG-DB-* |
| input | [input-and-injection.md](references/input-and-injection.md) | TG-INPUT-* |
| auth | [auth-and-sessions.md](references/auth-and-sessions.md) | TG-AUTH-* |
| rate-limit | [rate-limit-and-abuse.md](references/rate-limit-and-abuse.md) | TG-RATE-* |
| client | [client-code-exposure.md](references/client-code-exposure.md) | TG-CLIENT-* |
| platform | [platform-hardening.md](references/platform-hardening.md) | TG-PLATFORM-* |

## Templates

| Template | Use |
|----------|-----|
| [SECURITY.template.md](../../templates/SECURITY.template.md) | `/torusguard init` |
| [threat-model.template.md](../../templates/threat-model.template.md) | `/torusguard init` |
| [audit-report.template.md](../../templates/audit-report.template.md) | `/torusguard audit` |
| [deployment-preflight.template.md](../../templates/deployment-preflight.template.md) | `/torusguard verify` |
| [api-endpoint-review.template.md](../../templates/api-endpoint-review.template.md) | Endpoint review |
| [security-exception.template.md](../../templates/security-exception.template.md) | Documented exceptions |

## Workflow: `/torusguard init`

1. Inspect repository **without modifying application code**
2. Detect frontend, backend, database, auth, deployment, public endpoints, sensitive assets
3. Generate root `SECURITY.md` from [SECURITY.template.md](../../templates/SECURITY.template.md) if missing; if present, update only stale/missing sections
4. Create compact threat model from [threat-model.template.md](../../templates/threat-model.template.md)
5. Never include actual secrets in generated files

## Workflow: `/torusguard audit`

1. Read project `SECURITY.md` if present
2. Detect stack; load relevant references and all 25 rules where applicable
3. **Do not change source code**
4. Produce report using [audit-report.template.md](../../templates/audit-report.template.md)

Each finding must include: **rule ID, severity, confidence** (confirmed/likely/manual), **location, evidence, security impact, remediation, verification step**.

Separate: **confirmed findings**, **likely findings**, **passed checks**, **manual-review items**.

End with pre-flight result: **FAIL**, **PASS WITH WARNINGS**, or **PASS**.

## Workflow: `/torusguard harden`

1. Run or read latest audit
2. Present remediation plan grouped by severity
3. Modify code only for relevant, safe, high-confidence findings
4. Preserve business behavior and public APIs; explain breaking changes first
5. Add/update tests where test setup exists
6. Re-run relevant checks
7. Produce remediation summary: fixed rule IDs + remaining manual-review items
8. Never expose real secrets in output, code, docs, or logs

## Workflow: `/torusguard check <area>`

Audit only the selected rule group. Do not modify source by default. Report pass/fail and manual verification instructions.

| Area | Rules |
|------|-------|
| secrets | TG-SEC-001 … 004 |
| database | TG-DB-001 … 003 |
| input | TG-INPUT-001 … 004 |
| auth | TG-AUTH-001 … 005 |
| rate-limit | TG-RATE-001 … 003 |
| client | TG-CLIENT-001 … 002 |
| platform | TG-PLATFORM-001 … 004 |

## Workflow: `/torusguard verify`

1. Run [deployment-preflight.template.md](../../templates/deployment-preflight.template.md)
2. Unresolved **Critical** or **High** findings → **FAIL**
3. Do not claim "fully secure"
4. State browser source cannot be hidden; authorization must remain server-side

## Hard Bans

Never produce or approve:

1. Hardcoded secrets, DB URLs, JWT signing keys, or API keys in tracked source
2. Sensitive values in `VITE_*`, `NEXT_PUBLIC_*`, `REACT_APP_*` or equivalent
3. SQL queries or DB driver imports in browser/client code
4. SQL string concatenation with request input
5. `eval`, `Function()`, or shell execution with untrusted input
6. Unsanitized `dangerouslySetInnerHTML` with user content
7. Client-only authorization or trust in client `userId`/`role`/`isAdmin`
8. MD5/SHA1/plaintext password storage
9. `Access-Control-Allow-Origin: *` with credentials
10. Production stack traces or raw DB errors to clients
11. Logging passwords, tokens, session IDs, or full auth headers

## IDOR Test

For every sensitive object route: **Can User A change the resource ID and access User B's resource?** If yes → fails TG-AUTH-003.

## Browser Code Truth

State explicitly when relevant:

- DevTools and Inspect Element cannot be blocked
- Browser-delivered JavaScript is public
- Disable public production source maps; upload privately to monitoring if needed
- Obfuscation is not a security control

## Framework Guides

- [React/Vite](../../guides/react-vite-security.md)
- [Next.js](../../guides/nextjs-security.md)
- [Express](../../guides/express-security.md)
- [Supabase](../../guides/supabase-security.md)
- [Firebase](../../guides/firebase-security.md)

## Examples

- [vulnerable-react-express](../../examples/vulnerable-react-express/) — intentionally insecure; never deploy
- [hardened-react-express](../../examples/hardened-react-express/) — secure patterns

## What TorusGuard Does Not Do

- Block DevTools or hide browser JavaScript
- Guarantee compliance (PCI, HIPAA, SOC 2, GDPR)
- Detect every business-logic flaw
- Replace penetration testing or threat modeling
- Provide hosted dashboards, telemetry, or SaaS
