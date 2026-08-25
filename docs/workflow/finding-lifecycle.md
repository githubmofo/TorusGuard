# TorusGuard Finding Lifecycle Guide

This guide explains how security findings are tracked, classified, verified, remediated, and re-checked using the **TorusGuard v0.5.0 Workflow Engine**.

---

## 🔄 Finding Lifecycle Overview

TorusGuard findings follow a strict 6-stage state machine:

```text
Detect ──► Classify ──► Verify ──► Remediate ──► Re-check ──► Archive
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
  - **Taxonomy Category:** One of 9 normalized categories (e.g. `authentication-authorization`).
  - **Severity:** `Critical`, `High`, `Medium`, `Low`, or `Informational`.
  - **Initial Confidence:** `Confirmed`, `Likely`, or `Needs Review`.
- **Status:** Transitioned to `In Verification`.

---

## 3. 🛡️ Stage 3: Verify
- **Objective:** Establish whether the finding is a genuine, reachable vulnerability.
- **Evidence Evaluation Standard:**
  - **`Confirmed`:** Requires direct source evidence in the same module proving that an attacker-controlled parameter reaches an unmitigated sensitive sink.
  - **`Needs Review`:** Assigned whenever the code delegates protection to an external layer:
    - *Service Layer Delegation:* Controller calls `OrderService.get_order(id, user)` (must inspect service layer).
    - *Upstream Reverse Proxy:* Missing CSRF middleware on an internal API guarded by an API Gateway.
    - *Cloud IAM:* Database credentials managed via instance metadata or AWS IAM roles.
- **Rule:** A finding **cannot** be classified as `Confirmed` on assumptions alone.

---

## 4. 🛠️ Stage 4: Remediate
- **Action:** When `/torusguard harden` is run, the engine produces framework-native, least-invasive remediation proposals:
  - **Problem Statement:** Exact flaw in the current implementation.
  - **Risk Explanation:** Realistic attack scenario.
  - **Code Pattern:** Side-by-side **Before (Unsafe)** vs **After (Hardened)** diff.
  - **Verification Method:** Prescriptive command or unit test assertion.
  - **Residual Risk Notes:** Deployment-level considerations.

---

## 5. 🔁 Stage 5: Re-check
- **Action:** After applying fixes, run `/torusguard recheck`.
- **Differential Verification:** The engine re-scans the affected file.
- **State Transition:**
  - If the safe pattern is detected and the unsafe pattern is gone ──► Status becomes `Verified Safe` (`Remediated`).
  - If the flaw persists ──► Status reverts to `Open` / `In Verification`.

---

## 6. 📦 Stage 6: Archive
- **Action:** Once verified safe, findings are recorded in the timestamped project audit history (`SECURITY.md` or audit records) with cryptographic evidence and verification notes.

---

## 📊 Summary of Status Values

| Status | Meaning | Permitted Next Actions |
|---|---|---|
| **`Open`** | Validated vulnerability awaiting remediation | Apply fix via `/torusguard harden` |
| **`In Verification`** | Under evidence review or manual inspection | Verify reachability; resolve `Needs Review` questions |
| **`Remediation Proposed`** | Hardened code snippet generated | Review diff and apply patch |
| **`Remediated` / `Verified Safe`** | Post-fix re-check confirmed resolution | Advance to archive |
| **`Suppressed`** | Accepted risk with documented business justification | Record architectural rationale |
| **`Archived`** | Preserved in historical compliance record | Stored |
