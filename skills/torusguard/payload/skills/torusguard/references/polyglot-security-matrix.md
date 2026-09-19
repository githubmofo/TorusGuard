# TorusGuard Universal Polyglot Security Matrix

> **Loaded When:** Any language or framework is detected. Maps universal security invariants across major programming language ecosystems.

---

## 🛡️ Cross-Language Invariant Mappings

| Rule Family | Python | TypeScript / Node.js | Go | Rust | Java / Kotlin | C# / .NET |
|---|---|---|---|---|---|---|
| **TG-SEC (Secrets)** | `os.environ["KEY"]` | `process.env.KEY` | `os.Getenv("KEY")` | `std::env::var("KEY")` | `System.getenv("KEY")` | `Environment.GetEnvironmentVariable()` |
| **TG-DB (SQL Injection)** | `%s` / ORM bound | `$1` / Prisma / Drizzle | `?` / `$1` / GORM `?` | `sqlx::query!` / Diesel | Named parameters `:param` | `@p0` / `FromSqlInterpolated` |
| **TG-DB-004 (Tenant Scope)** | `.filter(tenant=...)` | `where: { tenantId }` | `.Where("tenant_id = ?", tid)` | `filter(tenant_id.eq(tid))` | `WHERE e.tenantId = :tid` | `.Where(x => x.TenantId == tid)` |
| **TG-AUTH (Access Control)** | `@login_required` / Depends | Middleware auth / Guards | Middleware handlers | Tower layer / extractors | `@PreAuthorize` / Spring Sec | `[Authorize]` attributes |
| **TG-CSRF (Request Forgery)** | CSRF Middleware | SameSite / csurf | Gorilla CSRF | Anti-CSRF token middleware | Spring Security CSRF | `[ValidateAntiForgeryToken]` |
| **TG-DIFF (Bypass Comments)** | No `# nosec` | No `// nosec` | No `/* nosec */` | No `#![allow(unsafe)]` | No `@SuppressWarnings` | No pragma disable |
| **TG-DIFF (TLS Verification)** | No `verify=False` | No `rejectUnauthorized:false` | No `InsecureSkipVerify: true` | No `danger_accept_invalid_certs`| No `TrustAllStrategy` | No `DangerousAcceptAny...` |

---

## 🚀 Polyglot Hardening Rules of Thumb

1. **Parameterize Everything:** Never concatenate raw user input into SQL, shell commands, LDAP filters, or template strings, regardless of language.
2. **Fail Closed on Auth:** Default all endpoints to authenticated; explicitly mark public routes rather than remembering to protect private ones.
3. **Strict Bounds:** Keep remediation diffs minimal ($\le 35$ additions, $\le 25$ deletions) to ensure auditability across all codebases.
