---
name: torusguard
description: "Universal autonomous security engine: 71 rules across 11 families, polyglot stack detection across 16+ languages, governed remediation (Ponytail Protocol <=35 add, <=25 del), SARIF v2.1.0 exports, single-file HTML dashboards, and persistent security memory context for modern web applications."
version: 1.3.0
---

# TorusGuard Master Security Router

**Principle:** If the browser or client receives it, users can inspect it. Keep secrets, database queries, and authorization strictly on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check
1. **If `.torusguard/` exists on disk:** Full autonomous governance active. Load `.torusguard/memory/context.json` into prompt context for local-first intelligence. Route commands to specialist workflows below.
2. **If `.torusguard/` is absent (Autonomous AI Mode):** Operates standalone in any AI agent (Kimi, Antigravity, VS Code, Cursor, Claude Code, Windsurf). Apply universal security invariants:
   - Server-side auth & tenant scoping (`.filter(tenant=...)`, `.Where("tenant_id = ?")`, `where: { tenantId: ... }`).
   - Zero client-side secrets (`SUPABASE_SERVICE_ROLE_KEY`, live API keys, Stripe secret keys).
   - Ponytail Protocol patch limits ($\le 35$ additions, $\le 25$ deletions, zero full-file rewrites).
   - *Upgrade:* Run `npx torusguard init` to unlock local `.torusguard/` workspace tracking, persistent memory, and individual slash commands.

---

## Specialist Skill Routing (Lazy Loading)
Load **only** the designated sub-skill on demand to preserve the 1,000–1,500 token budget:

| Command | Specialist Skill | Agent | Purpose |
| :--- | :--- | :--- | :--- |
| `/torusguard init` | `skills/torusguard-init/SKILL.md` | `profiler` | Workspace discovery, stack detection & scaffolding |
| `/torusguard authorize` | `skills/torusguard-authorize/SKILL.md` | `reviewer` | Legal scope definition & safety boundaries |
| `/torusguard audit` | `skills/torusguard-audit/SKILL.md` | `auditor` | Static AST security audit & root-cause clustering |
| `/torusguard verify` | `skills/torusguard-verify/SKILL.md` | `validator` | Evidence sufficiency & line match audit |
| `/torusguard web-validate` | `skills/torusguard-web-validate/SKILL.md` | `validator` | Authorized non-destructive HTTP probing |
| `/torusguard exploit-check`| `skills/torusguard-exploit-check/SKILL.md`| `validator` | Bounded single-step exploitability confirmation |
| `/torusguard harden` | `skills/torusguard-harden/SKILL.md` | `remediator`| Governed remediation under Ponytail Protocol |
| `/torusguard apply` | `skills/torusguard-apply/SKILL.md` | `remediator`| Governed patch application with rollback snapshots |
| `/torusguard recheck` | `skills/torusguard-recheck/SKILL.md` | `reviewer` | Differential AST re-scan & closure verification |
| `/torusguard report` | `skills/torusguard-report/SKILL.md` | `reviewer` | Executive posture reporting, SARIF & visual HTML export |
| `/torusguard status` | `skills/torusguard-status/SKILL.md` | `reviewer` | Diagnostic overview of posture, stack & rules |
| `/torusguard memory` | `skills/torusguard/SKILL.md` | `reviewer` | Persistent memory inspection, decay & context cards |
| `/torusguard full` | `skills/torusguard-full/SKILL.md` | *All* | End-to-end 7-stage closed-loop execution |

*Note: Never load all skills simultaneously. Lazy-load strictly on demand.*
