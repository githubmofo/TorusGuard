# Real-World Validation Record: Mixed Polyglot Platform


> 🛡️ **TorusGuard Validation Heritage:** This document preserves empirical validation records for this framework and milestone. For the current v1.3.5 active release line, 74-rule AST engine, living security report ground truth (`security_report.md`), and automated test suite (81/81 passing via `npm test`), refer to the [Validation Suite Overview](../README.md) and root [README](../../../README.md).

- **Repository:** Anonymized Polyglot Web & API Monorepo
- **Authorization:** Maintainer-permitted code review evaluation
- **Repository Version / Commit SHA:** `6e2a8c0f14b7d39a5e8c1f9a2b4d7e6c9f1a3b58`
- **Stack Detected:** 
  - Frontend: TypeScript, Next.js 14, React 18 (`package.json`, `pnpm-lock.yaml`)
  - Backend Microservice: Python 3.11, FastAPI, SQLAlchemy (`pyproject.toml`, `poetry.lock`)
- **TorusGuard Version:** v0.4.0
- **Date Tested:** 2026-08-21

---

## 🔍 Findings & Stack Detection Results

| Area / Component | Stack Detected | Reference Modules Loaded | Findings Outcome |
|---|---|---|---|
| `frontend/` | Next.js (App Router) | `secrets-and-config.md`, `client-code-exposure.md` | `TG-CLIENT-001` (Manual review on source map generation in production) |
| `services/api/` | FastAPI / SQLAlchemy | `fastapi-security.md`, `sqlalchemy-security.md`, `python-dependencies.md` | `TG-SUPPLY-001` (Lockfile verified), `TG-AUTH-001` (Auth dependency verified) |

---

## 📊 Results Summary

- **Stack Detection Accuracy:** 100% (Correctly identified polyglot subdirectories and loaded both Node.js and Python security references)
- **Confirmed Findings:** 0
- **Manual Review Findings:** 1
- **False Positives:** 0
- **Conclusion:** TorusGuard handles monorepo multi-manifest architectures cleanly without cross-language rule confusion.
