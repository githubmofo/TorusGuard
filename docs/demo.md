# TorusGuard Workflow Demo & Sample Output

This document illustrates how TorusGuard operates in practice, showing the exact expected flow from command execution to audit report generation, runtime validation, and governed remediation.

---

## 🛠️ Step 1: Initializing the Workspace (`/torusguard init`)

When you run `/torusguard init` in your AI chat:
1. The autonomous bootstrapper unpacks the `.torusguard/` directory into your project root.
2. It scans project manifests (`package.json`, `pyproject.toml`, `requirements.txt`) and auto-detects your stack (e.g., FastAPI + SQLAlchemy or Next.js 14 + Express).
3. It activates framework-tailored security rules in `.torusguard/rules/active/`.
4. It sets up the 5 specialist agent roles (`profiler`, `auditor`, `validator`, `remediator`, `reviewer`) and interactive playbooks in `.torusguard/workflows/`.

---

## 🔍 Step 2: Running a Static Security Audit (`/torusguard audit`)

When you prompt your AI assistant with `/torusguard audit`, the `auditor` agent reads your codebase against active security rules and generates an immutable run folder in `.torusguard/runs/<run-id>/`:

### Sample Generated `findings.md`:

```markdown
# 🛡️ TorusGuard Audit: EcoStore API

> **Run ID:** `run-20260902-120000-audit`  
> **Detected Stack:** Express + MongoDB + React  
> **Overall Posture:** 🔴 **Action Required (1 Critical, 1 High)**  
> **Confidence Model:** 5-Factor Mathematical Rubric (0–100)

---

## 📊 Executive Summary
The application is built on Express and MongoDB. While basic authentication is in place, the audit identified an unauthenticated state-changing route and an unvalidated mass assignment flaw in profile management.

| Severity | Rule ID | Title | Confidence | Root Cause Cluster |
|---|---|---|:---:|---|
| 🔴 **Critical** | `TG-CSRF-001` | Missing CSRF Protection on State-Changing Routes | **90 (Confirmed)** | `auth-session-boundary` |
| 🟠 **High** | `TG-AUTH-006` | Mass Assignment in User Profile Updates | **85 (High)** | `input-model-binding` |
| 🔍 **Review** | `TG-DB-004` | Tenant Isolation Scoping on Shared Collections | **55 (Needs Review)** | `tenant-scoping` |

---

## 🚨 Priority Finding Cards

### 🔴 Finding TG-CSRF-001: Missing CSRF Protection on Session Routes
* **Location:** `src/server.ts:45`
* **Fingerprint:** `lineHash:a7b8c9d0...` (line-shift invariant)
* **Score:** **90 / 100 (Confirmed)**
* **The Risk in Plain English:** When a user is logged in, a malicious third-party site can trick their browser into submitting unauthorized POST requests (e.g. changing passwords or transferring funds) using their active session cookie.
* **Evidence:**
  ```typescript
  // src/server.ts:45 - CSRF middleware missing on session-authenticated router:
  app.post("/api/user/email", authenticateSession, updateEmailHandler);
  ```
* **Remediation Diff:**
  ```diff
  + import { doubleCsrfProtection } from "./security/csrf";
  - app.post("/api/user/email", authenticateSession, updateEmailHandler);
  + app.post("/api/user/email", authenticateSession, doubleCsrfProtection, updateEmailHandler);
  ```
* **How to Verify:** Dispatch a POST request without the CSRF header and assert that the server returns HTTP `403 Forbidden`.

---

### 🟠 Finding TG-AUTH-006: Mass Assignment in User Profile Updates
* **Location:** `src/routes/profile.ts:32`
* **Score:** **85 / 100 (High Confidence)**
* **The Risk in Plain English:** An attacker can include `{ "isAdmin": true, "role": "superuser" }` in their profile update JSON payload and gain administrative privileges because input fields are passed unfiltered to the database.
* **Evidence:**
  ```typescript
  // src/routes/profile.ts:32 - Passing raw req.body to model:
  await User.findByIdAndUpdate(req.user.id, req.body);
  ```
* **Remediation Diff:**
  ```diff
  - await User.findByIdAndUpdate(req.user.id, req.body);
  + const { displayName, bio } = req.body;
  + await User.findByIdAndUpdate(req.user.id, { displayName, bio });
  ```
* **How to Verify:** Submit a PUT request containing `{ "isAdmin": true }` and confirm the user role remains unchanged in database state.
```

