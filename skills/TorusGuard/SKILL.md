---
name: torusguard
description: Security guardrails, provenance-tracked evidence, and auditable verification workflow for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, Django, DRF, FastAPI, Flask, SQLAlchemy, and Python APIs.
---

# TorusGuard (v0.7.0)

**Tagline:** Authorized runtime validation, bounded exploitability confirmation, governed remediation, and targeted recheck for AI-built web applications.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard v0.7.0 extends TorusGuard from a governed static remediation system into an **authorized runtime validation and bounded exploitability confirmation system**. It allows security architects and AI coding agents to validate findings against live, authorized applications, prove practical reachability without destructive payloads, capture redacted HTTP/browser evidence, and orchestrate role-separated multi-agent remediation.

---

## 🔄 Lifecycle Architecture (v0.7.0)

```text
+-----------------+     +-----------+     +--------------+     +--------------+     +-------------+     +----------+     +-----------+
| 0. Authorize    | --> | 1. Profile| --> | 2. Audit     | --> | 3. Validate  | --> | 4. Remediate| --> | 5. Apply | --> | 6. Recheck|
| (Legal & Scope) |     | (Stack/AST|     | (Cluster/ID) |     | (Exploitability)   | (Bundles)   |     | (Ponytail|     | (Fixed?)  |
+-----------------+     +-----------+     +--------------+     +--------------+     +-------------+     +----------+     +-----------+
```

1. **Authorize (`/torusguard authorize`):** Captures explicit target ownership or written permission, allowed duration, hosts, and paths. Writes `authorization.md` and `scope.json`.
2. **Profile (Profiler Role):** Discovers stack profile, framework layout, route ASTs, and storage boundaries.
3. **Audit (`/torusguard audit`):** Scans source code, derives invariant Stable Finding Fingerprints, and clusters alerts by root cause.
4. **Validate (`/torusguard web-validate` & `/torusguard exploit-check` - Validator Role):** Dispatches authorized, non-destructive HTTP/browser probes to evaluate practical exploitability into 5 formal statuses:
   - `Runtime Confirmed` (Indisputable proof with sensitive marker)
   - `Runtime Likely` (Strong runtime indicators)
   - `Needs Manual Review` (Inconclusive or complex boundary)
   - `Not Reproducible in Scope` (Protected by active gateway/middleware)
   - `Blocked by Environment / Controls` (Safety gate halted probe)
5. **Remediate (`/torusguard harden` - Remediator Role):** Formulates self-contained Remediation Bundles enriched with runtime exploitability insights.
6. **Apply (`/torusguard apply`):** Executes surgical, minimal-churn code changes guarded by line additions (<= 35) and deletions (<= 25).
7. **Re-check (`/torusguard recheck`):** Re-runs scoped recheck on modified files to guarantee fix integrity and detect regressions.
8. **Review & Sign-Off (Reviewer Role):** Audits evidence sufficiency, verifies safety policies, and signs off on unified reports and SARIF logs.

---

## 📂 Run Folder System (`RunManager`)
Every TorusGuard execution is strictly contained within a dedicated run folder (`runs/<run-id>/`):
- `authorization.md` & `scope.json`: Target authorization proof, approved hosts, and permitted paths.
- `manifest.json`: Execution metadata, git commit hash, and status counts.
- `summary.md`: Unified static + runtime exploitability report.
- `findings.md`: Detailed finding cards with stable IDs and evidence snippets.
- `web-validation.md`: HTTP interaction audit log and response statuses.
- `requests.json` & `responses.json`: Redacted request and response ledgers.
- `session-notes.md`: Active session state and cookie tracking notes.
- `browser-validation.md`: Client-side route guard verification and DOM evidence.
- `replay.json` & `replay.md`: Deterministic, replayable validation sequences.
- `agent-handoffs.md` & `role-audit.json`: Multi-agent role governance audit trail.
- `safety-decisions.json`: Safety gate evaluation decisions (`Auto-Allowed`, `Approval Required`, `Manual Only`).
- `remediation.md` & `bundles/`: Structured remediation bundles per cluster.
- `sarif.json`: Standard OASIS SARIF v2.1.0 log with `automationDetails.id`.

---

## 🛠️ Core Commands

| Command | Lifecycle Phase | Agent Role | Purpose | Modifies Code? |
|---|:---:|:---:|---|:---:|
| `/torusguard init` | Baseline | Architect | Initialize project baseline, SECURITY.md, and configuration | ❌ Docs only |
| `/torusguard authorize` | Legal Gate | Architect | Capture target ownership, scope limits, and write `scope.json` | ❌ No |
| `/torusguard audit` | Detect & Cluster | Profiler | Scan codebase ASTs; assign stable IDs and clusters | ❌ No |
| `/torusguard verify` | Verify | Validator | Validate evidence sufficiency and evaluate 0–100 confidence score | ❌ No |
| `/torusguard web-validate` | Runtime Probe | Validator | Execute scoped HTTP/API probes with automatic token redaction | ❌ No |
| `/torusguard exploit-check` | Exploitability | Validator | Run bounded exploitability confirmation for approved classes | ❌ No |
| `/torusguard replay` | Reproducibility | Validator | Deterministically replay verification trace from `replay.json` | ❌ No |
| `/torusguard harden` | Remediate | Remediator | Formulate structured remediation bundles with runtime context | ❌ No (Plan only) |
| `/torusguard apply` | Apply | Remediator | Use Ponytail to apply surgical governed patches | ✅ Yes (Bounded) |
| `/torusguard recheck` | Re-check | Reviewer | Execute targeted recheck on modified scopes | ❌ No |

