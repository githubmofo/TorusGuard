---
name: torusguard
description: Universal autonomous security engine: 74 canonical rules across 18 families, polyglot stack detection across 16+ languages, Ponytail remediation bounds (<=35 add, <=25 del), standardized 75-column terminal UI, SARIF v2.1.0 exports, and persistent security memory context.
version: 2.0.0
---

# TorusGuard Master Security Engine & Command Router

**Core Invariant:** If the browser or client receives it, users can inspect it. Never expose database credentials, master keys, or private API secrets in client bundles. Always isolate multi-tenant database queries.

---

## Tri-Mode Execution & Command Catalog

TorusGuard operates with 100% feature parity across the compiled terminal CLI, AI chat slash commands, and Model Context Protocol (MCP) tools:

| Capability | Terminal CLI Command | AI Chat Slash Command | Specialist Skill | Governed Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Init** | `torusguard init` | `/torusguard init` | `.torusguard/skills/torusguard-init` | Stack discovery, rule activation, workspace scaffolding |
| **Status** | `torusguard status` | `/torusguard status` | `.torusguard/skills/torusguard-status` | Posture score, active rules, run history, scope check |
| **Audit** | `torusguard audit` | `/torusguard audit` | `.torusguard/skills/torusguard-audit` | Static AST scan, invariant fingerprinting, confidence scoring |
| **OCR Vision**| `torusguard ocr-scan <path>` | `/torusguard ocr-scan` | `.torusguard/skills/torusguard-ocr-scan` | Tesseract OCR secret scan on images/diagrams |
| **Verify** | `torusguard verify` | `/torusguard verify` | `.torusguard/skills/torusguard-verify` | Evidence sufficiency audit & line match calibration |
| **Harden** | `torusguard harden <patch>` | `/torusguard harden` | `.torusguard/skills/torusguard-harden` | Ponytail patch formulation ($\le 35$ add, $\le 25$ del) & reflection validation |
| **Apply** | `torusguard apply [--yes]` | `/torusguard apply` | `.torusguard/skills/torusguard-apply` | Human Gate review, `.bak` snapshots, patch application |
| **Rollback** | `torusguard rollback` | `/torusguard rollback` | `.torusguard/skills/torusguard-apply` | Instant 1-step rollback from pre-apply snapshots |
| **Recheck** | `torusguard recheck` | `/torusguard recheck` | `.torusguard/skills/torusguard-recheck` | Targeted differential AST scan, fix closure verification |
| **Recipes** | `torusguard recipes` | `/torusguard recipes` | `.torusguard/skills/torusguard-harden` | Explore verified Golden Fix Recipes from persistent memory |
| **Report** | `torusguard report --html` | `/torusguard report` | `.torusguard/skills/torusguard-report` | Executive posture reporting, SARIF v2.1.0 & visual HTML |
| **Authorize** | `torusguard authorize` | `/torusguard authorize` | `.torusguard/skills/torusguard-authorize`| Legal scope definition & safety boundaries |
| **Validate** | `torusguard web-validate` | `/torusguard web-validate` | `.torusguard/skills/torusguard-web-validate`| Authorized non-destructive HTTP probing |
| **Exploit** | `torusguard exploit-check` | `/torusguard exploit-check`| `.torusguard/skills/torusguard-exploit-check`| Bounded single-step exploitability confirmation |
| **Full** | `torusguard full` | `/torusguard full` | `.torusguard/skills/torusguard-full` | End-to-end 7-stage closed-loop execution |
| **MCP Server**| `torusguard mcp` | — | Native Stdio JSON-RPC 2.0 | Serves native Model Context Protocol tools to AI coding agents |
| **Update** | `torusguard update` | `/torusguard update` | `.torusguard/skills/torusguard-init` | Self-update TorusGuard engine binary |
| **Help** | `torusguard help` | `/torusguard help` | — | Interactive command guide |

---

## Non-Negotiable Invariants

