# /torusguard recheck — Targeted Recheck & Regression Verification

**Command:** `/torusguard recheck [run_id]`  
**Primary Agent:** `reviewer` (`.torusguard/agents/reviewer.md`)  
**Lifecycle Phase:** Phase 6 (Targeted Recheck)

---

## Objective
Re-scan only the scoped files modified by patch application to confirm whether the targeted vulnerabilities are genuinely eliminated (`Confirmed Fixed`) and detect whether any new flaws were inadvertently introduced (`Regressed`).

---

## Execution Steps

### Step 1: Identify Modified Files
1. Read `manifest.json` from the active run folder to identify files modified during `/torusguard apply`.
2. Limit recheck scanning strictly to these modified files for maximum performance.

### Step 2: Targeted AST Scanning
1. Re-run relevant rule checks against the modified files.
2. Check if the original vulnerable sink pattern is still detectable.
3. Check if all other active security rules remain clean.

### Step 3: Classify Verification Outcome
Assign one of two formal outcomes:
- `Confirmed Fixed`: Vulnerability pattern is absent, safe mitigation pattern is present, and no new security flaws exist.
- `Regressed`: Original vulnerability remains OR new security flaws (e.g. `TG-SEC-001` or missing error check) were introduced.

### Step 4: Write Recheck Ledger
Generate `.torusguard/runs/<run-id>/recheck.md`:
```markdown
# Targeted Recheck Ledger

| Finding ID | Rule | File | Pre-Patch Status | Recheck Outcome |
| :--- | :--- | :--- | :--- | :--- |
| TG-FIND-001 | TG-DB-004 | views.py | Confirmed | ✅ Confirmed Fixed |
```

Update `manifest.json` with recheck status counts.

### Step 5: Output Summary
```markdown
🔍 [TorusGuard] Targeted Recheck Complete
- Modified Files Scanned: <Count>
- Confirmed Fixed: <Count>
- Regressed: 0 (No regressions detected)
- Recheck Ledger: .torusguard/runs/<run-id>/recheck.md

Next Step: Run `/torusguard report` to generate the final signed security report and SARIF log.
```
