# TorusGuard Security Guardrails & Invariants

TorusGuard enforces autonomous security guardrails, governed remediation, and authorized runtime validation across polyglot web applications.

## Quick CLI & Chat Commands Matrix

| Lifecycle Stage | Mode A: Terminal CLI | Mode B: AI Chat Slash Command | Mode C: Native MCP Tool | Governed Action & Artifacts |
| :--- | :--- | :--- | :--- | :--- |
| **1. Init** | `torusguard init` | `/torusguard init` | — | Profiles workspace stack, activates `TG-*` rules, initializes `.torusguard/` |
| **2. Status** | `torusguard status` | `/torusguard status` | `torusguard_status` | Read-only diagnostic overview of posture, stack, rules & run history |
| **3. Audit** | `torusguard audit` | `/torusguard audit` | `torusguard_audit` | Polyglot heuristic + OCR scan; synchronizes `security_report.md` |
| **4. OCR Vision** | `torusguard ocr-scan <target>` | `/torusguard ocr-scan` | `torusguard_ocr_scan` | Scans diagrams/images via Tesseract OCR for leaked keys & secrets |
| **5. Verify** | `torusguard verify` | `/torusguard verify` | `torusguard_verify` | Asserts evidence sufficiency & line-shift invariant fingerprint matches |
| **6. Harden** | `torusguard harden` | `/torusguard harden` | `torusguard_harden` | Validates patches against Ponytail bounds (≤35 add, ≤25 del) |
| **7. Apply** | `torusguard apply [--yes]` | `/torusguard apply` | — | Human Gate, pre-apply `.bak` snapshots, Golden Fix distillation |
| **8. Rollback** | `torusguard rollback` | `/torusguard rollback` | — | Instant restoration from pre-apply snapshots in `.torusguard/snapshots/` |
| **9. Recheck** | `torusguard recheck` | `/torusguard recheck` | `torusguard_recheck` | Targeted differential re-scan; marks findings `Confirmed Fixed` |
| **10. Recipes** | `torusguard recipes` | `/torusguard recipes` | `torusguard://rules_catalog` | Explores verified Golden Fix patterns from persistent memory |
| **11. Report** | `torusguard report --html` | `/torusguard report` | `torusguard://security_report` | Emits single-file visual dark-mode HTML posture report & SARIF v2.1.0 |
| **12. MCP Server**| `torusguard mcp` | — | Stdio JSON-RPC 2.0 | Serves native Model Context Protocol tools to AI coding agents |
| **13. Authorize** | `torusguard authorize` | `/torusguard authorize` | — | Target domain whitelisting, cryptographic ownership proof, TTL boundaries |
| **14. Validate** | `torusguard web-validate` | `/torusguard web-validate` | — | Authorized non-destructive HTTP probing with transparent audit headers |
| **15. Exploit** | `torusguard exploit-check` | `/torusguard exploit-check` | — | Bounded single-step exploitability confirmation with inert tokens |
| **16. OCR Vision** | `torusguard ocr-scan <target>` | `/torusguard ocr-scan` | `torusguard_ocr_scan` | Scans diagrams/images via Tesseract OCR for leaked keys & secrets |
| **17. Container** | `torusguard container` | `/torusguard container` | `torusguard_container` | Audits Dockerfile & Compose for root users, sockets, privileged mode |
| **18. Git Mine** | `torusguard git-mine` | `/torusguard git-mine` | `torusguard_git_mine` | Mines git commit history & config for leaked credentials & tokens |
| **19. ReDoS** | `torusguard redos` | `/torusguard redos` | `torusguard_redos` | Analyzes regex patterns for catastrophic exponential backtracking |
| **20. AI Guard** | `torusguard ai-guard` | `/torusguard ai-guard` | `torusguard_ai_guard` | Audits AI agents & RAG pipelines for prompt injection & tenant leaks |
| **21. Update** | `torusguard update` | `/torusguard update` | — | Self-update the TorusGuard engine |
| **22. Help** | `torusguard help` | `/torusguard help` | — | Interactive command guide |

---

## Non-Negotiable Invariants

