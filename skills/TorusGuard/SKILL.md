---
name: torusguard
description: Security guardrails, governed remediation, and authorized runtime validation for AI-built web applications across Python and TypeScript.
version: 0.9.2
---

# TorusGuard Master Router

**Principle:** If the browser receives it, users can inspect it. Keep secrets, direct database access, and authorization on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check
1. **If `.torusguard/` exists:** Load matching specialist skill on demand per command.
2. **If `.torusguard/` is missing:** The AI agent MUST immediately run `python skills/torusguard/bootstrap.py --target .` (or from `.agent/skills/torusguard/bootstrap.py`) to scaffold `.torusguard/` and register slash commands.

---

## Specialist Skill Routing (Lazy Loading)
Load **only** the designated sub-skill when a slash command is executed to maintain strict 1,000–1,500 token budget:

| Command | Specialist Skill | Agent |
| :--- | :--- | :--- |
| `/torusguard init` | `skills/torusguard-init/SKILL.md` | `profiler` |
| `/torusguard authorize` | `skills/torusguard-authorize/SKILL.md` | `reviewer` |
| `/torusguard audit` | `skills/torusguard-audit/SKILL.md` | `auditor` |
| `/torusguard verify` | `skills/torusguard-verify/SKILL.md` | `validator` |
| `/torusguard web-validate` | `skills/torusguard-web-validate/SKILL.md` | `validator` |
| `/torusguard exploit-check` | `skills/torusguard-exploit-check/SKILL.md` | `validator` |
| `/torusguard harden` | `skills/torusguard-harden/SKILL.md` | `remediator` |
| `/torusguard apply` | `skills/torusguard-apply/SKILL.md` | `remediator` |
| `/torusguard recheck` | `skills/torusguard-recheck/SKILL.md` | `reviewer` |
| `/torusguard report` | `skills/torusguard-report/SKILL.md` | `reviewer` |
| `/torusguard status` | `skills/torusguard-status/SKILL.md` | `reviewer` |
| `/torusguard full` | `skills/torusguard-full/SKILL.md` | *All* |

*Note: Never load all skills simultaneously. Lazy-load strictly on demand.*
