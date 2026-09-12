# TorusGuard Finding Lifecycle Guide

This guide explains how security findings are tracked, classified, verified, remediated, applied, and re-checked using the **TorusGuard Workflow Engine** and synchronized with the **Living Security Report (`security_report.md`)**.

---

## 🔄 Finding Lifecycle Overview & State Machine

TorusGuard findings follow a strict closed-loop state machine synchronized across both Terminal CLI runs and AI Agent chat sessions:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     TORUSGUARD FINDING LIFECYCLE STATE MACHINE              │
└─────────────────────────────────────────────────────────────────────────────┘
  [ OPEN 🔴 ] ──(verify)──► [ VERIFIED 🟠 ] ──(harden)──► [ CANDIDATE 🟡 ]
                                                                 │
                                                               (apply)
                                                                 │
                                                                 ▼
  [ RESOLVED 🟢 ] ◄──(recheck: confirmed)── [ APPLIED 🔵 ]
         │
         └──(recheck: failed)──► [ REGRESSED ❌ ]
```

---

## 1. 🔍 Stage 1: Discovery (`OPEN 🔴`)
- **CLI:** `npx torusguard audit`
- **Chat:** `/torusguard audit`
- **Action:** Scans repository source files against all 74 AST rules across 18 families.
- **Ledger Sync:** Finding is added to `security_report.md` with status `OPEN 🔴` and initial confidence score (0–100).
- **Artifacts:** `security_report.md`, `.torusguard/runs/<run_id>/findings.json`.

---

## 2. 🛡️ Stage 2: Evidence Verification (`VERIFIED 🟠`)
- **CLI:** `npx torusguard verify` (or `npx torusguard web-validate`)
- **Chat:** `/torusguard verify` (or `/torusguard web-validate`)
- **Action:** Evaluates source code line matches, confirms line-shift invariant fingerprints (`FindingFingerprint`), and audits evidence sufficiency.
- **Ledger Sync:** Validated findings transition to `VERIFIED 🟠`. If protected by external gateways or absent on disk, status is set to `FALSE POSITIVE ⚪`.

---

## 3. 🛠️ Stage 3: Patch Formulation (`CANDIDATE 🟡`)
- **CLI:** `npx torusguard harden`
- **Chat:** `/torusguard harden`
- **Action:** Formulates minimal surgical candidate patches adhering strictly to the **Ponytail Protocol** ($\le 35$ additions, $\le 25$ deletions per bundle).
- **Ledger Sync:** Transitioned to `CANDIDATE 🟡` with patch diff referenced in candidate bundle directory.

---

## 4. ⚡ Stage 4: Governed Application (`APPLIED 🔵`)
- **CLI:** `npx torusguard apply [--yes]`
- **Chat:** `/torusguard apply`
- **Action:** Human Gate presents interactive diffs (`[y/N/all/quit]`). Automatically creates byte-for-byte rollback backups in `.torusguard/snapshots/<run_id>/` before modifying target files on disk.
- **Ledger Sync:** Status transitions to `APPLIED 🔵`.

---

## 5. 🔁 Stage 5: Differential Recheck (`RESOLVED 🟢` / `REGRESSED ❌`)
- **CLI:** `npx torusguard recheck`
- **Chat:** `/torusguard recheck`
- **Action:** Scopes AST re-scan strictly to modified files and trust boundaries.
- **Transitions:**
  - `✔ [Confirmed Fixed]` $\rightarrow$ transitions finding to `RESOLVED 🟢`.
  - `✖ [Regressed]` $\rightarrow$ transitions finding to `REGRESSED ❌` and alerts operator.
- **Memory Distillation:** Verified fixes are distilled into Golden Fix Recipes in `.torusguard/memory/patterns.json`.

---

## 📊 Summary of Lifecycle Statuses

| Lifecycle Status | Symbol | Operational Meaning | Permitted Next Action |
| :--- | :---: | :--- | :--- |
| **`OPEN`** | 🔴 | Newly discovered candidate finding awaiting review | Run `verify` or `harden` |
| **`VERIFIED`** | 🟠 | Evidence confirmed and line coordinates validated | Run `harden` |
| **`CANDIDATE`** | 🟡 | Surgical Ponytail patch formulated in bundle | Run `apply` |
| **`APPLIED`** | 🔵 | Patch applied to disk; backup saved in snapshots | Run `recheck` |
| **`RESOLVED`** | 🟢 | Recheck confirmed fix closure with 0 regressions | Distill Golden Recipe |
| **`REGRESSED`** | ❌ | Recheck detected secondary vulnerability or incomplete fix | Run `rollback` or re-harden |
| **`FALSE POSITIVE`**| ⚪ | Insufficient evidence, mock fixture, or protected route | Closed with explanation |
