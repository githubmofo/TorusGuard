# TorusGuard Workflow Demo & Sample Output

This document illustrates how TorusGuard operates in practice, showing the exact expected flow from command execution to audit report generation and remediation.

---

## 🛠️ Step 1: Initializing Security Documentation (`/torusguard init`)

When you run `/torusguard init` in your AI chat:
1. The agent inspects your project structure without modifying source code.
2. It generates a clean `SECURITY.md` (vulnerability disclosure policy) in your root directory.
3. It creates a developer-friendly threat model in `docs/threat-model.md` identifying public endpoints, trust boundaries, and protected assets.

---

## 🔍 Step 2: Running an Audit (`/torusguard audit`)

When you prompt your AI assistant with `/torusguard audit`, the agent reads your codebase against the TorusGuard rule catalog and generates a **Human-First** report:

### Sample Generated `audit-report.md`:

```markdown
# 🛡️ Security Audit Report: EcoStore API

> **Target:** `src/`, `server.js`  
> **Date:** 2026-08-20  
> **Overall Posture:** 🔴 **Action Required (1 Critical, 1 High)**

---

## 📊 Executive Summary
The application is built on Express and MongoDB. While basic authentication is in place, the audit identified a critical missing CSRF defense on state-changing endpoints and an unvalidated user object update in profile management.

| Severity Level | Count | Action Required |
|---|:---:|---|
| 🔴 **Critical** | 1 | Immediate fix required before deployment |
| 🟠 **High** | 1 | Fix required |
| 🟡 **Medium / Low** | 0 | None detected |
| 🔍 **Manual Review** | 1 | Verify Supabase RLS policy in cloud console |

---

## 🚨 Priority Findings

### 🔴 1. Missing CSRF Protection on Session-Authenticated Routes
* **Location:** `server.js:45`
* **Category:** `CSRF Protection` (`TG-CSRF-001`) • **Confidence:** Confirmed
* **The Risk in Plain English:** When a user is logged in, a malicious third-party website can trick their browser into submitting unauthorized POST requests (e.g. changing passwords or transferring funds) using their active session cookie.
* **Evidence:**
  ```javascript
  // server.js:45 - CSRF middleware commented out:
  // app.use(csurf({ cookie: true }));
  ```
* **How to Fix:**
  ```javascript
  // ✅ Enable CSRF token middleware on state-changing endpoints:
  const csurf = require("csurf");
  app.use(csurf({ cookie: { httpOnly: true, sameSite: "strict" } }));
  ```
* **How to Verify:** Submit a POST request without a `_csrf` token and verify that the server returns HTTP `403 Forbidden`.

---

### 🟠 2. Mass Assignment in User Profile Updates
* **Location:** `routes/profile.js:32`
* **Category:** `Authorization` (`TG-AUTH-006`) • **Confidence:** Confirmed
* **The Risk in Plain English:** An attacker can include `{ "isAdmin": true, "balance": 99999 }` in their profile update JSON payload and gain administrative privileges because input fields are not filtered.
* **Evidence:**
  ```javascript
  // routes/profile.js:32 - Passing raw req.body to update:
  await User.findByIdAndUpdate(req.user.id, req.body);
  ```
* **How to Fix:**
  ```javascript
  // ✅ Whitelist only permitted editable fields:
  const { displayName, bio } = req.body;
  await User.findByIdAndUpdate(req.user.id, { displayName, bio });
  ```
* **How to Verify:** Send a PUT request with `{ "isAdmin": true }` and confirm that the user role remains unchanged in the database.

---

## 🔍 Items Requiring Manual Review

* [ ] **Supabase Row-Level Security (`TG-DB-002`)**: The application connects to Supabase tables. Ensure that RLS policies are enabled in the Supabase Dashboard, as static code cannot verify cloud table configurations.
```

---

## 💡 Confirmed vs. Manual Review: Understanding the Difference

| Category | What It Means | Example |
|---|---|---|
| **`Confirmed`** | Directly observed in source code or project configuration with high certainty. | A hardcoded API key in `config.js` or `User.update(req.body)`. |
| **`Manual Review`** | The code pattern depends on external infrastructure, cloud IAM, or business intent that cannot be fully verified through static analysis alone. | Whether a webhook endpoint has an IP allowlist configured in Cloudflare or AWS WAF. |

---

## 🛠️ Step 3: Hardening & Applying Patches (`/torusguard harden` & `/torusguard apply`)

Once you review the report:
1. **Formulate the Plan:** Type `/torusguard harden` in your AI chat to generate framework-native remediation guides and candidate diffs.
2. **Apply the Patch:** Type `/torusguard apply` to let the **Ponytail engine** surgically apply the minimal, bounded patch without modifying unrelated code.
3. **Verify the Fix:** Type `/torusguard recheck` to verify that the vulnerability transitions to `Verified Fixed` with zero regression.
