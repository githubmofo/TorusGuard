---
name: torusguard
description: "Autonomous security engine: 88 rules across 22 families, polyglot heuristic scanning, First-Principles suite (Docker, Git Mine, ReDoS, AI & RAG), Hybrid First-Principles Vision OCR, governed remediation (Ponytail Protocol ≤35 add, ≤25 del), SARIF v2.1.0 exports, dark-mode HTML dashboards, fail-closed cryptography, SSRF defense, and DoS-resilient scanning for AI-built web applications."
version: 2.2.0
---

# TorusGuard Master Security Router

**Principle:** If the browser or client receives it, users can inspect it. Keep secrets, database queries, and authorization strictly on trusted server-side code.

---

## ⚡ Workspace Bootstrap Check
1. **If `.torusguard/` exists on disk:** Full autonomous governance active. Load `.torusguard/memory/context.json` into prompt context for local-first intelligence. Route commands to specialist workflows below.
2. **If `.torusguard/` is absent (Autonomous AI Mode):** Operates standalone in any AI agent (Antigravity, Cursor, Claude Code, Windsurf, VS Code, Kimi). Apply universal security invariants:
   - Server-side auth & tenant scoping (`.filter(tenant=...)`, `.Where("tenant_id = ?")`, `where: { tenantId: ... }`).
   - Zero client-side secrets (`SUPABASE_SERVICE_ROLE_KEY`, live API keys, Stripe secret keys).
   - Ponytail Protocol patch limits (≤35 additions, ≤25 deletions, zero full-file rewrites).
   - *Upgrade:* Run `torusguard init` to unlock local `.torusguard/` workspace tracking, persistent memory, and individual slash commands.

---

## Specialist Skill Routing (Lazy Loading)
Load **only** the designated sub-skill on demand to preserve the token budget:

| Command | Specialist Skill | Agent | Purpose |
| :--- | :--- | :--- | :--- |
| `/torusguard` | `skills/torusguard/SKILL.md` | `reviewer` | Interactive command center & overview |
| `/torusguard init` | `skills/torusguard-init/SKILL.md` | `profiler` | Workspace discovery, stack detection & scaffolding |
| `/torusguard status` | `skills/torusguard-status/SKILL.md` | `reviewer` | Diagnostic overview of posture, stack & rules |
| `/torusguard audit` | `skills/torusguard-audit/SKILL.md` | `auditor` | Static heuristic security audit & root-cause clustering |
| `/torusguard ocr-scan` | `skills/torusguard-ocr-scan/SKILL.md` | `auditor` | Hybrid First-Principles Vision OCR scan on images/diagrams |
| `/torusguard container` | `skills/torusguard-container/SKILL.md`| `auditor` | Dockerfile & Compose non-root & socket safety audit |
| `/torusguard git-mine` | `skills/torusguard-git-mine/SKILL.md` | `auditor` | Git commit packfile and config secret mining |
| `/torusguard redos` | `skills/torusguard-redos/SKILL.md` | `auditor` | Catastrophic regex exponential backtracking analysis |
| `/torusguard ai-guard` | `skills/torusguard-ai-guard/SKILL.md` | `auditor` | AI prompt injection and tenant vector isolation audit |
| `/torusguard verify` | `skills/torusguard-verify/SKILL.md` | `validator` | Evidence sufficiency & line match audit |
| `/torusguard harden` | `skills/torusguard-harden/SKILL.md` | `remediator`| Governed remediation under Ponytail Protocol |
| `/torusguard apply` | `skills/torusguard-apply/SKILL.md` | `remediator`| Governed patch application with rollback snapshots |
| `/torusguard rollback` | `skills/torusguard-apply/SKILL.md` | `remediator`| Instant restoration from pre-apply snapshots |
| `/torusguard recheck` | `skills/torusguard-recheck/SKILL.md` | `reviewer` | Differential re-scan & closure verification |
| `/torusguard review` | `skills/torusguard-review/SKILL.md` | `reviewer` | Incremental Git diff and PR gate review |
| `/torusguard recipes` | `skills/torusguard/SKILL.md` | `reviewer` | Persistent memory inspection & Golden Fix recipes |
| `/torusguard report` | `skills/torusguard-report/SKILL.md` | `reviewer` | Executive posture reporting, SARIF & visual HTML export |
| `/torusguard threatmodel` | `skills/torusguard-threatmodel/SKILL.md`| `reviewer`| Synthesize STRIDE threat model & Mermaid DFDs |
| `/torusguard benchmark` | `skills/torusguard/SKILL.md` | `validator` | SecurityReviewBench precision & recall suite |
| `/torusguard authorize` | `skills/torusguard-authorize/SKILL.md` | `reviewer` | Legal scope definition & safety boundaries |
| `/torusguard web-validate` | `skills/torusguard-web-validate/SKILL.md` | `validator` | Authorized non-destructive HTTP probing |
| `/torusguard exploit-check`| `skills/torusguard-exploit-check/SKILL.md`| `validator` | Bounded single-step exploitability confirmation |
| `/torusguard mcp` | `.agents/mcp_config.json` | `server` | Native Model Context Protocol (MCP) JSON-RPC 2.0 stdio server |
| `/torusguard full` | `skills/torusguard-full/SKILL.md` | *All* | End-to-end 7-stage closed-loop execution |

*Note: Never load all skills simultaneously. Lazy-load strictly on demand.*
