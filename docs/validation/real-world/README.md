# TorusGuard Real-World Repository Validation Program

> **Protocol & Scope:** In accordance with responsible disclosure standards (OWASP, NIST), TorusGuard real-world testing is strictly conducted on maintainer-authorized repositories, local open-source evaluations, and internal architectures without scanning or probing live production endpoints.

---

## 🎯 Program Objectives
1. **Stack Detection Fidelity:** Verify that TorusGuard correctly identifies frameworks, ORMs, and package managers in non-trivial project structures.
2. **Quality of Findings:** Measure the ratio of actionable `Confirmed` findings vs. necessary `Manual Review` items.
3. **False Positive Suppression:** Identify and eliminate misleading or false positive rule triggers.
4. **Remediation Usability:** Ensure developers can apply framework-idiomatic fixes directly from TorusGuard guides.

---

## 📑 Real-World Validation Index

| Target Repository | Category & Stack | Primary Rules Evaluated | Record Link |
|---|---|---|---|
| **Django & DRF Multi-Tenant SaaS** | Python (Django 4.2, DRF, PostgreSQL) | `TG-AUTH-007`, `TG-AUTH-006`, `TG-RATE-001`, `TG-SEC-001` | [django-drf-real-world.md](django-drf-real-world.md) |
| **FastAPI Microservice & Webhook Engine** | Python (FastAPI, Pydantic v2, httpx) | `TG-SSRF-001`, `TG-WEBHOOK-001`, `TG-AUTH-006` | [fastapi-real-world.md](fastapi-real-world.md) |
| **Flask Enterprise Portal** | Python (Flask, Flask-WTF, SQLAlchemy) | `TG-CSRF-001`, `TG-INPUT-004`, `TG-AUTH-007`, `TG-SEC-001` | [flask-sqlalchemy-real-world.md](flask-sqlalchemy-real-world.md) |
| **Polyglot Mixed-Stack Platform** | Node.js (Next.js) + Python (FastAPI microservice) | Stack detection, multiple manifest handling, multi-language rule dispatch | [mixed-stack-real-world.md](mixed-stack-real-world.md) |

---

## 📊 Summary Quality Metrics

| Metric | Target Standard | Observed Result | Status |
|---|---|:---:|:---:|
| **Stack Detection Accuracy** | 100% detection of active frameworks & manifests | 100% | ✅ PASS |
| **False Positive Rate (Confirmed Findings)** | < 5% | 0% | ✅ PASS |
| **Manual Review Context Quality** | Clear questions & architectural prompts | High | ✅ PASS |
| **Remediation Usability** | Native framework code snippets directly applicable | 100% | ✅ PASS |
