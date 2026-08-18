# TorusGuard Framework Guides

Stack-specific security checklists and patterns for TorusGuard audits and hardening.

| Guide | Stack | Primary rules |
|-------|-------|---------------|
| [react-vite-security.md](react-vite-security.md) | React + Vite | TG-SEC-002, TG-DB-001, TG-CLIENT-001, TG-CLIENT-002 |
| [nextjs-security.md](nextjs-security.md) | Next.js App/Pages Router | TG-SEC-002, TG-AUTH-002, TG-CLIENT-001 |
| [express-security.md](express-security.md) | Node.js + Express | TG-INPUT-001, TG-PLATFORM-001 … 004, TG-RATE-* |
| [supabase-security.md](supabase-security.md) | Supabase | TG-DB-002, TG-DB-003, TG-AUTH-003 |
| [firebase-security.md](firebase-security.md) | Firebase | TG-DB-003, TG-AUTH-002, TG-AUTH-003 |

Use with `/torusguard check <area>` and the matching reference module in `skills/torusguard/references/`.
