# TorusGuard API & Skill Interface Specification

## 1. Overview
This document specifies the formal application programming interfaces, CLI command dispatchers, skill contracts, and schema payloads utilized by TorusGuard.

---

## 2. Skill Commands Interface

TorusGuard exposes five canonical workflow commands via the open `skills` specification (`skills/torusguard/SKILL.md`):

### 2.1. `/torusguard init`
- **Purpose:** Initializes security baseline, creates `SECURITY.md`, and sets up local scan configuration.
- **Input Parameters:**
  - `stack` *(optional)*: Explicit stack override (`django`, `fastapi`, `flask`, `express`, `nextjs`).
  - `policy` *(optional)*: Strictness level (`standard`, `strict`, `p0-only`).
- **Artifacts Created:**
  - `SECURITY.md`
  - `.torusguard/config.yaml`
- **Exit Codes:** `0` (Success), `1` (Initialization Error).

### 2.2. `/torusguard audit`
- **Purpose:** Executes full static security analysis against the current workspace.
- **Input Parameters:**
  - `--path <dir>`: Target root directory (default: `.`).
  - `--format <json|md>`: Output report format (default: `md`).
  - `--output <path>`: Custom report path.
  - `--min-severity <P0|P1|P2>`: Filter threshold.
- **Artifacts Emitted:**
  - `.torusguard/runs/run-<timestamp>-<id>/findings/finding-*.json`
  - `docs/validation/audit-report.md`

### 2.3. `/torusguard verify`
- **Purpose:** Performs deep evidence verification and confidence score evaluation on detected findings.
- **Input Parameters:**
  - `--finding-id <id>`: Target specific finding (or all active findings if omitted).
- **Behavior:** Validates AST reachability, confirms SHA-256 evidence integrity, and computes 0–100 confidence rubric.

### 2.4. `/torusguard harden`
- **Purpose:** Generates least-invasive, framework-native remediation patches (Ponytail Protocol).
- **Input Parameters:**
  - `--dry-run`: Generates unified diffs without writing to disk.
  - `--finding-id <id>`: Target specific finding.
  - `--auto-approve`: Applies changes automatically if project tests pass.
- **Output:** Unified Git diffs saved to `.torusguard/runs/.../patches/`.

### 2.5. `/torusguard recheck`
- **Purpose:** Re-evaluates modified code to assert vulnerability resolution.
- **Output States:**
  - `Verified Fixed`: Vulnerability resolved, 0 new risks.
  - `Still Present`: Unsafe pattern still detectable.
  - `Partially Fixed`: Vulnerability reduced but residual flaw exists.
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
