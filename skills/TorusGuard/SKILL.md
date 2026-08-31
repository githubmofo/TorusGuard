---
name: torusguard
description: Security guardrails, provenance-tracked evidence, and auditable verification workflow for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, Django, DRF, FastAPI, Flask, SQLAlchemy, and Python APIs.
---

# TorusGuard (v0.6.3)

**Tagline:** Governed security remediation, root-cause clustering, minimal patching, and targeted verification for AI-built web applications.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard v0.6.3 is a Markdown-first, portable AI-agent skill and governed remediation engine. It is not an unmanaged vulnerability scanner or offensive exploit suite. It orchestrates the full remediation lifecycle: scanning codebases, computing stable finding fingerprints that survive line shifts, clustering alerts by root cause, generating structured remediation bundles, applying minimal bounded code patches, executing targeted rechecks on impacted scopes, and exporting SARIF-compatible artifacts for ecosystem integration.

---

## 🔄 Governed Remediation Lifecycle (v0.6.x Architecture)

```text
┌───────────┐     ┌────────────┐     ┌───────────┐     ┌─────────────┐     ┌──────────┐     ┌───────────┐     ┌───────────┐
│ 1. Detect │ ──► │ 2.Classify │ ──► │ 3. Verify │ ──► │ 4.Remediate │ ──► │ 5. Apply │ ──► │ 6.Recheck │ ──► │ 7.Archive │
└───────────┘     └────────────┘     └───────────┘     └─────────────┘     └──────────┘     └───────────┘     └───────────┘
```

1. **Detect (`/torusguard audit`):** Scan repository AST & source files; assign deterministic Stable Finding Fingerprints.
2. **Classify:** Map findings into systemic **Root-Cause Clusters** with shared remediation plans.
3. **Verify (`/torusguard verify`):** Calculate auditable 0–100 confidence scores and package raw technical evidence.
4. **Remediate (`/torusguard harden`):** Formulate self-contained **Remediation Bundles** (`finding.md`, `remediation.md`, `minimal_patch_plan.md`, `verify-after-change.md`, `metadata.json`).
5. **Apply (`/torusguard apply`):** Execute **Minimal Patch Governance** (Ponytail protocol) to surgically modify only affected files while blocking oversized or risky diffs.
6. **Re-check (`/torusguard recheck`):** Run **Targeted Scoped Rechecks** on modified code and adjacent trust boundaries to confirm status (`Confirmed Fixed`, `Partially Fixed`, `Needs Manual Review`, `Regressed`).
7. **Archive:** Save run manifests, diff summaries, and optional SARIF exports to the isolated run folder.

---

## 📂 Run Folder System (`RunManager`)
Every TorusGuard v6 execution is strictly contained within a dedicated run folder (`runs/<run-id>/`):
- `manifest.json`: Execution metadata, git commit hash, and status counts.
- `summary.md`: Executive summary and root-cause cluster breakdown.
- `findings.md`: Detailed finding cards with stable IDs and evidence snippets.
- `remediation.md`: Structured remediation guidance per cluster.
- `apply-plan.md`: Patch policy decisions, line additions/deletions, and escalation status.
- `recheck.md`: Targeted recheck outcome and regression analysis.
- `evidence.json`: Full evidence ledger with SHA-256 integrity hashes.
- `diff-summary.md`: Unified git diff ledger of all applied changes.
- `changed-files.txt`: Line-separated list of modified files.
- `sarif.json`: Standard SARIF v2.1.0 JSON structured export.
- `logs/`: Subdirectory for runtime and execution logs.

---

## 🛠️ Core Commands

| Command | Lifecycle Phase | Purpose | Modifies Code? |
|---|:---:|---|:---:|
| `/torusguard init` | Baseline | Create/update project `SECURITY.md`, threat model, and baseline | ❌ Docs only |
| `/torusguard audit` | Detect & Classify | Scan codebase; compute stable finding IDs and root-cause clusters | ❌ No |
| `/torusguard verify` | Verify | Validate evidence sufficiency and evaluate 0–100 confidence score | ❌ No |
| `/torusguard harden` | Remediate | Generate structured remediation bundles in the run folder | ❌ No (Plan only) |
| `/torusguard apply` | Apply | Use Ponytail to write minimal governed patches to active code | ✅ Yes (Bounded) |
| `/torusguard recheck` | Re-check | Execute targeted re-audit on post-fix scope and trust boundaries | ❌ No |

**Audit focus areas:** `auth`, `input`, `database`, `files`, `secrets`, `supply-chain`, `network`, `ssrf`, `webhooks`, `websockets`, `graphql`, `business-logic`, `rate-limit`, `client`, `platform`, `cache`, `django`, `drf`, `fastapi`, `flask`, `sqlalchemy`.

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
