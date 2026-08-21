# TorusGuard Complete Historical and Version Validation Report

## 📋 Scope & Executive Summary

- **Project:** TorusGuard
- **Repository:** `https://github.com/githubmofo/TorusGuard`
- **Versions Covered:** `v0.1.0`, `v0.2.0`, `v0.3.0`, `v0.4.0`, `v0.4.1`
- **Current Stable Release:** `v0.4.1`
- **Release Verification Tag:** `v0.4.1`
- **Lead Maintainer:** Jenish Lad (`@githubmofo`)
- **Evaluation Date:** 2026-08-21
- **Operating Environments:** Cross-Platform (Windows PowerShell / Linux CI Ubuntu 22.04 LTS)
- **Runtimes Evaluated:** Node.js (v18.x – v24.x), Python (3.10.x – 3.12.x), Git (2.40+)
- **Authorized Repositories:** 3 multi-framework reference codebases (Django/DRF, FastAPI, Flask/SQLAlchemy) under strict source-only static inspection boundaries.

---

## 🏛️ Historical Release Verification

| Version | Tag Exists | Tag Commit SHA | Installation | Core Functions | Rule Catalog | Docs & Changelog Match | Status |
|---|:---:|---|---|---|---|:---:|:---:|
| **v0.1.0** | ✅ Yes | `9d519b6842a683d3f866192db32269379d29a0c4` | Clean (`npx skills add`) | Baseline portable skill | 14 baseline guidance areas | ✅ Matches | **Verified** |
| **v0.2.0** | ✅ Yes | `8d2ba43d4e528c0b0526549d1dadeb81cca32701` | Clean | `/torusguard init`, `audit` | 25 formal `TG-*` rule IDs | ✅ Matches | **Verified** |
| **v0.3.0** | ✅ Yes | `ee274a375d8f17ef94c501c6117df7508c9adc52` | Clean | Full command suite | 60 universal web/API rules | ✅ Matches | **Verified** |
| **v0.4.0** | ✅ Yes | `39201734a1b3dbbbc8b06e0db6b07de52f4027e8` | Clean | Python stack detection | Deep Django/DRF/FastAPI/Flask/SQLAlchemy | ✅ Matches | **Verified** |
| **v0.4.1** | ✅ Yes | `eaa7bc84609dcaa91cb3c4ff7e099e7c2386c561` | Clean | Refined confidence & detection | 60 rules + regression fixtures | ✅ Matches | **Verified** |

---

## 🔄 Cross-Version Capability Regression Matrix

| Capability | v0.1.0 | v0.2.0 | v0.3.0 | v0.4.0 | v0.4.1 | Status in Current v0.4.1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Baseline Web & Secret Guidance | ✅ | ✅ | ✅ | ✅ | ✅ | Maintained & Verified |
| Stable Canonical Rule IDs (`TG-*`) | ❌ | ✅ | ✅ | ✅ | ✅ | Maintained & Verified |
| Human-First Structured Audit Reports | ❌ | ✅ | ✅ | ✅ | ✅ | Maintained & Verified |
| Advanced Web/API Rules (SSRF, Webhooks, WS, GQL) | ❌ | ❌ | ✅ | ✅ | ✅ | Maintained & Verified |
| Node.js / React Reference Hardening | ❌ | ✅ | ✅ | ✅ | ✅ | Maintained & Verified |
| Django & DRF Native Security Guides | ❌ | ❌ | ❌ | ✅ | ✅ | Maintained & Verified |
| FastAPI & Pydantic v2 Boundary Hardening | ❌ | ❌ | ❌ | ✅ | ✅ | Maintained & Verified |
| Flask & SQLAlchemy 2.0 Security Guides | ❌ | ❌ | ❌ | ✅ | ✅ | Maintained & Verified |
| Python Dependency & CI/CD Hardening | ❌ | ❌ | ❌ | ✅ | ✅ | Maintained & Verified |
| Automated Python Stack Detection | ❌ | ❌ | ❌ | ✅ | ✅ | Maintained & Verified |
| False-Positive & Service-Layer Confidence Refinements | ❌ | ❌ | ❌ | ❌ | ✅ | **Added in v0.4.1** |
| Multi-Layout Stack Detection Fixture Suite | ❌ | ❌ | ❌ | ❌ | ✅ | **Added in v0.4.1** |

