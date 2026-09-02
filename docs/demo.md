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
