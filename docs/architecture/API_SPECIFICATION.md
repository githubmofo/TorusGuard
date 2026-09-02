# TorusGuard API & Skill Interface Specification

## 1. Overview
This document specifies the formal application programming interfaces, CLI command dispatchers, skill contracts, and schema payloads utilized by TorusGuard.

---

## 2. Skill Commands Interface

TorusGuard exposes 11 canonical workflow commands via the open `skills` specification (`skills/torusguard/SKILL.md`):

### 2.1. `/torusguard init`
- **Purpose:** Initializes `.torusguard/` workspace, detects technology stack, and activates tailored security rules.
- **Bound Script:** `python .torusguard/scripts/stack_detect.py`

### 2.2. `/torusguard authorize`
- **Purpose:** Creates and cryptographically manages the target authorization manifest (`scope.json` and `authorization.md`).
- **Bound Script:** `python .torusguard/scripts/safety_gate.py --check-scope`

### 2.3. `/torusguard audit`
- **Purpose:** Executes full static AST analysis, clusters by root cause, and assigns line-shift invariant fingerprints.
- **Bound Script:** `python .torusguard/scripts/finding_scorer.py --audit`

### 2.4. `/torusguard verify`
- **Purpose:** Performs deep evidence verification, validates AST reachability, and computes 0–100 confidence rubric.
- **Bound Script:** `python .torusguard/scripts/finding_scorer.py --score 90`

### 2.5. `/torusguard web-validate`
- **Purpose:** Executes authorized, non-destructive HTTP endpoint probing within allowed scope.
- **Bound Script:** `python .torusguard/scripts/safety_gate.py --method GET`

### 2.6. `/torusguard exploit-check`
- **Purpose:** Executes bounded, non-destructive proof-of-concept canary checks (e.g. CSRF/IDOR reachability).
- **Bound Script:** `python .torusguard/scripts/safety_gate.py --method POST`

### 2.7. `/torusguard harden`
- **Purpose:** Formulates self-contained 4-artifact remediation packages adhering to the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions).
- **Artifacts:** `finding.md`, `remediation.md`, `minimal_patch_plan.md`, `verify-after-change.md`

### 2.8. `/torusguard apply`
- **Purpose:** Backs up pre-apply snapshots to `pre_apply/<file>.bak` and applies surgical, minimal patches to disk.
- **Exit Codes:** `0` (Applied), `1` (Pre-flight rejected).

### 2.9. `/torusguard recheck`
- **Purpose:** Re-evaluates post-fix code to assert vulnerability resolution (`Confirmed Fixed`) and detect secondary regressions.
- **Bound Script:** `python .torusguard/scripts/sarif_exporter.py`

### 2.10. `/torusguard report`
- **Purpose:** Generates executive Markdown summaries and exports OASIS SARIF v2.1.0 scan results.
- **Bound Script:** `python .torusguard/scripts/sarif_exporter.py --output results.sarif`

### 2.11. `/torusguard status`
- **Purpose:** Read-only inspection of active workspace posture, unexpired authorization TTLs, and run history.
- **Bound Script:** `python .torusguard/scripts/run_manager.py --status`
  - `New Risk`: Patch introduced a secondary vulnerability.

---

## 3. Schema Contracts & Data Models

### 3.1. Finding Object Model (`schemas/finding.schema.json`)
```json
{
  "finding_id": "TG-2026-0827-001",
  "rule_id": "TG-AUTH-008",
  "title": "Untrusted Role Header Injection",
  "category": "authentication-authorization",
  "severity": "Critical",
  "confidence_score": 92,
  "confidence_band": "Confirmed",
  "lifecycle_stage": "Remediated",
  "target": {
    "file_path": "backend/api/auth.py",
    "line_start": 42,
    "line_end": 48
  },
  "evidence": {
    "code_snippet": "role = request.headers.get('X-User-Role')",
    "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "masked": false
  },
  "remediation": {
    "priority": "Immediate P0",
    "suggested_diff_path": ".torusguard/runs/run-01/patches/patch-001.diff"
  }
}
```

### 3.2. Retest Record Model (`schemas/retest.schema.json`)
```json
{
  "retest_id": "RET-2026-0827-001",
  "finding_id": "TG-2026-0827-001",
  "timestamp": "2026-08-27T11:00:00Z",
  "recheck_status": "Verified Fixed",
  "verified_by": "TorusGuard Recheck Engine v0.5.6",
  "post_fix_evidence_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
}
```

---

## 4. Integration & Return Codes
- `0`: Scan clean / All findings remediated and verified safe.
- `1`: Syntax or runtime execution error in target repository.
- `2`: P0 / Critical security findings detected (CI blocking gate).
- `3`: Recheck failed / Regression detected.
