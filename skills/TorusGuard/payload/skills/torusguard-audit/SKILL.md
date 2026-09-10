---
name: torusguard-audit
description: Static AST security scanning, line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring via CLI or AI Agent.
version: 1.3.4
workflow: .torusguard/workflows/audit.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - .torusguard/scripts/audit_runner.py
  - .torusguard/scripts/term_ui.py
  - .torusguard/scripts/finding_scorer.py
---

# TorusGuard Audit — Static Code Security Analysis

## Objective
Execute static AST analysis across polyglot project files, evaluate code against 71 canonical security rules across 11 families, assign stable line-shift invariant fingerprints, cluster architectural root causes, and score findings with auditable 0–100 confidence ratings.

---

## Two Execution Modes

### Mode A: Automated CLI Execution
Run the static security audit from your terminal:
```bash
# Scan current repository
npx torusguard audit

# Scan specific directory or example app
npx torusguard audit ./examples/vulnerable-react-express

# Include test fixtures and spec directories
npx torusguard audit --include-tests

# Output machine-readable JSON
npx torusguard audit --json
```
**Under the Hood:** Executes `python .torusguard/scripts/audit_runner.py`.
- Auto-detects repository stack and skips build/cache directories (`node_modules`, `.git`, `.venv`, `dist`, `build`).
- Evaluates files across 11 canonical security families:
  - `TG-SEC-*`: Hardcoded credentials, private keys, JWT secrets, client env leaks.
  - `TG-INPUT-*`: SQL injection, command injection, path traversal, unsafe HTML rendering.
  - `TG-DB-*`: Missing tenant isolation, service role keys in client code.
  - `TG-AUTH-*`: Plaintext passwords, missing cookie security flags (httpOnly, secure, sameSite).
  - `TG-PLATFORM-*`: Permissive wildcard CORS with credentials, missing security headers.
  - `TG-DIFF-*`: Disabled TLS verification (`verify=False`, `rejectUnauthorized: false`).
- Generates run directory: `.torusguard/runs/run-YYYYMMDD-HHMMSS-audit/`.
- Writes `findings.json`, `findings.md`, and `manifest.json`.
- Displays standardized 75-column terminal cards.
- Returns exit code `1` if findings are discovered, `0` if clean.

### Mode B: In-Session AI Chat Agent Scan
When auditing files directly in AI chat:
1. **Discover Sinks:** Use `grep_search` and `view_file` to search for dangerous patterns across server and client code.
2. **Cluster Root Causes:** Group findings by causal architecture (e.g. `cluster-tenant-isolation`, `cluster-credentials-exposure`, `cluster-injection`).
3. **Audit Evidence Sufficiency:** Ensure that user-controlled input reaches the vulnerable sink without prior sanitization or schema validation.
4. **Present Actionable Findings:** Display finding cards with severity, rule ID, file, line, and remediation recommendation.
5. **Prompt Next Phase:** Guide the operator to `/torusguard harden` or `npx torusguard harden`.

---

## Canonical Rule Families
| Family | Scope | Example Violations |
| :--- | :--- | :--- |
| **TG-SEC** | Secrets & Credentials | Hardcoded JWT secret, API key strings, token logging |
| **TG-INPUT** | Injection & Input Validation | Raw SQL interpolation, DOM `innerHTML`, `path.join` traversal |
| **TG-DB** | Database & Tenant Scoping | Unscoped `.objects.get(id=...)`, Prisma missing `tenantId` |
| **TG-AUTH** | Authentication & Cookies | Insecure cookies (missing httpOnly/secure/sameSite) |
| **TG-PLATFORM** | Server & Platform Config | Wildcard CORS (`origin: '*'`) with credentials |
| **TG-DIFF** | Security Bypasses | Disabled TLS verification (`verify=False`) |

---

## Output Card Format
```markdown
### 🛡️ TorusGuard Static Security Audit Completed
- **Run ID:** `run-20260910-121618-audit`
- **Scope:** 7 files evaluated across 11 canonical families
- **Status:** ✖ CRITICAL FINDINGS DETECTED
- **Findings:** 2 Critical, 2 High, 2 Medium/Low (6 total)
- **Clusters:** 3 architectural root causes identified
- **Artifacts:** `.torusguard/runs/<run_id>/findings.json`
- **Next Action:** Run `npx torusguard harden` or `/torusguard harden`
```
