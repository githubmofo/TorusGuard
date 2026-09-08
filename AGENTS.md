# TorusGuard Security Guardrails & Invariants

TorusGuard enforces autonomous security guardrails, governed remediation, and authorized runtime validation across polyglot web applications.

## Quick CLI & Chat Commands
- **Audit:** `npx torusguard audit` or `/torusguard audit` (Static AST security audit & scoring)
- **Harden:** `npx torusguard harden` or `/torusguard harden` (Ponytail Protocol candidate patches $\le 35$ add, $\le 25$ del)
- **Apply:** `npx torusguard apply` or `/torusguard apply` (Human Gate, `.bak` rollback snapshots, Golden Fix distillation)
- **Rollback:** `npx torusguard rollback` (Instant restore from pre-apply snapshots in `.torusguard/snapshots/`)
- **Re-check:** `npx torusguard recheck` or `/torusguard recheck` (Differential AST fix closure verification)
- **Recipes:** `npx torusguard recipes` (Explore verified Golden Fix Recipes from persistent memory)
- **Report:** `npx torusguard report --html` (Generate single-file visual dark-mode HTML posture report)
- **Sync:** `npx torusguard rules sync` (Synchronize AI editor rules across Cursor, Claude, Antigravity, Windsurf)

## Non-Negotiable Invariants
1. **Browser-Code Truth:** If the browser receives it, users can inspect it. Never expose database credentials, service role keys, or private API secrets in frontend or client bundles.
2. **Multi-Tenant Isolation:** Always scope database lookups by tenant or user ownership (e.g. `tenant_id`, `where: { tenantId: ... }`).
3. **Ponytail Churn Bounds:** Never attempt full-file rewrites. Patches must be minimal surgical diffs ($\le 35$ additions, $\le 25$ deletions).
4. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, or `[AllowAnonymous]`.
