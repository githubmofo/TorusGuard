# TorusGuard Security Guardrails & Invariants

TorusGuard enforces autonomous security guardrails, governed remediation, and authorized runtime validation across polyglot web applications.

## Quick CLI & Chat Commands
- **Init:** `npx torusguard init` or `/torusguard init` (Project stack detection, rule activation, workspace scaffolding)
- **Status:** `npx torusguard status` or `/torusguard status` (Read-only diagnostic overview of posture, stack & rules)
- **Audit:** `npx torusguard audit` or `/torusguard audit` (Static AST security audit & scoring)
- **Verify:** `npx torusguard verify` or `/torusguard verify` (Evidence sufficiency verification & line match audit)
- **Harden:** `npx torusguard harden` or `/torusguard harden` (Ponytail Protocol candidate patches $\le 35$ add, $\le 25$ del)
- **Apply:** `npx torusguard apply [--yes]` or `/torusguard apply` (Human Gate, `.bak` rollback snapshots, Golden Fix distillation)
- **Rollback:** `npx torusguard rollback` or `/torusguard rollback` (Instant restore from pre-apply snapshots in `.torusguard/snapshots/`)
- **Recheck:** `npx torusguard recheck` or `/torusguard recheck` (Differential AST fix closure verification)
- **Recipes:** `npx torusguard recipes` or `/torusguard recipes` (Explore verified Golden Fix Recipes from persistent memory)
- **Report:** `npx torusguard report --html` or `/torusguard report` (Generate single-file visual dark-mode HTML posture report)
- **Authorize:** `npx torusguard authorize` or `/torusguard authorize` (Runtime target scope definition & TTL boundaries)
- **Validate:** `npx torusguard web-validate` or `/torusguard web-validate` (Authorized non-destructive HTTP probing)
- **Exploit:** `npx torusguard exploit-check` or `/torusguard exploit-check` (Bounded single-step exploitability confirmation)
- **Sync:** `npx torusguard rules sync` or `/torusguard rules sync` (Synchronize AI editor rules across Cursor, Claude, Antigravity, Windsurf)

## Non-Negotiable Invariants
1. **Browser-Code Truth:** If the browser receives it, users can inspect it. Never expose database credentials, service role keys, or private API secrets in frontend or client bundles.
2. **Multi-Tenant Isolation:** Always scope database lookups by tenant or user ownership (e.g. `tenant_id`, `where: { tenantId: ... }`).
3. **Ponytail Churn Bounds:** Never attempt full-file rewrites. Patches must be minimal surgical diffs ($\le 35$ additions, $\le 25$ deletions).
4. **Standardized 75-Column Terminal:** All CLI terminal outputs must strictly adhere to 75 visual columns with Unicode emoji width calculation, ANSI escape stripping, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, or `[AllowAnonymous]`.
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before modifying files on disk.