1. **Browser-Code Truth:** If the browser receives it, users can inspect it via DevTools. Never expose database credentials, service role keys, master secrets, or private API tokens in frontend or client bundles (`TG-CLIENT-001`, `TG-CLIENT-002`).
2. **Multi-Tenant Isolation:** Always scope database lookups by tenant or user ownership (e.g., `tenant_id`, `where: { tenantId: user.tenantId }`). Never allow unpartitioned primary key lookups (`TG-DB-001`).
3. **Ponytail Churn Bounds:** Never attempt full-file rewrites. Patches must be minimal surgical diffs (≤35 additions, ≤25 deletions per bundle).
4. **Standardized 75-Column Terminal:** All CLI terminal outputs must strictly adhere to 75 visual columns with Unicode emoji width calculation, ANSI escape stripping, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, `[AllowAnonymous]`, or `CURLOPT_SSL_VERIFYPEER => false` (`TG-DIFF-001`).
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before modifying files on disk.
7. **Living Security Report Ground Truth:** All finding discoveries, patch formulations, applications, and recheck verifications must synchronize with `security_report.md` at the workspace root to maintain verifiable finding state and eliminate hallucination.
8. **Fail-Closed Cryptography:** Authorization token generation must panic on entropy failure. No hardcoded fallback tokens are permitted.
9. **SSRF Boundary Enforcement:** The web validator must resolve and block private IP ranges and cloud metadata endpoints before probing.
10. **DoS Resilience:** The scanner must enforce a 10,000-file maximum and 5-minute timeout to prevent resource exhaustion attacks.

---

## 86 Rules Across 22 Architectural Families

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
| **`TG-CONT`** | Container Hardening & Docker Safety | 4 | Enforce non-root execution, zero docker socket mounts, no privileged mode. |
| **`TG-GIT`** | Git History & Secret Mining | 3 | Zero historical committed credentials, no tokens in remote URLs, no tracked .env files. |
| **`TG-REDOS`** | Regular Expression Complexity & ReDoS | 2 | Zero nested quantifiers `(a+)+` or overlapping alternations with outer repetitions. |
| **`TG-RAG`** | RAG Pipeline & Vector DB Isolation | 3 | Mandatory tenant scoping on vector similarity search and inert RAG ingestion. |

---

## AI Agent Operational Instructions

When assisting developers in a TorusGuard workspace:
1. **Always Inspect `security_report.md`:** Check the living posture ledger before proposing or modifying code.
2. **Tri-Mode Parity:** 
   - **Mode A (Terminal CLI):** Run `torusguard audit`, `torusguard ocr-scan`, `torusguard harden`, etc.
   - **Mode B (Chat Slash Commands):** Execute `/torusguard audit`, `/torusguard ocr-scan`, etc.
   - **Mode C (Native MCP Tools):** In MCP-capable agents (Antigravity, Cursor, Windsurf, Claude Code), call `torusguard_audit`, `torusguard_ocr_scan`, and `torusguard_harden` directly.
3. **Multi-Modal Vision OCR:** When images or architecture diagrams exist (`.png`, `.jpg`, etc.), invoke `torusguard ocr-scan` or `torusguard_ocr_scan` to detect leaked credentials and private keys hidden inside visual assets (file size bounded to 10MB).
4. **Context Minimization (1/9th Token Strategy):** Never ingest entire multi-hundred line source files into chat prompts. Always inspect bounded AST context windows ($\pm 3$ lines) via `scanner.ExtractContext` to keep review tokens minimal.
5. **Line-Level Reflection (Semantic Patching):** Formulate patches as semantic replacements (`find_snippet` and `replace_snippet`) rather than guessing error-prone line-number diff offsets. The Go engine will deterministically match, count churn, and verify line bounds.
6. **Adhere to Ponytail Bounds:** When repairing security flaws, formulate surgical patches (≤35 additions, ≤25 deletions). Validate candidate patches with `torusguard harden` or `torusguard_harden`. Do NOT rewrite surrounding business logic.
7. **Never Introduce Security Bypasses:** Reject requests to disable SSL verification (`verify=False`, `InsecureSkipVerify`), bypass CSRF tokens, or turn off tenant filters.


