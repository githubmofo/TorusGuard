# TorusGuard Demo Guide

## Quick Demo: Scan and Report

This guide walks through a complete TorusGuard workflow in under 2 minutes.

### Step 1: Initialize

```bash
cd your-project
torusguard init
```

**Output:**
```
🛡️ TorusGuard Workspace Initialized
Stack detected: [node, go]
Rules activated: 74 rules across 18 families
```

### Step 2: Audit

```bash
torusguard audit
```

**Output:**
```
Starting static heuristic security scan...
Loaded 74 rules from catalog.
Hardcoded secret found in src/config.js
Potential SQL Injection (string concatenation) found in src/db/queries.js
✔ Scan complete. Check security_report.md.
```

### Step 3: Review Findings

```bash
cat security_report.md
```

### Step 4: Generate Report

```bash
torusguard report --sarif
```

**Output:**
```
✔ Dynamic SARIF report generated at report.sarif
```

### Step 5: Apply a Fix

```bash
# After your AI agent generates a patch:
torusguard harden fix.patch     # Validate bounds
torusguard apply --yes fix.patch # Apply with snapshot
torusguard recheck               # Verify fix
```

---

## Full Lifecycle Demo

```bash
torusguard init                    # 1. Scaffold workspace
torusguard audit                   # 2. Scan for vulnerabilities
torusguard authorize               # 3. Generate auth token
torusguard web-validate            # 4. Probe running app
torusguard exploit-check           # 5. Test with inert payloads
torusguard verify                  # 6. Check evidence
torusguard harden candidate.patch  # 7. Validate patch bounds
torusguard apply --yes candidate.patch  # 8. Apply with snapshot
torusguard recheck                 # 9. Verify fix
torusguard report --html           # 10. Generate dashboard
torusguard status                  # 11. Check final posture
```

---

## AI Agent Demo (Slash Commands)

In any supported AI agent (Antigravity, Cursor, Claude Code, Windsurf):

```
/torusguard init          → Initializes workspace
/torusguard audit         → Runs security scan
/torusguard harden        → Validates patch bounds
/torusguard apply         → Applies patch with Human Gate
/torusguard report        → Generates posture report
```

The AI agent handles intelligence (analyzing findings, generating patches), while the Go binary handles enforcement (scanning, bounds checking, snapshotting).
