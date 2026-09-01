# TorusGuard Security Philosophy & Governance Principles

TorusGuard is a Markdown-first, portable AI-agent security guidance framework and authorized runtime validation system. It is designed to empower software developers, security champions, and AI coding agents to detect, verify, govern, and remediate web application vulnerabilities without introducing chaos, operational risk, or unverified claims.

---

## 1. Core Principles & Non-Negotiables

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

## 2. TorusGuard's Dual Role: Detection & Governed Remediation

TorusGuard bridges the gap between static AST analysis, practical runtime verification, and governed automated code fixes:

### A. Static Detection & Clustering
- Detects known vulnerability anti-patterns across 64 canonical security rules spanning secrets, authentication, multi-tenancy, input validation, CSRF, SSRF, webhooks, GraphQL, WebSockets, and CI/CD pipelines.
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

### C. Governed, Surgical Remediation
- Governs automated code changes using strict line churn boundaries ($\le 35$ additions, $\le 25$ deletions per file).
- Enforces mandatory human security sign-offs whenever sensitive modules (auth, tenancy, secrets, uploads, CI/CD) are modified.
- Validates all code changes through targeted re-checks scoped to modified files and adjacent trust boundaries.