---

## 🔍 Stack Detection & Reference Loading

When executing `/torusguard audit`, inspect repository files and output the detected stack block:

### Standard Detected Stack Output Format
```markdown
## Detected Stack
- Language: Python / JavaScript / TypeScript
- Framework: Django / DRF / FastAPI / Flask / Next.js / Express / None
- Data layer: SQLAlchemy / Django ORM / Supabase / None
- Dependency files: pyproject.toml / requirements.txt / package.json
- Detection evidence: <file and line reference, e.g. manage.py:5>
- Detection confidence: Confirmed / Likely / Needs Review
```

### Detection Evidence Mapping
| Detected File / Indicator | Target Stack | Reference Modules to Load |
|---|---|---|
| `package.json`, `next.config.js` | Next.js | `secrets-and-config.md`, `client-code-exposure.md`, `platform-hardening.md` |
| `express`, `server.js`, `app.js` | Node.js / Express | `input-and-injection.md`, `auth-and-sessions.md`, `csrf-and-cross-origin.md` |
| `manage.py`, `settings.py`, `django` | Django | `python-security-overview.md`, `django-security.md`, `python-dependencies.md` |
| `rest_framework` | DRF | `drf-security.md`, `django-security.md`, `python-security-overview.md` |
| `fastapi`, `FastAPI()` (in code) | FastAPI | `fastapi-security.md`, `sqlalchemy-security.md`, `python-dependencies.md` |
| `flask`, `Flask(__name__)` | Flask | `flask-security.md`, `sqlalchemy-security.md`, `python-dependencies.md` |
| `sqlalchemy` (in imports/models) | SQLAlchemy | `sqlalchemy-security.md` |
| `requirements.txt`, `pyproject.toml` | Python Supply Chain | `python-dependencies.md` |

---

## 📊 Auditable 0–100 Confidence Scoring Rubric

TorusGuard evaluates finding confidence using an objective 5-factor scoring model (Max: 100 pts):
1. **Evidence Quality (35 pts):** Exact AST source code match vs regex or indirect indicator.
2. **Reproduction Success (25 pts):** Deterministic reproduction in test fixture.
3. **Independent Confirmations (15 pts):** Corroborated across multiple files/manifests.
4. **Environmental Clarity (15 pts):** Absence of ambiguous out-of-band proxy/service layers.
5. **Manual Review Status (10 pts):** Verified by a human security engineer.

**Classification Bands:**
- `90–100`: 🔒 **`Confirmed`** (Indisputable proof; immediate fix required)
- `70–89`: 🟢 **`High Confidence`** (Strong indicators; localized verification recommended)
- `50–69`: 🟡 **`Medium Confidence`** (Probable flaw; runtime confirmation recommended)
- `< 50`: 🔍 **`Needs Review` / `Unconfirmed`** (Requires manual verification of architecture)

---

## 🌟 Human-First Output Standard

Every generated report must follow this card-style hierarchy:

1. **Stack Statement at Top:** Standard `## Detected Stack` block with specific file and line citations.
2. **Executive Summary:** Posture indicator (`🔴 Action Required` / `🟡 Warnings Found` / `🟢 Ready`), metric table, and average confidence score.
3. **Card-Style Finding Layout:**
   - Title & Badges: Severity (`🔴 Critical`, `🟠 High`, `🟡 Medium`, `🔵 Low`) | Auditable Confidence (`95/100 🔒 Confirmed`)
   - **Provenance Chain:** Discovery rule, triggering input, decision path, verification method.
   - **Raw Evidence Package:** Exact code excerpt with SHA-256 integrity checksum.
   - **Analysis & Risk Rationale:** Strict separation of objective Raw Facts from AI Risk Interpretation.
   - **Remediation & Diff:** Framework-native **Before / After** diff.
   - **Retest Status:** Explicit verification method and post-fix evidence hash.
4. **Clear Next Steps:** Prioritized 1-2-3 actions.

---

## ⚖️ Rules of Engagement & Safety Constraints

- **Folder-per-run isolation:** Never dump artifacts directly into the project root. Always use `run_path` (e.g., `.torusguard/runs/run-.../`).
- **Ponytail Integration for `/torusguard apply`:**
  - Ponytail is strictly an AI-agent code-writer skill for applying remediation, not for discovering findings. It must not change TorusGuard rules or engine logic.
  - The AI agent reads `remediation.md` and applies the fixes using Ponytail principles.
  - Ensure the agent preserves all existing authentication, authorization, tenant isolation, validation, error handling, and security logging.
  - Prefer small edits to existing code over rewrites. Avoid excessive comments, boilerplate, wrappers, and full-file rewrites.
  - Save the patch or change summary in `patches/` before applying directly, or use a dry-run/review mode for critical authentication, tenant, and database changes.
- Never report a finding as `Confirmed` without direct source code snippet evidence.
- If a controller delegates authorization to a domain service layer, score `< 50` and classify as `Needs Review` (`TG-AUTH-007`).
- Never report an unpinned dependency as exploitable without an advisory or audit result (`TG-SUPPLY-002`).
- Never report SSRF as `Confirmed` merely because an HTTP client is imported; verify user control over the destination URL (`TG-SSRF-001`).
- Never include real production credentials or tokens in generated reports.
