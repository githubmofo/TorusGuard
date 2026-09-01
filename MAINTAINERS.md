# TorusGuard Maintainer Security & Project Hygiene Guide

This document defines mandatory security practices, account hygiene standards, branch review gates, and release governance rules for maintainers of the TorusGuard project.

---

## 1. Maintainer Account Security
- **Mandatory Multi-Factor Authentication (MFA):** Hardware security keys (FIDO2/WebAuthn) or time-based one-time password (TOTP) apps must be enforced on all maintainer GitHub accounts. SMS-based 2FA is prohibited.
- **Zero Shared Accounts:** All maintainers must use individual, named accounts. Shared or bot credentials with write access are strictly forbidden.
- **Least Privilege Access:** Maintainers are granted repository permissions aligned strictly with their operational domain (Docs, Rules, Core Engine).

---

## 2. Branch Protection & Review Policies
- **Protected Branches:** Branch protection is strictly enforced on `main` and active release branches (`v6`).
  - Force-pushes and branch deletions are permanently disabled.
  - Direct commits to protected branches are blocked; all changes must arrive via Pull Request.
- **Mandatory Code Review:** At least one independent maintainer review is mandatory before merging any PR touching:
  - Security rule catalogs (`rules/`)
  - Runtime validation and exploitability confirmation (`core/runtime_validator.py`, `core/exploit_checker.py`)
  - Remediation and governance engines (`core/governance.py`, `core/bundle.py`, `core/rechecker.py`)
  - Legal authorization and safety gates (`core/authorization.py`, `core/safety_gate.py`)
- **Automated CI Status Checks:** All CI validation workflows must pass cleanly before any merge is permitted.

---

## 3. Dependency Management & Supply Chain Hygiene
- **Deterministic Lockfiles:** All dependencies must be pinned using cryptographically reproducible lockfiles (`requirements.txt`, `uv.lock`, or `poetry.lock`).
- **Dependency Review & Auditing:** Automated dependency vulnerability scanning (`pip-audit`, GitHub Dependabot) is enabled. Pull requests introducing known CVEs or unpinned packages are blocked.
- **Supply Chain Hardening:** Third-party GitHub Actions must be pinned to immutable commit SHAs, never mutable release tags.

---

## 4. Secrets & Credential Protection
- **Zero Committed Secrets:** Secret scanning and push protection are enabled across all branches.
- **Pre-Commit Linting:** Maintainers must run local credential scanning before committing. Any credential detected in git history mandates immediate revocation and rotation.
- **Ephemeral Test Credentials:** All test fixtures must use synthetic canary tokens (e.g., `sk_test_...` or fake JWTs). Production keys are strictly prohibited in the codebase.

---

## 5. Release Governance & Signing
- **Cryptographic Release Signing:**
  - Every release tag must be a signed git tag (`git tag -s vX.Y.Z`).
  - Packaged tarballs and wheels must publish detached GPG signatures and a signed `SHA256SUMS` manifest.
- **Mandatory Release Verification Criteria:**
  No release may be tagged unless all validation harnesses pass with 100% success:
  1. `validate_v0_7_0_runtime.py` (Runtime validation, safety gates, role handoffs)
  2. `validate_v0_6_3_hardening.py` (Drift invariance, SARIF dedup, sensitive escalation)
  3. `validate_qa_v0_6_0.py` (Governed remediation, clustering, targeted recheck)
  4. `runner.py` & `validate_e2e.py` (Core schemas, confidence scoring, replay integrity)

---

## 6. Security Incident Response & Contact
- **Vulnerability Reports:** Security researchers should report vulnerabilities via GitHub Private Vulnerability Reporting or directly to `security@torusguard.dev` / `@githubmofo`.
- **Response Commitment:** Initial triage within 48 hours; public coordinated advisory within 7 days of patch verification.
