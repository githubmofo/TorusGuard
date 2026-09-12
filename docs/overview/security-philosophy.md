# TorusGuard Security Philosophy & Governance Principles

TorusGuard is a Markdown-first, portable AI-agent security guidance framework, autonomous remediation engine, and authorized runtime validation system. It is designed to empower software developers, security champions, and AI coding agents to detect, verify, govern, and remediate web application vulnerabilities without introducing chaos, operational risk, or unverified claims.

---

## 1. Non-Negotiable Core Invariants

TorusGuard enforces seven immutable engineering and architectural invariants across all workflows:

1. **The Browser-Code Truth:** Any code, state, or secret transmitted to a client browser can and will be inspected via DevTools. All authorization, tenant isolation, and credential handling must reside strictly on trusted server runtimes (`TG-CLIENT-001`, `TG-CLIENT-002`).
2. **Multi-Tenant Isolation:** Always scope database lookups and state mutations by tenant or user ownership (e.g., `tenant_id`, `where: { tenantId: user.tenantId }`). Never permit unpartitioned primary key lookups (`TG-DB-001`).
3. **Ponytail Churn Bounds:** Never attempt full-file rewrites. Automated and agentic patches must be minimal surgical diffs ($\le 35$ additions, $\le 25$ deletions per bundle).
4. **Standardized 75-Column Terminal:** All CLI terminal outputs must strictly adhere to 75 visual columns with Unicode emoji width calculation, ANSI escape stripping, and visual truncation with ellipsis (`...`).
5. **Zero Security Bypasses:** Never insert `# nosec`, `verify=False`, `InsecureSkipVerify: true`, `csrf().disable()`, `[AllowAnonymous]`, or `CURLOPT_SSL_VERIFYPEER => false` (`TG-DIFF-001`).
6. **Snapshots Before Edits:** Every code modification must capture a byte-for-byte pre-apply backup in `.torusguard/snapshots/<run_id>/` before modifying files on disk.
7. **Living Security Report Ground Truth:** All finding discoveries, patch formulations, applications, and recheck verifications must synchronize with `security_report.md` at the workspace root to maintain verifiable finding state and eliminate hallucination.

---

## 2. Strict Safety & Operational Boundaries

### 🔒 1. Strict Authorization Prerequisite
TorusGuard enforces a hard legal boundary before any network-level probing is permitted:
- **No Authorization, Zero Probing:** Any runtime HTTP request, route inspection, or browser navigation is blocked at the execution boundary unless an explicit, unexpired `authorization.md` and `scope.json` manifest is present in the active run directory.
- **Strict Scope Bounding:** Probes are constrained to whitelisted target hosts (`target_hosts`), allowed path prefixes (`allowed_path_prefixes`), bounded request quotas (`max_requests`), and maximum crawl depths (`max_depth`). Out-of-scope targets trigger an immediate `AuthorizationError`.
- **Absolute Denial for Forbidden Paths:** Administrative endpoints matching destructive signatures (e.g., `/admin/delete`, `/system/shutdown`, `/db/reset`) are permanently blocked by policy.

### 🛡️ 2. Bounded, Non-Destructive Probing Only
TorusGuard rejects weaponized testing techniques:
- **Single-Step Confirmation:** Runtime exploitability checks operate through passive or strictly bounded single-step HTTP queries that stop on the first verifiable proof of weakness (e.g., observing a sensitive canary string or inspecting unescaped response headers).
- **Zero Destructive Exploits:** TorusGuard strictly prohibits denial-of-service payloads, memory corruption techniques, multi-threaded password brute forcing, or high-volume parameter fuzzing.
- **Safety Over Exploitation:** If a vulnerability cannot be safely proven without risking data destruction or denial of service, TorusGuard stops probing and flags the finding as `Needs Manual Review`.

### 🚦 3. Tiered Safety Review Gates
All actions executed by TorusGuard agents are evaluated against tiered review levels:
- **Auto-Allowed:** Safe, non-mutating HTTP `GET` requests against non-sensitive, in-scope public routes.
- **Approval Required:** State-altering operations or requests targeting sensitive modules (authentication, tenant management, file uploads) require pre-approved explicit authorization.
- **Manual Only:** Highly dangerous or destructive operations are permanently blocked from automated execution and delegated strictly to human security professionals.

### 🚫 4. No Weaponized Offensive Tooling
TorusGuard is deliberately **not** an autonomous offensive penetration testing agent:
- It does not search for 0-days across arbitrary third-party infrastructure.
- It does not attempt privilege escalation beyond bounded contract assertions.
- It exists solely to assist engineering teams in establishing reliable guardrails, verifying static detection claims against authorized staging environments, and applying governed, surgical fixes.

---

## 3. TorusGuard's Dual Role: Detection & Governed Remediation

TorusGuard bridges the gap between static AST analysis, practical runtime verification, and governed automated code fixes:

### A. Static Detection & Clustering (74 Rules Across 18 Families)
- Detects known vulnerability anti-patterns across 74 canonical security rules spanning secrets (`TG-SEC`), authentication (`TG-AUTH`), multi-tenancy (`TG-DB`), input validation (`TG-INPUT`), rate limiting (`TG-RATE`), agentic AI defense (`TG-AGENT`), SSRF (`TG-SSRF`), webhooks (`TG-WEBHOOK`), WebSockets (`TG-WS`), CSRF (`TG-CSRF`), GraphQL (`TG-GQL`), supply chain (`TG-SUPPLY`), business logic (`TG-BIZ`), cache poisoning (`TG-CACHE`), client secrets (`TG-CLIENT`), server platform (`TG-PLATFORM`), diff integrity (`TG-DIFF`), and edge computing (`TG-EDGE`).
- Derives line-shift invariant fingerprints (`FindingFingerprint`) that survive code refactorings.
- Clusters repeated vulnerabilities by underlying root causes (e.g., `cluster-tenant-isolation`) to prevent alert fatigue.

### B. Guided Runtime Validation
- Evaluates practical reachability on authorized staging/test instances.
- Replaces subjective risk assertions with five formal, evidence-backed statuses:
  1. `Runtime Confirmed`: Indisputable proof with sensitive marker reflection.
  2. `Runtime Likely`: Status code and behavioral indicators strongly suggest exploitability without payload reflection.
  3. `Needs Manual Review`: Ambiguous responses (e.g., HTTP 500/502) or complex architectural boundaries requiring human review.
  4. `Not Reproducible in Scope`: Route protected by active gateways, 401/403 barriers, or middleware.
  5. `Blocked by Environment / Controls`: Safety gate halted probing to protect system stability.

### C. Governed, Surgical Remediation & Living Ledger
- Governs automated code changes using strict line churn boundaries ($\le 35$ additions, $\le 25$ deletions per bundle).
- Enforces mandatory human security sign-offs (Human Gate) with pre-apply rollback snapshots archived in `.torusguard/snapshots/<run_id>/`.
- Validates all code changes through targeted differential AST re-checks.
- Automatically maintains `security_report.md` at workspace root as the single source of truth across both CLI and AI chat sessions.
