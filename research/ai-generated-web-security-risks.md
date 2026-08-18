# AI-Generated Web Security Risks

Research notes on common security mistakes in AI-generated web applications.

## Why AI Agents Create Insecure Code

1. **Speed over safety** — Agents optimize for working demos, not production hardening
2. **Tutorial patterns** — Training data includes outdated examples (MD5, localStorage JWT)
3. **Monolithic generation** — DB queries placed in React components for convenience
4. **Missing threat model** — Agents rarely ask "what is public vs trusted?"
5. **Copy-paste secrets** — Placeholder values left in code or committed `.env` files

## Top 15 Risks (by frequency in AI-generated apps)

| Rank | Risk | Module |
|------|------|--------|
| 1 | Hardcoded secrets and API keys | secrets-and-config |
| 2 | Missing input validation | input-and-injection |
| 3 | SQL injection via string concatenation | input-and-injection |
| 4 | No authorization / IDOR | auth-and-sessions |
| 5 | Database access in frontend | frontend-no-db |
| 6 | Missing rate limits on auth endpoints | rate-limit-and-abuse |
| 7 | JWT in localStorage | auth-and-sessions |
| 8 | CORS wildcard with credentials | platform-hardening |
| 9 | Public production source maps | client-code-exposure |
| 10 | Plaintext or weak password hashing | auth-and-sessions |
| 11 | Verbose error messages / stack traces | platform-hardening |
| 12 | Missing security headers | platform-hardening |
| 13 | Secrets in `VITE_*` / `NEXT_PUBLIC_*` env vars | secrets-and-config |
| 14 | No file upload restrictions | input-and-injection |
| 15 | Account enumeration via login errors | auth-and-sessions |

## Browser Exposure Truth

AI agents sometimes suggest "hiding" API keys, admin routes, or business logic in frontend code. This is ineffective:

- All JavaScript sent to the browser can be read
- DevTools cannot be disabled by application code
- Minification and obfuscation are not security controls
- Source maps restore original TypeScript/React source

**Correct approach:** Treat browser code as public; enforce security server-side.

## Agent Instruction Gaps

Standard agent prompts rarely include:

- Pre-flight security checklist before code generation
- Distinction between audit mode (read-only) and harden mode (write)
- Framework-specific secure defaults
- Explicit "hard bans" that fail closed
- IDOR testing requirement for resource routes

TorusGuard addresses these gaps through structured skill commands and reference modules.

## References

- OWASP Top 10 (2021)
- OWASP ASVS
- CWE/SANS Top 25
- Supabase RLS documentation
- Firebase Security Rules documentation
