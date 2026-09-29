---
name: torusguard-audit
description: Taint-aware static AST security scanning, cross-file interprocedural dataflow, 88 rules across 22 families, line-shift invariant fingerprinting, and 7-signal calibrated confidence scoring via CLI or AI Agent.
version: 2.1.1
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/audit_runner.py
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/core/taint_graph.py
  - .torusguard/core/cross_file_taint.py
  - .torusguard/core/confidence.py
  - .torusguard/core/parser.py
  - .torusguard/core/incremental.py

---

# TorusGuard Audit — Deep Taint-Aware Static Code Security Analysis

## Objective
Execute deep static analysis combining **Tree-sitter polyglot AST parsing**, **source-to-sink taint tracking**, and **interprocedural call-graph analysis** across Python, JavaScript/TypeScript, Go, Rust, Java, Ruby, PHP, and C#. Evaluates code against 88 canonical rules across 22 architectural families, generates line-shift invariant fingerprints, clusters systemic root causes, and computes 7-signal evidence-chain confidence ratings.

---

## Tri-Mode Execution Parity

### Mode A: Automated Terminal CLI
Run the static security audit from your terminal:
```bash
# Full codebase audit with taint dataflow analysis
torusguard audit

# Incremental scan (sub-second diff on changed files only)
torusguard audit --incremental

# Continuous watch mode (re-scan debounced on file save)
torusguard audit --watch

# Audit specific directory or microservice
torusguard audit ./examples/vulnerable-react-express

# Export findings to OASIS SARIF v2.1.0 format
torusguard audit --sarif --sarif-out ./report.sarif

# Machine-readable JSON output
torusguard audit --json
```

### Mode B: In-Session AI Chat Slash Command (`/torusguard audit`)
When executing audits directly in AI chat:
1. **Trace Dataflow (Sources → Sinks):** Track user inputs (`request.GET`, `req.body`, `r.URL.Query()`) through assignments and helper functions to dangerous sinks (`execute()`, `innerHTML`, `open()`).
2. **Verify Sanitizer Absence:** Confirm that input is not cleansed by `int()`, `escape()`, `shlex.quote()`, or `zod.safeParse()`.
3. **Cross-File Correlation:** Trace calls across module boundaries up to 5 interprocedural hops using `CrossFileTaintAnalyzer`.
4. **Cluster Root Causes:** Group findings into architectural failure patterns (e.g. `cluster-prompt-injection`, `cluster-tenant-isolation`, `cluster-supply-chain`).
5. **Calibrate Confidence:** Score findings via the 7-signal evidence chain model.
6. **Synchronize Ground Truth:** Record active findings in `security_report.md` at workspace root.

### Mode C: Native MCP Tool Calling
MCP agents invoke `torusguard_audit(target_root, incremental, use_taint)` via JSON-RPC 2.0 stdio to receive structured findings with verified taint paths and confidence scores.

---

## Architectural Rule Taxonomy (86 Rules Across 22 Families)

| Family Code | Security Domain | Core Invariant Enforced |
| :--- | :--- | :--- |
| **`TG-SEC`** | Secrets & Credentials | Zero hardcoded API keys, private certificates, or JWT secrets. |
| **`TG-AUTH`** | Authentication & Session | Enforce timing-safe compares, strong password hashing, algorithm verification. |
| **`TG-DB`** | Database & Tenancy | Parameterized SQL queries and tenant partition scoping across all lookups. |
| **`TG-INPUT`** | Input & Sanitization | Strict path sanitization, command argument escaping, safe template rendering. |
| **`TG-RATE`** | Rate Limiting | Rate-limiting middleware on auth endpoints and payload size bounds. |
| **`TG-AGENT`** | AI Agents & Prompts | Structural prompt isolation, inert XML delimiters, MCP tool schema validation. |
| **`TG-SSRF`** | Outbound Net & SSRF | Hostname whitelisting, private IP blocklist (127.0.0.1, 169.254.169.254). |
| **`TG-WEBHOOK`**| Webhook Verification | Cryptographic HMAC-SHA256 signature verification and replay prevention. |
| **`TG-WS`** | WebSockets | Origin verification, handshake authentication, inbound frame size limits. |
| **`TG-CSRF`** | CSRF Protection | SameSite cookie attributes and anti-CSRF token verification on state mutations. |
| **`TG-GQL`** | GraphQL Safety | Query depth limiting (max depth 6) and production schema introspection suppression. |
| **`TG-SUPPLY`** | Supply Chain & CI/CD | Immutable commit SHA pinning in GitHub Actions, lockfile integrity audits. |
| **`TG-BIZ`** | Business Logic | Non-negative quantity asserts, transaction locks, server-side discount bounds. |
| **`TG-CACHE`** | Cache Poisoning | Cache-Control headers on sensitive responses, unkeyed header sanitization. |
| **`TG-CLIENT`** | Client Bundle Secrets | Zero private environment variables (`process.env.SUPABASE_SERVICE_ROLE`) in client. |
| **`TG-PLATFORM`**| Platform Hardening | Helmet security headers, debug mode suppression, cookie secure flags. |
| **`TG-DIFF`** | Security Bypasses | Block `# nosec`, `InsecureSkipVerify`, and enforce Ponytail line budgets. |
| **`TG-EDGE`** | Edge & Serverless | Subrequest fan-out limits and serverless execution timeouts. |
| **`TG-CONT`** | Container Safety | Enforce non-root execution, zero docker socket mounts, no privileged mode. |
| **`TG-GIT`** | Git History Secrets | Zero historical committed credentials, no tokens in remote URLs. |
| **`TG-REDOS`** | ReDoS Prevention | Zero nested quantifiers `(a+)+` or catastrophic backtracking regular expressions. |
| **`TG-RAG`** | RAG & Vector DB | Mandatory tenant scoping on vector similarity search and inert ingestion. |

