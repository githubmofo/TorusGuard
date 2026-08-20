---
name: torusguard
description: Security guardrails for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, and APIs.
---

# TorusGuard

**Tagline:** Security guardrails for AI-built web apps.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard is a Markdown-first, portable AI-agent skill. It is not an npm package, hosted service, browser extension, or automated vulnerability scanner. It guides audit and remediation through structured rules, templates, and human-friendly references.

TorusGuard must never claim it can block DevTools, make an application fully secure, or replace professional penetration testing, code review, compliance work, or threat modeling.

## When to Activate

Use when the user builds or deploys web apps, adds APIs, connects databases, implements auth, reviews security, audits repositories, fixes vulnerabilities, or asks about rate limits, secrets, source maps, SSRF, webhooks, or CORS.

## Commands

| Command | Purpose | Changes code? |
|---------|---------|:---:|
| `/torusguard init` | Create/update project `SECURITY.md` and readable threat model | Docs only |
| `/torusguard audit` | Scan codebase; produce a clean, human-readable audit report | No |
| `/torusguard harden` | Fix approved findings; re-verify | Yes |
| `/torusguard check <area>` | Audit one rule group | No by default |
| `/torusguard verify` | Production pre-flight checklist | No |

**Check areas:** `secrets`, `database`, `input`, `auth`, `rate-limit`, `client`, `platform`, `ssrf`, `business-logic`, `csrf`, `webhook`, `graphql`, `websocket`, `supply-chain`, `cache`

---

## 🌟 Human-First Output Standard (Critical)

**All files and messages generated for the developer must be human-first and easy to read.**
Avoid dense, unreadable multi-column tables. Every generated report must prioritize clear visual hierarchy:

1. **Executive Summary at Top:** Traffic-light posture indicator (`🔴 Action Required` / `🟡 Warnings` / `🟢 Ready`), finding count summary table, and a 2-3 sentence plain-English status overview.
2. **Card-Style Finding Layout:** Present each finding as a clean section with:
   - Clear Title & Severity Emoji (`🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`)
   - Exact Location (`file:line`) and Rule ID (`TG-...`)
   - **The Risk in Plain English:** Explain what an attacker could do without confusing jargon.
   - **Evidence & Fix Snippet:** Show the exact offending code and the safe **Before / After** fix.
3. **Clear Next Steps:** Simple, prioritized 1-2-3 remediation steps so the user knows what to do next.

---

## Mandatory Security Read

Before editing application code, print a concise security read in chat:

```text
🛡️ TorusGuard Security Read
• Stack: [Frontend, Backend, Database, Host]
• Auth & Trust Boundaries: [Auth mechanism, public vs protected endpoints]
• Key Assets: [Secrets, user data, admin actions]
• Audit Scope: [Relevant rule categories]
```

In existing repositories: **audit before hardening**. Do not rewrite unrelated product UI or features.

---

## Workflow: `/torusguard init`

1. Inspect repository **without modifying application code**.
2. Detect stack (frontend, backend, database, auth, deployment).
3. Generate root `SECURITY.md` from `templates/SECURITY.template.md` (clean responsible disclosure policy).
4. Create a clean, readable threat model in `docs/threat-model.md` using `templates/threat-model.template.md`.
5. Never include real secrets or environment values in generated files.

---

## Workflow: `/torusguard audit`

1. Read project `SECURITY.md` and codebase.
2. Scan against TorusGuard rules (Secrets, Auth, Input, SSRF, CSRF, Database, Webhooks, etc.).
3. **Do not modify source code** (100% read-only).
4. Produce a clean, human-first `audit-report.md` using `templates/audit-report.template.md`.
5. Group findings by severity and include plain-English risk descriptions + concrete code fix examples.
6. Provide a prioritized remediation order and prompt the user: *"Run `/torusguard harden` to automatically apply recommended fixes."*

---

## Workflow: `/torusguard harden`

1. Read the latest `audit-report.md` (or run a quick audit if none exists).
2. Present a clear, concise remediation plan to the developer.
3. Apply least-invasive, safe fixes for confirmed high-confidence findings.
4. Preserve existing application logic, routes, and business behavior.
5. Explain any necessary breaking changes or dependency upgrades clearly before applying.
6. Re-verify the fixed files and print a clean summary of resolved issues and remaining manual tasks.

---

## Workflow: `/torusguard verify`

1. Run pre-flight checklist against `templates/deployment-preflight.template.md`.
2. Verify:
   - No `.env` or secret keys are tracked in git.
   - Public production source maps are disabled.
   - Server-side validation and security headers are in place.
   - Critical routes enforce authentication and authorization.
3. Output a clear **PASS**, **PASS WITH WARNINGS**, or **FAIL** decision with actionable bullet points.

---

## Evidence Confidence Levels
- **Confirmed**: Directly observed in source code or configuration.
- **Likely**: Strong indicators present; runtime/deployment verification recommended.
- **Manual review**: Requires developer business context (e.g. business workflow intent, cloud IAM).
- **Informational**: Hardening recommendation or best practice.

## Rules of Engagement Constraints
- Never report an outdated dependency as exploitable without an advisory or audit result.
- Never report cache vulnerability solely because a middleware call is commented out; inspect actual response headers.
- Never call SSRF confirmed merely because a project uses an HTTP client.
- Never call business-logic abuse confirmed without identifying a concrete workflow and abuse path.
- Never claim that a static Markdown skill executed a real scan unless an actual scanner was used.
- Never include sensitive values from the target repository in an audit report.