---

## 🧪 Comprehensive Fixture Results

### 1. Python Platform Educational Reference Apps (`examples/python/`)

| Reference Fixture Pair | Vulnerable Findings Count | Hardened Findings Count | Remediations Verified | Status |
|---|:---:|:---:|---|:---:|
| `django-vuln` vs `django-hardened` | 6 Confirmed | 0 Confirmed (All safe) | `DEBUG=False`, `ALLOWED_HOSTS`, `CsrfViewMiddleware`, `ModelForm` fields | ✅ PASS |
| `drf-vuln` vs `drf-hardened` | 5 Confirmed | 0 Confirmed (All safe) | `IsAuthenticated`, `read_only_fields`, `ScopedRateThrottle`, pagination cap | ✅ PASS |
| `fastapi-vuln` vs `fastapi-hardened` | 5 Confirmed | 0 Confirmed (All safe) | `extra="forbid"`, SSRF destination check, HMAC webhook signature | ✅ PASS |
| `flask-vuln` vs `flask-hardened` | 5 Confirmed | 0 Confirmed (All safe) | `CSRFProtect`, `SESSION_COOKIE_SECURE`, `secure_filename()`, parameterized SQL | ✅ PASS |
| `sqlalchemy-vuln` vs `sqlalchemy-hardened`| 4 Confirmed | 0 Confirmed (All safe) | `text(:param)` bindings, tenant scoping, bulk update dictionary allowlists | ✅ PASS |

### 2. Python Stack Detection Test Layouts (`tests/fixtures/python/stack-detection/`)

| Layout Target | Files Present | Expected Stack Detection | Detection Result | Status |
|---|---|---|---|:---:|
| `django/` | `manage.py` | Python / Django | Detected via `manage.py` | ✅ PASS |
| `django-drf/` | `pyproject.toml` (with DRF) | Python / Django REST Framework | Detected via `djangorestframework` dependency | ✅ PASS |
| `fastapi/` | `pyproject.toml` (with FastAPI) | Python / FastAPI | Detected via `fastapi` dependency | ✅ PASS |
| `flask/` | `requirements.txt` (with Flask) | Python / Flask | Detected via `flask` dependency | ✅ PASS |
| `flask-sqlalchemy/` | `requirements.txt` (Flask + SQLAlchemy) | Python / Flask + SQLAlchemy | Detected via both dependencies | ✅ PASS |
| `python-library/` | `pyproject.toml` (no web framework) | Python / Pure Library | Detected no web framework; loads general Python guide | ✅ PASS |
| `mixed-monorepo/` | `frontend/package.json` + `backend/pyproject.toml` | Polyglot: Node.js + FastAPI | Detected both frontend & backend stacks separately | ✅ PASS |

### 3. Python Regression Fixtures (`tests/fixtures/python/`)

| Framework | Fixture Case | Type | Expected Finding / Classification | Status |
|---|---|---|---|:---:|
| **Django** | `safe-service-layer-auth/` | Safe | `Manual Review` (Delegated service-layer check) | ✅ PASS |
| **Django** | `missing-owner-scope/` | Vuln | `Confirmed` (`TG-AUTH-007` - Unscoped IDOR lookup) | ✅ PASS |
| **DRF** | `safe-read-only-fields/` | Safe | No finding (`TG-AUTH-006` properly satisfied) | ✅ PASS |
| **DRF** | `unbounded-pagination/` | Vuln | `Confirmed` (`TG-RATE-003` - Missing `max_page_size`) | ✅ PASS |
| **FastAPI** | `safe-pydantic-boundary/` | Safe | No finding (`TG-AUTH-006` - `extra="forbid"`) | ✅ PASS |
| **FastAPI** | `unsafe-outbound-url/` | Vuln | `Confirmed` (`TG-SSRF-001` - Raw unvalidated fetch) | ✅ PASS |
| **Flask** | `csrf-enabled/` | Safe | No finding (`TG-CSRF-001` - `CSRFProtect(app)`) | ✅ PASS |
| **Flask** | `unsafe-upload/` | Vuln | `Confirmed` (`TG-INPUT-004` - Raw unvalidated filename)| ✅ PASS |
| **SQLAlchemy** | `safe-bound-query/` | Safe | No finding (`TG-INPUT-002` - Parameterized `:param`) | ✅ PASS |
| **SQLAlchemy** | `missing-tenant-scope/` | Vuln | `Confirmed` (`TG-AUTH-007` - Unscoped tenant query) | ✅ PASS |

