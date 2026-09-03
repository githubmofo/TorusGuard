---
name: torusguard
description: "Autonomous security engine: 71 rules across 11 families, governed remediation (Ponytail Protocol), SARIF v2.1.0 exports, and 5-agent authority separation for Python & TypeScript web applications."
version: 0.9.5
---

# TorusGuard Master Security Router

**Principle:** If the browser receives it, users can inspect it. Keep secrets, database queries, and authorization strictly on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check
1. **If `.torusguard/` exists on disk:** Full governance active. Route slash commands to local specialist workflows below.
2. **If `.torusguard/` is absent (Autonomous AI Mode):** Operates standalone in any AI agent (Kimi, Antigravity, VS Code, Cursor). Apply in-memory security invariants:
   - Server-side auth & tenant scoping (`.filter(tenant=...)`).
   - Zero client-side secrets (`SUPABASE_SERVICE_ROLE_KEY`, live API keys).
   - Ponytail Protocol patch limits ($\le 35$ additions, $\le 25$ deletions).
   - *Upgrade:* Run `npx torusguard init` to unlock local `.torusguard/` run tracking & individual commands.

---

## Specialist Skill Routing (Lazy Loading)
Load **only** the designated sub-skill on demand to preserve the 1,000–1,500 token budget:

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
