---
name: torusguard-audit
description: Static AST security scanning, line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/scanner.go
  - cmd/torusguard/main.go
---

# TorusGuard Audit — Static Code Security Analysis

## Objective
Execute static AST analysis across polyglot project files, evaluate code against 74 canonical security rules across 18 families, assign stable line-shift invariant fingerprints, cluster architectural root causes, synchronize findings with `security_report.md`, and score findings with auditable 0–100 confidence ratings.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run the static security audit from your terminal:
```bash
# Scan current repository
torusguard audit

# Scan specific directory or example app
torusguard audit ./examples/vulnerable-react-express

# Include test fixtures and spec directories
torusguard audit --include-tests

# Output machine-readable JSON
torusguard audit --json
```
**Under the Hood:** Executes compiled Go static analysis engine (`internal/scanner`).
- Auto-detects repository stack and skips build/cache directories (`node_modules`, `.git`, `.venv`, `dist`, `build`).
- Evaluates files across 18 canonical security families:
  - `TG-SEC-*`: Hardcoded credentials, private keys, JWT secrets, client env leaks.
  - `TG-INPUT-*`: SQL injection, command injection, path traversal, unsafe HTML rendering.
  - `TG-DB-*`: Missing tenant isolation, service role keys in client code.
  - `TG-AUTH-*`: Plaintext passwords, missing cookie security flags (httpOnly, secure, sameSite).
  - `TG-PLATFORM-*`: Permissive wildcard CORS with credentials, missing security headers.
  - `TG-DIFF-*`: Disabled TLS verification (`verify=False`, `InsecureSkipVerify: true`).
  - `TG-NPE-*`: Null-pointer exceptions, unchecked nil error dereferences.
  - `TG-CONC-*`: Concurrency hazards, goroutine loop variable capture.
- Writes findings directly to `security_report.md` at workspace root.
- Displays standardized 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Scan
When auditing files directly in AI chat:
1. **Discover Sinks:** Use `grep_search` and `view_file` to search for dangerous patterns across server and client code.
2. **Cluster Root Causes:** Group findings by causal architecture (e.g. `cluster-tenant-isolation`, `cluster-credentials-exposure`, `cluster-injection`).
3. **Audit Evidence Sufficiency:** Ensure that user-controlled input reaches the vulnerable sink without prior sanitization or schema validation.
4. **Context Minimization (1/9th Token Strategy):** Inspect only bounded AST context windows ($\pm 3$ lines) via `scanner.ExtractContext` rather than ingesting entire files.
5. **Present Actionable Findings:** Display finding cards with severity, rule ID, file, line, and remediation recommendation.
6. **Prompt Next Phase:** Guide the operator to `/torusguard harden` or `torusguard harden`.

### Mode C: Native MCP Tool Execution
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Tool Invocation:** Call `torusguard_audit` with target arguments:
  ```json
  {
    "target": ".",
    "include_ocr": true,
    "max_image_mb": 10
  }
  ```
- **Programmatic Return:** Receives formatted finding summaries, active rule counts, and confirmation that `security_report.md` is updated on disk.
- **Resource Companion:** Inspect the living report via resource `torusguard://security_report` or rules catalog via `torusguard://rules_catalog`.

---

## Canonical Rule Families
| Family | Scope | Example Violations |
| :--- | :--- | :--- |
| **TG-SEC** | Secrets & Credentials | Hardcoded JWT secret, API key strings, token logging |
| **TG-INPUT** | Injection & Input Validation | Raw SQL interpolation, DOM `innerHTML`, `path.join` traversal |
| **TG-DB** | Database & Tenant Scoping | Unscoped `.objects.get(id=...)`, Prisma missing `tenantId` |
| **TG-AUTH** | Authentication & Cookies | Insecure cookies (missing httpOnly/secure/sameSite) |
| **TG-PLATFORM** | Server & Platform Config | Wildcard CORS (`origin: '*'`) with credentials |
| **TG-DIFF** | Security Bypasses | Disabled TLS verification (`verify=False`, `# nosec`) |
| **TG-NPE** | Null Dereference / NPE | Unchecked optional chaining, unhandled nil error returns |
| **TG-CONC** | Concurrency & Thread-Safety | Goroutine loop variable capture, unmutexed map mutations |

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Static Security Audit Completed
- **Run ID:** `run-20260910-121618-audit`
- **Scope:** 7 files evaluated across 18 canonical families
- **Status:** ✖ CRITICAL FINDINGS DETECTED
- **Findings:** 2 Critical, 2 High, 2 Medium/Low (6 total)
- **Clusters:** 3 architectural root causes identified
- **Artifacts:** `security_report.md`
- **Next Action:** Run `torusguard harden` or `/torusguard harden`
```

---

## 🏛️ OpenCodeReview Precision & Context Minimization
- **1/9th Token Minimization:** Use `scanner.ExtractContext` to extract only the bounded $\pm 3$ lines context window instead of ingesting entire files.
- **Line-Level Pinning:** Every finding is reported with exact 1-indexed line numbers, line content, severity, and suggested remediation.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Unbounded File Reading** | Reads entire 800+ line files to diagnose a 1-line vulnerability. | Read only the bounded context ($\pm 3$ lines) around the finding's line number. |
| **Ignoring NPE / Concurrency** | Focuses only on secrets and misses thread-safety and null-pointer hazards. | Enforce `TG-NPE-001` and `TG-CONC-001` checks during audit review. |
| **False Positive Escalation** | Flags documentation strings or mock test fixtures as production vulnerabilities. | Skip test files (`*_test.go`, `.test.ts`) and verify sink exploitability before reporting. |
| **Missing Sync to Ground Truth** | Produces analysis in chat without checking or updating `security_report.md`. | Always reconcile against `security_report.md` at workspace root. |

---

## ✅ Pre-Flight Self-Audit

Before completing an audit pass, verify:
- [ ] Did I run `torusguard audit` or inspect `security_report.md` first?
- [ ] Are all reported findings pinned to precise line numbers?
- [ ] Did I verify user input reaches the sink without prior validation?
- [ ] Did I extract only the minimal AST context window ($\pm 3$ lines) to conserve tokens?
- [ ] Did I evaluate against all 18 families including NPE and concurrency rules?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Scan source code and image assets using torusguard audit or torusguard_audit MCP tool.
BUILD:  Synthesize findings clustered by root cause with exact line numbers and bounded AST snippets.
CONFIRM: Synchronize living findings into security_report.md and guide operator to /torusguard harden.
```
