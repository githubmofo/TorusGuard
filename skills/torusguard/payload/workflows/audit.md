---
description: Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: auditor
lifecycle-phase: Phase 2 (Static Audit & Clustering)
required-skills:
  - torusguard-audit
scripts-binding:
  - internal/scanner/scanner.go
  - cmd/torusguard/main.go
  - cmd/torusguard/mcp.go
---

# /torusguard audit — Static Security Code Scan & Clustering

$ARGUMENTS

---

## Objective
Execute static AST analysis across polyglot project files, evaluate code against 74 canonical security rules across 18 families, assign stable line-shift invariant fingerprints, cluster architectural root causes, synchronize findings with `security_report.md`, and score findings with auditable 0–100 confidence ratings.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard audit [--include-tests] [--json]` | Shell execution of compiled Go binary. |
| **Mode B: AI Chat Slash** | `/torusguard audit` | Conversational guided audit with bounded context inspection. |
| **Mode C: Native MCP Tool** | `torusguard_audit` | Autonomous agent tool invocation via stdio JSON-RPC. |

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace prerequisites before launching static audit:
1. **Init State (`torusguard.json`):** Assert repository is initialized or run `torusguard init`.
2. **Active Rules (`rules/active/`):** Confirm rule definitions exist.
3. **Exclusions:** Assert `node_modules/`, `.venv/`, `dist/`, `.git/` are skipped.
4. **Syntax Check:** Check for syntax errors before parsing ASTs.

---

## Living Report Invariant
- Audit discoveries automatically synchronize to `security_report.md` at workspace root.
- Findings transition into `OPEN 🔴` status with stable invariant fingerprints.

---

## Execution Steps

1. **Launch Audit Scan:**
   - **Mode A (CLI):** Run `torusguard audit` in terminal.
   - **Mode B (Chat):** Parse AST sinks using `grep_search` and bounded `ExtractContext`.
   - **Mode C (MCP):** Call `torusguard_audit` with `{"target": "."}`.
2. **Scan Codebase ASTs:** Match 74 canonical rules across 18 families against source trees.
3. **Compute Stable Fingerprints:** Hash AST context to produce stable line-shift invariant IDs.
4. **Cluster Root Causes:** Group findings sharing identical sinks or causal architecture.
5. **Synchronize Ground Truth:** Update `security_report.md` at workspace root.

---

## Output Card Format

```markdown
### 🔎 TorusGuard Static Audit Results
- **Files Scanned:** [Count] source files
- **Total Findings:** [Count] ([Critical] Critical, [High] High)
- **Root Cause Clusters:** [Count] architectural issues
- **Confidence:** [Score]/100
- **Living Report:** `security_report.md`
```

---

## Next Steps

1. Run `/torusguard verify` to validate exploitability and review evidence.
2. Run `/torusguard harden` to generate minimal surgical remediation plans.
