# TorusGuard Finding Lifecycle Guide

This guide explains how security findings are tracked, classified, verified, remediated, applied, and re-checked using the **TorusGuard Workflow Engine**.

---

## 🔄 Finding Lifecycle Overview

TorusGuard findings follow a strict 7-stage closed-loop state machine:

```text
Detect ──► Classify ──► Verify ──► Remediate ──► Apply ──► Re-check ──► Archive
```

---

## 1. 🔍 Stage 1: Detect
- **Trigger:** When `/torusguard audit` is executed across a repository.
- **Action:** The engine inspects files matching the detected stack (e.g. `settings.py`, `views.py`, `serializers.py`, `schemas.py`, `main.py`, `pyproject.toml`, `requirements.txt`).
- **Initial Output:** Code fragments and coordinates suspected of containing security weaknesses.

---

## 2. 🏷️ Stage 2: Classify
- **Action:** The candidate is normalized into the TorusGuard finding schema:
  - **Rule ID:** Canonical identifier (e.g. `TG-AUTH-007`).
  - **Taxonomy Category:** One of 12 normalized categories (e.g. `authentication-authorization`, `agent`, `edge`).
  - **Severity:** `Critical`, `High`, `Medium`, `Low`, or `Informational`.
  - **Initial Confidence:** `Confirmed`, `High Confidence`, or `Needs Review`.
- **Status:** Transitioned to `In Verification`.

---

## 3. 🛡️ Stage 3: Verify
- **Objective:** Establish whether the finding is a genuine, reachable vulnerability via static scoring or authorized runtime probing (`/torusguard verify`, `web-validate`, `exploit-check`).
- **Evidence Evaluation Standard:**
  - **`Confirmed`:** Requires direct source evidence or runtime canary confirmation proving that an attacker-controlled parameter reaches an unmitigated sensitive sink.
  - **`Needs Review`:** Assigned whenever the code delegates protection to an external layer:
    - *Service Layer Delegation:* Controller calls `OrderService.get_order(id, user)` (must inspect service layer).
    - *Upstream Reverse Proxy:* Missing CSRF middleware on an internal API guarded by an API Gateway.
    - *Cloud IAM:* Database credentials managed via instance metadata or AWS IAM roles.
- **Rule:** A finding **cannot** be classified as `Confirmed` on assumptions alone.

---

## 4. 🛠️ Stage 4: Remediate
- **Formulation (`/torusguard harden`):** Generates 4-artifact remediation packages adhering to the Ponytail Protocol:
  - **`finding.md`:** Finding card and line coordinates.
  - **`remediation.md`:** Technical mechanics and Before/After examples.
  - **`minimal_patch_plan.md`:** Surgical patch bounded by $\le 35$ additions and $\le 25$ deletions.
  - **`verify-after-change.md`:** Concrete validation recipe.

---

## 5. ⚡ Stage 5: Apply
- **Execution (`/torusguard apply`):** Employs the Ponytail engine to apply surgical, minimal patches directly to repository source files.
- **Rollback Safety:** Automatically writes byte-for-byte rollback copies to `pre_apply/<file>.bak` before modifying any target file.

---

## 6. 🔁 Stage 6: Re-check
- **Verification (`/torusguard recheck`):** Scopes differential re-audits strictly to modified files, asserting `Confirmed Fixed` or detecting regressions.

---

## 7. 📦 Stage 7: Archive
- **Reporting (`/torusguard report`):** Emits signed executive markdown reports and exports OASIS SARIF v2.1.0 scan results for CI/CD integration.
---

## 📊 Summary of Status Values

| Status | Meaning | Permitted Next Actions |
|---|---|---|
| **`Open`** | Validated vulnerability awaiting remediation | Generate fix via `/torusguard harden` |
| **`In Verification`** | Under evidence review or manual inspection | Verify reachability; resolve `Needs Review` questions |
| **`Remediation Proposed`** | Hardened code snippet generated | Apply patch via `/torusguard apply` |
| **`Remediated` / `Verified Safe`** | Post-fix re-check confirmed resolution | Advance to archive |
| **`Suppressed`** | Accepted risk with documented business justification | Record architectural rationale |
| **`Archived`** | Preserved in historical compliance record | Stored |
