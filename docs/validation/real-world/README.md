# TorusGuard Real-World Repository Validation Program

> 🛡️ **TorusGuard Validation Heritage:** This document preserves real-world empirical validation protocols and repository evaluations. For the current v1.3.5 active release line, 74-rule AST engine, living security report ground truth (`security_report.md`), and automated test suite (81/81 passing via `npm test`), refer to the [Validation Suite Overview](../README.md) and root [README](../../../README.md).

> **Protocol & Scope:** In accordance with responsible disclosure standards (OWASP, NIST), TorusGuard real-world testing is strictly conducted on maintainer-authorized repositories, local open-source evaluations, and internal architectures without scanning or probing live production endpoints.

---

## 🎯 Program Objectives
1. **Stack Detection Fidelity:** Verify that TorusGuard correctly identifies frameworks, ORMs, and package managers in non-trivial project structures across 16+ languages.
2. **Quality of Findings:** Measure the ratio of actionable `Confirmed` findings vs. necessary `Manual Review` items across all 74 rules in 18 families.
3. **False Positive Suppression:** Identify and eliminate misleading or false positive rule triggers.
4. **Remediation Usability:** Ensure developers can apply framework-idiomatic fixes directly from TorusGuard guides with Ponytail bounds ($\le 35$ additions, $\le 25$ deletions).

---

## 📑 Real-World Validation Index

| Target Repository | Category & Stack | Primary Rules Evaluated | Record Link |
|---|---|---|---|
| **Django & DRF Multi-Tenant SaaS** | Python (Django 4.2, DRF, PostgreSQL) | `TG-AUTH-007`, `TG-AUTH-006`, `TG-RATE-001`, `TG-SEC-001` | [django-drf-real-world.md](django-drf-real-world.md) |
| **FastAPI Microservice & Webhook Engine** | Python (FastAPI, Pydantic v2, httpx) | `TG-SSRF-001`, `TG-WEBHOOK-001`, `TG-AUTH-006` | [fastapi-real-world.md](fastapi-real-world.md) |
| **Flask Enterprise Portal** | Python (Flask, Flask-WTF, SQLAlchemy) | `TG-CSRF-001`, `TG-INPUT-004`, `TG-AUTH-007`, `TG-SEC-001` | [flask-sqlalchemy-real-world.md](flask-sqlalchemy-real-world.md) |
| **Polyglot Mixed-Stack Platform** | Node.js (Next.js) + Python (FastAPI microservice) | Stack detection, multiple manifest handling, multi-language rule dispatch | [mixed-stack-real-world.md](mixed-stack-real-world.md) |

---

## 📊 Summary Quality Metrics (v1.3.5 Baseline)

| Metric | Target Standard | Observed Result | Status |
|---|---|:---:|:---:|
| **Stack Detection Accuracy** | 100% detection of active frameworks & manifests | 100% | ✅ PASS |
| **False Positive Rate (Confirmed Findings)** | < 5% | 0% | ✅ PASS |
| **Manual Review Context Quality** | Clear questions & architectural prompts | High | ✅ PASS |
| **Remediation Usability** | Native framework code snippets directly applicable | 100% | ✅ PASS |
| **Living Security Report Closure** | Synchronized state ledger with 0 regressions | 100/100 | ✅ PASS |
