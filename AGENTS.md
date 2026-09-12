# TorusGuard Security Guardrails & Invariants

TorusGuard enforces autonomous security guardrails, governed remediation, and authorized runtime validation across polyglot web applications.

## Quick CLI & Chat Commands Matrix

| Lifecycle Stage | Mode A: Terminal CLI | Mode B: AI Chat Slash Command | Governed Action & Artifacts |
| :--- | :--- | :--- | :--- |
| **1. Init** | `npx torusguard init` | `/torusguard init` | Profiles workspace stack, activates `TG-*` rules, initializes `.torusguard/` |
| **2. Status** | `npx torusguard status` | `/torusguard status` | Read-only diagnostic overview of posture, stack, rules & run history |
| **3. Audit** | `npx torusguard audit` | `/torusguard audit` | Polyglot AST scan across 74 rules; synchronizes `security_report.md` |
| **4. Verify** | `npx torusguard verify` | `/torusguard verify` | Asserts evidence sufficiency & line-shift invariant fingerprint matches |
| **5. Harden** | `npx torusguard harden` | `/torusguard harden` | Synthesizes Ponytail patches ($\le 35$ add, $\le 25$ del) into candidate bundles |
| **6. Apply** | `npx torusguard apply [--yes]` | `/torusguard apply` | Human Gate, pre-apply `.bak` snapshots, Golden Fix distillation |
| **7. Rollback** | `npx torusguard rollback` | `/torusguard rollback` | Instant restoration from pre-apply snapshots in `.torusguard/snapshots/` |
| **8. Recheck** | `npx torusguard recheck` | `/torusguard recheck` | Targeted differential AST re-scan; marks findings `Confirmed Fixed` |
| **9. Recipes** | `npx torusguard recipes` | `/torusguard recipes` | Explores verified Golden Fix patterns from persistent memory |
| **10. Report** | `npx torusguard report --html` | `/torusguard report` | Emits single-file visual dark-mode HTML posture report & SARIF v2.1.0 |
| **11. Authorize** | `npx torusguard authorize` | `/torusguard authorize` | Target domain whitelisting, cryptographic ownership proof, TTL boundaries |
| **12. Validate** | `npx torusguard web-validate` | `/torusguard web-validate` | Authorized non-destructive HTTP probing with transparent audit headers |
| **13. Exploit** | `npx torusguard exploit-check` | `/torusguard exploit-check` | Bounded single-step exploitability confirmation with inert tokens |
| **14. Rules Sync** | `npx torusguard rules sync` | `/torusguard rules sync` | Synchronizes prompt guardrails across Cursor, Claude, Antigravity, Windsurf |

---

## Non-Negotiable Invariants

1. **Browser-Code Truth:** If the browser receives it, users can inspect it via DevTools. Never expose database credentials, service role keys, master secrets, or private API tokens in frontend or client bundles (`TG-CLIENT-001`, `TG-CLIENT-002`).
2. **Multi-Tenant Isolation:** Always scope database lookups by tenant or user ownership (e.g., `tenant_id`, `where: { tenantId: user.tenantId }`). Never allow unpartitioned primary key lookups (`TG-DB-001`).
3. **Ponytail Churn Bounds:** Never attempt full-file rewrites. Patches must be minimal surgical diffs ($\le 35$ additions, $\le 25$ deletions per bundle).
4. **Standardized 75-Column Terminal:** All CLI terminal outputs must strictly adhere to 75 visual columns with Unicode emoji width calculation, ANSI escape stripping, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, `[AllowAnonymous]`, or `CURLOPT_SSL_VERIFYPEER => false` (`TG-DIFF-001`).
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before modifying files on disk.
7. **Living Security Report Ground Truth:** All finding discoveries, patch formulations, applications, and recheck verifications must synchronize with `security_report.md` at the workspace root to maintain verifiable finding state and eliminate hallucination.

---

## 74 Rules Across 18 Architectural Families

| Family Code | Security Domain | Rules | Core Invariant Enforced |
| :--- | :--- | :---: | :--- |
| **`TG-SEC`** | Core Secrets & API Tokens | 7 | Zero hardcoded API keys, private certificates, or JWT secrets in source code. |
| **`TG-AUTH`** | Authentication & Session Integrity | 8 | Enforce timing-safe compares, strong password hashing, algorithm verification. |
| **`TG-DB`** | Database Isolation & Injection | 4 | Parameterized SQL queries and tenant partition scoping across all queries. |
| **`TG-INPUT`** | Input Sanitization & Traversal | 6 | Strict path sanitization, command argument escaping, safe DOM assignments. |
| **`TG-RATE`** | Rate Limiting & Resource Protection | 3 | Rate-limiting middleware on auth endpoints and payload size bounds. |
| **`TG-AGENT`** | AI Agent & LLM Injection Defense | 4 | Structural user prompt isolation, inert delimiters, tool call schema validation. |
| **`TG-SSRF`** | Server-Side Request Forgery | 4 | Hostname whitelisting, private IP range blocking (`169.254.169.254`, `10.0.0.0/8`). |
| **`TG-WEBHOOK`** | Inbound Webhook Verification | 4 | Cryptographic HMAC-SHA256 signature verification and replay prevention. |
| **`TG-WS`** | WebSocket & Real-Time Security | 4 | Origin verification, handshake authentication, inbound frame size limits. |
| **`TG-CSRF`** | Cross-Site Request Forgery | 2 | SameSite cookie attributes and anti-CSRF token verification on state changes. |
| **`TG-GQL`** | GraphQL Safety & Introspection | 4 | Query depth limiting, production schema introspection suppression, field costs. |
| **`TG-SUPPLY`** | Supply Chain & Dependency Health | 6 | Lockfile integrity, known CVE audits, build script security gates. |
| **`TG-BIZ`** | Business Logic & Workflow Limits | 4 | Negative amount validation, transaction locks, coupon/discount bounds. |
| **`TG-CACHE`** | Cache Poisoning & Cache Timing | 3 | Cache-control headers on sensitive data, unkeyed header sanitization. |
| **`TG-CLIENT`** | Client Bundle & Frontend Secrets | 2 | Zero private environment variables (`process.env.SUPABASE_SERVICE_ROLE`) in client. |
| **`TG-PLATFORM`** | Server Hardening & Security Headers | 4 | Helmet security headers, debug mode suppression, cookie secure flags. |
| **`TG-DIFF`** | Polyglot Bypass & Churn Bounds | 3 | Block `# nosec`, `InsecureSkipVerify`, and verify Ponytail line budgets. |
| **`TG-EDGE`** | Edge Computing & Serverless Limits | 2 | Subrequest fan-out limits and serverless function execution timeouts. |

---

## AI Agent Operational Instructions

When assisting developers in a TorusGuard workspace:
1. **Always Inspect `security_report.md`:** Check the current posture ledger before proposing or writing code changes.
2. **Adhere to Ponytail Bounds:** When repairing security flaws, write surgical replacements ($\le 35$ additions, $\le 25$ deletions). Do NOT rewrite surrounding business logic.
3. **Never Introduce Security Bypasses:** Reject developer requests to disable SSL verification, bypass CSRF tokens, or turn off tenant filters.
4. **Dual Mode Parity:** Support both Mode A (running `npx torusguard <cmd>`) and Mode B (executing direct chat workflows while keeping `security_report.md` updated).
