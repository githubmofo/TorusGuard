# TorusGuard Maintainer Security & Project Hygiene Guide

This document defines mandatory security practices, account hygiene standards, branch review gates, manifest verification protocols, and release governance rules for maintainers of the TorusGuard project.

---

## 1. Maintainer Account Security & Identity
- **Mandatory Multi-Factor Authentication (MFA):** Hardware security keys (FIDO2/WebAuthn, e.g., YubiKey) or time-based one-time password (TOTP) applications must be enforced on all maintainer GitHub accounts. SMS-based 2FA is strictly prohibited.
- **Zero Shared Accounts:** All maintainers must use individual, named accounts. Shared credentials or generic service accounts with write access are strictly forbidden.
- **Least Privilege Access:** Maintainers are granted repository permissions aligned strictly with their operational domain (Docs, Rules, Core Engine, Security).
- **SSH Key Hygiene:** Maintainers must use Ed25519 SSH keys with passphrase protection for git operations.

---

## 2. Branch Protection & Review Policies
- **Protected Branches:** Branch protection is strictly enforced on `main` and active release branches.
  - Force-pushes and branch deletions are permanently disabled.
  - Direct commits to protected branches are blocked; all changes must arrive via Pull Request.
  - Linear git history is enforced.
- **Mandatory Code Review:** At least one independent maintainer review is mandatory before merging any PR touching:
  - Security rule catalogs (`rules/`, `.torusguard/rules/`)
  - Runtime validation and safety gates (`.torusguard/scripts/safety_gate.py`)
  - Remediation and governance engines (`.torusguard/scripts/run_manager.py`)
  - Offline installer and payload bootstrapper (`skills/torusguard/bootstrap.py`, `install.py`)
  - Integrity manifest engine (`.torusguard/scripts/manifest_builder.py`)
- **Automated CI Status Checks:** All 9 automated test suites must pass cleanly before any merge is permitted.

---

## 3. Supply Chain Hygiene & Dependency Management
- **Deterministic Lockfiles:** All dependencies must be pinned using cryptographically reproducible lockfiles (`requirements.txt`, `uv.lock`, or `poetry.lock`).
- **Dependency Review & Auditing:** Automated dependency vulnerability scanning (`pip-audit`, GitHub Dependabot) is enabled. Pull requests introducing known CVEs or unpinned packages are blocked.
- **Supply Chain Hardening:** Third-party GitHub Actions must be pinned to immutable commit SHAs, never mutable release tags.
- **Zero Heavy Runtime Dependencies:** TorusGuard's installer and core automation scripts must maintain zero external dependencies beyond standard Python 3.10+ standard libraries.

---

## 4. Manifest Integrity & Payload Synchronization
Whenever changes are made to `.torusguard/` (rules, workflows, agents, scripts, templates, schemas, references):
1. **Rebuild Cryptographic Manifest:**
   Run the manifest builder to update SHA-256 digests for all indexed files:
   ```bash
   python .torusguard/scripts/manifest_builder.py --write
   ```
2. **Verify Manifest Check:**
   Confirm that all 88 workspace files match their cryptographic signatures:
   ```bash
   python .torusguard/scripts/manifest_builder.py --check
   ```
3. **Synchronize Offline Template Payload:**
   Sync the template directory so external installations via `npx skills add` receive updated files:
   ```bash
   python -c "import shutil; shutil.rmtree('skills/torusguard/payload', ignore_errors=True); shutil.copytree('.torusguard', 'skills/torusguard/payload', ignore=shutil.ignore_patterns('runs', '*.pyc', '__pycache__'))"
   ```

---

## 5. Secrets & Credential Protection
- **Zero Committed Secrets:** Secret scanning and push protection are enabled across all branches.
- **Pre-Commit Linting:** Maintainers must run local credential scanning before committing. Any credential detected in git history mandates immediate revocation, rotation, and git history rewrite.
- **Ephemeral Test Credentials:** All test fixtures must use synthetic canary tokens (e.g., `sk_test_...` or dummy JWTs). Production keys are strictly prohibited in the codebase.

---

## 6. Release Governance & Cryptographic Signing
- **Cryptographic Release Signing:**
  - Every release tag must be a signed git tag (`git tag -s vX.Y.Z -m "Release vX.Y.Z"`).
  - Packaged release tarballs and wheels must publish detached GPG signatures and a signed `SHA256SUMS` manifest.
- **Mandatory Pre-Release Verification:**
  No release tag may be published unless all **9 automated test suites** achieve a **100% pass rate (381 test assertions)**:
  1. `harness/validate_v0_9_2_workflows_and_skills.py` (Workflows & skills command-engine standard)
  2. `.torusguard/scripts/manifest_builder.py --check` (Cryptographic SHA-256 workspace integrity)
  3. `harness/validate_v0_9_1_installer.py` (Clean-room `npx skills add` and `install.py` simulations)
  4. `harness/validate_v0_9_0_skills.py` (Granular skills frontmatter, line budgets, and routing)
  5. `harness/runner.py` (Core schemas, confidence scoring, 3-pass replay integrity)
  6. `harness/validate_v0_7_0_runtime.py` (Runtime validation, safety gates, role handoffs)
  7. `harness/validate_v0_8_0_part1.py` (Workspace foundation integrity)
  8. `harness/validate_v0_8_0_part2.py` (Agent definitions and workflows)
  9. `harness/validate_v0_8_0_part3.py` (Automation scripts and framework references)

---

## 7. Security Incident Response & Contact
- **Vulnerability Reports:** Security researchers should report vulnerabilities via GitHub Private Vulnerability Reporting or directly to `security@torusguard.dev` / `@githubmofo` (Jenish Lad).
- **Response Commitment:** Initial triage within **24 to 48 hours**; public coordinated advisory within **5 to 7 days** of patch verification.
