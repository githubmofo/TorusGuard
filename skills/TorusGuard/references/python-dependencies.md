# TorusGuard Skill Reference: Python Dependencies and Supply Chain

> **Loaded When:** Python dependency manifests (`requirements.txt`, `pyproject.toml`, `Pipfile`, `poetry.lock`, `uv.lock`) or `.github/workflows/*.yml` are detected.

---

## 🛡️ Key Inspection Areas & Rules

### 1. Lockfile Integrity
* `TG-SUPPLY-001`: Verify that deterministic lockfiles exist alongside manifests and are not excluded in `.gitignore`.

### 2. Known CVE Vulnerability Auditing
* `TG-SUPPLY-002`: Check for vulnerable dependencies using `pip-audit`. Avoid recommending blind major-version upgrades that introduce breaking changes without tests.

### 3. CI/CD Workflow Hardening
* `TG-SUPPLY-004`: Inspect `.github/workflows/*.yml` for unpinned 3rd-party actions and overbroad default permissions.