---

## Evidence-Chain Confidence Scoring (0–100)

Findings are evaluated against 7 empirical signals:

```
Final Score = Σ weighted signals:
- rule_severity_base (0.20): Critical=90, High=75, Medium=50, Low=25
- taint_path_confirmed (0.25): 100 if source→sink reachability is confirmed, 0 otherwise
- taint_depth (0.10): direct=100, 1-hop=80, 2-hop=60, 3+=40
- sanitizer_absence (0.15): 100 if no known sanitizer present, 0 if sanitized
- framework_context_match (0.10): 100 if sink matches detected stack, 50 default
- evidence_snippet_quality (0.10): 100 for multi-line AST context, 50 for single line
- test_fixture_penalty (-0.10): -50 penalty if located in test suite or fixtures
- memory_boost: -30 (false positive class) to +15 (regression watch)

Classification Bands:
- 90–100: Confirmed (High priority for automated Ponytail hardening)
- 70–89:  High Confidence (Requires review & remediation)
- 50–69:  Medium Confidence (Context verification needed)
- 0–49:   Needs Review (Suppressed or test fixture)
```

---

## 🏛️ Context Minimization & Performance Invariants
- **1/9th Token Strategy:** Never ingest entire files into agent context. Always inspect bounded AST context windows ($\pm 3$ lines) via `scanner.ExtractContext`.
- **Incremental Cache:** Uses cryptographic content hashes in `.torusguard/cache/ast_cache.json` to complete repeat audits in under 1 second.
- **Fail-Closed Safety:** Incomplete parses or syntax anomalies in non-standard files gracefully degrade to fallback token parsing without aborting the audit.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Grepping Without Taint** | Flags `db.execute(query)` even when `query` is hardcoded or parameterized. | Verify user input reaches the sink via `core.taint_graph` before reporting. |
| **Ignoring Sanitizers** | Reports injection even though `int(user_id)` or `shlex.quote()` cleans the input. | Check if any node in the dataflow path acts as a registered sanitizer. |
| **Single-File Blindness** | Misses vulnerabilities when input enters `utils.py` and reaches a sink in `views.py`. | Trace interprocedural call chains using `CrossFileTaintAnalyzer` (up to 5 hops). |
| **Unbounded File Dumps** | Reads entire 1,000-line source files into chat context. | Read only the bounded context ($\pm 3$ lines) around the finding's line number. |
| **Missing Ground Truth Sync** | Produces analysis in chat without synchronizing `security_report.md`. | Always update `security_report.md` with active findings and run IDs. |

---

## ✅ Pre-Flight Self-Audit

Before finishing an audit pass, confirm:
- [ ] Did I run `torusguard audit` or inspect `security_report.md`?
- [ ] Are all reported findings backed by confirmed taint paths or verified regex patterns?
- [ ] Did I verify user input reaches the sink without prior sanitization?
- [ ] Are findings pinned to exact 1-indexed line numbers with stable region hashes?
- [ ] Did I synchronize discovering state into `security_report.md`?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY:  Scan source code with polyglot AST parser and trace dataflow reachability from sources to sinks.
BUILD:   Group findings by root cause, compute 7-signal calibrated confidence scores, and format 75-column terminal cards.
CONFIRM: Synchronize all findings to security_report.md at workspace root and guide operator to /torusguard harden.
```

---

## 🔄 Rollback Defaults

If audit data becomes corrupted or a run needs to be reverted:
1. Historical runs are preserved immutably in `.torusguard/runs/<run_id>/`.
2. AST cache can be cleared anytime by deleting `.torusguard/cache/ast_cache.json`.
3. Pre-apply code snapshots remain intact in `.torusguard/snapshots/`.
