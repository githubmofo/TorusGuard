---
description: Taint-aware static security AST scanning, cross-file interprocedural dataflow, 86+ rules across 22 families, and 7-signal calibrated confidence scoring.
tools: Read, Grep, Glob, Bash, Write, run_command
version: 2.0.0
agent: auditor
lifecycle-phase: Phase 2 (Static Audit & Clustering)
required-skills:
  - torusguard-audit
scripts-binding:
  - .torusguard/scripts/audit_runner.py
  - .torusguard/scripts/finding_scorer.py
  - .torusguard/core/cross_file_taint.py
  - .torusguard/core/confidence.py
  - .torusguard/core/incremental.py
---

# /torusguard audit — Deep Taint-Aware Static Security Code Scan & Clustering

$ARGUMENTS

---

## Objective
Execute deep taint-aware static AST analysis across polyglot project files, evaluate code against 86+ canonical security rules across 22 families, trace interprocedural source-to-sink dataflows, assign stable line-shift invariant fingerprints, cluster architectural root causes, synchronize findings with `security_report.md`, and score findings with auditable 7-signal evidence-chain confidence ratings.

---

## Tri-Mode Execution

| Mode | Command / Tool | Execution Method |
| :--- | :--- | :--- |
| **Mode A: Terminal CLI** | `torusguard audit [--incremental] [--watch] [--json]` | Shell execution of TorusGuard audit engine. |
| **Mode B: AI Chat Slash** | `/torusguard audit` | Conversational guided audit with bounded context inspection. |
| **Mode C: Native MCP Tool** | `torusguard_audit` | Autonomous agent tool invocation via stdio JSON-RPC. |

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace prerequisites before launching static audit:
1. **Init State (`torusguard.json`):** Assert repository is initialized or run `torusguard init`.
2. **Active Rules (`rules/`):** Confirm rule definitions exist across the 22 architectural families.
3. **Exclusions:** Assert `node_modules/`, `.venv/`, `dist/`, `.git/` are skipped.
4. **Syntax Check:** Check for syntax errors before parsing ASTs.

---

## Living Report Invariant
- Audit discoveries automatically synchronize to `security_report.md` at workspace root.
- Findings transition into `OPEN 🔴` status with stable invariant fingerprints.

---

## Execution Steps

1. **Launch Audit Scan:**
   - **Mode A (CLI):** Run `torusguard audit` (or `python .torusguard/scripts/audit_runner.py`). Use `--incremental` for fast diffs.
   - **Mode B (Chat):** Parse AST sinks and trace sources to sinks using `core.taint_graph` and bounded context windows.
   - **Mode C (MCP):** Call `torusguard_audit` with `{"target": "."}`.
2. **Scan Codebase ASTs:** Match 86+ canonical rules across 22 families against source trees.
3. **Trace Taint Dataflows:** Follow untrusted inputs from sources to dangerous sinks across module boundaries.
4. **Compute Stable Fingerprints:** Hash AST context to produce stable line-shift invariant IDs (`TG-XXX-<hash12>`).
5. **Cluster Root Causes:** Group findings into the 22 canonical architectural root causes.
6. **Synchronize Ground Truth:** Update `security_report.md` at workspace root.

---

## Output Card Format

```markdown
### 🔎 TorusGuard Static Audit Results
- **Files Scanned:** [Count] source files ([Changed] changed)
- **Taint Paths Confirmed:** [Count] verified dataflows
- **Total Findings:** [Count] ([Critical] Critical, [High] High)
- **Root Cause Clusters:** [Count] architectural issues
- **Confidence:** [Score]/100 (Evidence-Chain Calibrated)
- **Living Report:** `security_report.md`
```

---

## Next Steps

1. Run `/torusguard verify` to validate exploitability and review evidence.
2. Run `/torusguard harden` to generate minimal surgical remediation plans conforming to the Ponytail protocol (<= 35 additions, <= 25 deletions).
