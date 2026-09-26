---
name: torusguard-harden
description: Package surgical remediation bundles conforming to the Ponytail Protocol (<= 35 additions, <= 25 deletions) via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/harden.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/harden/harden.go
  - internal/harden/patch.go
  - internal/harden/reflection.go
  - cmd/torusguard/main.go
---

# TorusGuard Harden — Governed Remediation & Bundle Packaging

## Objective
Formulate minimal, surgical code fixes bound by the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions), packaging unified diffs or semantic reflection patches into auditable remediation bundles ready for review.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution (Recommended First Step)
Run the autonomous remediation engine via the terminal:
```bash
# Validate candidate patch or semantic patch against Ponytail bounds
torusguard harden candidate.patch

# Validate semantic JSON patch
torusguard harden patch.json
```
**Under the Hood:** Executes compiled Go hardening engine (`internal/harden`).
- Evaluates patch churn strictly against Ponytail bounds ($\le 35$ additions, $\le 25$ deletions).
- Scans replacement code for security bypasses (`# nosec`, `verify=False`, `InsecureSkipVerify: true`).
- Supports both unified diff files (`.diff`, `.patch`) and Semantic Reflection JSON files.
- Renders pixel-perfect 75-column terminal cards.

### Mode B: In-Session AI Chat Agent Remediation
When findings require complex architectural changes, or when formulating fixes:
1. **Locate Target Finding:** Inspect `security_report.md` at workspace root.
2. **Inspect AST Context (1/9th Token Strategy):** Inspect only surrounding lines ($\pm 3$ lines) via `ExtractContext` rather than ingesting entire files.
3. **Formulate Minimal Semantic Patch:** Formulate a surgical code modification using the Line-Level Reflection Module:
   - Provide `target_file`, `find_snippet`, and `replace_snippet`.
   - Parameterize SQL queries (replace concatenation with `?` or `$1` or `%s`).
   - Add tenant isolation (`where: { tenantId: user.tenantId }`).
   - Replace unsafe HTML injection with safe text rendering (`textContent`).
   - Sanitize path traversal using `filepath.Base()` or `path.basename()`.
   - Restore TLS verification flags.
4. **Validate Ponytail Bounds:** Count additions ($\le 35$) and deletions ($\le 25$). Never perform full-file rewrites.
5. **Report to Operator:** Present proposed diff card and recommend running `/torusguard apply` or `torusguard apply`.

### Mode C: Native MCP Tool Execution
For autonomous AI coding agents (Antigravity, Cursor, Windsurf, Claude Code):
- **Tool Invocation:** Call `torusguard_harden` with semantic reflection arguments:
  ```json
  {
    "target_file": "src/controllers/userController.js",
    "find_snippet": "const query = `SELECT * FROM users WHERE id = ${req.params.id}`;",
    "replace_snippet": "const query = 'SELECT * FROM users WHERE id = ? AND tenant_id = ?';\nconst params = [req.params.id, req.user.tenantId];"
  }
  ```
- **Programmatic Return:** Receives exact line ranges matched by Go AST, calculated additions/deletions, and verification that no `# nosec` or security bypasses exist.

---

## 🏛️ Line-Level Reflection Module (OpenCodeReview Hybrid Engine)
Instead of forcing the LLM to guess error-prone unified diff line offsets (`@@ -14,6 +14,8 @@`), TorusGuard allows formulating **Semantic Patches**:
```json
{
  "target_file": "server/index.js",
  "rule_id": "TG-SEC-001",
  "find_snippet": "const jwtSecret = 'hardcoded-dev-secret-key-12345';",
  "replace_snippet": "const jwtSecret = process.env.JWT_SECRET;",
  "rationale": "Extracted hardcoded JWT secret to environment variable"
}
```
The Go engine deterministically matches `find_snippet` against the target file, counts additions/deletions, verifies Ponytail bounds, and guarantees zero line-number drift.

---

## Non-Negotiable Invariants
- **Ponytail Limit:** Strict upper bound of $\le 35$ additions and $\le 25$ deletions per bundle.
- **Dry-Run Rule:** Never modify target source code during `harden`. All edits must be reviewed before application in Phase 5 (`apply`).
- **No Unrelated Churn:** Do not reformat unrelated code, reorder imports, or change styles.
- **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `[AllowAnonymous]`, or `csrf().disable()`.

---

## Output Card Format
```markdown
### 🛠️ TorusGuard Remediation Bundle Formulated
- **Target Finding:** `[TG-SEC-001]` at `server/index.js:9`
- **Ponytail Churn:** +1 / -1 (Compliant <= 35 add, <= 25 del)
- **Strategy:** Migrated hardcoded JWT secret to environment variable process.env.JWT_SECRET
- **Mode:** Line-Level Reflection Match (Semantic Patch)
- **Next Step:** Run `torusguard apply` or `/torusguard apply` to review and apply
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Line-Number Drift** | Formulates diff headers with estimated line numbers that fail `git apply`. | Use semantic patches (`find_snippet` -> `replace_snippet`) so Go reflection pins line bounds. |
| **Exceeding Ponytail Budget** | Produces patches with +50 additions or +40 deletions rewriting surrounding logic. | Split complex remediations or keep changes surgical ($\le 35$ additions, $\le 25$ deletions). |
| **Introducing Bypass Flags** | Inserts `# nosec`, `verify=False`, or `@csrf_exempt` to quickly silence warnings. | Fix the root cause without disabling security invariants. Bypasses trigger immediate error. |
| **Formatting Unrelated Lines** | Re-indents or cleans up imports in unrelated sections of the target file. | Zero unrelated churn. Touch only the lines required for vulnerability remediation. |

---

## ✅ Pre-Flight Self-Audit

Before formulating a remediation bundle, verify:
- [ ] Did I read only the bounded AST context window ($\pm 3$ lines) to keep tokens minimal?
- [ ] Is `find_snippet` an exact, verbatim substring of the target file?
- [ ] Are total additions $\le 35$ and deletions $\le 25$?
- [ ] Does `replace_snippet` strictly avoid any bypass flags (`# nosec`, `verify=False`)?
- [ ] Does the fix preserve existing application behavior and business contracts?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Inspect target finding context and verify verbatim match of find_snippet in source code.
BUILD:  Formulate minimal SemanticPatch or unified diff conforming to Ponytail budget (<=35 add, <=25 del).
CONFIRM: Validate via torusguard harden or torusguard_harden MCP tool; verify zero bypass rejections.
```
