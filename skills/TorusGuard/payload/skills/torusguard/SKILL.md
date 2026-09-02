---
name: torusguard
description: Security guardrails, provenance-tracked evidence, authorized runtime validation, and auditable verification workflow for AI-built web apps across Python (Django, DRF, FastAPI, Flask, SQLAlchemy) and TypeScript (React, Next.js, Express, Supabase, Firebase).
version: 0.9.2
---

# TorusGuard (v0.9.2 Skill Kit)

**Tagline:** Security guardrails, governed remediation, and authorized runtime validation for AI-built web applications.  
**Core Principle:** If the browser receives it, users can inspect it. Keep secrets, direct database access, and authorization decisions on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check (Pre-Flight)

Before executing any TorusGuard security action or slash command:

1. **Verify Workspace Setup:**
   Check if the workspace contains `.torusguard/TORUSGUARD.md`.
2. **If `.torusguard/TORUSGUARD.md` exists:**
   Load `.torusguard/TORUSGUARD.md` as your primary rules file. Route all commands through `.torusguard/config/slash-commands.json` or to their designated specialist skill.
3. **If `.torusguard/` is missing:**
   The workspace is not yet initialized. Run `python <path-to-skill>/bootstrap.py` or instruct the user to run `/torusguard init` to autonomously scaffold `.torusguard/`.

---

## 🔀 Specialist Skill Routing (Lazy Loading)

Each TorusGuard command has a dedicated specialist skill with complete, self-contained instructions.
When a specific command is invoked, load **only** the matching specialist skill:

| Command | Load Specialist Skill | Agent | Lifecycle Phase |
| :--- | :--- | :--- | :--- |
| `/torusguard init` | `skills/torusguard-init/SKILL.md` | `profiler` | Baseline Discovery |
| `/torusguard authorize` | `skills/torusguard-authorize/SKILL.md` | `reviewer` | Legal Scope Gate |
| `/torusguard audit` | `skills/torusguard-audit/SKILL.md` | `auditor` | Static Scan & Cluster |
| `/torusguard verify` | `skills/torusguard-verify/SKILL.md` | `validator` | Evidence Verification |
| `/torusguard web-validate`| `skills/torusguard-web-validate/SKILL.md` | `validator` | Runtime HTTP Probing |
| `/torusguard exploit-check`| `skills/torusguard-exploit-check/SKILL.md`| `validator` | Exploitability Check |
| `/torusguard harden` | `skills/torusguard-harden/SKILL.md` | `remediator` | Remediation Bundles |
| `/torusguard apply` | `skills/torusguard-apply/SKILL.md` | `remediator` | Governed Patch Apply |
| `/torusguard recheck` | `skills/torusguard-recheck/SKILL.md` | `reviewer` | Regression Re-scan |
| `/torusguard report` | `skills/torusguard-report/SKILL.md` | `reviewer` | Report & SARIF Export |
| `/torusguard status` | `skills/torusguard-status/SKILL.md` | *System* | Status & History |
| `/torusguard full` | `skills/torusguard-full/SKILL.md` | *All* | End-to-End Pipeline |

*Do not load all skills simultaneously. Load only the specific specialist matching the command to preserve context budget.*

---

## 🛡️ Governance & Rules Reference

Full operating rules, 0–100 confidence scoring, and role definitions are located in:
- **Master Rules:** `.torusguard/TORUSGUARD.md`
- **Configuration:** `.torusguard/config/torusguard.json`
- **Command Registry:** `.torusguard/config/slash-commands.json`
- **Active Rules:** `.torusguard/rules/active/`
- **Run Artifacts:** `.torusguard/runs/<run-id>/`