---

## 🧪 Step 3: Runtime Verification (`/torusguard verify` & `web-validate`)

Before applying code changes, the `validator` agent can confirm whether findings are live and exploitable:
1. **Scope Check:** Enforces target host allowlisting via `.torusguard/config/scope.json`.
2. **Safety Gate:** Bounded HTTP probes run through `safety_gate.py` (`Auto-Allowed` GETs, `Approval Required` state-changes, `Manual Only` destructive verbs).
3. **Secret Masking:** All captured tokens, cookies, and passwords are automatically redacted in `requests.json` and `responses.json`.
4. **Deterministic Replay:** Emits `replay.json` containing exact test sequences for regression tracking.

---

## 🛠️ Step 4: Governed Remediation (`/torusguard harden` & `apply`)

Once candidate fixes are reviewed:
1. **Formulate the Remediation Bundle:** Run `/torusguard harden` to generate 4-artifact remediation packages strictly adhering to the **Ponytail Protocol** ($\le 35$ additions, $\le 25$ deletions per bundle).
2. **Pre-Apply Snapshot:** Run `/torusguard apply`. TorusGuard automatically saves a byte-for-byte rollback backup in `pre_apply/<file>.bak` before modifying any code.
3. **Targeted Recheck:** Run `/torusguard recheck` to differentially re-audit the modified lines. The finding transitions to `Confirmed Fixed` and a verified SARIF v2.1.0 report is exported to `.torusguard/runs/<run-id>/results.sarif`.

---

## 🔒 Step 5: Git Pre-Commit Diff Guard (`npx torusguard diff-guard`)

Install the local pre-commit hook in one command:
```bash
npx torusguard diff-guard --install-hook
```

When an engineer or AI agent stages code with a security bypass or leaked credentials:
```bash
git commit -m "feat: bypass ssl check for dev"
```

TorusGuard instantly blocks the commit:
```text
🚨 TorusGuard Diff Guard: BLOCKED (Exit 1)
--------------------------------------------------
File: internal/client/transport.go
Line: +42: InsecureSkipVerify: true
Violation: [TG-DIFF-001] Dangerous security bypass detected in staged diff.
Remediation: Remove InsecureSkipVerify: true and configure proper CA certificates.
```

---

## 🔄 Step 6: AI IDE Rules Auto-Sync (`npx torusguard rules sync`)

Compile project security invariants into prompt-optimized rules for your AI editor:
```bash
npx torusguard rules sync --format all
```

Output:
```text
🛡️  TorusGuard AI IDE Rules Sync Engine v1.3.0
============================================================
Detected Stack: Express, React, TypeScript (ORM: Prisma)
Compiling security rules with max overhead <= 300 tokens...

  ✓ Updated .cursorrules (245 prompt tokens)
  ✓ Updated CLAUDE.md (260 prompt tokens)
  ✓ Updated .agent/rules/torusguard.md (230 prompt tokens)
  ✓ Updated .windsurfrules (245 prompt tokens)

✨ Successfully synced 4 AI IDE rule files.
```

---

## 📊 Step 7: Single-File Visual HTML Posture Dashboard (`npx torusguard report --html`)

Generate a standalone, zero-external-CDN dark-mode dashboard:
```bash
npx torusguard report --html
```

Output:
```text
📊 Visual HTML Security Posture Report generated:
   --> .torusguard/runs/report-latest.html
   Size: 34.2 KB (100% self-contained, offline-ready, dark-mode)
```

The report renders:
- Circular animated SVG Security Posture Score gauge (0–100).
- 7-Stage closed-loop governance pipeline timeline.
- Dynamic polyglot ecosystem badges.
- Golden Fix Recipes card grid with before/after diffs.

---

## 🧠 Step 8: Adaptive Security Memory (`npx torusguard memory`)

Inspect project security intelligence accumulated across audit runs:
```bash
npx torusguard memory status
```

Output:
```text
🧠 TorusGuard Security Memory Status
============================================================
Events Recorded:      14 events (Ledger: memory/events/)
Distilled Patterns:   3 active patterns (memory/patterns.json)
Golden Fix Recipes:   2 recipes (memory/golden_recipes/)
Active Context Card:  ~210 tokens (memory/context.json)
TTL Decay:            90 days active (0 expired events)
```
