# Python Dependency and CI/CD Security Guide (TorusGuard v0.4.0)

> **Scope:** Supply chain and CI/CD security standards for Python projects. Covers virtual environment isolation, reproducible lockfiles, automated vulnerability scanning (`pip-audit`), pinned GitHub Actions, and secret protection in build pipelines.

---

## 🔒 1. Dependency Manifests & Deterministic Locking (`TG-SUPPLY-001`)

Always generate and commit deterministic lockfiles to prevent malicious upstream dependency substitutions.

| Package Tool | Manifest File | Committed Lockfile |
|---|---|---|
| **Poetry** | `pyproject.toml` | `poetry.lock` |
| **uv** | `pyproject.toml` | `uv.lock` |
| **Pipenv** | `Pipfile` | `Pipfile.lock` |
| **Pip** | `requirements.in` | `requirements.txt` (via `pip-compile`) |

---

## 🔍 2. Automated Vulnerability Scanning (`TG-SUPPLY-002`)

Integrate `pip-audit` into local development workflows and continuous integration (CI) pipelines.

```bash
# Audit active environment
pip-audit

# Audit specific requirements file
pip-audit -r requirements.txt
```

> *TorusGuard Statement:* Run ecosystem vulnerability tools like `pip-audit` as part of your regular dependency review; TorusGuard guides secure integration boundaries but does not independently maintain CVE vulnerability feeds.

---

## ⚙️ 3. Hardening CI/CD Workflows (`TG-SUPPLY-004`)

In GitHub Actions (`.github/workflows/*.yml`):

### 1. Pin Actions to Full Commit SHAs
```yaml
# ❌ VULNERABLE: Mutable tag can be hijacked
- uses: actions/checkout@v4

# ✅ SAFE: Pinned immutable commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

### 2. Enforce Least Privilege Permissions
```yaml
permissions:
  contents: read
  issues: none
  pull-requests: none
```

### 3. Isolate Secrets from Pull Requests
Never inject production secrets into untrusted `pull_request` workflow triggers from forks.

---

## 📋 Manual Review Checklist for Python Dependencies

- [ ] Lockfiles (`poetry.lock`, `uv.lock`, or pinned `requirements.txt`) are committed to version control.
- [ ] `pip-audit` runs on every pull request in CI.
- [ ] GitHub Actions workflows use pinned commit SHAs and `permissions: read-all` / scoped permissions.
- [ ] Package registry tokens (`PYPI_API_TOKEN`) are configured as repository secrets and never hardcoded in scripts.
