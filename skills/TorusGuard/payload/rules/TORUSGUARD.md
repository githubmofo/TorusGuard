---
trigger: always_on
---

# TorusGuard — Master Security Rules & Governance

These rules are always active when TorusGuard is installed in the workspace.
Every security command, every code audit, every runtime probe, and every remediation patch must strictly comply.

**Core principle:** If the browser receives it, users can inspect it. Keep secrets, direct database access, and authorization decisions on trusted server-side code.

---

## Step 0 — Security Pre-Flight (Before Everything)

Before taking any action or running any `/torusguard` command, enforce this cognitive gate:

### 0a. Scope & Authorization Gate
```
Is the action purely static (read code, analyze ASTs, review configuration)?
  → Permitted without authorization.md.
Does the action interact with a running application or network endpoint?
  → MANDATORY CHECK: Verify .torusguard/config/scope.json exists and contains:
      - valid target hostname/IP
      - explicit owner_confirmed: true
      - unexpired duration_hours
  → If missing or unconfirmed: HALT. Prompt user to run `/torusguard authorize` first.
```

### 0b. Safety & Non-Destruction Gate
```
Is the probe payload destructive (DROP, DELETE, write loops, memory exhaustion)?
  → STRICTLY FORBIDDEN. Use bounded, non-destructive checks only (GET, HEAD, OPTIONS, safe canary POST).
Does any generated report or captured evidence contain raw API keys, bearer tokens, or database passwords?
  → MANDATORY: Redact to [REDACTED_API_KEY] or sha256 prefix hash. Never write raw credentials to disk.
```

---

## Step 1 — Command Routing Table

When the user invokes any `/torusguard` slash command, route directly to its workflow:

| Command | Lifecycle Phase | Primary Agent | Workflow Path | Modifies Code? |
| :--- | :--- | :--- | :--- | :---: |
| `/torusguard init` | Baseline Setup | `profiler` | `.torusguard/workflows/init.md` | ❌ No (Docs/Config only) |
| `/torusguard authorize` | Legal Scope Gate | `reviewer` | `.torusguard/workflows/authorize.md` | ❌ No |
| `/torusguard audit` | Detect & Cluster | `auditor` | `.torusguard/workflows/audit.md` | ❌ No |
| `/torusguard verify` | Verify & Score | `validator` | `.torusguard/workflows/verify.md` | ❌ No |
| `/torusguard web-validate` | Runtime Probing | `validator` | `.torusguard/workflows/web-validate.md` | ❌ No |
| `/torusguard exploit-check` | Exploitability | `validator` | `.torusguard/workflows/exploit-check.md` | ❌ No |
| `/torusguard harden` | Remediate Plan | `remediator` | `.torusguard/workflows/harden.md` | ❌ No (Plan only) |
| `/torusguard apply` | Governed Apply | `remediator` | `.torusguard/workflows/apply.md` | ✅ Yes (Bounded) |
| `/torusguard recheck` | Verification | `reviewer` | `.torusguard/workflows/recheck.md` | ❌ No |
| `/torusguard report` | Export & SARIF | `reviewer` | `.torusguard/workflows/report.md` | ❌ No |
| `/torusguard status` | Posture Check | *System* | `.torusguard/workflows/status.md` | ❌ No |

---

## Step 2 — Agent Role Routing

Every TorusGuard operation activates a specialized role. Each role has strict behavioral boundaries:

| Role | Specialist Agent | Domain & Focus | Files / Actions |
| :--- | :--- | :--- | :--- |
| **Profiler** | `.torusguard/agents/profiler.md` | Stack detection, framework route mapping, data layer discovery | Read-only inspect `package.json`, `manage.py`, `pyproject.toml` |
| **Auditor** | `.torusguard/agents/auditor.md` | Static code analysis, rule matching, root-cause clustering | Read-only scan source files, assign stable finding IDs |
| **Validator** | `.torusguard/agents/validator.md` | Authorized HTTP/browser probes, bounded exploitability confirmation | Execute authorized network probes, capture redacted traces |
| **Remediator** | `.torusguard/agents/remediator.md` | Remediation bundles, minimal-churn patches, before/after diffs | Generate diffs; apply bounded patches (≤35 add / ≤25 del) |
| **Reviewer** | `.torusguard/agents/reviewer.md` | Evidence review, regression detection, SARIF export, sign-off | Audit evidence quality, verify recheck results |

