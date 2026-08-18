# Secrets and Environment Configuration

## When to load

Load during `/TorusGuard check secrets`, secret-related audits, or before adding environment variables, CI config, or deployment secrets.

## Linked rules

- [TG-SEC-001](../../rules/TG-SEC-001-hardcoded-secrets.md) — Hardcoded Secret (Critical)
- [TG-SEC-002](../../rules/TG-SEC-002-public-environment-secrets.md) — Public Environment Secret (Critical)
- [TG-SEC-003](../../rules/TG-SEC-003-tracked-env-file.md) — Tracked Environment File (High)
- [TG-SEC-004](../../rules/TG-SEC-004-sensitive-logging.md) — Sensitive Data Logging (Medium)

## Hard bans

- Never hardcode database URLs, JWT secrets, passwords, or API keys in source
- Never expose service-role or admin credentials to the browser
- Never put secrets in `VITE_*`, `NEXT_PUBLIC_*`, or `REACT_APP_*` variables
- Never log passwords, tokens, session IDs, API keys, or full authorization headers
- Never commit `.env`, credentials JSON, or private key files

## Frontend env prefixes are public

| Prefix | Reaches browser? |
|--------|------------------|
| `VITE_` | Yes |
| `NEXT_PUBLIC_` | Yes |
| `REACT_APP_` | Yes |
| (no prefix) | Server only |

Only intentionally public configuration may use client prefixes.

## Safe defaults

1. Server-only env for all secrets
2. `.env` in `.gitignore`
3. `.env.example` with placeholder values only
4. Rotate/revoke any discovered leaked secret immediately
5. Separate dev/test/production secret stores where applicable

## Audit checklist

- [ ] No real secrets in tracked source (TG-SEC-001)
- [ ] No sensitive values in public env vars (TG-SEC-002)
- [ ] `.env` not tracked by Git (TG-SEC-003)
- [ ] Logs redact auth material (TG-SEC-004)
- [ ] `.env.example` exists with safe placeholders

## Framework notes

- **Vite/CRA/Next public vars** — treat as published in the client bundle
- **Supabase** — anon key in browser OK; service-role server-only
- **Firebase** — client config public; Admin SDK credentials server-only
- **CI/CD** — use platform secret stores, not plaintext in workflow files

## Manual review

- Verify secret rotation after any exposure
- Review CI logs for accidental secret echo
- Confirm production secrets differ from development

## Related rules

TG-DB-002, TG-DB-003, TG-CLIENT-002