1. **Browser-Code Truth:** If the client receives it, it is public. Zero hardcoded secrets (`SUPABASE_SERVICE_ROLE_KEY`, private tokens, live API keys) in frontend code (`TG-CLIENT-001`).
2. **Multi-Tenant Isolation:** All database lookups must be scoped by organization or user ownership (`tenant_id`, `organization_id`, `where: { tenantId }`) (`TG-DB-001`).
3. **Ponytail Churn Bounds:** Patches must be minimal and surgical ($\le 35$ additions, $\le 25$ deletions). Never perform full-file rewrites.
4. **Standardized 75-Column Terminal:** All CLI terminal output is strictly normalized to 75 visual columns with Unicode emoji width calculation, ANSI escape handling, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `[AllowAnonymous]`, or `csrf().disable()` (`TG-DIFF-001`).
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before touching disk code.
7. **Living Report Ground Truth:** All findings synchronize directly with `security_report.md` at workspace root.

---

## 🏛️ Alibaba OpenCodeReview Hybrid Architecture Integration
TorusGuard employs the dual-track hybrid architecture battle-tested at Alibaba Group scale:
1. **Deterministic Engineering Pipeline (Go CLI Engine):** Mechanical tasks (file traversal, whitespace tolerance, exact AST matching, Ponytail churn bounds calculation, pre-apply snapshot capture, and OCR extraction) are strictly executed by the compiled Go binary.
2. **Context Minimization (1/9th Token Strategy):** Agents never dump full files into prompt context. Bounded AST windows ($\pm 3$ lines) are extracted via `ExtractContext` to keep review tokens hyper-dense.
3. **Line-Level Reflection:** In remediation, the agent provides semantic intent (`find_snippet` + `replace_snippet`). The Go CLI reflection module pins and verifies line bounds deterministically, preventing line-number drift.

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
├── skills/                      # Canonical distribution skills for end-user AI agents
├── workflows/                   # Operational step-by-step workflow guides
└── snapshots/
    └── run-YYYYMMDD-HHMMSS-audit/ # Pre-apply .bak files for instant rollback
```

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Line-Number Diff Hallucination** | Guesses line numbers in unified diff headers (`@@ -42,5 +42,7 @@`) causing patch rejection. | Use the Line-Level Reflection Module (`SemanticPatch` with `find_snippet` and `replace_snippet`) to let Go resolve exact lines. |
| **Context Window Bloating** | Dumps entire 1,000-line source files into conversation when diagnosing a single finding. | Use bounded AST context extraction ($\pm 3$ lines) matching OpenCodeReview's 1/9th token efficiency. |
| **Full-File Rewrites** | Rewrites the entire file or surrounding business logic when fixing a vulnerability. | Strictly conform to Ponytail bounds ($\le 35$ additions, $\le 25$ deletions per bundle). |
| **Security Bypass Insertion** | Introduces `# nosec`, `verify=False`, or `[AllowAnonymous]` to make tests pass. | Strictly forbidden (`TG-DIFF-001`). Rejections are enforced fail-closed by the Go engine. |
| **Missing Multi-Tenant Scope** | Modifies queries to filter only by record `id`. | Always scope database lookups by tenant or user ownership (`tenantId: user.tenantId`). |

---

## ✅ Pre-Flight Self-Audit

Before producing any security remediation or analysis, verify:
- [ ] Did I read `security_report.md` at workspace root before proposing changes?
- [ ] Did I inspect only the bounded AST context window ($\pm 3$ lines) rather than the entire file?
- [ ] Does my proposed remediation stay strictly within Ponytail bounds ($\le 35$ additions, $\le 25$ deletions)?
- [ ] Is the fix free of any `# nosec`, `verify=False`, or bypass flags?
- [ ] Did I verify multi-tenant isolation on all database and model queries?
- [ ] Can this patch be applied via deterministic reflection (`find_snippet` -> `replace_snippet`)?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Inspect living security_report.md and bounded AST context snippet.
BUILD:  Formulate surgical SemanticPatch (find_snippet + replace_snippet within <=35 add / <=25 del).
CONFIRM: Validate via torusguard harden, apply snapshot, and execute differential torusguard recheck.
```
