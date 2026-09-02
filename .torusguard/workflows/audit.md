---
description: Static security AST scanning, stable line-shift invariant fingerprinting, root-cause clustering, and 0-100 confidence scoring.
tools: Read, Grep, Glob, Bash, Write
version: 0.9.2
agent: auditor
lifecycle-phase: Phase 2 (Static Audit & Clustering)
required-skills:
  - torusguard-audit
scripts-binding:
  - .torusguard/scripts/run_manager.py
  - .torusguard/scripts/finding_scorer.py
---

# /torusguard audit — Static Security Code Scan & Clustering

$ARGUMENTS

---

## Objective
Static security AST scanning, stable fingerprinting, root-cause clustering, and 0-100 scoring.

---

## Mandatory Pre-Flight Context Inspection

Inspect workspace prerequisites before launching static audit:
1. **Init State (`torusguard.json`):** Assert repository is initialized.
2. **Active Rules (`rules/active/`):** Confirm rule definitions exist.
3. **Exclusions:** Assert `node_modules/`, `.venv/`, `dist/`, `.git/` are skipped.
4. **Run Folder:** Allocate isolated folder in `.torusguard/runs/`.
5. **Syntax Check:** Check for syntax errors before parsing ASTs.

---

## When to Use /torusguard audit

| Trigger Scenario | Recommended Action |
| :--- | :--- |
| First-time scan of repository or new branch | Run `/torusguard audit` |
| Pre-commit review and PR security checks | Run `/torusguard audit` |
| Uninitialized project | Run `/torusguard init` first |
| Live endpoint or runtime probing | Run `/torusguard web-validate` |
| Differential check after patch | Run `/torusguard recheck` |

---

## Execution Steps

1. **Allocate Run Folder:** Run `python .torusguard/scripts/run_manager.py create audit`.
2. **Scan Codebase ASTs:** Match active rules against source trees.
3. **Compute Stable Fingerprints:** Hash AST context to produce stable IDs.
4. **Cluster Root Causes:** Group findings sharing identical sinks.
5. **Score Confidence (0–100):** Run `python .torusguard/scripts/finding_scorer.py --run <run_dir>`.
6. **Emit Artifacts:** Write `findings.md`, `findings.json`, and `summary.md`.

---

## Failure Recovery

- **Zero Rules Active:** Re-run `/torusguard init` to activate rules.
- **AST Parse Error:** Log syntax error on malformed file, skip, and continue.
- **Scorer Failure:** Ensure Python 3.10+; verify finding JSON structure.
- **Halt Trigger:** Abort if run folder cannot be allocated or disk write fails.

---

## Hallucination Guard

- ❌ Never invent finding IDs without AST line hashing.
- ❌ Never flag test fixtures as critical security flaws.
- ✅ Always calculate scores using `.torusguard/scripts/finding_scorer.py`.

---

## Output Card Format

```markdown
### 🔎 TorusGuard Static Audit Results
- **Run ID:** `run-YYYYMMDD-HHMMSS-audit`
- **Files Scanned:** [Count] source files
- **Total Findings:** [Count] ([Critical] Critical, [High] High)
- **Root Cause Clusters:** [Count] architectural issues
- **Confidence:** [Score]/100
- **Artifact:** `.torusguard/runs/<run_id>/findings.md`
```

---

## Next Steps

1. Run `/torusguard verify` to validate exploitability and review evidence.
2. Run `/torusguard harden` to generate minimal surgical remediation plans.
