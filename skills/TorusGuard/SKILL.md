---
name: torusguard
description: Security guardrails, provenance-tracked evidence, authorized runtime validation, and auditable verification workflow for AI-built web apps across Python (Django, DRF, FastAPI, Flask, SQLAlchemy) and TypeScript (React, Next.js, Express, Supabase, Firebase).
---

# TorusGuard (v0.8.0 Skill Kit)

**Tagline:** Security guardrails, governed remediation, and authorized runtime validation for AI-built web applications.  
**Core Principle:** If the browser receives it, users can inspect it. Keep secrets, direct database access, and authorization decisions on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check (Pre-Flight)

Before executing any TorusGuard security action or slash command:

1. **Verify Workspace Setup:**
   Check if the workspace contains `.torusguard/TORUSGUARD.md`.
2. **If `.torusguard/TORUSGUARD.md` exists:**
   Load `.torusguard/TORUSGUARD.md` as your primary rules file. Route all commands through `.torusguard/config/slash-commands.json`.
3. **If `.torusguard/` is missing:**
   The workspace is not yet initialized. Instruct the user to run `/torusguard init` to scaffold `.torusguard/`.

---

## 🛠️ Available Commands

All commands are defined in `.torusguard/config/slash-commands.json` and executed via their respective workflow:

| Command | Primary Role | Lifecycle Phase | Description |
| :--- | :--- | :--- | :--- |
| `/torusguard init` | `profiler` | Baseline | Detect project stack, activate rules, initialize `.torusguard/` |
| `/torusguard authorize` | `reviewer` | Legal Gate | Capture target ownership, hosts, paths, and generate `scope.json` |
| `/torusguard audit` | `auditor` | Static Scan | Scan source ASTs, assign Stable IDs, cluster by root cause |
| `/torusguard verify` | `validator` | Verification | Validate evidence sufficiency and evaluate 0–100 confidence score |
| `/torusguard web-validate` | `validator` | Runtime Probe | Dispatch authorized HTTP/API probes with token redaction |
| `/torusguard exploit-check` | `validator` | Exploitability | Execute bounded exploitability checks for approved classes |
| `/torusguard harden` | `remediator` | Remediation | Generate structured remediation bundles with before/after diffs |
| `/torusguard apply` | `remediator` | Patch Apply | Apply surgical governed patches (<=35 add, <=25 del) |
| `/torusguard recheck` | `reviewer` | Verification | Re-scan modified files to verify fixes and detect regressions |
| `/torusguard report` | `reviewer` | Export | Generate unified Markdown report and OASIS SARIF v2.1.0 output |
| `/torusguard status` | *System* | Status | Show project security posture, run history, and active rules |

---

## 🛡️ Governance & Rules Reference

Full operating rules, 0–100 confidence scoring, and role definitions are located in:
- **Master Rules:** `.torusguard/TORUSGUARD.md`
- **Configuration:** `.torusguard/config/torusguard.json`
- **Command Registry:** `.torusguard/config/slash-commands.json`
- **Active Rules:** `.torusguard/rules/active/`
- **Run Artifacts:** `.torusguard/runs/<run-id>/`