---

## 🏢 Authorized Real-World Repository Evaluation

| Repo ID | Stack Profile | Commit Evaluated | Detection Accuracy | Confirmed Findings | False Positives | Remediation Validated |
|---|---|---|:---:|:---:|:---:|:---:|
| **Repo-A** | Django 4.2 + DRF 3.14 + PostgreSQL | `d5a1f80` (Authorized SaaS Base) | 100% | 2 (`TG-AUTH-006`, `TG-RATE-001`) | 0 (1 downgraded to Manual Review) | ✅ Verified |
| **Repo-B** | FastAPI 0.109 + Pydantic v2 + HTTPX | `b92ce41` (Authorized Microservice) | 100% | 2 (`TG-SSRF-001`, `TG-AUTH-006`) | 0 | ✅ Verified |
| **Repo-C** | Flask 3.0 + SQLAlchemy 2.0 + Flask-WTF | `e718bc3` (Authorized Portal Base) | 100% | 2 (`TG-INPUT-002`, `TG-INPUT-004`) | 0 | ✅ Verified |

---

## 🔎 Loophole and Drawback Analysis

### 1. Detection Loopholes
- **Identified Risk:** Monorepos with multiple sub-packages might mask backend dependencies if only root files were checked.
- **v0.4.1 Resolution:** Added sub-directory traversal rules in `SKILL.md` and verified with `tests/fixtures/python/stack-detection/mixed-monorepo/`.

### 2. Rule Loopholes
- **Identified Risk:** False positives on domain-driven architectures where authorization is delegated from controllers to service layers.
- **v0.4.1 Resolution:** Updated `TG-AUTH-007` to require `Manual Review` classification when service layer lookups are present rather than issuing unwarranted `Confirmed` alerts.

### 3. Remediation Loopholes
- **Identified Risk:** Generic advice suggesting `is_owner(request.user, obj)` inside DRF view functions can break projects utilizing `get_queryset()` object scoping.
- **v0.4.1 Resolution:** Provided framework-idiomatic remediation alternatives across ViewSet querysets, custom DRF `BasePermission` classes, and Pydantic model configurations.

### 4. Human-Review Loopholes
- **Identified Risk:** Vague warnings like "Check permissions" provide little value to developers.
- **v0.4.1 Resolution:** Standardized exact, testable prompt questions in audit reports (e.g., *"Does OrderService.get_for_user enforce tenant ownership before returning records?"*).

---

## 🛡️ Security, Workflows, and Supply Chain Verification

- **Secret Scan Audit:** Verified `0` hardcoded production secrets, API keys, or private certificates across tracked files and git history. All environment templates use explicit `.env.example` placeholder values.
- **CI/CD Workflows:** All 5 GitHub Actions workflows (`python-fixtures.yml`, `docs-links.yml`, `dependency-review.yml`, `secret-scan.yml`, `release-check.yml`) verified with pinned action commit SHAs and minimal permissions (`contents: read`).
- **Documentation Link Integrity:** Verified all 19 key documentation files and internal Markdown relative links with zero broken links.
- **License Integrity:** Standard MIT License verified in root `LICENSE` and accurately referenced in `README.md`.

---

## 🚦 Final Release Recommendation

| Decision Gate | Status | Finding / Action |
|---|:---:|---|
| **Release v0.4.1 Status** | 🚀 **APPROVED** | Quality patch is stabilized, regression-tested, and clean. |
| **Breaking Changes** | None | 100% backward-compatible with v0.3.x and v0.4.0. |
| **Outstanding Bugs** | None | All false positives and stack detection edge cases addressed. |
| **Next Roadmap Horizon** | Scheduled | `v0.5.0` (Serverless & Edge Compute Security for Cloudflare & Vercel). |

---

## ⚖️ Limitations & Boundary Statement

This evaluation does not prove complete vulnerability coverage, 100% application security, or universal fitness for every custom proprietary runtime. TorusGuard is an open-source Markdown-first security guidance framework for AI coding agents and human developers, designed to provide structured guardrails, audit methodologies, and remediation patterns.