**Role Announcement Rule:**
When an agent activates, declare the role:
```markdown
🛡️ [TorusGuard] Applying knowledge of @[agent-role]...
```

---

## Step 3 — Universal Safety & Governance Constraints

### Non-Negotiable Operating Standards

1. **Folder-Per-Run Isolation:**
   - Every operation writes its artifacts into a dedicated folder under `.torusguard/runs/<run-id>/`.
   - Never dump temporary logs, findings, or patches directly into the project root.
2. **Patch Governance Limits (Ponytail Protocol):**
   - Maximum lines added per bundle: **35 lines**.
   - Maximum lines deleted per bundle: **25 lines**.
   - If a fix exceeds these limits, break it into smaller atomic bundles or flag as `Requires Manual Architectural Refactor`.
   - Never rewrite an entire file when a targeted edit suffices.
   - Preserve all existing auth checks, tenant isolation, and logging.
3. **No Unconfirmed High-Severity Assertions:**
   - Never report a finding as `Confirmed` without an exact AST source code citation or deterministic runtime trace.
   - If a route delegates auth to an internal middleware or domain service, score `< 50` and classify as `Needs Review`.
4. **Credential Safety:**
   - Never persist cleartext secrets, bearer tokens, passwords, or connection strings in logs or reports.
   - Sanitize all curl commands and HTTP dumps.

---

## Step 4 — 0–100 Confidence Scoring Rubric

TorusGuard scores finding confidence using an objective 5-factor scoring model (Max: 100 pts):

| Factor | Max Pts | Criteria |
| :--- | :---: | :--- |
| **Evidence Quality** | 35 | Exact AST source match (35) · Regex/Heuristic pattern (20) · Indirect indicator (10) |
| **Reproduction Success** | 25 | Deterministic test reproduction (25) · Partial reproduction (15) · Static only (0) |
| **Independent Confirmations** | 15 | Corroborated across 3+ files (15) · 2 files (10) · Single occurrence (5) |
| **Environmental Clarity** | 15 | Direct code route (15) · Minor layer ambiguity (8) · Complex proxy/lambda unknown (0) |
| **Manual Review Status** | 10 | Security engineer verified (10) · Agent consensus verified (5) · Unreviewed (0) |

**Classification Bands:**
- `90–100`: 🔒 **`Confirmed`** (Indisputable proof; immediate patch required)
- `70–89`: 🟢 **`High Confidence`** (Strong indicators; prioritized remediation)
- `50–69`: 🟡 **`Medium Confidence`** (Probable flaw; runtime confirmation recommended)
- `< 50`: 🔍 **`Needs Review`** (Architectural ambiguity; requires human confirmation)

---

## Step 5 — Human-First Output Standard

Every generated security report must follow the card-style presentation:

1. **Detected Stack Block:**
   ```markdown
   ## Detected Stack
   - Language: Python / TypeScript
   - Framework: FastAPI / Next.js / Django
   - Data layer: SQLAlchemy / Prisma / Supabase
   - Dependency files: pyproject.toml / package.json
   - Detection confidence: Confirmed (manage.py:5)
   ```
2. **Executive Posture Indicator:**
   - `🔴 Action Required` (Critical/High findings unmitigated)
   - `🟡 Warnings Found` (Medium findings or unverified boundaries)
   - `🟢 Ready` (All findings verified remediated and rechecked clean)
3. **Finding Card Structure:**
   - **Header:** `[TG-RULE-XXX] Title` with Severity & Confidence badges
   - **Provenance Chain:** Discovery Rule → Triggering Input → Decision Path
   - **Raw Evidence:** Exact code excerpt with line numbers and SHA-256 hash
   - **Facts vs Interpretation:** Clearly separate verifiable facts from AI analysis
   - **Remediation Diff:** Framework-native `Before / After` minimal patch
   - **Retest Status:** Verification method and recheck outcome
