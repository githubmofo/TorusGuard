# Awesome TorusGuard Security Invariants [![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![TorusGuard v2.2.0](https://img.shields.io/badge/TorusGuard-v2.2.0-00DC82.svg)](https://github.com/githubmofo/TorusGuard) [![Rules: 88](https://img.shields.io/badge/Rules-88-blue.svg)](https://github.com/githubmofo/TorusGuard) [![Ponytail Bounds](https://img.shields.io/badge/Ponytail%20Bounds-%E2%89%A435%20add%20%2F%20%E2%89%A425%20del-blueviolet.svg)](https://github.com/githubmofo/TorusGuard)

> A curated, standardized catalog of autonomous security invariants, zero-regression guardrails, and verified Golden Fix recipes for polyglot web applications built with AI agents.
> 
> *Inspired by [sindresorhus/awesome](https://github.com/sindresorhus/awesome) and [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x).*

---

## Contents

- [The TorusGuard Philosophy](#the-torusguard-philosophy)
- [Rule Taxonomy & Architectural Families](#rule-taxonomy--architectural-families)
  - [TG-SEC — Secrets & Token Hygiene (7 rules)](#tg-sec--secrets--token-hygiene)
  - [TG-AUTH — Authentication & Session Integrity (8 rules)](#tg-auth--authentication--session-integrity)
  - [TG-DB — Multi-Tenant Isolation & SQL Injection (4 rules)](#tg-db--multi-tenant-isolation--sql-injection)
  - [TG-INPUT — Traversal & Command Injection (8 rules)](#tg-input--traversal--command-injection)
  - [TG-RATE — Rate Limiting & Resource Protection (3 rules)](#tg-rate--rate-limiting--resource-protection)
  - [TG-AGENT — AI Agent & Prompt Injection Defense (4 rules)](#tg-agent--ai-agent--prompt-injection-defense)
  - [TG-SSRF — Server-Side Request Forgery Boundaries (4 rules)](#tg-ssrf--server-side-request-forgery-boundaries)
  - [TG-WEBHOOK — Inbound Webhook Verification (4 rules)](#tg-webhook--inbound-webhook-verification)
  - [TG-WS — WebSocket & Real-Time Integrity (4 rules)](#tg-ws--websocket--real-time-integrity)
  - [TG-CSRF — Cross-Site Request Forgery (2 rules)](#tg-csrf--cross-site-request-forgery)
  - [TG-GQL — GraphQL Safety & Introspection (4 rules)](#tg-gql--graphql-safety--introspection)
  - [TG-SUPPLY — Supply Chain & Dependency Health (6 rules)](#tg-supply--supply-chain--dependency-health)
  - [TG-BIZ — Business Logic & Transaction Bounds (4 rules)](#tg-biz--business-logic--transaction-bounds)
  - [TG-CACHE — Cache Poisoning & Timing Safety (3 rules)](#tg-cache--cache-poisoning--timing-safety)
  - [TG-CLIENT — Client Bundle Leakage Guard (2 rules)](#tg-client--client-bundle-leakage-guard)
  - [TG-PLATFORM — Server & Header Hardening (4 rules)](#tg-platform--server--header-hardening)
  - [TG-DIFF — Bypass Guard & Churn Bounds (3 rules)](#tg-diff--bypass-guard--churn-bounds)
  - [TG-EDGE — Edge & Serverless Execution Bounds (2 rules)](#tg-edge--edge--serverless-execution-bounds)
  - [TG-CONT — Container Hardening & Docker Safety (4 rules)](#tg-cont--container-hardening--docker-safety)
  - [TG-GIT — Git Commit Secret Mining (3 rules)](#tg-git--git-commit-secret-mining)
  - [TG-REDOS — Regular Expression Complexity & ReDoS (2 rules)](#tg-redos--regular-expression-complexity--redos)
  - [TG-RAG — RAG Pipeline & Vector Scoping (3 rules)](#tg-rag--rag-pipeline--vector-scoping)
- [How to Explore in CLI & Chat](#how-to-explore-in-cli--chat)
- [Contributing New Rules](#contributing-new-rules)

---

## The TorusGuard Philosophy

1. **Browser-Code Truth:** If the client receives it, developers inspect it. Never expose service role keys or database credentials to client bundles (`TG-CLIENT-001`).
2. **Multi-Tenant Isolation by Default:** Every database query must be partition-scoped (`tenant_id`). Primary-key only lookups are strictly prohibited (`TG-DB-001`).
3. **Ponytail Churn Bounds:** Automated fixes must be surgical minimal diffs (≤35 additions, ≤25 deletions per bundle). Full-file rewrites are prohibited (`TG-DIFF-003`).
4. **Zero Security Bypasses:** Linter suppression bypasses like `# nosec`, `InsecureSkipVerify: true`, or `csrf().disable()` are permanently blocked (`TG-DIFF-001`).
5. **Living Posture Ledger:** Finding ground truth is recorded in `security_report.md` at workspace root.

---

## Rule Taxonomy & Architectural Families

### TG-SEC — Secrets & Token Hygiene
*Eliminates hardcoded API keys, private certificates, and unrotated credentials from source code.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-SEC-001` | Hardcoded API Key or Secret Token in Source | `Critical` | CWE-798 | +4 / -1 |
| `TG-SEC-002` | Unencrypted Cloud Access Credentials (AWS/GCP/Azure) | `Critical` | CWE-522 | +3 / -1 |
| `TG-SEC-003` | Leaked Personal Access Token (PAT) | `Critical` | CWE-798 | +3 / -1 |
| `TG-SEC-004` | Database URI Containing Plaintext Password | `High` | CWE-256 | +4 / -1 |
| `TG-SEC-005` | Private Cryptographic Key Block Header in Code | `Critical` | CWE-321 | +3 / -1 |
| `TG-SEC-006` | Hardcoded JWT Secret String | `High` | CWE-321 | +3 / -1 |
| `TG-SEC-007` | Generic Hardcoded Password Assignment | `High` | CWE-259 | +4 / -1 |

---

### TG-AUTH — Authentication & Session Integrity
*Enforces timing-attack resilience, strong password hashing, algorithm pinning, and secure cookies.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-AUTH-001` | Timing-Unsafe Secret Comparison (`===` instead of `timingSafeEqual`) | `High` | CWE-208 | +5 / -2 |
| `TG-AUTH-002` | Weak Cryptographic Hash for Passwords (MD5 / SHA1) | `Critical` | CWE-328 | +6 / -3 |
| `TG-AUTH-003` | JWT Verification Missing Explicit `algorithms` Whitelist | `High` | CWE-347 | +4 / -1 |
| `TG-AUTH-004` | Missing `HttpOnly` Flag on Authentication Session Cookie | `Medium` | CWE-1004 | +2 / -1 |
| `TG-AUTH-005` | Missing `Secure` Flag on HTTPS Production Cookie | `Medium` | CWE-614 | +2 / -1 |
| `TG-AUTH-006` | Insecure Default Session Lifetime (> 7 Days Without Rotation) | `Low` | CWE-613 | +2 / -1 |
| `TG-AUTH-007` | Deprecated PBKDF2 Low Iteration Count (< 600,000) | `Medium` | CWE-916 | +2 / -1 |
| `TG-AUTH-008` | Missing Re-Authentication on Sensitive Action Endpoint | `High` | CWE-306 | +8 / -2 |

---

### TG-DB — Multi-Tenant Isolation & SQL Injection
*Prevents cross-tenant data leaks and SQL injection attacks across ORMs and raw queries.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-DB-001` | Multi-Tenant Database Query Missing Tenant Partition Scope | `Critical` | CWE-284 | +5 / -1 |
| `TG-DB-002` | String-Concatenated Raw SQL Query Construction | `Critical` | CWE-89 | +6 / -2 |
| `TG-DB-003` | Unsanitized Dynamic Table or Column Identifier in SQL | `High` | CWE-89 | +5 / -2 |
| `TG-DB-004` | Unbounded Large Dataset Query Missing `LIMIT` Pagination | `Medium` | CWE-770 | +3 / -1 |

---

### TG-INPUT — Traversal & Command Injection
*Restricts arbitrary file system path traversal, OS command execution, and unsafe deserialization.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-INPUT-001` | Path Traversal via Unvalidated User Input in `fs` Path | `High` | CWE-22 | +6 / -2 |
| `TG-INPUT-002` | Arbitrary Command Execution via Shell `exec` / `system` | `Critical` | CWE-78 | +8 / -3 |
| `TG-INPUT-003` | Unsafe Object Deserialization (`pickle` / `yaml.unsafe_load`) | `Critical` | CWE-502 | +4 / -2 |
| `TG-INPUT-004` | Open Redirect via Unvalidated Query Parameter | `Medium` | CWE-601 | +6 / -2 |
| `TG-INPUT-005` | Prototype Pollution via Unsafe Object Recursive Merge | `High` | CWE-1321 | +7 / -2 |
| `TG-INPUT-006` | Unsanitized User Input Passed to `eval()` or `Function()` | `Critical` | CWE-95 | +4 / -2 |
| `TG-INPUT-007` | Dangerous HTML Output Rendering (`dangerouslySetInnerHTML`) | `High` | CWE-79 | +5 / -1 |
| `TG-INPUT-008` | Unbounded File Upload Missing MIME-Type & Extension Bounds | `High` | CWE-434 | +8 / -2 |

---

### TG-AGENT — AI Agent & Prompt Injection Defense
*Prevents direct and indirect prompt injection, unconstrained tool calling, and RAG tenant leakage.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-AGENT-001` | Direct String Concatenation of User Input into System Prompt | `Critical` | CWE-20 | +6 / -2 |
| `TG-AGENT-002` | AI Tool Calling Execution Missing Strict JSON Schema Validation | `High` | CWE-20 | +7 / -2 |
| `TG-AGENT-003` | Unbounded Tool Recursion or Unrestricted File Access Tool | `High` | CWE-770 | +5 / -1 |
| `TG-AGENT-004` | Unsanitized Model Output Interpolated Directly into Shell/HTML | `Critical` | CWE-74 | +6 / -2 |

---

### TG-SSRF — Server-Side Request Forgery Boundaries
*Enforces outbound request whitelisting and blocks access to cloud metadata (`169.254.169.254`).*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-SSRF-001` | Unrestricted Outbound HTTP Request to User-Supplied URL | `Critical` | CWE-918 | +8 / -2 |
| `TG-SSRF-002` | Missing Private / Link-Local IP Filtering (`169.254.169.254`) | `Critical` | CWE-918 | +6 / -1 |
| `TG-SSRF-003` | Missing Hostname Whitelist Verification on Dynamic Webhook | `High` | CWE-918 | +7 / -2 |
| `TG-SSRF-004` | Following Unrestricted HTTP 3xx Redirects into Internal Subnets | `High` | CWE-918 | +4 / -1 |

---

### TG-CONT — Container Hardening & Docker Safety
*Guarantees non-root container execution, prevents docker socket exposure, and blocks privileged flags.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-CONT-001` | Dockerfile Running As Root User (Missing `USER nonroot`) | `High` | CWE-250 | +3 / -1 |
| `TG-CONT-002` | Docker Socket (`/var/run/docker.sock`) Mounted in Container | `Critical` | CWE-250 | +2 / -2 |
| `TG-CONT-003` | Container Execution with `privileged: true` | `Critical` | CWE-250 | +1 / -1 |
| `TG-CONT-004` | Missing Read-Only Root Filesystem (`read_only: true`) | `Medium` | CWE-732 | +2 / -1 |

---

### TG-REDOS — Regular Expression Complexity & ReDoS
*Analyzes regex ASTs for catastrophic exponential backtracking using Thompson NFA simulation.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-REDOS-001` | Nested Quantifier Detected in Regex Pattern (`(a+)+`) | `High` | CWE-1333 | +3 / -1 |
| `TG-REDOS-002` | Overlapping Alternation with Outer Repetition (`(a|a)+`) | `High` | CWE-1333 | +3 / -1 |

---

### TG-RAG — RAG Pipeline & Vector DB Isolation
*Guarantees multi-tenant scoping on vector similarity lookups and neutral prompt delimiter wrapping.*

| Rule ID | Invariant Title | Severity | CWE | Ponytail Budget |
| :--- | :--- | :---: | :---: | :---: |
| `TG-RAG-001` | Vector Similarity Search Missing Tenant Scoping Filter | `Critical` | CWE-284 | +5 / -1 |
| `TG-RAG-002` | RAG Ingestion Pipeline Concatenates Documents Without Delimiters | `High` | CWE-74 | +4 / -1 |
| `TG-RAG-003` | Embedding Cache Missing Tenant Isolation Key Partition | `High` | CWE-284 | +3 / -1 |

---

## How to Explore in CLI & Chat

### 1. Terminal Command Center
```bash
# Launch interactive terminal center with menu navigation:
torusguard

# Or via npm/npx without global installation:
npx torusguard
```

### 2. Inspect Golden Fix Recipes
```bash
# Browse verified recipes in persistent security memory:
torusguard recipes

# Export recipes for team review:
torusguard recipes export
```

### 3. AI Chat Slash Commands
In your AI IDE (Cursor, Windsurf, Claude Code, Antigravity):
```
/torusguard audit       # Run static AST security scan
/torusguard ocr-scan    # Scan images with hybrid first-principles extractor
/torusguard recipes     # Explore distilled Golden Fix patterns
/torusguard report      # Generate visual HTML dashboard and SARIF
```

---

## Contributing New Rules

To propose an invariant or Golden Fix recipe:
1. Ensure the invariant falls into one of the 22 architectural families.
2. Formulate a minimal Golden Fix conforming to Ponytail Protocol bounds (≤35 additions, ≤25 deletions).
3. Validate against the zero-bypass invariant (never introduce `# nosec` or `InsecureSkipVerify`).
4. Submit a Pull Request following conventional commit standards.
