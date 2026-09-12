# TorusGuard Workflow Demo & Sample Output

This document illustrates how TorusGuard operates in practice, showing the exact flow from command execution to audit report generation, runtime validation, governed remediation, and living report synchronization.

TorusGuard supports **100% functional parity** between **Mode A (Terminal CLI)** and **Mode B (AI Agent Chat)**.

---

## 🛠️ Step 1: Initializing the Workspace

Initialize the workspace using either terminal CLI or AI chat:

```bash
# Mode A: Terminal CLI
npx torusguard init

# Mode B: AI Chat Slash Command
/torusguard init
```

### What Happens:
1. The autonomous bootstrapper unpacks the `.torusguard/` directory into your project root.
2. It scans project manifests (`package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `pom.xml`, `Cargo.toml`) and auto-detects your polyglot stack.
3. It activates framework-tailored security rules across 74 rules in 18 families.
4. It sets up `.torusguard/config/torusguard.json` and creates the initial `SECURITY.md` baseline.

---

## 🔍 Step 2: Running a Static Security Audit

Run an AST static security scan across all 74 rules:

```bash
# Mode A: Terminal CLI
npx torusguard audit

# Mode B: AI Chat Slash Command
/torusguard audit
```

### Terminal CLI Output (Standardized 75-Column Terminal):
```text
===========================================================================
               🛡️ TORUSGUARD STATIC AST AUDIT REPORT 🛡️                    
===========================================================================
 Target Path : .                                                           
 Timestamp   : 2026-09-12 22:15:00 IST                                     
 Stack       : Express + MongoDB + React                                   
 Rules Active: 74 rules across 18 architectural families                   
 Status      : 🔴 ACTION REQUIRED (1 Critical, 1 High)                     
---------------------------------------------------------------------------
 Findings Summary:
   🔴 Critical : 1 finding
   🟠 High     : 1 finding
   🟡 Medium   : 0 findings
   🔍 Review   : 1 finding
---------------------------------------------------------------------------
 Living Report : Synchronized to security_report.md                        
 Run Artifacts : .torusguard/runs/run-20260912-221500-audit/               
 Next Action   : Run 'npx torusguard harden' or '/torusguard-harden'       
===========================================================================
```

### Living Security Report Synchronization (`security_report.md`):
The audit automatically logs finding cards into `security_report.md` at workspace root:

```markdown
### 🔴 Finding TG-CSRF-001: Missing CSRF Protection on Session Routes
* **Location:** `src/server.ts:45`
* **Fingerprint:** `lineHash:a7b8c9d0...` (line-shift invariant)
* **Status:** `OPEN 🔴`
* **Score:** **90 / 100 (Confirmed)**
* **The Risk in Plain English:** When a user is logged in, an attacker site can trick their browser into submitting unauthorized POST requests using their active session cookie.
* **Evidence:**
  ```typescript
  // src/server.ts:45 - CSRF middleware missing on session-authenticated router:
  app.post("/api/user/email", authenticateSession, updateEmailHandler);
  ```
```

---

## 🧪 Step 3: Evidence & Runtime Verification

Verify finding evidence sufficiency and probe target endpoints non-destructively:

```bash
# Mode A: Terminal CLI
npx torusguard verify
npx torusguard web-validate

# Mode B: AI Chat Slash Command
/torusguard verify
/torusguard web-validate
```

1. **Evidence Verification:** Evaluates source code line matches, confirms line-shift invariant fingerprints, and recalibrates confidence scores.
2. **Scope Check:** Enforces target host allowlisting via `.torusguard/config/scope.json`.
3. **Safety Gate:** Bounded HTTP probes run through `safety_gate.py` (`Auto-Allowed` GETs, `Approval Required` state-changes, `Manual Only` destructive verbs).
4. **Secret Masking:** All captured tokens, cookies, and passwords are automatically redacted in `requests.json` and `responses.json`.

---

## 🛠️ Step 4: Governed Remediation & Ponytail Patches

Formulate and apply minimal surgical fixes strictly bounded by the **Ponytail Protocol** ($\le 35$ additions, $\le 25$ deletions per bundle):

```bash
# Mode A: Terminal CLI
npx torusguard harden
npx torusguard apply [--yes]

# Mode B: AI Chat Slash Command
/torusguard harden
/torusguard apply
```

### Interactive Human Gate (`npx torusguard apply`):
```text
===========================================================================
               🛡️ TORUSGUARD GOVERNED REMEDIATION GATE 🛡️                   
===========================================================================
 Candidate Bundles: 2 formulated patches                                    
 Target Files     : src/server.ts, src/routes/profile.ts                   
 Churn Bounds     : <= 35 additions, <= 25 deletions per bundle            
 Pre-Apply Backup : .torusguard/snapshots/run-20260912-221500/             
---------------------------------------------------------------------------
 Inspect Patch: [1/2] TG-CSRF-001 in src/server.ts
 @@ -44,3 +44,4 @@
 + import { doubleCsrfProtection } from "./security/csrf";
 - app.post("/api/user/email", authenticateSession, updateEmailHandler);
 + app.post("/api/user/email", authenticateSession, doubleCsrfProtection, updateEmailHandler);
---------------------------------------------------------------------------
 Apply this patch to disk? [y/N/all/quit]: y
   ✔ Applied patch to src/server.ts (Backup saved)
===========================================================================
```

---

## 🔄 Step 5: Differential Recheck & State Machine Closure

Verify that applied patches eliminate vulnerabilities without introducing regressions:

```bash
# Mode A: Terminal CLI
npx torusguard recheck

# Mode B: AI Chat Slash Command
/torusguard recheck
```

### Terminal CLI Output:
```text
===========================================================================
               🛡️ TORUSGUARD DIFFERENTIAL RECHECK 🛡️                       
===========================================================================
 Scanned Scope : Modified files (src/server.ts, src/routes/profile.ts)      
 Status        : 🟢 FIXES VERIFIED & CLOSED                                
---------------------------------------------------------------------------
 Results:
   ✔ [Confirmed Fixed] TG-CSRF-001 in src/server.ts:45
   ✔ [Confirmed Fixed] TG-AUTH-006 in src/routes/profile.ts:32
---------------------------------------------------------------------------
 Living Report : Updated security_report.md (Health Score: 100/100 🟢)      
 Golden Fixes  : 2 new patterns saved to .torusguard/memory/patterns.json  
===========================================================================
```

If an error or regression occurs, roll back instantly:
```bash
npx torusguard rollback
```

---

## 🔒 Step 6: Git Pre-Commit Diff Guard

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
===========================================================================
 🚨 TORUSGUARD DIFF GUARD: BLOCKED (Exit 1)                                
===========================================================================
 File     : internal/client/transport.go                                   
 Line     : +42: InsecureSkipVerify: true                                  
 Violation: [TG-DIFF-001] Dangerous security bypass detected in diff.      
 Remedy   : Remove InsecureSkipVerify: true and configure trusted CAs.     
===========================================================================
```

---

## 🔄 Step 7: AI IDE Rules Auto-Sync

Compile project security invariants into prompt-optimized rules for Cursor, Claude Code, Antigravity, and Windsurf:
```bash
npx torusguard rules sync --format all
```

---

## 📊 Step 8: Visual Single-File HTML Posture Dashboard

Generate an interactive, dark-mode, zero-external-CDN dashboard:
```bash
npx torusguard report --html
```

The report provides:
- Circular animated SVG Security Posture Score gauge (0–100).
- 7-Stage closed-loop governance pipeline timeline.
- Golden Fix Recipes card grid with interactive unified diff viewer.
- Full SARIF v2.1.0 and JSON export options.
