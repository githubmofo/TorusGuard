---
name: torusguard
description: Security guardrails, provenance-tracked evidence, and auditable verification workflow for AI-built web apps. Audit and harden secrets, frontend database access, input validation, authentication, authorization, rate limits, source-map exposure, SSRF, webhooks, and production configuration across React, Vite, Next.js, Node.js, Express, Supabase, Firebase, Django, DRF, FastAPI, Flask, SQLAlchemy, and Python APIs.
---

# TorusGuard (v0.5.4)

**Tagline:** Security guardrails, provenance-tracked evidence, and auditable verification workflow for AI-built web apps.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, database access, and authorization decisions on trusted server-side code.

TorusGuard is a Markdown-first, portable AI-agent skill and security workflow engine. It is not an npm package, hosted SaaS service, browser extension, or black-box vulnerability scanner. It guides audit, verification, remediation, and re-checking through structured rules, normalized evidence packages with SHA-256 checksums, auditable confidence scoring, prioritized remediation roadmaps, and deterministic fixture replays.

TorusGuard must never claim it can block DevTools, make an application 100% secure, or replace professional penetration testing, manual code review, compliance audits, or formal threat modeling.

---

## 🔄 Finding Lifecycle (v0.5.5 Architecture)

TorusGuard operates on a 7-stage lifecycle for every candidate security finding:

```text
[ Detect ] ──► [ Classify ] ──► [ Verify ] ──► [ Remediate ] ──► [ Apply ] ──► [ Re-check ] ──► [ Archive ]
```

1. **Detect:** Scan repository source code, environment templates, and configuration files.
2. **Classify:** Assign canonical Rule ID (`TG-*`), taxonomy category, risk severity rubric, and provenance chain.
3. **Verify:** Calculate auditable 0–100 confidence score and package raw technical evidence with SHA-256 checksums.
4. **Remediate:** Formulate least-invasive, framework-native code modifications with Before/After diffs into a remediation guide.
5. **Apply:** Use Ponytail to apply the remediation guide via safe, minimal code patches.
6. **Re-check:** Execute differential re-audit on post-fix code to assert resolution (`Verified Fixed`).
7. **Archive:** Preserve timestamped verification evidence in the project audit record.

---

## 📂 Output Hygiene: Folder-Per-Run (`RunFolder`)
All TorusGuard operations must be isolated into a per-run folder context:
- Base pattern: `.torusguard/runs/run-YYYYMMDD-HHMMSS/`
- Every invocation (`audit`, `harden`, `apply`, `recheck`) within a session uses this folder.
- Output routing:
  - Findings: `run_path/findings.md`
  - Remediation guides: `run_path/remediation.md`
  - Diffs/Patches: `run_path/patches/` (directory)
  - Logs: `run_path/logs/ponytail.log`
  - Validation: `run_path/recheck.md`
  - Metadata: `run_path/metadata.json`

---

## 🛠️ Core Commands

| Command | Lifecycle Phase | Purpose | Changes Code? |
|---------|:---:|---------|:---:|
| `/torusguard init` | Baseline | Create/update project `SECURITY.md`, threat model, and finding registry | Docs only |
| `/torusguard audit` | Detect & Classify | Scan codebase; produce Human-First normalized audit report | Writes to `findings/` |
| `/torusguard verify` | Verify | Validate evidence sufficiency, compute 0–100 confidence | No |
| `/torusguard harden` | Remediate | Generate structured remediation guide with exact rule/file markers | Writes to `remediation/` |
| `/torusguard apply` | Apply | Use Ponytail to write minimal patches from the remediation guide | Writes to `patches/` (Applies on approval) |
| `/torusguard recheck` | Re-check | Execute differential re-audit on post-fix code to assert `Verified Fixed` | Writes to `validation/` |

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
