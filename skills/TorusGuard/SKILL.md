---
name: torusguard
description: Universal autonomous security engine: 74 canonical rules across 18 families, polyglot stack detection across 16+ languages, Ponytail remediation bounds (<=35 add, <=25 del), standardized 75-column terminal UI, living security_report.md ground-truth ledger, SARIF v2.1.0 exports, and persistent security memory context.
version: 1.3.5
---

# TorusGuard Master Security Engine & Command Router

**Core Invariant:** If the browser or client receives it, users can inspect it. Never expose database credentials, master keys, or private API secrets in client bundles. Always isolate multi-tenant database queries.

---

## Command Catalog: Terminal CLI & AI Chat Parity

TorusGuard operates with 100% feature parity across both the terminal CLI and AI chat slash commands:

| Capability | Terminal CLI Command | AI Chat Slash Command | Specialist Skill | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Init** | `npx torusguard init` | `/torusguard init` | `skills/torusguard-init` | Stack discovery, rule activation, workspace scaffolding |
| **Status** | `npx torusguard status` | `/torusguard status` | `skills/torusguard-status` | Posture score, active rules, run history, scope check |
| **Audit** | `npx torusguard audit` | `/torusguard audit` | `skills/torusguard-audit` | Static AST scan, invariant fingerprinting, confidence scoring |
| **Verify** | `npx torusguard verify` | `/torusguard verify` | `skills/torusguard-verify` | Evidence sufficiency audit & line match calibration |
| **Harden** | `npx torusguard harden` | `/torusguard harden` | `skills/torusguard-harden` | Ponytail patch formulation ($\le 35$ add, $\le 25$ del) |
| **Apply** | `npx torusguard apply [--yes]` | `/torusguard apply` | `skills/torusguard-apply` | Human Gate review, `.bak` snapshots, patch application |
| **Rollback** | `npx torusguard rollback` | `/torusguard rollback` | `skills/torusguard-apply` | Instant 1-step rollback from pre-apply snapshots |
| **Recheck** | `npx torusguard recheck` | `/torusguard recheck` | `skills/torusguard-recheck` | Targeted differential AST scan, fix closure verification |
| **Recipes** | `npx torusguard recipes` | `/torusguard recipes` | `skills/torusguard-harden` | Explore verified Golden Fix Recipes from persistent memory |
| **Report** | `npx torusguard report --html` | `/torusguard report` | `skills/torusguard-report` | Executive posture reporting, SARIF v2.1.0 & visual HTML |
| **Authorize** | `npx torusguard authorize` | `/torusguard authorize` | `skills/torusguard-authorize`| Legal scope definition & safety boundaries |
| **Validate** | `npx torusguard web-validate` | `/torusguard web-validate` | `skills/torusguard-web-validate`| Authorized non-destructive HTTP probing |
| **Exploit** | `npx torusguard exploit-check` | `/torusguard exploit-check`| `skills/torusguard-exploit-check`| Bounded single-step exploitability confirmation |
| **Full** | `npx torusguard full` | `/torusguard full` | `skills/torusguard-full` | End-to-end 7-stage closed-loop execution |
| **Sync** | `npx torusguard rules sync` | `/torusguard rules sync` | `skills/torusguard-init` | Synchronize rules across AI editors (Cursor, Claude, Antigravity) |

---

## Non-Negotiable Invariants

1. **Browser-Code Truth:** If the client receives it, it is public. Zero hardcoded secrets (`SUPABASE_SERVICE_ROLE_KEY`, private tokens, live API keys) in frontend code.
2. **Multi-Tenant Isolation:** All database lookups must be scoped by organization or user ownership (`tenant_id`, `organization_id`, `where: { tenantId }`).
3. **Ponytail Churn Bounds:** Patches must be minimal and surgical ($\le 35$ additions, $\le 25$ deletions). Never perform full-file rewrites.
4. **Standardized 75-Column Terminal:** All CLI terminal output is strictly normalized to 75 visual columns with Unicode emoji width calculation, ANSI escape handling, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `[AllowAnonymous]`, or `csrf().disable()`.
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before touching disk code.
7. **Living Security Report Ground Truth:** All finding discoveries, patch formulations, applications, and recheck verifications must synchronize with `security_report.md` at the workspace root to maintain verifiable finding state and eliminate hallucination.

---

## Workspace Layout Structure
```
.torusguard/
├── config/
│   ├── torusguard.json          # Detected stack, settings, and rule counts
│   └── scope.json               # Authorized runtime validation targets & TTL
├── memory/
│   ├── context.json             # Aggregated security memory context
│   ├── patterns.json            # Distilled Golden Fix Recipes
│   └── events.json              # Historical audit, apply, and recheck events
├── rules/
│   └── active/                  # Active TG-* rule definitions
├── runs/
│   └── run-YYYYMMDD-HHMMSS-audit/
│       ├── findings.json        # Machine-readable AST findings
│       ├── findings.md          # Actionable markdown finding cards
│       ├── remediation.md       # Formulated candidate patch catalog
│       ├── diff_summary.md      # Summary of applied diffs
│       ├── recheck.md           # Differential recheck status transitions
│       ├── report.html          # Single-file visual dark-mode HTML report
│       ├── results.sarif        # OASIS SARIF v2.1.0 log
│       └── bundles/             # Formulated Ponytail remediation bundles
└── snapshots/
    └── run-YYYYMMDD-HHMMSS-audit/ # Pre-apply .bak files for instant rollback
```
