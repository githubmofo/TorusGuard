# TorusGuard Security Philosophy

## The Problem

AI coding assistants generate functional code at unprecedented speed, but they consistently overlook foundational security boundaries:

- **Client-side secret exposure** — Embedding database credentials, service role keys, and API tokens directly in frontend bundles.
- **Missing tenant isolation** — Allowing unpartitioned primary key lookups that expose one user's data to another.
- **SQL injection via string interpolation** — Using template literals instead of parameterized queries.
- **SSRF vectors** — Fetching user-provided URLs without hostname whitelisting or private IP blocking.
- **Full-file rewrites** — Rewriting entire files during remediation, introducing unreviewed changes alongside the security fix.

## The Solution

TorusGuard acts as a **deterministic security gate** between AI-generated code and production. It separates concerns:

- **Intelligence** stays in the AI agent (patch generation, root-cause analysis).
- **Enforcement** stays in the Go binary (bounds checking, scanning, snapshotting).

This separation ensures that security rules are never bypassed by the AI's reasoning, regardless of how the developer's prompt is worded.

## Core Principles

### 1. Fail-Closed Over Fail-Open

When TorusGuard encounters an ambiguous state, it fails closed:
- Crypto failure → panic (no fallback tokens)
- Scan timeout → abort (no partial results presented as complete)
- Path escape → block (no "best effort" snapshot outside workspace)

### 2. Surgical Over Sweeping

The Ponytail Protocol enforces minimal diffs:
- ≤35 line additions per patch bundle
- ≤25 line deletions per patch bundle
- Zero full-file rewrites

This ensures every changed line is reviewable in a single screen. It prevents AI agents from burying security changes inside large refactors.

### 3. Evidence Over Claims

TorusGuard maintains a living `security_report.md` as the single source of truth. Every finding must be:
- Discovered (via `audit`)
- Verified (via `verify`)
- Remediated (via `harden` + `apply`)
- Confirmed (via `recheck`)

No finding is marked as fixed without re-scanning the modified file.

### 4. Human Gate Over Automation

The `apply` command requires explicit `--yes` confirmation. This is intentional: no AI agent should modify source files without a human explicitly approving the change. The pre-apply `.bak` snapshot is created *before* confirmation, ensuring rollback is always possible.

### 5. Transparency Over Obscurity

- The web validator injects `X-TorusGuard-Audit: true` headers so target applications know they are being probed.
- The exploit checker uses only inert payloads (e.g., `1' OR '1'='1`) that cannot cause real damage.
- All scan findings include the file path and matching pattern for auditability.

## What TorusGuard Is Not

- **Not a WAF.** It does not intercept live traffic or sit in the request path.
- **Not a SAST replacement.** It uses heuristic regex scanning, not full AST parsing. It complements tools like Semgrep, not replaces them.
- **Not a vulnerability database.** It does not track CVEs or maintain dependency advisories. Use `npm audit` or Snyk for that.
- **Not an AI agent.** It is a deterministic enforcer. Intelligence comes from the host AI agent; TorusGuard provides the guardrails.
