# Input Validation and Injection Prevention

## When to load

Load during `/TorusGuard check input`, API route reviews, or upload/webhook implementation.

## Linked rules

- [TG-INPUT-001](../../rules/TG-INPUT-001-missing-server-validation.md) — Missing Server Validation (High)
- [TG-INPUT-002](../../rules/TG-INPUT-002-raw-sql-concatenation.md) — Raw SQL Concatenation (Critical)
- [TG-INPUT-003](../../rules/TG-INPUT-003-unsafe-html-or-code-execution.md) — Unsafe HTML/Code Execution (High)
- [TG-INPUT-004](../../rules/TG-INPUT-004-unrestricted-file-upload.md) — Unrestricted File Upload (High)

## Hard bans

- No raw SQL concatenation with request input
- No `eval`, `Function()`, or shell execution with untrusted input
- No unsanitized user HTML via `dangerouslySetInnerHTML`
- No file upload without size, type, and authorization checks
- No trust in `req.body.role`, `isAdmin`, or `userId`

## Safe defaults

- Validate all external input on the server: body, query, params, headers, cookies, webhooks, uploads
- Treat third-party API and **LLM output** as untrusted
- Use Zod, Joi, Yup, or Ajv schemas at route entry
- Parameterized queries or safe ORM APIs only
- Redirect URLs must use allowlists
- Uploads: MIME allowlist, size cap, server-generated filenames, storage outside web root

## Audit checklist

- [ ] Every API route validates input (TG-INPUT-001)
- [ ] No concatenated SQL (TG-INPUT-002)
- [ ] No unsafe HTML/code execution (TG-INPUT-003)
- [ ] Upload routes restricted (TG-INPUT-004)

## Framework notes

- **Express** — validation middleware before handlers
- **Next.js** — validate in route handlers and Server Actions
- **Supabase** — Edge Functions validate before privileged ops

## Manual review

- Business-logic validation beyond schema (e.g., cross-field rules)
- NoSQL injection patterns in MongoDB query builders

## Related rules

TG-AUTH-002, TG-RATE-003, TG-PLATFORM-004
