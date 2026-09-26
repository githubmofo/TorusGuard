---
description: Baseline project discovery, workspace scaffolding, stack detection, and framework-tailored security rule activation.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: profiler
lifecycle-phase: Phase 0 (Baseline Setup)
required-skills:
  - torusguard-init
scripts-binding:
  - internal/workspace/workspace.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard init — Project Baseline & Workspace Initialization

$ARGUMENTS

---

## Objective
Baseline project discovery, workspace scaffolding across polyglot stacks, and activation of 74 canonical security rules across 18 families.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard init [--force] [--stack <name>]` | Terminal execution of workspace scaffolder. |
| **Mode B: AI Chat Slash** | `/torusguard init` | Conversational stack profiling and rule activation. |
| **Mode C: Native MCP Tool** | Administrative Command | Agents execute `torusguard init` via shell and monitor via `torusguard_status`. |

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace state before running initialization:
1. **Config State (`.torusguard/config/torusguard.json`):** Check if workspace is already initialized.
2. **Project Manifests:** Check root for `package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `pyproject.toml`.
3. **Disclosure Policy (`SECURITY.md`):** Check for existing responsible disclosure policy.

---

## Living Report Invariant
- Provisions baseline `SECURITY.md` responsible disclosure policy.
- Activates tailored rules across 18 families based on detected stack.

---

## Execution Steps

1. **Scaffold Directory Topology:** Create `.torusguard/` structure (`config/`, `rules/active/`, `runs/`, `snapshots/`, `memory/`).
2. **Detect Stack:** Automatically identify frameworks across 16+ polyglot languages.
3. **Persist Configuration:** Write `.torusguard/config/torusguard.json`.
4. **Provision Policy:** Generate baseline `SECURITY.md` at workspace root.
5. **Recommend Audit:** Direct user to `/torusguard audit` or `torusguard audit`.

---

## Output Card Format

```markdown
### 🛡️ TorusGuard Workspace Initialization
- **Primary Framework:** [Detected Stack]
- **Active Rules:** 74 rules enabled across 18 families
- **Config:** `.torusguard/config/torusguard.json` generated
- **Policy:** `SECURITY.md` provisioned
- **Status:** READY — run `/torusguard audit` to scan codebase
```

---

## Next Steps

1. Run `/torusguard authorize` to define allowed target URLs and legal scan boundaries.
2. Run `/torusguard audit` to execute the baseline static security audit.
