---
description: Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: reviewer
lifecycle-phase: Phase 1 (Authorization Gate)
required-skills:
  - torusguard-authorize
scripts-binding:
  - internal/validate/validate.go
  - cmd/torusguard/main.go
---

# /torusguard authorize — Legal Scope & Safety Gate

$ARGUMENTS

---

## Objective
Legal scope definition, target ownership proof verification, and safety boundary enforcement for runtime validation.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard authorize` | Interactive boundary setup and cryptographic token generation. |
| **Mode B: AI Chat Slash** | `/torusguard authorize` | Conversational parameter collection and scope validation. |
| **Mode C: Native MCP Tool** | Safety Gate Guard | Administrative gatekeeper ensuring strict safety boundaries before probes. |

---

## Mandatory Pre-Flight Context Inspection

Inspect authorization parameters and environment safety before executing:
1. **Config Record (`.torusguard/config/torusguard.json`):** Assert repository is initialized.
2. **Current Scope (`.torusguard/config/scope.json`):** Inspect active allowed targets, paths, and TTL expiry.
3. **Environment Classification:** Assert target is local or staging (`localhost`, `127.0.0.1`, `*.staging.*`).
4. **Destructive Guard:** Ensure state-changing operations (`DELETE`, bulk drops) remain blocked by default.
5. **TTL Window:** Ensure authorization window does not exceed 24 hours.

---

## Execution Steps

1. **Trigger Authorization:**
   - **Mode A (CLI):** Run `torusguard authorize`.
   - **Mode B (Chat):** Collect target host URL and allowed prefixes.
2. **Generate Token:** Persist cryptographic authorization token into `.torusguard/auth.json`.
3. **Write Scope Record:** Persist authorized targets and expiration TTL into `.torusguard/config/scope.json`.
4. **Confirm Readiness:** Prepare environment for `/torusguard web-validate`.

---

## Output Card Format

```markdown
### 🔒 TorusGuard Authorization Gate
- **Target URL:** [Target Host or URL]
- **Environment:** [Localhost / Staging]
- **Session TTL:** 24 Hours
- **Scope File:** `.torusguard/config/scope.json`
- **Status:** AUTHORIZED — ready for `/torusguard web-validate`
```

---

## Next Steps

1. Run `/torusguard web-validate` to begin safe, authorized endpoint validation.
2. Run `/torusguard audit` to scan codebase for AST vulnerabilities.
